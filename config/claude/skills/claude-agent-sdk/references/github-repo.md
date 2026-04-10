---
title: GitHub Repository
canonical_url: https://github.com/anthropics/claude-agent-sdk-python
fetch_before_acting: true
---

# claude-agent-sdk-python (GitHub)

> For the latest README and examples, WebFetch https://github.com/anthropics/claude-agent-sdk-python for the latest.

## Summary

Official Python SDK for building agents with Claude Code's autonomous loop.

### Installation

```bash
pip install claude-agent-sdk
```

Prerequisites: Python 3.10+. CLI is bundled with the package.

### Two APIs

| API | Purpose |
|-----|---------|
| `query()` | Simple async queries, new session per call |
| `ClaudeSDKClient` | Interactive conversations, maintains context |

### Key Features

- Full Claude Code toolset (Read, Write, Edit, Bash, etc.)
- Custom tools via in-process MCP servers (`@tool` decorator)
- Programmatic hooks (PreToolUse, PostToolUse, etc.)
- Permission modes (acceptEdits, dontAsk, bypassPermissions)
- Session management (resume, fork, continue)
- Structured outputs via JSON Schema
- File checkpointing and rewind

### Example: Custom Tool

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions

@tool("greet", "Greet a user", {"name": str})
async def greet_user(args):
    return {"content": [{"type": "text", "text": f"Hello, {args['name']}!"}]}

server = create_sdk_mcp_server(name="my-tools", version="1.0.0", tools=[greet_user])
options = ClaudeAgentOptions(
    mcp_servers={"tools": server},
    allowed_tools=["mcp__tools__greet"],
)
```

### Example: Hooks

```python
async def check_bash(input_data, tool_use_id, context):
    command = input_data["tool_input"].get("command", "")
    if "rm -rf" in command:
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "Blocked"}}
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Bash", hooks=[check_bash])]},
)
```

### Examples in Repo

- `examples/quick_start.py` — minimal agent
- `examples/streaming_mode.py` — real-time streaming
- `examples/mcp_calculator.py` — custom tools
- `examples/hooks.py` — hook patterns

### Migration from < 0.1.0

- `ClaudeCodeOptions` renamed to `ClaudeAgentOptions`
- Merged system prompt configuration
- New programmatic subagents and session forking
