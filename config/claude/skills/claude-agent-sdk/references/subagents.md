---
title: Subagents
canonical_url: https://platform.claude.com/docs/en/agent-sdk/subagents
fetch_before_acting: true
---

# Subagents in the SDK

> Before implementing subagents, WebFetch https://platform.claude.com/docs/en/agent-sdk/subagents for the latest.

## Summary

Subagents are isolated agent instances for focused subtasks. Benefits: context isolation, parallelization, specialized instructions, tool restrictions.

### Programmatic Definition

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async for message in query(
    prompt="Review the auth module for security issues",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Glob", "Agent"],  # Agent tool required
        agents={
            "code-reviewer": AgentDefinition(
                description="Expert code reviewer for security and quality",
                prompt="You are a code review specialist...",
                tools=["Read", "Grep", "Glob"],  # Read-only
                model="sonnet",
            ),
            "test-runner": AgentDefinition(
                description="Runs and analyzes test suites",
                prompt="You are a test execution specialist...",
                tools=["Bash", "Read", "Grep"],
            ),
        },
    ),
):
    ...
```

### AgentDefinition Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | When to use this agent (Claude reads this) |
| `prompt` | Yes | System prompt for the subagent |
| `tools` | No | Allowed tools (inherits all if omitted) |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |
| `skills` | No | Skill names available to this agent |
| `mcpServers` | No | MCP servers by name or inline config |

### What Subagents Inherit

| Receives | Does NOT receive |
|----------|-----------------|
| Own system prompt + Agent tool's prompt | Parent's conversation history |
| Project CLAUDE.md (via settingSources) | Parent's system prompt |
| Tool definitions (subset or inherited) | Skills (unless in `skills` field) |

### Invocation

- **Automatic**: Claude matches task to agent `description`
- **Explicit**: "Use the code-reviewer agent to check auth"
- **Dynamic**: Factory functions that return `AgentDefinition` based on runtime config

### Common Tool Combos

| Use Case | Tools |
|----------|-------|
| Read-only analysis | `Read`, `Grep`, `Glob` |
| Test execution | `Bash`, `Read`, `Grep` |
| Code modification | `Read`, `Edit`, `Write`, `Grep`, `Glob` |

### Constraints

- Subagents **cannot** spawn their own subagents (no `Agent` in `tools`)
- Parent receives subagent's final message as Agent tool result
- Subagent transcripts persist independently of main conversation
