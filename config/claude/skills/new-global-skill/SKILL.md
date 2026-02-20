---
name: new-global-skill
description: Interactive wizard to create new global Claude Code skills for dotfiles distribution. Use when creating skills available across all projects, adding personal workflows to dotfiles, or scaffolding ~/.claude/skills. Keywords: create global skill, new global skill, dotfiles skill, personal skill, cross-project skill, global workflow
---

# New Global Skill Creator

Interactive wizard to scaffold a new global Claude Code skill for distribution via dotfiles.

## Workflow

1. **Gather requirements** — capability type, invocation mode, scope, tool access via AskUserQuestion
2. **Name & describe** — kebab-case name + trigger-rich description
3. **Generate content** — pick template, avoid project-specific assumptions
4. **Create files** — write SKILL.md (+ reference files for advanced skills) in `config/claude/skills/`
5. **Confirm & install** — show file tree, activation phrases, and symlink command

---

## Requirements Gathering

- Ask four targeted questions (capability, invocation, scope, tools) before writing any files
- Never assume invocation mode or tool access — always confirm
- Use AskUserQuestion tool with 2-4 options per question
- Read reference for exact question structure

References: [requirements-wizard](references/requirements-wizard.md)

---

## Naming & Description

- kebab-case, max 64 chars, describe what it does not how
- Description must include: functionality + trigger scenarios + keywords
- Template: `[Primary function]. Use when [scenarios]. Keywords: [terms].`
- Max 1024 chars for description; include 5-10 trigger keywords

References: [naming-and-descriptions](references/naming-and-descriptions.md)

---

## Skill Content

- Choose the template matching the capability (code analysis, test gen, docs, data)
- Global skills must avoid project-specific tech stack assumptions — they run everywhere
- For advanced scope: use reference-file pattern — lean SKILL.md + references/ dir
- Skills with >150 lines of content should split into reference files

References: [skill-templates](references/skill-templates.md)

---

## File Structure & Tools

- Simple: `config/claude/skills/<name>/SKILL.md` only
- Advanced: add `references/`, `scripts/`, or `templates/` subdirectories
- Add `allowed-tools:` frontmatter if user chose restricted tool access
- Common combos: read-only = `Read, Grep, Glob`; data = `Read, Write, Bash(jq:*)`

References: [file-structure-and-tools](references/file-structure-and-tools.md)

---

## Confirmation & Installation

- Show created file tree with `ls -R config/claude/skills/<name>/`
- List example phrases that would activate the skill
- Explain why the description will trigger reliably
- Remind user to run `./scripts/link-config.sh` (or manually symlink) and restart Claude Code

References: [best-practices](references/best-practices.md)

---

## Guardrails

- Do not create files until all four requirement questions are answered
- Do not hard-code machine paths or secrets in generated skills
- Generated skills with non-trivial content (>150 lines) should themselves use the reference-file pattern
- Avoid project-specific assumptions — global skills must work across all projects
