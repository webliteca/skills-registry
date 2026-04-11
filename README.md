# Skills Registry

A central registry of skills deployed to Maven via the [skills-jar-maven-plugin](https://github.com/webliteca/skills-jar-maven-plugin). The registry is a single XML file (`skills.xml`) validated against an XML schema (`skills-registry.xsd`).

## Registry format

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

### Field rules

| Field | Required | Format | Mutable |
|---|---|---|---|
| `name` | yes | kebab-case (`[a-z][a-z0-9]*(-[a-z0-9]+)*`) | no |
| `groupId` | yes | Maven groupId (`com.example.app`) | no |
| `artifactId` | yes | Maven artifactId (`my-library`) | no |
| `version` | no | Free-form non-empty string | yes |
| `description` | yes | Free-form non-empty string | yes |

Skill names must be unique across the entire registry.

## Adding a skill

1. Fork this repository or create a branch.
2. Add a new `<skill>` entry to `skills.xml`.
3. Open a pull request targeting `main`.
4. CI will validate the XML against the schema and enforce change rules.
5. Once checks pass and the PR is approved, merge.

## Validation rules

The CI workflow (`.github/workflows/validate-pr.yml`) runs on every PR to `main` and enforces:

1. **Valid XML** — `skills.xml` must conform to `skills-registry.xsd`.
2. **Immutability** — `name`, `groupId`, and `artifactId` of existing skills cannot be changed.
3. **Deletion requires approval** — removing a skill fails CI unless the `approved:deletion` label is added to the PR.
4. **Schema changes require approval** — modifying `skills-registry.xsd` fails CI unless the `approved:schema-change` label is added to the PR.

## Local validation

Validate the XML against the schema locally with `xmllint`:

```bash
xmllint --schema skills-registry.xsd skills.xml --noout
```

Run the change validation script (compares against `main`):

```bash
python3 scripts/validate-skills.py
```
