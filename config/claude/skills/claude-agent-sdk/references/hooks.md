---
title: Hooks
canonical_url: https://code.claude.com/docs/en/agent-sdk/hooks
fetch_before_acting: true
---

# Intercept and Control Agent Behavior with Hooks

> Before implementing hooks, WebFetch https://code.claude.com/docs/en/agent-sdk/hooks for the latest. For shell-command hook examples and the full JSON schema, also see https://code.claude.com/docs/en/hooks-guide and https://code.claude.com/docs/en/hooks.

## Summary

Hooks are callback functions that fire at specific agent events. Use them to block dangerous operations, log tool calls, transform inputs/outputs, inject context, and track lifecycle.

### Available Hook Events

| Event | Python | TypeScript | Description |
|-------|--------|------------|-------------|
| `PreToolUse` | Yes | Yes | Before tool execution (block/modify input) |
| `PostToolUse` | Yes | Yes | After successful tool return |
| `PostToolUseFailure` | Yes | Yes | After tool execution failure |
| `UserPromptSubmit` | Yes | Yes | User prompt submitted |
| `Stop` | Yes | Yes | Agent execution stops |
| `SubagentStart` | Yes | Yes | Subagent initialized |
| `SubagentStop` | Yes | Yes | Subagent completed |
| `PreCompact` | Yes | Yes | Before context compaction |
| `PermissionRequest` | Yes | Yes | Permission dialog about to appear |
| `Notification` | Yes | Yes | Status notifications |
| `SessionStart` | No\* | Yes | Session init |
| `SessionEnd` | No\* | Yes | Session termination |
| `Setup` | No | Yes | Session setup/maintenance |
| `TeammateIdle` | No | Yes | Agent team teammate idle |
| `TaskCompleted` | No | Yes | Background task completed |
| `ConfigChange` | No | Yes | Config file changed |
| `WorktreeCreate` | No | Yes | Git worktree created |
| `WorktreeRemove` | No | Yes | Git worktree removed |

\*Python SDK exposes `SessionStart`/`SessionEnd` only as shell-command hooks loaded via `setting_sources=["project"]`. The Claude Code hooks guide has more event types (`PermissionDenied`, `StopFailure`, `InstructionsLoaded`, `CwdChanged`, `FileChanged`, `PostCompact`, `Elicitation`, `TaskCreated`, etc.) that are currently shell-command only and reach Python through `setting_sources`.

### Hook Configuration

```python
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[validate_bash], timeout=60),
            HookMatcher(hooks=[global_logger]),  # No matcher = all tools
        ],
        "PostToolUse": [HookMatcher(hooks=[log_tool_use])],
    }
)
```

`timeout` is in **seconds**, default 60. Multiple `HookMatcher`s in an array execute in order.

### Callback Signature

```python
async def my_hook(
    input_data: dict,       # Typed per event (tool_name, tool_input, message, ...)
    tool_use_id: str | None, # Correlates Pre/Post events for the same tool call
    context,                 # Python: reserved. TS: { signal: AbortSignal }
) -> dict:
    return {}  # Empty = allow
```

All inputs share `session_id`, `cwd`, `hook_event_name`. `agent_id` / `agent_type` are set when the hook fires inside a subagent (Python: `PreToolUse`, `PostToolUse`, `PostToolUseFailure` only; TS: all events).

### Hook Outputs

Two categories of fields:
- **Top-level**: controls the conversation — `systemMessage` injects a visible message to the model; `continue_` (Python) / `continue` (TS) stops the agent after the hook.
- **`hookSpecificOutput`**: controls the current operation — fields depend on the event (`permissionDecision`, `updatedInput`, `additionalContext`, ...).

**Allow**: `return {}`

**Block (PreToolUse)**:
```python
return {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Dangerous command blocked",
    }
}
```

**Modify input (PreToolUse)** — must pair `updatedInput` with `permissionDecision: "allow"`:
```python
return {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": {**input_data["tool_input"], "file_path": "/sandbox/..."},
    }
}
```

**Inject context into the conversation** (any event):
```python
return {"systemMessage": "Remember: /etc is protected"}
```

**Append to tool result (PostToolUse)**:
```python
return {
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "Tool output sanitized",
    }
}
```

**Async (fire-and-forget side effects)**:
```python
return {"async_": True, "asyncTimeout": 30000}  # ms; TS uses `async`
```
Async hooks cannot block, modify, or inject context — the agent has already moved on. Use for logging, metrics, webhooks.

### Priority Rules

**deny > ask > allow** — any hook returning deny blocks the operation. Permission rules from settings still apply on top: returning `"allow"` from a hook does **not** override a deny rule from `settings.json` or managed policy.

### Matchers

- `"Bash"` — specific tool
- `"Write|Edit"` — regex alternation
- `"^mcp__"` — all MCP tools (pattern is `mcp__<server>__<action>`)
- omitted — match everything

Tool-event matchers filter by **tool name only**. For path or argument filtering, inspect `input_data["tool_input"]` inside the callback. Non-tool events match against different fields (notification type, session start source, etc.).

### Common Patterns

- **Chain hooks**: separate `HookMatcher`s in one array run in order — rate limiter → auth → sanitizer → logger
- **Subagent tracking**: `SubagentStop` hook reads `agent_id`, `agent_transcript_path`
- **HTTP webhooks in `PostToolUse`**: wrap in try/except — unhandled exceptions interrupt the agent
- **Slack notifications**: forward `Notification` events (types: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`)
- **Load shell-command hooks**: set `setting_sources=["project"]` in `ClaudeAgentOptions` to pick up `.claude/settings.json` hooks — the only way to use `SessionStart`/`SessionEnd` (and newer Claude Code events) from Python

### Pitfalls

- `updatedInput` must be inside `hookSpecificOutput` with `permissionDecision: "allow"` — top-level `updatedInput` is ignored
- `hookSpecificOutput` always needs the `hookEventName` field
- `Stop` hooks must check `input_data["stop_hook_active"]` and exit early to avoid infinite loops
- Parallel hooks that return `updatedInput` for the same tool call → last write wins, non-deterministic
- `max_turns` limit can end a session before hooks fire
- `permissionDecision: "allow"` cannot override deny rules from permission settings

## Authoring preference: UV scripts

When writing hook **implementations as standalone scripts** — whether as shell-command hooks in `.claude/settings.json` or as subprocess-invoked helpers from SDK callbacks — prefer [UV scripts](https://docs.astral.sh/uv/guides/scripts/) with PEP 723 inline metadata over requirements files or ad-hoc venvs.

Create the hook as an executable script with a shebang that invokes `uv run`:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""PreToolUse hook: block Bash commands that touch /etc."""
import json
import sys

event = json.load(sys.stdin)
command = event.get("tool_input", {}).get("command", "")

if "/etc" in command:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Commands touching /etc are blocked",
        }
    }))
    sys.exit(0)

sys.exit(0)
```

Make it executable (`chmod +x`) and wire it in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block_etc.py"
          }
        ]
      }
    ]
  }
}
```

**Why UV scripts for hooks**:
- Self-contained dependencies declared inline (PEP 723) — no `requirements.txt`, no activated venv
- `uv` resolves and caches the environment on first run, then reuses it
- One file to commit; runs anywhere `uv` is installed
- Fast cold start vs. spawning a full Python project
- Works identically for shell-command hooks and for callbacks that want to subprocess out to isolated logic

For SDK-native callbacks (Python functions passed directly to `HookMatcher(hooks=[...])`), UV scripts aren't applicable — those run in your agent process. Use them when the hook is an external program, which is the only option for shell-command hooks and the cleanest option when you want to isolate dependencies from your agent's environment.
