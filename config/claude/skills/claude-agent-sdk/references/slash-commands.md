---
title: Slash Commands
canonical_url: https://platform.claude.com/docs/en/agent-sdk/slash-commands
fetch_before_acting: true
---

# Slash Commands in the SDK

> Before implementing slash commands, WebFetch https://platform.claude.com/docs/en/agent-sdk/slash-commands for the latest.

## Summary

Control Claude Code sessions with `/` commands sent as prompt strings through the SDK.

### Sending Slash Commands

```python
async for message in query(prompt="/compact", options=ClaudeAgentOptions(max_turns=1)):
    if isinstance(message, ResultMessage):
        print("Command executed:", message.result)
```

### Built-in Commands

| Command | Purpose |
|---------|---------|
| `/compact` | Summarize older messages to free context |
| `/clear` | Start fresh conversation |
| `/help` | Get help information |

### Discovering Available Commands

```python
async for message in query(prompt="Hello", options=ClaudeAgentOptions(max_turns=1)):
    if isinstance(message, SystemMessage) and message.subtype == "init":
        print("Commands:", message.data["slash_commands"])
```

### Custom Commands (Legacy)

Files in `.claude/commands/` or `~/.claude/commands/`:

```markdown
---
allowed-tools: Read, Grep, Glob
description: Run security scan
---

Analyze the codebase for security vulnerabilities...
```

**Note**: `.claude/commands/` is legacy. Prefer `.claude/skills/<name>/SKILL.md` which supports the same `/name` invocation plus autonomous invocation by Claude.

### Arguments and Placeholders

```markdown
---
argument-hint: [issue-number] [priority]
---
Fix issue #$1 with priority $2.
```

### Dynamic Context

```markdown
## Context
- Current status: !`git status`
- Current diff: !`git diff HEAD`
```

### File References

```markdown
Review these configs:
- Package: @package.json
- TypeScript: @tsconfig.json
```
