---
title: Permissions
canonical_url: https://platform.claude.com/docs/en/agent-sdk/permissions
fetch_before_acting: true
---

# Configure Permissions

> Before implementing permission logic, WebFetch https://platform.claude.com/docs/en/agent-sdk/permissions for the latest.

## Summary

Permissions control how Claude uses tools via modes, allow/deny rules, hooks, and callbacks.

### Evaluation Order

1. **Hooks** — can allow, deny, or pass through
2. **Deny rules** — `disallowed_tools` + settings.json denies (even bypasses `bypassPermissions`)
3. **Permission mode** — `bypassPermissions` approves, `acceptEdits` approves file ops, etc.
4. **Allow rules** — `allowed_tools` + settings.json allows
5. **`can_use_tool` callback** — custom approval (skipped in `dontAsk` mode)

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Unmatched tools trigger `can_use_tool`; no callback = deny |
| `acceptEdits` | Auto-approves file edits (Edit, Write, mkdir, rm, mv, cp) |
| `dontAsk` | Denies anything not pre-approved; `can_use_tool` never called |
| `plan` | Read-only tools run; modifying tools blocked |
| `bypassPermissions` | All tools run without prompts (sandbox only!) |

### Allow/Deny Rules

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep"],  # Auto-approved
    disallowed_tools=["Bash"],               # Always denied
    permission_mode="dontAsk",               # Deny everything else
)
```

**Warning**: `allowed_tools` does NOT constrain `bypassPermissions`. Use `disallowed_tools` to block specific tools in bypass mode.

### Scoped Tool Rules

- `"Bash(npm:*)"` — allow only npm commands
- `"Skill(commit)"` — allow specific skill
- `"mcp__server__*"` — wildcard for MCP server

### Dynamic Permission Changes

```python
async with ClaudeSDKClient(options=options) as client:
    await client.set_permission_mode("acceptEdits")  # Change mid-session
```

### Key Design Patterns

| Scenario | Config |
|----------|--------|
| Read-only agent | `allowed_tools=["Read","Glob","Grep"]`, `permission_mode="dontAsk"` |
| Trusted dev workflow | `permission_mode="acceptEdits"` |
| Headless CI | `permission_mode="bypassPermissions"` in container |
| Interactive approval | `permission_mode="default"` + `can_use_tool` callback |
