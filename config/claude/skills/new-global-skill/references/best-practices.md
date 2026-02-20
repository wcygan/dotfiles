---
title: Best Practices
description: Quality checklist, activation examples, installation steps, and confirmation workflow for generated global skills
tags: [best-practices, quality, confirmation, activation, installation]
---

# Best Practices

## Quality Checklist for Generated Global Skills

✅ **Descriptive names** — What it does, not how (max 64 chars)
✅ **Rich descriptions** — Functionality + triggers + keywords (max 1024 chars)
✅ **Clear instructions** — Step-by-step guidance for Claude
✅ **Cross-project safe** — No hard-coded project-specific paths, frameworks, or tools
✅ **Invocation mode set** — `disable-model-invocation` or `user-invocable: false` if needed
✅ **Structured output** — Specify format, tools, file locations
✅ **Examples** — Show expected patterns and formats
✅ **Tool specification** — Mention which tools to use
✅ **Progressive disclosure** — Lean SKILL.md + optional reference files for detail

## Confirmation Workflow

After creating skill files:

1. Show created file structure: `ls -R config/claude/skills/<name>/`
2. Explain what the skill does and what phrases will trigger it
3. Provide 3-4 example user requests that would activate it
4. Suggest a test request the user can try immediately
5. **Always show the installation reminder** — global skills need to be linked to activate

## Installation Reminder

Always include this after creating the skill:

```
To activate your new global skill:
1. Run: ./scripts/link-config.sh
   Or manually: ln -sf ~/Development/dotfiles/config/claude/skills/<name> ~/.claude/skills/
2. Start a new Claude Code session to pick up the skill
```

## Activation Examples

| Skill | Example Trigger Phrases |
|-------|-------------------------|
| `code-quality-analyzer` | "Review this code for security issues" |
| `test-suite-generator` | "I need tests for this module" / "Improve coverage" |
| `doc-generator` | "Generate a README for this project" |
| `data-file-processor` | "Parse this JSON file and extract the IDs" |

## Skill Activation Mechanics

Skills activate when user requests match the description keywords. The description is checked against:
- User's explicit request
- Current context (open files, recent commands)
- Conversation topic

**Good trigger phrases include:**
- Action verbs: "review", "analyze", "generate", "extract", "parse"
- Subject matter: "code", "tests", "docs", "JSON", "CSV"
- Outcome focus: "improve coverage", "find security issues"

## Propagating the Reference Pattern

When generating a new skill that will have substantial content (>150 lines), structure it using the same reference-file pattern:

```
config/claude/skills/<new-skill-name>/
├── SKILL.md              (lean overview, ~70 lines)
└── references/
    ├── workflow.md       (detailed step-by-step)
    ├── templates.md      (output templates)
    └── examples.md       (worked examples)
```

This keeps the main SKILL.md readable and context-efficient.

## Global vs Project Skill Reminder

| Concern | Global Skill | Project Skill |
|---------|-------------|---------------|
| Location | `config/claude/skills/<name>/` | `.claude/skills/<name>/` |
| Scope | All projects | Current project only |
| Tech assumptions | Avoid project-specific | Can reference CLAUDE.md |
| Installation | Run `./scripts/link-config.sh` | Committed to project repo |
| Distribution | Via dotfiles | Via project git |
