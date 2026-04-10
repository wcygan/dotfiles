---
title: User Input & Approvals
canonical_url: https://platform.claude.com/docs/en/agent-sdk/user-input
fetch_before_acting: true
---

# Handle Approvals and User Input

> Before implementing approval flows, WebFetch https://platform.claude.com/docs/en/agent-sdk/user-input for the latest.

## Summary

Claude requests user input for **tool approval** (permissions) and **clarifying questions** (`AskUserQuestion`). Both trigger the `can_use_tool` callback.

### Basic Setup

```python
async def handle_tool_request(tool_name, input_data, context):
    if tool_name == "AskUserQuestion":
        return await handle_questions(input_data)
    # Prompt user and return allow or deny
    return PermissionResultAllow(updated_input=input_data)

options = ClaudeAgentOptions(can_use_tool=handle_tool_request)
```

### Response Types

```python
from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny

# Allow (optionally modify input)
return PermissionResultAllow(updated_input=input_data)
return PermissionResultAllow(updated_input={**input_data, "file_path": "/sandbox/..."})

# Deny (with message Claude sees)
return PermissionResultDeny(message="User rejected this action")
return PermissionResultDeny(message="Try archiving instead of deleting", interrupt=True)
```

### Tool Input Fields

| Tool | Key Fields |
|------|-----------|
| `Bash` | `command`, `description`, `timeout` |
| `Write` | `file_path`, `content` |
| `Edit` | `file_path`, `old_string`, `new_string` |
| `Read` | `file_path`, `offset`, `limit` |

### Handling Clarifying Questions

Claude calls `AskUserQuestion` with structured questions:

```python
async def handle_questions(input_data):
    answers = {}
    for q in input_data.get("questions", []):
        # Display q["question"], q["options"], q["multiSelect"]
        # Collect user selection
        answers[q["question"]] = selected_label  # or comma-joined labels
    return PermissionResultAllow(
        updated_input={"questions": input_data["questions"], "answers": answers}
    )
```

**Question format**: `question` (text), `header` (short label), `options` (2-4 choices with `label`+`description`), `multiSelect` (bool).

### Python Workaround

Python `can_use_tool` requires streaming mode and a dummy `PreToolUse` hook:

```python
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}

options = ClaudeAgentOptions(
    can_use_tool=my_handler,
    hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
)
```

### Limitations

- `AskUserQuestion` not available in subagents
- 1-4 questions per call, 2-4 options each
