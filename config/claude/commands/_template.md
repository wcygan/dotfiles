---
description: Brief purpose (required for SlashCommand tool)
allowed-tools: [list specific tools only]
argument-hint: <expected-args>
---

## Context (optional - use ! for dynamic data)
- Example: !`pwd`
- Example: !`git branch --show-current`

## Task
Clear, focused instructions using $ARGUMENTS or $1, $2 for specific args

Keep commands:
- Simple and single-purpose
- Properly scoped with allowed-tools
- Documented with clear descriptions
- Practical with concrete examples

Related commands: /other-relevant-command
