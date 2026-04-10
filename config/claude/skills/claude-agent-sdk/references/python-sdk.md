---
title: Python SDK Reference
canonical_url: https://platform.claude.com/docs/en/agent-sdk/python
fetch_before_acting: true
---

# Python SDK Reference

> Before implementing or giving definitive API guidance, WebFetch https://platform.claude.com/docs/en/agent-sdk/python for the latest.

## Table of Contents

- [query() function](#query-function)
- [ClaudeSDKClient class](#claudesdkclient-class)
- [ClaudeAgentOptions](#claudeagentoptions)
- [Message types](#message-types)
- [Tool definition](#tool-definition)
- [Session management](#session-management)
- [Error types](#error-types)

## query() Function

Creates a new session per call. Best for one-shot tasks.

```python
async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeAgentOptions | None = None,
    transport: Transport | None = None,
) -> AsyncIterator[Message]
```

## ClaudeSDKClient Class

Maintains conversation context across multiple exchanges. Use as async context manager.

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("First question")
    async for msg in client.receive_response():
        print(msg)
    await client.query("Follow-up")  # context retained
    async for msg in client.receive_response():
        print(msg)
```

Key methods: `connect()`, `query()`, `receive_messages()`, `receive_response()`, `interrupt()`, `set_permission_mode()`, `set_model()`, `rewind_files()`, `disconnect()`

## ClaudeAgentOptions

Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `allowed_tools` | `list[str]` | Auto-approve these tools |
| `disallowed_tools` | `list[str]` | Block these tools |
| `permission_mode` | `PermissionMode` | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `system_prompt` | `str \| SystemPromptPreset` | Custom or preset system prompt |
| `mcp_servers` | `dict[str, McpServerConfig]` | MCP server configs |
| `max_turns` | `int` | Cap tool-use round trips |
| `max_budget_usd` | `float` | Cap spend |
| `model` | `str` | Model ID override |
| `cwd` | `str \| Path` | Working directory |
| `output_format` | `dict` | Structured output schema |
| `can_use_tool` | `CanUseTool` | Permission callback |
| `hooks` | `dict[HookEvent, list[HookMatcher]]` | Programmatic hooks |
| `agents` | `dict[str, AgentDefinition]` | Subagent definitions |
| `setting_sources` | `list[SettingSource]` | Load from `"user"`, `"project"`, `"local"` |
| `enable_file_checkpointing` | `bool` | Track file changes |
| `thinking` | `ThinkingConfig` | `adaptive`, `enabled` (with budget), or `disabled` |
| `effort` | `Literal["low","medium","high","max"]` | Reasoning depth |
| `resume` | `str` | Resume session by ID |
| `fork_session` | `bool` | Fork from resumed session |
| `continue_conversation` | `bool` | Continue most recent session |
| `env` | `dict[str, str]` | Environment variables |

## Message Types

```python
Message = UserMessage | AssistantMessage | SystemMessage | ResultMessage | StreamEvent | RateLimitEvent
```

- **AssistantMessage**: `content: list[ContentBlock]`, `model`, `usage`
- **ResultMessage**: `subtype` (`success`, `error_max_turns`, `error_max_budget_usd`, etc.), `session_id`, `total_cost_usd`, `usage`, `structured_output`
- **Content blocks**: `TextBlock`, `ThinkingBlock`, `ToolUseBlock`, `ToolResultBlock`

## Tool Definition

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("name", "description", {"param": type})
async def my_tool(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": "result"}]}

server = create_sdk_mcp_server(name="my-server", version="1.0.0", tools=[my_tool])
```

## Session Management

```python
from claude_agent_sdk import list_sessions, get_session_messages, tag_session

sessions = list_sessions(directory="/path", limit=10)
messages = get_session_messages(session_id="...", directory="/path")
tag_session(session_id="...", tag="needs-review")
```

## Error Types

- `ClaudeSDKError` — base
- `CLINotFoundError` — Claude Code not installed
- `CLIConnectionError` — connection failed
- `ProcessError` — process failed (has `exit_code`, `stderr`)
- `CLIJSONDecodeError` — parse failure
