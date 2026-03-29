---
title: Hooks
canonical_url: https://code.claude.com/docs/en/hooks-guide
fetch_before_acting: true
---

# Hooks

> Before writing or modifying hooks, WebFetch https://code.claude.com/docs/en/hooks-guide for the latest.

## Summary

Hooks are shell commands that execute at specific lifecycle points in Claude Code. They provide deterministic control — actions that always happen, not relying on the LLM to choose.

### Hook Types

- `"type": "command"` — run a shell command (most common)
- `"type": "http"` — POST event data to a URL
- `"type": "prompt"` — single-turn LLM evaluation (Haiku by default)
- `"type": "agent"` — multi-turn verification with tool access

### Key Events

| Event | When | Common Use |
|-------|------|-----------|
| `SessionStart` | Session begins/resumes | Inject context |
| `PreToolUse` | Before tool call | Block dangerous commands |
| `PostToolUse` | After tool call | Auto-format edited files |
| `PermissionRequest` | Permission dialog | Auto-approve safe tools |
| `Notification` | Claude needs input | Desktop notification |
| `Stop` | Claude finishes | Verify completeness |
| `ConfigChange` | Config file changes | Audit logging |
| `PreCompact` / `PostCompact` | Context compaction | Re-inject critical context |

### Exit Codes

- **0** — proceed (stdout added to context for some events)
- **2** — block the action (stderr fed back to Claude)
- **Other** — proceed (stderr logged, not shown)

### Matchers

Filter hooks by tool name, session start type, etc. Regex patterns supported.
Example: `"matcher": "Edit|Write"` fires only on file edits.

### Where to Configure

| Location | Scope |
|----------|-------|
| `~/.claude/settings.json` | All projects |
| `.claude/settings.json` | This project |
| `.claude/settings.local.json` | This project (gitignored) |
| Skill/agent frontmatter | While skill active |

### Common Patterns

- Desktop notifications on `Notification`
- Auto-format with Prettier on `PostToolUse` `Edit|Write`
- Block edits to protected files on `PreToolUse`
- Re-inject context after compaction on `SessionStart` `compact`
- Auto-approve safe permissions on `PermissionRequest`
