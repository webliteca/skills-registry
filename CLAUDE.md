# CLAUDE.md

This file provides guidance for Claude Code when working in this repository.

## Repository overview

This is the **skills registry** — a central catalog of skills deployed to Maven via the skills-jar-maven-plugin. The registry is a single XML file validated by an XSD schema, with CI enforcement on pull requests.

## Key files

- `skills.xml` — The registry. Contains all registered skills.
- `skills-registry.xsd` — XML Schema defining the structure and constraints for `skills.xml`.
- `.github/workflows/validate-pr.yml` — GitHub Actions workflow that runs on PRs to `main`.
- `scripts/validate-skills.py` — Python script that enforces immutability, deletion, and schema change rules.

## Rules for modifying skills.xml

- **Adding skills**: Add a new `<skill>` element. The `name` must be unique, kebab-case, and not already exist.
- **Immutable fields**: `name`, `groupId`, and `artifactId` cannot be changed once a skill is registered.
- **Mutable fields**: `version` and `description` can be updated freely.
- **Deleting skills**: Requires the `approved:deletion` label on the PR.
- **Modifying the schema**: Requires the `approved:schema-change` label on the PR.

## Validation commands

```bash
# Validate XML against the schema
xmllint --schema skills-registry.xsd skills.xml --noout

# Run change validation (compares working copy against origin/main)
python3 scripts/validate-skills.py
```

## Skill XML format

```xml
<skill>
  <name>my-skill</name>                  <!-- unique, kebab-case, immutable -->
  <groupId>com.example</groupId>          <!-- Maven groupId, immutable -->
  <artifactId>my-library</artifactId>     <!-- Maven artifactId, immutable -->
  <version>1.0.0</version>                <!-- optional, mutable -->
  <description>What the skill does</description> <!-- required, mutable -->
</skill>
```

## Branch workflow

The `main` branch is protected. All changes must go through a pull request. CI must pass before merging.
