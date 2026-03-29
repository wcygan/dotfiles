---
title: Skill Authoring Best Practices
canonical_url: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
fetch_before_acting: true
---

# Skill Best Practices

> Before writing or reviewing skills, WebFetch https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices for the latest.

## Core Principles

### Conciseness is Key

Default assumption: Claude is already very smart. For each piece of info, ask:
- Does Claude already know this? (general knowledge → skip)
- Can Claude discover this? (from code/tools → skip)
- Is this the only place Claude will learn this? (→ keep)

### Degrees of Freedom

Match specificity to task fragility:
- **Low freedom** (exact commands): fragile operations, safety-critical steps
- **High freedom** (goals only): context-dependent decisions, creative work

### Progressive Disclosure

Three levels: frontmatter (always loaded) → SKILL.md body (on invoke) → reference files (on demand). Keep SKILL.md under 500 lines. Move detail to references.

### Feedback Loops

Use the "run validator → fix errors → repeat" pattern. Provide checklists Claude can track progress with.

## Description Best Practices

- Front-load the key use case (truncated at ~250 chars in listing)
- Include trigger scenarios and keywords
- Write in third person
- Template: `[What it does]. Use when [scenarios]. Keywords: [terms].`

## Anti-Patterns

- Over-explaining what Claude already knows
- Including README content in SKILL.md
- Deeply nested references (keep one level deep)
- Mixing guidelines with exact commands (pick one per section)
- Descriptions that are too vague to trigger
