---
title: Hooks
canonical_url: https://platform.claude.com/docs/en/agent-sdk/hooks
fetch_before_acting: true
---

# Intercept and Control Agent Behavior with Hooks

> Before implementing hooks, WebFetch https://platform.claude.com/docs/en/agent-sdk/hooks for the latest.

## Summary

Hooks are callback functions that fire at specific agent events. Use them to block dangerous operations, log tool calls, transform inputs/outputs, and track lifecycle.

### Available Hook Events

| Event | Python | Description |
|-------|--------|-------------|
| `PreToolUse` | Yes | Before tool execution (can block/modify) |
| `PostToolUse` | Yes | After tool returns |
| `PostToolUseFailure` | Yes | Tool execution failure |
| `UserPromptSubmit` | Yes | Prompt submission |
| `Stop` | Yes | Agent execution stops |
| `SubagentStart` | Yes | Subagent initialized |
| `SubagentStop` | Yes | Subagent completed |
| `PreCompact` | Yes | Before context compaction |
| `PermissionRequest` | Yes | Permission decision needed |
| `Notification` | Yes | Status notifications |
| `SessionStart` | TS only | Session init |
| `SessionEnd` | TS only | Session termination |

### Hook Configuration

```python
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[validate_bash], timeout=120),
            HookMatcher(hooks=[global_logger]),  # No matcher = all tools
        ],
        "PostToolUse": [HookMatcher(hooks=[log_tool_use])],
    }
)
```

### Callback Signature

```python
async def my_hook(
    input_data: dict,      # Event details (tool_name, tool_input, etc.)
    tool_use_id: str | None,  # Correlates Pre/Post events
    context: HookContext,     # Session metadata
) -> dict:
    return {}  # Empty = allow
```

### Hook Outputs

**Allow**: `return {}`

**Block**:
```python
return {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Dangerous command blocked",
    }
}
```

**Modify input**:
```python
return {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": {**input_data["tool_input"], "file_path": "/sandbox/..."},
    }
}
```

**Inject context**: `return {"systemMessage": "Remember: /etc is protected"}`

**Async (fire-and-forget)**: `return {"async_": True, "asyncTimeout": 30000}`

### Priority Rules

**deny > ask > allow** — if any hook returns deny, operation is blocked.

### Matchers

- `"Bash"` — match specific tool
- `"Write|Edit"` — match multiple tools
- `"^mcp__"` — regex for MCP tools
- `None` — match everything

### Common Patterns

- **Chain hooks**: rate limiter → auth check → input sanitizer → logger
- **Subagent tracking**: `SubagentStop` hook to aggregate results
- **HTTP webhooks**: POST tool usage to external service in `PostToolUse`
- **Slack notifications**: Forward `Notification` events to Slack
