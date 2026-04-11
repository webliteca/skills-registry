#!/usr/bin/env python3
"""Validate skills registry changes in a pull request.

Checks:
  1. Skill names, groupIds, and artifactIds are immutable (cannot be modified).
  2. Deleting skills requires the 'approved:deletion' label on the PR.
  3. Modifying the XML schema requires the 'approved:schema-change' label on the PR.
"""

import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET


def get_base_file(filepath):
    """Get file contents from the base branch (main)."""
    try:
        result = subprocess.run(
            ["git", "show", "origin/main:" + filepath],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def parse_skills(xml_content):
    """Parse skills XML into a dict keyed by skill name."""
    root = ET.fromstring(xml_content)
    skills = {}
    for skill in root.findall("skill"):
        name_el = skill.find("name")
        group_el = skill.find("groupId")
        artifact_el = skill.find("artifactId")
        name = name_el.text.strip() if name_el is not None and name_el.text else ""
        group_id = group_el.text.strip() if group_el is not None and group_el.text else ""
        artifact_id = (
            artifact_el.text.strip()
            if artifact_el is not None and artifact_el.text
            else ""
        )
        skills[name] = {
            "name": name,
            "groupId": group_id,
            "artifactId": artifact_id,
        }
    return skills


def get_pr_labels():
    """Get labels from the current PR via GitHub event data."""
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        return set()
    with open(event_path) as f:
        event = json.load(f)
    labels = event.get("pull_request", {}).get("labels", [])
    return {label["name"] for label in labels}


def main():
    errors = []

    # Read current skills.xml
    try:
        with open("skills.xml") as f:
            current_content = f.read()
        current_skills = parse_skills(current_content)
    except (FileNotFoundError, ET.ParseError) as e:
        print(f"Failed to parse skills.xml: {e}")
        return 1

    # Get base branch skills.xml
    base_content = get_base_file("skills.xml")
    if base_content is None:
        print(
            "No skills.xml found on main branch. "
            "Skipping immutability and deletion checks."
        )
        print("Validation passed.")
        return 0

    try:
        base_skills = parse_skills(base_content)
    except ET.ParseError as e:
        print(
            f"Failed to parse base skills.xml: {e}. "
            "Skipping comparison checks."
        )
        print("Validation passed.")
        return 0

    pr_labels = get_pr_labels()

    # --- Check immutability: name, groupId, artifactId cannot change ---
    for name, base_skill in base_skills.items():
        if name in current_skills:
            current_skill = current_skills[name]
            if base_skill["groupId"] != current_skill["groupId"]:
                errors.append(
                    f"Skill '{name}': groupId is immutable. "
                    f"Cannot change from '{base_skill['groupId']}' "
                    f"to '{current_skill['groupId']}'."
                )
            if base_skill["artifactId"] != current_skill["artifactId"]:
                errors.append(
                    f"Skill '{name}': artifactId is immutable. "
                    f"Cannot change from '{base_skill['artifactId']}' "
                    f"to '{current_skill['artifactId']}'."
                )

    # --- Check for deleted skills ---
    deleted_skills = set(base_skills.keys()) - set(current_skills.keys())
    if deleted_skills:
        if "approved:deletion" in pr_labels:
            print(
                f"Skill deletion approved via label: "
                f"{', '.join(sorted(deleted_skills))}"
            )
        else:
            errors.append(
                f"Skills deleted: {', '.join(sorted(deleted_skills))}. "
                f"Add the 'approved:deletion' label to this PR to approve."
            )

    # --- Check for schema changes ---
    base_schema = get_base_file("skills-registry.xsd")
    if base_schema is not None:
        try:
            with open("skills-registry.xsd") as f:
                current_schema = f.read()
            if base_schema != current_schema:
                if "approved:schema-change" in pr_labels:
                    print("Schema change approved via label.")
                else:
                    errors.append(
                        "XML schema (skills-registry.xsd) has been modified. "
                        "Add the 'approved:schema-change' label to this PR "
                        "to approve."
                    )
        except FileNotFoundError:
            errors.append(
                "XML schema file (skills-registry.xsd) has been deleted."
            )

    # --- Report results ---
    if errors:
        print("Validation failed:\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
