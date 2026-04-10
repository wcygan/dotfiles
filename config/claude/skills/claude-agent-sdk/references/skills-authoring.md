---
title: Skills Authoring (Claude Code)
canonical_url: https://code.claude.com/docs/en/skills
fetch_before_acting: true
---

# Skills Authoring — Claude Code

> Before creating or modifying skills, WebFetch https://code.claude.com/docs/en/skills for the latest.

## Summary

Skills are `SKILL.md` files with YAML frontmatter that extend Claude Code. They support auto-invocation, user invocation (`/name`), supporting files, dynamic context injection, and subagent execution.

### File Structure

```
.claude/skills/<name>/
  SKILL.md           # Required — frontmatter + instructions
  references/        # Optional — detail docs loaded on demand
  scripts/           # Optional — bundled scripts
```

### Where Skills Live

| Location | Path | Scope |
|----------|------|-------|
| Personal | `~/.claude/skills/<name>/SKILL.md` | All projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin enabled |

### Key Frontmatter

| Field | Description |
|-------|-------------|
| `name` | Display name, becomes `/name`. ≤64 chars, lowercase+hyphens |
| `description` | When to use it. Critical for auto-invocation. ≤1024 chars |
| `disable-model-invocation` | `true` = user-only invoke |
| `user-invocable` | `false` = Claude-only invoke |
| `allowed-tools` | Restrict tools during skill execution |
| `context: fork` | Run in isolated subagent |
| `agent` | Agent type for forked execution (e.g., `Explore`) |
| `model` | Model override |
| `effort` | Reasoning effort override |
| `argument-hint` | Autocomplete hint (e.g., `[issue-number]`) |

### Invocation Control

| Setting | User | Claude | When Loaded |
|---------|------|--------|-------------|
| (default) | Yes | Yes | Description always, full on invoke |
| `disable-model-invocation: true` | Yes | No | Not until user invokes |
| `user-invocable: false` | No | Yes | Description always, full on invoke |

### String Substitutions

- `$ARGUMENTS` — all args after skill name
- `$N` or `$ARGUMENTS[N]` — positional args (0-based)
- `${CLAUDE_SESSION_ID}` — current session ID
- `${CLAUDE_SKILL_DIR}` — skill directory path
- `` !`command` `` — shell output injected before Claude sees content

### Three Skill Patterns

1. **Reference** (inline, Claude-invoked): background knowledge, no `context: fork`
2. **Task** (user-invoked, inline): step-by-step workflows, `disable-model-invocation: true`
3. **Forked** (subagent): `context: fork` + optional `agent: Explore`, isolated execution

### Bundled Skills

| Skill | Purpose |
|-------|---------|
| `/batch <instruction>` | Fan-out changes across codebase in parallel worktrees |
| `/claude-api` | Load Claude API/SDK reference material |
| `/debug [desc]` | Enable debug logging and troubleshoot |
| `/loop [interval] <prompt>` | Run prompt repeatedly on interval |
| `/simplify [focus]` | Review changed files for quality issues |

### Best Practices

- Keep `SKILL.md` under 500 lines
- Move detailed docs to `references/` (one level deep)
- Front-load description with key use case (truncated at ~250 chars)
- Write descriptions in third person
- Use consistent terminology throughout
- Build feedback loops (validate → fix → repeat)
- Test with fresh Claude instance on similar tasks
