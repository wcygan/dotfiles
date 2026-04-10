---
name: claude-agent-sdk
description: >
  Claude Agent SDK for Python (and TypeScript) — building programmatic agents with
  claude-agent-sdk. Covers query(), ClaudeSDKClient, custom tools, hooks, permissions,
  sessions, subagents, structured outputs, file checkpointing, system prompts, skills,
  slash commands, and tool search. Auto-loads when working with claude_agent_sdk imports,
  agent SDK code, or building autonomous Claude agents.
  Keywords: claude-agent-sdk, agent sdk, query, ClaudeSDKClient, ClaudeAgentOptions,
  custom tools, mcp server, hooks, permissions, subagents, structured output, sessions,
  file checkpointing, tool search, agent loop, slash commands, skills sdk
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch, Bash(cat *), Bash(gh *), Bash(git *), Bash(ls *), Bash(uv *)
---

# Claude Agent SDK

Reference knowledge for building agents with the Claude Agent SDK (Python focus, TypeScript parity).

## Fetch Strategy

- **Quick answers**: use the local summary in the reference file
- **Before making changes or giving definitive guidance**: WebFetch the canonical URL to get the latest docs, then act on the live content

## Installation (Python with uv)

```bash
uv init && uv add claude-agent-sdk
```

Or with pip:
```bash
pip install claude-agent-sdk
```

Requires Python 3.10+. The Claude Code CLI is bundled with the package.

## Core APIs

| API | Use Case |
|-----|----------|
| `query()` | One-shot tasks, new session per call |
| `ClaudeSDKClient` | Multi-turn conversations, maintains context |

## Quick Start

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs and fix them.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

## Topic Routing

| Topic | Reference | Canonical URL |
|-------|-----------|---------------|
| Getting started with Python (uv) | [quickstart](references/quickstart.md) | https://platform.claude.com/docs/en/agent-sdk/quickstart#python-(uv) |
| Python SDK full API reference | [python-sdk](references/python-sdk.md) | https://platform.claude.com/docs/en/agent-sdk/python |
| GitHub repo and README | [github-repo](references/github-repo.md) | https://github.com/anthropics/claude-agent-sdk-python |
| Agent loop lifecycle and messages | [agent-loop](references/agent-loop.md) | https://platform.claude.com/docs/en/agent-sdk/agent-loop |
| Loading CLAUDE.md, skills, hooks | [claude-code-features](references/claude-code-features.md) | https://platform.claude.com/docs/en/agent-sdk/claude-code-features |
| Session management (resume, fork) | [sessions](references/sessions.md) | https://platform.claude.com/docs/en/agent-sdk/sessions |
| Custom tool definitions | [custom-tools](references/custom-tools.md) | https://platform.claude.com/docs/en/agent-sdk/custom-tools |
| Scaling to many tools | [tool-search](references/tool-search.md) | https://platform.claude.com/docs/en/agent-sdk/tool-search |
| Permission modes and rules | [permissions](references/permissions.md) | https://platform.claude.com/docs/en/agent-sdk/permissions |
| User input and approval flows | [user-input](references/user-input.md) | https://platform.claude.com/docs/en/agent-sdk/user-input |
| Intercepting tool calls with hooks | [hooks](references/hooks.md) | https://platform.claude.com/docs/en/agent-sdk/hooks |
| File change tracking and rewind | [file-checkpointing](references/file-checkpointing.md) | https://platform.claude.com/docs/en/agent-sdk/file-checkpointing |
| Validated JSON output schemas | [structured-outputs](references/structured-outputs.md) | https://platform.claude.com/docs/en/agent-sdk/structured-outputs |
| Customizing system prompts | [system-prompts](references/system-prompts.md) | https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts |
| Spawning isolated subagents | [subagents](references/subagents.md) | https://platform.claude.com/docs/en/agent-sdk/subagents |
| Built-in and custom slash commands | [slash-commands](references/slash-commands.md) | https://platform.claude.com/docs/en/agent-sdk/slash-commands |
| Skills in the SDK | [skills-sdk](references/skills-sdk.md) | https://platform.claude.com/docs/en/agent-sdk/skills |
| Skills authoring (Claude Code) | [skills-authoring](references/skills-authoring.md) | https://code.claude.com/docs/en/skills |

## Key Concepts

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Unmatched tools trigger `canUseTool` callback |
| `acceptEdits` | Auto-approves file edits |
| `dontAsk` | Denies anything not in `allowed_tools` |
| `bypassPermissions` | Runs everything (sandboxed envs only) |
| `plan` | Read-only; tools that modify are blocked |

### Message Types

- `SystemMessage` — session lifecycle (`init`, `compact_boundary`)
- `AssistantMessage` — Claude's responses and tool calls
- `UserMessage` — tool results fed back to Claude
- `ResultMessage` — final message with cost, usage, session_id
- `StreamEvent` — partial messages (when enabled)

### Tool Naming for Custom Tools

Pattern: `mcp__{server_name}__{tool_name}`

Example: server `"weather"` + tool `"get_temperature"` → `mcp__weather__get_temperature`

### Auth Providers

- **Anthropic API**: `ANTHROPIC_API_KEY` in `.env`
- **Amazon Bedrock**: `CLAUDE_CODE_USE_BEDROCK=1`
- **Google Vertex AI**: `CLAUDE_CODE_USE_VERTEX=1`
- **Microsoft Azure**: `CLAUDE_CODE_USE_FOUNDRY=1`
