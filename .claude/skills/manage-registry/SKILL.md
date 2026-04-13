---
name: manage-registry
description: Add or update a skill entry in the skills registry, validate it, and create a pull request.
---

# Manage Skills Registry

You are helping a user add or update a skill in the skills registry. This registry is the central catalog for skills installable via the `install-skill` CLI.

## Step 1: Determine the operation

Ask the user what they want to do:

1. **Add a new skill** to the registry
2. **Update an existing skill** (change version or description)

If updating, ask which skill they want to update. Show the current entries in `skills.xml` so they can pick one.

## Step 2: Gather skill information

### For a new skill

Ask the user for the following, one question at a time:

1. **Skill name** — must be kebab-case (lowercase letters, digits, hyphens). Pattern: `[a-z][a-z0-9]*(-[a-z0-9]+)*`. Examples: `my-skill`, `react-helper`, `teavm-lambda`.

2. **Source type** — ask: "Is this skill deployed as a Maven artifact or hosted in a GitHub repository?"
   - **Maven**: ask for `groupId` (e.g., `com.example`) and `artifactId` (e.g., `my-library`)
   - **GitHub**: ask for the repository in `owner/repo` format (e.g., `myorg/my-skill-repo`)

3. **Version** (optional) — a specific version, tag, or branch. If they don't have one, skip it.

4. **Description** — a short, clear description of what the skill does.

### For an update

Only `version` and `description` can be changed. The name, groupId, artifactId, and repository are **immutable** — they cannot be modified after registration. If the user wants to change immutable fields, explain that they must register a new skill instead.

## Step 3: Validate the name is unique

Read `skills.xml` and check that the chosen name does not already exist in the registry. If it does, tell the user and ask them to pick a different name or update the existing entry instead.

## Step 4: Create a branch

Create a new branch for the change:

```
git checkout -b add-skill/<skill-name>
```

Or for updates:

```
git checkout -b update-skill/<skill-name>
```

## Step 5: Edit skills.xml

Add or update the `<skill>` entry in `skills.xml`. Insert new entries at the end of the `<skills>` list, before the closing `</skills>` tag.

### Maven skill entry format

```xml
  <skill>
    <name>SKILL_NAME</name>
    <groupId>GROUP_ID</groupId>
    <artifactId>ARTIFACT_ID</artifactId>
    <version>VERSION</version>          <!-- omit if no version -->
    <description>DESCRIPTION</description>
  </skill>
```

### GitHub skill entry format

```xml
  <skill>
    <name>SKILL_NAME</name>
    <repository>OWNER/REPO</repository>
    <version>VERSION</version>          <!-- omit if no version -->
    <description>DESCRIPTION</description>
  </skill>
```

A skill must have **either** `groupId` + `artifactId` (Maven) **or** `repository` (GitHub), never both.

## Step 6: Validate locally

Run the schema validation:

```bash
xmllint --schema skills-registry.xsd skills.xml --noout
```

If it fails, fix the XML and re-validate. Common issues:
- Name doesn't match kebab-case pattern
- Missing required fields
- Both Maven and GitHub coordinates present
- Invalid characters in groupId, artifactId, or repository

## Step 7: Commit and push

```bash
git add skills.xml
git commit -m "Add skill: <skill-name>"   # or "Update skill: <skill-name>"
git push -u origin <branch-name>
```

## Step 8: Create the pull request

Create a PR targeting `main` with a clear title and description. Use this format:

- **Title**: `Add skill: <skill-name>` or `Update skill: <skill-name>`
- **Body**: Include the skill details (name, source, version, description) and mention what the skill does for users who will review the PR.

## Important rules

- **Immutable fields**: Once a skill is registered, its `name`, `groupId`, `artifactId`, and `repository` cannot be changed. Only `version` and `description` are mutable.
- **Source type lock-in**: A skill cannot be changed from Maven to GitHub or vice versa.
- **Deletion**: Removing a skill from the registry requires the `approved:deletion` label on the PR. Do not delete skills unless the user explicitly asks.
- **Schema changes**: Do not modify `skills-registry.xsd`. Changes to the schema require the `approved:schema-change` label.
- **One skill per PR**: Keep PRs focused on a single skill addition or update for easier review.
