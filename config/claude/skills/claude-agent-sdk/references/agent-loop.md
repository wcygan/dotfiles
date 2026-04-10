---
title: Agent Loop
canonical_url: https://platform.claude.com/docs/en/agent-sdk/agent-loop
fetch_before_acting: true
---

# How the Agent Loop Works

> Before implementing loop logic or debugging agent behavior, WebFetch https://platform.claude.com/docs/en/agent-sdk/agent-loop for the latest.

## Summary

The SDK runs Claude Code's autonomous execution loop: prompt → evaluate → tool calls → results → repeat → final answer.

### Loop Lifecycle

1. **Receive prompt** — SDK yields `SystemMessage` with subtype `"init"`
2. **Evaluate and respond** — Claude responds with text and/or tool calls → `AssistantMessage`
3. **Execute tools** — SDK runs tools, returns results to Claude
4. **Repeat** — Steps 2-3 cycle (each cycle = one turn)
5. **Return result** — Final `AssistantMessage` (no tool calls) + `ResultMessage`

### Turns

A turn = one round trip (Claude outputs tool calls → SDK executes → results fed back). Turns continue until Claude produces output with no tool calls.

### Controlling the Loop

| Option | Controls | Default |
|--------|----------|---------|
| `max_turns` | Max tool-use round trips | No limit |
| `max_budget_usd` | Max cost before stopping | No limit |
| `effort` | Reasoning depth (`low`, `medium`, `high`, `max`) | Model default |

### Message Types

| Type | When | Content |
|------|------|---------|
| `SystemMessage` | Session lifecycle | `init`, `compact_boundary` |
| `AssistantMessage` | After each Claude response | Text + tool calls |
| `UserMessage` | After tool execution | Tool results |
| `ResultMessage` | Final message always | `subtype`, cost, usage, session_id |
| `StreamEvent` | When partial messages enabled | Raw API events |

### Result Subtypes

| Subtype | Meaning |
|---------|---------|
| `success` | Task completed normally |
| `error_max_turns` | Hit turn limit |
| `error_max_budget_usd` | Hit budget limit |
| `error_during_execution` | API failure or cancellation |
| `error_max_structured_output_retries` | Schema validation failed |

### Context Window

Everything accumulates: system prompt, tool definitions, conversation history, tool I/O. Prompt caching reduces cost for repeated prefixes. **Automatic compaction** summarizes older history when approaching limits (yields `compact_boundary` message).

### Context Efficiency Tips

- Use **subagents** for subtasks (fresh context, only summary returns)
- Be selective with tools (each adds schema to context)
- Watch MCP server costs (all tool schemas per request)
- Use lower `effort` for routine tasks
- Use `ToolSearch` for on-demand tool loading
