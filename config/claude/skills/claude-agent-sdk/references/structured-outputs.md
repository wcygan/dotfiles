---
title: Structured Outputs
canonical_url: https://platform.claude.com/docs/en/agent-sdk/structured-outputs
fetch_before_acting: true
---

# Get Structured Output from Agents

> Before implementing structured outputs, WebFetch https://platform.claude.com/docs/en/agent-sdk/structured-outputs for the latest.

## Summary

Define a JSON Schema for the output shape. Agent uses tools freely, then returns validated JSON matching your schema.

### Basic Usage

```python
schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "founded_year": {"type": "number"},
    },
    "required": ["company_name"],
}

async for message in query(
    prompt="Research Anthropic",
    options=ClaudeAgentOptions(output_format={"type": "json_schema", "schema": schema}),
):
    if isinstance(message, ResultMessage) and message.structured_output:
        print(message.structured_output)
```

### With Pydantic (Type-Safe)

```python
from pydantic import BaseModel

class FeaturePlan(BaseModel):
    feature_name: str
    summary: str
    steps: list[Step]
    risks: list[str]

options = ClaudeAgentOptions(
    output_format={"type": "json_schema", "schema": FeaturePlan.model_json_schema()}
)

# Parse result
if isinstance(message, ResultMessage) and message.structured_output:
    plan = FeaturePlan.model_validate(message.structured_output)
```

### Error Handling

| Result Subtype | Meaning |
|---------------|---------|
| `success` | Output validated successfully |
| `error_max_structured_output_retries` | Couldn't produce valid output |

### Tips

- Keep schemas focused — deeply nested required fields are harder to satisfy
- Make fields optional when task might not have all info
- Use clear prompts — ambiguous prompts make output harder
- Supports: all basic types, enum, const, required, nested objects, `$ref`
