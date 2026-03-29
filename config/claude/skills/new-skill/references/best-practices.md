---
title: Best Practices
description: Quality checklist, activation examples, and confirmation workflow for generated skills
tags: [best-practices, quality, confirmation, activation]
---

# Best Practices

## Quality Checklist for Generated Skills

✅ **Descriptive names** — What it does, not how (max 64 chars)
✅ **Rich descriptions** — Functionality + triggers + keywords (max 1024 chars)
✅ **Clear instructions** — Step-by-step guidance for Claude
✅ **Project context** — Reference tech stack, conventions, CLAUDE.md
✅ **Structured output** — Specify format, tools, file locations
✅ **Examples** — Show expected patterns and formats
✅ **Tool specification** — Mention which tools to use
✅ **Progressive disclosure** — Lean SKILL.md + optional reference files for detail

## Confirmation Workflow

After creating skill files:

1. Show created file structure: `ls -R .claude/skills/<name>/`
2. Explain what the skill does and what phrases will trigger it
3. Provide 3-4 example user requests that would activate it
4. Suggest a test request the user can try immediately

## Activation Examples

| Skill | Example Trigger Phrases |
|-------|-------------------------|
| `code-quality-analyzer` | "Review this code for security issues" |
| `test-suite-generator` | "I need tests for this module" / "Improve coverage" |
| `documentation-generator` | "Generate a README for this project" |
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

## Dynamic Context Injection

For forked skills (`context: fork`), the subagent has no conversation history. Use
`` !`command` `` syntax to inject project state before Claude sees the prompt.

### When to use

- **Forked skills** that need project context (git state, file listings, tool versions)
- **Any skill** that benefits from live data at invocation time
- **Not needed** for inline skills that already have conversation context

### Syntax

```markdown
Current branch: !`git branch --show-current`
Recent commits: !`git log --oneline -5`
Project type: !`ls -1 package.json Cargo.toml go.mod 2>/dev/null`
```

### Error handling

Always use `2>/dev/null` or `|| echo 'fallback'` for commands that might not exist:

```markdown
Node version: !`node --version 2>/dev/null || echo 'not installed'`
```

### Bundled scripts

Use `${CLAUDE_SKILL_DIR}` to reference scripts bundled with the skill:

```markdown
Analysis: !`python ${CLAUDE_SKILL_DIR}/scripts/analyze.py`
```

### Key considerations

- Commands run **before** Claude sees anything — this is preprocessing
- Keep commands fast — they block skill loading
- Command output replaces the placeholder inline
- If a command fails silently, the placeholder becomes empty string

## Propagating the Reference Pattern

When generating a new skill that will have substantial content (>150 lines), structure it using the same reference-file pattern:

```
.claude/skills/<new-skill-name>/
├── SKILL.md              (lean overview, ~70 lines)
└── references/
    ├── workflow.md       (detailed step-by-step)
    ├── templates.md      (output templates)
    └── examples.md       (worked examples)
```

This keeps the main SKILL.md readable and context-efficient.
