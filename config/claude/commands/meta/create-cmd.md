---
description: Create new slash command with best practices
allowed-tools: Read, Write, Bash(fd:*)
argument-hint: <command-name>
---

## Context
- Existing commands: !`fd . config/claude/commands -t f --extension md -x echo {/}`
- Docs: https://docs.claude.com/en/docs/claude-code/slash-commands

## Task
Create command: $ARGUMENTS

Use this template:

```markdown
---
description: Brief purpose (required)
allowed-tools: [specific tools only]
argument-hint: <expected-args>
---

## Context (optional)
[Use ! for dynamic environment data]

## Task
[Clear, focused instructions]
$ARGUMENTS handling as needed
```

Save to: config/claude/commands/<category>/$ARGUMENTS.md

Keep commands simple and focused on single responsibility.
