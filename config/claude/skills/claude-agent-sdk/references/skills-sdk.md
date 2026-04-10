---
title: Skills in the SDK
canonical_url: https://platform.claude.com/docs/en/agent-sdk/skills
fetch_before_acting: true
---

# Agent Skills in the SDK

> Before configuring skills in SDK applications, WebFetch https://platform.claude.com/docs/en/agent-sdk/skills for the latest.

## Summary

Skills are `SKILL.md` files that give Claude specialized knowledge and invocable workflows. They load on demand (descriptions at startup, full content when triggered).

### Using Skills in the SDK

```python
options = ClaudeAgentOptions(
    cwd="/path/to/project",
    setting_sources=["user", "project"],  # Required to discover skills
    allowed_tools=["Skill", "Read", "Write", "Bash"],  # Skill tool must be listed
)

async for message in query(prompt="Help me process this PDF", options=options):
    print(message)
```

### Skill Locations

| Source | Path | Loaded When |
|--------|------|-------------|
| Project | `.claude/skills/` | `setting_sources` includes `"project"` |
| User | `~/.claude/skills/` | `setting_sources` includes `"user"` |
| Plugin | `<plugin>/skills/` | Plugin enabled |

### Key Points

- Skills must be **filesystem artifacts** — no programmatic registration API
- `allowed-tools` frontmatter in SKILL.md does NOT apply in SDK (use `allowed_tools` in options)
- For locked-down agents: `allowed_tools=["Skill", ...]` + `permission_mode="dontAsk"`
- Claude auto-invokes skills based on `description` field matching

### Discovering Skills

```python
async for message in query(
    prompt="What Skills are available?",
    options=ClaudeAgentOptions(setting_sources=["user", "project"], allowed_tools=["Skill"]),
):
    print(message)
```

### Troubleshooting

1. **Skills not found**: Check `setting_sources` is set (most common issue)
2. **Wrong directory**: `cwd` must point to directory with `.claude/skills/`
3. **Skill not used**: Check description has matching keywords
4. **Skill tool not enabled**: Include `"Skill"` in `allowed_tools`
