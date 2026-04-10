---
title: Modifying System Prompts
canonical_url: https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts
fetch_before_acting: true
---

# Modifying System Prompts

> Before customizing system prompts, WebFetch https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts for the latest.

## Summary

Four ways to customize Claude's behavior via system prompts, from least to most invasive.

### Default Behavior

The SDK uses a **minimal** system prompt by default (essential tool instructions only). To get the full Claude Code prompt, use the preset.

### Method 1: CLAUDE.md (Project Instructions)

File-based, version-controlled, shared with team. Requires `setting_sources`:

```python
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"},
    setting_sources=["project"],  # Required to load CLAUDE.md
)
```

### Method 2: Preset with Append

Keep full Claude Code behavior, add your instructions:

```python
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": "Always include type hints in Python code.",
    }
)
```

### Method 3: Custom String

Replace the default entirely:

```python
options = ClaudeAgentOptions(
    system_prompt="You are a Python specialist. Write clean, typed code."
)
```

**Warning**: Loses built-in tools guidance, safety instructions, and environment context.

### Method 4: Output Styles

Saved markdown files in `~/.claude/output-styles/` or `.claude/output-styles/`. Loaded via `setting_sources`.

### Comparison

| Method | Persistence | Tools Preserved | Shared |
|--------|-------------|-----------------|--------|
| CLAUDE.md | Per-project file | Yes | Via git |
| Preset + append | Session only | Yes | In code |
| Custom string | Session only | No | In code |
| Output styles | Saved files | Yes | Via filesystem |

### Key Point

`setting_sources` is required to load CLAUDE.md. The `claude_code` preset alone does NOT load it.
