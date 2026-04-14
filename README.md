# Skills Registry

A central registry of skills deployed to Maven via the [skills-jar-maven-plugin](https://github.com/webliteca/skills-jar-maven-plugin) or hosted on GitHub repositories. The registry is a single XML file (`skills.xml`) validated against an XML schema (`skills-registry.xsd`).

## Registry format

A skill can be sourced from either Maven or GitHub, not both.

### Maven skill

```xml
<skills>
  <skill>
    <name>my-skill</name>
    <groupId>com.example</groupId>
    <artifactId>my-library</artifactId>
    <version>1.0.0</version>          <!-- optional -->
    <description>Some description of the skill</description>
  </skill>
</skills>
```

### GitHub skill

```xml
<skills>
  <skill>
    <name>my-skill</name>
    <repository>owner/repo</repository>
    <version>v1.0</version>            <!-- optional tag/branch -->
    <description>Some description of the skill</description>
  </skill>
</skills>
```

### Field rules

| Field | Required | Format | Mutable |
|---|---|---|---|
| `name` | yes | kebab-case (`[a-z][a-z0-9]*(-[a-z0-9]+)*`) | no |
| `groupId` | for Maven skills | Maven groupId (`com.example.app`) | no |
| `artifactId` | for Maven skills | Maven artifactId (`my-library`) | no |
| `repository` | for GitHub skills | GitHub `owner/repo` | no |
| `version` | no | Free-form non-empty string | yes |
| `description` | yes | Free-form non-empty string | yes |

Each skill uses either `groupId` + `artifactId` (Maven) or `repository` (GitHub). Skill names must be unique across the entire registry.

## Adding a skill

### Using Claude Code (recommended)

The easiest way to add or update a skill is with the built-in `manage-registry` skill. Clone the repo and run it:

```bash
git clone https://github.com/webliteca/skills-registry.git
cd skills-registry
```

Then in Claude Code, ask it to add your skill. The `manage-registry` skill in `.claude/skills/` will guide you through the process — gathering the required fields, validating the XML, and creating a PR.

Alternatively, you can install the skill with the install-skill CLI and use it in any project:

```bash
install-skill manage-registry
```

### Manually

1. Fork this repository or create a branch.
2. Add a new `<skill>` entry to `skills.xml`.
3. Open a pull request targeting `main`.
4. CI will validate the XML against the schema and enforce change rules.
5. Once checks pass and the PR is approved, merge.

## Validation rules

The CI workflow (`.github/workflows/validate-pr.yml`) runs on every PR to `main` and enforces:

1. **Valid XML** — `skills.xml` must conform to `skills-registry.xsd`.
2. **Immutability** — `name` is always immutable. For Maven skills, `groupId` and `artifactId` cannot be changed. For GitHub skills, `repository` cannot be changed. The source type (Maven vs GitHub) cannot be changed.
3. **Deletion requires approval** — removing a skill fails CI unless the `approved:deletion` label is added to the PR.
4. **Schema changes require approval** — modifying `skills-registry.xsd` fails CI unless the `approved:schema-change` label is added to the PR.

## Using skills from the registry

Skills registered here can be installed using the [install-skill CLI](https://github.com/webliteca/install-skill-cli):

```bash
# Install a single skill by name
install-skill teavm-lambda

# Install a specific version
install-skill teavm-lambda@0.1.2
```

For project-level skill management, create a `.skills-versions` file listing the skills your project needs:

```
teavm-lambda 0.1.2
my-other-skill 1.0.0
```

Then run `install-skill` with no arguments to install all listed skills. See the [install-skill-cli README](https://github.com/webliteca/install-skill-cli) for full documentation.

## Local validation

Validate the XML against the schema locally with `xmllint`:

```bash
xmllint --schema skills-registry.xsd skills.xml --noout
```

Run the change validation script (compares against `main`):

```bash
python3 scripts/validate-skills.py
```
