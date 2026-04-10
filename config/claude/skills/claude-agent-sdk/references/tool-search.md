---
title: Tool Search
canonical_url: https://platform.claude.com/docs/en/agent-sdk/tool-search
fetch_before_acting: true
---

# Scale to Many Tools with Tool Search

> Before configuring tool search, WebFetch https://platform.claude.com/docs/en/agent-sdk/tool-search for the latest.

## Summary

Tool search dynamically discovers and loads tools on demand instead of loading all definitions into context. Solves context bloat and selection accuracy degradation with 30+ tools.

### How It Works

1. Tool definitions withheld from context
2. Agent receives summary of available tools
3. Agent searches when it needs a capability
4. 3-5 most relevant tools loaded into context
5. Tools stay available for subsequent turns
6. After compaction, previously discovered tools may be removed; agent searches again as needed

### Configuration

Set via `env` option on `query()`:

| `ENABLE_TOOL_SEARCH` | Behavior |
|-----------------------|----------|
| (unset) or `true` | Always on (default) |
| `auto` | Activates when tools exceed 10% of context |
| `auto:N` | Activates at N% threshold |
| `false` | Off — all tools loaded every turn |

```python
options = ClaudeAgentOptions(
    mcp_servers={"enterprise": {"type": "http", "url": "https://tools.example.com/mcp"}},
    allowed_tools=["mcp__enterprise__*"],
    env={"ENABLE_TOOL_SEARCH": "auto:5"},
)
```

### Optimization Tips

- Use descriptive tool names: `search_slack_messages` > `query_slack`
- Include specific keywords in descriptions
- Add system prompt section listing available tool categories

### Limits

- Max 10,000 tools in catalog
- Returns 3-5 tools per search
- Haiku models don't support tool search
