---
title: Skills
canonical_url: https://code.claude.com/docs/en/skills
fetch_before_acting: true
---

# Skills

> Before making changes to skills or giving definitive guidance, WebFetch https://code.claude.com/docs/en/skills for the latest.

## Summary

Skills are `SKILL.md` files with YAML frontmatter that extend Claude Code's capabilities. They replaced the older `.claude/commands/` system (which still works).

### File Structure

```
skills/<name>/
  SKILL.md           # Required — frontmatter + instructions
  references/        # Optional — detail docs loaded on demand
  REFERENCE.md       # Optional — single reference file
  scripts/           # Optional — bundled scripts
```

### Where Skills Live

| Location | Path | Scope |
|----------|------|-------|
| Personal | `~/.claude/skills/<name>/SKILL.md` | All projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin enabled |

### Key Frontmatter Fields

- `name` — display name, becomes `/name`
- `description` — critical for auto-invocation (max 1024 chars)
- `disable-model-invocation: true` — user-only invoke
- `user-invocable: false` — Claude-only invoke
- `context: fork` — run in isolated subagent
- `agent: Explore` — which agent type for forked skills
- `allowed-tools` — restrict available tools
- `effort` — reasoning effort level
- `argument-hint` — shown during autocomplete

### Three Patterns

1. **Reference** (inline, auto-invoked) — background knowledge Claude applies automatically
2. **Task** (user-invoked, inline) — workflows triggered with `/name`
3. **Forked** (subagent context) — isolated execution with `context: fork`

### Dynamic Context

- `$ARGUMENTS` — all args passed after skill name
- `${CLAUDE_SESSION_ID}` — current session ID
- `` !`command` `` — shell output injected before Claude sees the prompt
