---
title: File Structure & Tools
description: Directory layout, tool restriction patterns, and the reference-file pattern for advanced skills
tags: [file-structure, tools, directory, restrictions, reference-pattern]
---

# File Structure & Tools

## Simple Skill (single file)

```
.claude/skills/<skill-name>/
└── SKILL.md
```

## Advanced Skill (with resources)

```
.claude/skills/<skill-name>/
├── SKILL.md              (required — main instructions)
├── references/           (optional — on-demand detail files)
│   ├── topic-a.md
│   └── topic-b.md
├── scripts/              (optional — executable helpers)
│   └── helper.sh
└── templates/            (optional — file templates)
    └── template.md
```

## Creating the Directory and Files

1. Create directory: `.claude/skills/<skill-name>/`
2. Create `SKILL.md` with generated content
3. If advanced scope, create `references/` subdirectory with topic files
4. Customize based on:
   - Project tech stack (deno.json, CLAUDE.md)
   - Existing patterns in codebase
   - User's specific requirements
   - Tool restrictions if specified

## Tool Restrictions

If user chose "Restricted" tools, add `allowed-tools` to frontmatter:

```yaml
---
name: skill-name
description: Description here
allowed-tools: Read, Grep, Glob, Bash(jq:*), Bash(yq:*)
---
```

Common tool combinations:

| Use Case         | allowed-tools                              |
|------------------|--------------------------------------------|
| Read-only analysis | `Read, Grep, Glob`                       |
| Data processing  | `Read, Write, Bash(jq:*), Bash(yq:*)`     |
| Code review      | `Read, Grep, Glob`                         |
| File generation  | `Read, Write, Grep`                        |

## Invocation Frontmatter

| Invocation Mode      | Frontmatter                        |
|----------------------|------------------------------------|
| User-invoked only    | `disable-model-invocation: true`   |
| Claude auto-only     | `user-invocable: false`            |
| Both (default)       | _(no invocation flags needed)_     |
| Forked (subagent)    | `context: fork`                    |
| Forked + Explore     | `context: fork` + `agent: Explore` |

## All Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `name` | Display name, becomes `/name` | `name: my-skill` |
| `description` | Triggers auto-invocation (max 1024 chars) | `description: Analyze code...` |
| `argument-hint` | Shown during autocomplete | `argument-hint: [file-path]` |
| `disable-model-invocation` | User-only invoke | `disable-model-invocation: true` |
| `user-invocable` | Claude-only invoke | `user-invocable: false` |
| `allowed-tools` | Restrict available tools | `allowed-tools: Read, Grep, Glob` |
| `context` | Execution context | `context: fork` |
| `agent` | Agent type for forked skills | `agent: Explore` |
| `effort` | Reasoning effort level | `effort: low` |
| `model` | Override model | `model: sonnet` |
| `paths` | File globs that trigger the skill | `paths: ["*.rs", "Cargo.toml"]` |
| `shell` | Shell for `!`command`` execution | `shell: bash` |
| `hooks` | Lifecycle hooks scoped to skill | _(see hooks docs)_ |

## Reference-File Pattern

For skills with substantial content, split into lean SKILL.md + reference files:

1. **SKILL.md**: ~70 lines with bullet principles and `References:` links per section
2. **Reference files**: detailed content loaded only when that section is needed

Benefits:
- Reduces context waste — Claude only loads full detail when a topic arises
- Easier to maintain — each reference file has a single focus
- Scales naturally — add reference files as skill grows

**Link format in SKILL.md sections:**
```markdown
References: [topic-name](references/topic-name.md)
```

**Reference file frontmatter:**
```yaml
---
title: Topic Name
description: What this reference covers
tags: [tag1, tag2]
---
```
