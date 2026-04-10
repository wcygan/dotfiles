---
title: Custom Tools
canonical_url: https://platform.claude.com/docs/en/agent-sdk/custom-tools
fetch_before_acting: true
---

# Give Claude Custom Tools

> Before implementing custom tools, WebFetch https://platform.claude.com/docs/en/agent-sdk/custom-tools for the latest.

## Summary

Define custom tools with the SDK's in-process MCP server so Claude can call your functions, APIs, and domain-specific logic.

### Tool Definition (Python)

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("get_temperature", "Get current temperature at a location", {"latitude": float, "longitude": float})
async def get_temperature(args: dict[str, Any]) -> dict[str, Any]:
    # Fetch data...
    return {"content": [{"type": "text", "text": f"Temperature: 72°F"}]}

weather_server = create_sdk_mcp_server(name="weather", version="1.0.0", tools=[get_temperature])
```

### Using Custom Tools

```python
options = ClaudeAgentOptions(
    mcp_servers={"weather": weather_server},
    allowed_tools=["mcp__weather__get_temperature"],
)
```

Tool name pattern: `mcp__{server_name}__{tool_name}`

Wildcard: `mcp__weather__*` approves all tools from a server.

### Tool Handler Return Format

```python
# Success
return {"content": [{"type": "text", "text": "result"}]}

# Error (Claude sees message, loop continues)
return {"content": [{"type": "text", "text": "Failed: ..."}], "is_error": True}

# Image
return {"content": [{"type": "image", "data": base64_bytes, "mimeType": "image/png"}]}

# Resource
return {"content": [{"type": "resource", "resource": {"uri": "file:///report.md", "text": "# Report..."}}]}
```

### Input Schema Options

- **Simple dict**: `{"latitude": float, "longitude": float}` (all required)
- **Full JSON Schema**: `{"type": "object", "properties": {...}, "required": [...]}` (for enums, optional fields, nested objects)

### Tool Annotations

```python
from claude_agent_sdk import ToolAnnotations

@tool("name", "desc", {"param": str}, annotations=ToolAnnotations(readOnlyHint=True))
async def my_tool(args):
    ...
```

| Field | Default | Effect |
|-------|---------|--------|
| `readOnlyHint` | `False` | Enables parallel execution |
| `destructiveHint` | `True` | Informational |
| `idempotentHint` | `False` | Informational |
| `openWorldHint` | `True` | Informational |

### Controlling Built-in Tools

- `tools=["Read", "Grep"]` — only these built-ins in context (MCP tools unaffected)
- `tools=[]` — remove all built-ins, only MCP tools
- `disallowed_tools=["Bash"]` — block specific tools
