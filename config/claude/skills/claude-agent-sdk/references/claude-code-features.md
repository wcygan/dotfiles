---
title: Claude Code Features in the SDK
canonical_url: https://platform.claude.com/docs/en/agent-sdk/claude-code-features
fetch_before_acting: true
---

# Use Claude Code Features in the SDK

> Before configuring settings sources or loading project features, WebFetch https://platform.claude.com/docs/en/agent-sdk/claude-code-features for the latest.

## Summary

By default, the SDK loads no filesystem settings. Use `setting_sources` to load CLAUDE.md, skills, hooks, and permissions from the filesystem.

### Setting Sources

```python
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # Load from ~/.claude/ and ./.claude/
    allowed_tools=["Skill", "Read", "Edit", "Bash"],
)
```

| Source | Loads From | Content |
|--------|-----------|---------|
| `"project"` | `<cwd>/.claude/` + parent dirs | Project CLAUDE.md, rules, skills, hooks, settings |
| `"user"` | `~/.claude/` | User CLAUDE.md, rules, skills, settings |
| `"local"` | `<cwd>/` | CLAUDE.local.md, settings.local.json |

To match full CLI behavior, use `["user", "project", "local"]`.

### Feature Matrix

| Feature | How to Enable |
|---------|--------------|
| CLAUDE.md | `setting_sources=["project"]` |
| Skills | `setting_sources` + `allowed_tools=["Skill"]` |
| Filesystem hooks | `setting_sources=["project"]` (auto-loaded from settings.json) |
| Programmatic hooks | `hooks={}` parameter in options |
| Subagents | `agents={}` parameter + `allowed_tools=["Agent"]` |
| MCP servers | `mcp_servers={}` parameter |
| System prompt | `system_prompt` parameter |

### Hook Types

| Type | Best For |
|------|----------|
| Filesystem (settings.json) | Shared between CLI and SDK; shell commands, HTTP, prompt, agent types |
| Programmatic (callbacks) | Application-specific logic; structured decisions; in-process |

### Choosing the Right Feature

| Goal | Use |
|------|-----|
| Project conventions always followed | CLAUDE.md via `setting_sources` |
| Reference material loaded when relevant | Skills via `setting_sources` + `Skill` tool |
| Reusable workflow (deploy, review) | User-invocable skills |
| Isolated subtask (research, review) | Subagents via `agents` parameter |
| Deterministic logic on tool calls | Hooks via `hooks` parameter |
| External service access | MCP via `mcp_servers` parameter |
