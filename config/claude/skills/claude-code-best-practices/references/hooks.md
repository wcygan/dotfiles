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

### Practical Hook Recipes

**1. Inject dynamic context on session start:**

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo \"Current branch: $(git branch --show-current)\nRecent commits:\n$(git log --oneline -5)\nOpen PRs: $(gh pr list --limit 5 --json number,title -q '.[].number' 2>/dev/null | tr '\\n' ',')\""
      }]
    }]
  }
}
```

**2. Log every Bash command Claude runs:**

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
      }]
    }]
  }
}
```

**3. Route permission prompts externally (e.g., to a webhook/app):**

```json
{
  "hooks": {
    "PermissionRequest": [{
      "matcher": "",
      "hooks": [{
        "type": "http",
        "url": "https://your-webhook.example.com/claude-permissions",
        "headers": { "Authorization": "Bearer $WEBHOOK_TOKEN" },
        "allowedEnvVars": ["WEBHOOK_TOKEN"]
      }]
    }]
  }
}
```

**4. Poke Claude to keep going when it stops prematurely:**

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Check if all requested tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
      }]
    }]
  }
}
```

**5. Re-inject critical context after compaction:**

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
      }]
    }]
  }
}
```

### Additional Events

| Event | When | Use Case |
|-------|------|----------|
| `UserPromptSubmit` | Before Claude processes your prompt | Validate/transform input |
| `SubagentStart` / `SubagentStop` | Subagent lifecycle | Track parallel work |
| `TaskCreated` / `TaskCompleted` | Task lifecycle | External task tracking |
| `CwdChanged` | Directory change | Reload env (e.g., direnv) |
| `FileChanged` | Watched file changes | React to `.env` / `.envrc` changes |
| `WorktreeCreate` / `WorktreeRemove` | Worktree lifecycle | Custom VCS worktree logic |
| `StopFailure` | API error ends turn | Alert on rate limits |
| `SessionEnd` | Session terminates | Cleanup temporary resources |
