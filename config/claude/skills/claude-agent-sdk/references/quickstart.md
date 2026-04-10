---
title: Quickstart (Python with uv)
canonical_url: https://platform.claude.com/docs/en/agent-sdk/quickstart#python-(uv)
fetch_before_acting: true
---

# Quickstart — Python (uv)

> Before building or giving definitive guidance, WebFetch https://platform.claude.com/docs/en/agent-sdk/quickstart#python-(uv) for the latest.

## Summary

Build an AI agent that reads code, finds bugs, and fixes them autonomously.

### Prerequisites

- Python 3.10+
- An Anthropic account with API key

### Setup

```bash
mkdir my-agent && cd my-agent
uv init && uv add claude-agent-sdk
```

Set API key in `.env`:
```
ANTHROPIC_API_KEY=your-api-key
```

### Minimal Agent

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

### Key Components

- **`query()`** — main entry point, returns async iterator of messages
- **`prompt`** — what you want Claude to do
- **`options`** — configuration: `allowed_tools`, `permission_mode`, `system_prompt`, `mcp_servers`, etc.

### Tool Presets

| Tools | Capability |
|-------|-----------|
| `Read`, `Glob`, `Grep` | Read-only analysis |
| `Read`, `Edit`, `Glob` | Analyze and modify |
| `Read`, `Edit`, `Bash`, `Glob`, `Grep` | Full automation |

### Permission Modes

| Mode | Use Case |
|------|----------|
| `acceptEdits` | Trusted dev workflows |
| `dontAsk` | Locked-down headless agents |
| `bypassPermissions` | Sandboxed CI environments |
| `default` | Custom approval via `canUseTool` |

### Auth Alternatives

- **Bedrock**: `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials
- **Vertex AI**: `CLAUDE_CODE_USE_VERTEX=1` + GCP credentials
- **Azure**: `CLAUDE_CODE_USE_FOUNDRY=1` + Azure credentials
