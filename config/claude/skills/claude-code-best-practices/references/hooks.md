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

Exit codes are the blunt instrument. For finer control, print JSON on stdout — see below.

### Returning Structured Output (stdout JSON)

A hook can print a JSON object on stdout to shape Claude's behavior precisely. Event-specific fields nest under `hookSpecificOutput` with a matching `hookEventName` — a **flat** `{"permissionDecision": ...}` is silently ignored. (The full per-event schema lives in the reference, not the guide: https://code.claude.com/docs/en/hooks — WebFetch it before relying on a field.)

**Universal fields** (any event): `continue` (`false` aborts the turn), `stopReason` (shown when `continue:false`), `suppressOutput`, `systemMessage` (warning surfaced to the user).

**`PreToolUse` — decide and rewrite a tool call before it runs:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Writes to .env are blocked by policy",
    "updatedInput": { "command": "git push origin main --dry-run" },
    "additionalContext": "Pushes are dry-run only on this branch."
  }
}
```

- `permissionDecision`: `allow` | `deny` | `ask` | `defer` (`defer` = fall through to normal permission flow)
- `updatedInput`: replaces the tool's input (same schema as `tool_input`) — e.g. inject `--dry-run` mid-flight
- `additionalContext`: text injected alongside the decision

**`SessionStart` — inject context and arm file watching:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Branch: feat/auth. 3 uncommitted files.",
    "watchPaths": ["/abs/path/.env", "/abs/path/tsconfig.json"],
    "initialUserMessage": "Resume the auth refactor.",
    "reloadSkills": true
  }
}
```

`watchPaths` takes **absolute** paths and fires `FileChanged` events on change. `initialUserMessage` applies in `-p` (headless) mode.

**`PostToolUse` / `UserPromptSubmit` — block or annotate after the fact:** top-level `decision: "block"` + `reason`, plus `hookSpecificOutput.additionalContext`. `PermissionRequest` is different again — it returns `hookSpecificOutput.decision` as an object (`{ "behavior": "allow|deny", "updatedInput": {...}, "rules": [...] }`). Confirm the exact shape per event in the reference.

### Async & One-Shot Hooks

Three config fields sit alongside `type` / `command` / `matcher` / `timeout` and change *when* a hook runs:

| Field | Effect |
|-------|--------|
| `async: true` | Runs in the background, never blocks. Fire-and-forget (audit logs, metrics). Cannot block via exit 2. |
| `asyncRewake: true` | Implies `async`. Non-blocking on the happy path; the operation proceeds. But exit 2 **wakes Claude after the fact** — the hook's stderr (or stdout if stderr is empty) is injected as a system reminder so Claude can react to a slow background failure. Use for long secret/security scans. |
| `once: true` | Runs once per session, then removes itself. **Only honored in skill frontmatter** — ignored in `settings.json` and agent frontmatter. |

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.command' >> ~/.claude/audit.log",
        "async": true
      }]
    }]
  }
}
```

### Matchers

Filter hooks by tool name, session start type, etc. Regex patterns supported.
Example: `"matcher": "Edit|Write"` fires only on file edits.

The `if` field (and permission rules generally) use **glob** syntax, not regex: `Bash(npm *)`, `Bash(git commit *)`, `Read(src/**/*.ts)`, `Write(.env*)`, and MCP tools as `mcp__<server>__<tool>` (e.g. `mcp__slack__post_message`, `mcp__slack__*`). Full pattern language: https://code.claude.com/docs/en/permissions.

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

### Gotcha: `env` block does not shell-expand

The `env` block in `settings.json` passes values **literally** — no `${VAR}` expansion. Setting `"TALOSCONFIG": "${CLAUDE_PROJECT_DIR}/talos/config"` exports the literal string `${CLAUDE_PROJECT_DIR}/talos/config`, not the resolved path.

For env vars that need a dynamic project-relative path, use `CLAUDE_ENV_FILE` from a `SessionStart` / `CwdChanged` / `FileChanged` hook. Hooks run in a shell where `$CLAUDE_PROJECT_DIR` is set, and anything appended to `$CLAUDE_ENV_FILE` is applied to every subsequent Bash tool call:

```python
# .claude/hooks/set_env.py (SessionStart hook)
import os, shlex
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
env_file = os.environ.get("CLAUDE_ENV_FILE")
if env_file:
    with open(env_file, "a") as f:
        f.write(f"export MY_VAR={shlex.quote(str(REPO_ROOT / 'some/path'))}\n")
```

Only `SessionStart`, `CwdChanged`, and `FileChanged` hooks have access to `CLAUDE_ENV_FILE`. Append (`>>`), don't overwrite — other hooks may write to it too.

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
