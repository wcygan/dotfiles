---
name: new-skill
description: Interactive wizard to create new agent skills for Claude Code. Use when creating skills, building agent capabilities, adding model-invoked workflows, or setting up skill directories. Keywords: create skill, new skill, agent skill, skill wizard, build skill, SKILL.md
---

# New Skill Creator

Interactive wizard to scaffold a new Claude Code agent skill from scratch.

## Workflow

1. **Gather requirements** — capability type, scope, tool access via AskUserQuestion
2. **Name & describe** — kebab-case name + trigger-rich description
3. **Generate content** — pick template, customize for project context
4. **Create files** — write SKILL.md (+ reference files for advanced skills)
5. **Confirm** — show file tree and example activation phrases

---

## Requirements Gathering

- Ask three targeted questions (capability, scope, tools) before writing any files
- Never assume capability type or tool access — always confirm
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
- Customize for project tech stack from deno.json, CLAUDE.md, existing patterns
- For advanced scope: use reference-file pattern — lean SKILL.md + references/ dir
- Skills with >150 lines of content should split into reference files

References: [skill-templates](references/skill-templates.md)

---

## File Structure & Tools

- Simple: `.claude/skills/<name>/SKILL.md` only
- Advanced: add `references/`, `scripts/`, or `templates/` subdirectories
- Add `allowed-tools:` frontmatter if user chose restricted tool access
- Common combos: read-only = `Read, Grep, Glob`; data = `Read, Write, Bash(jq:*)`

References: [file-structure-and-tools](references/file-structure-and-tools.md)

---

## Confirmation

- Show created file tree with `ls -R .claude/skills/<name>/`
- List example phrases that would activate the skill
- Explain why the description will trigger reliably
- Suggest a test request the user can try immediately

References: [best-practices](references/best-practices.md)

---

## Guardrails

- Do not create files until all three requirement questions are answered
- Do not hard-code machine paths or secrets in generated skills
- Generated skills with non-trivial content (>150 lines) should themselves use the reference-file pattern
- Always read existing CLAUDE.md and project context before generating skill content
