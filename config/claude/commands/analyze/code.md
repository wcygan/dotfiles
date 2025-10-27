---
description: Analyze code structure and patterns
allowed-tools: Bash(fd:*), Bash(rg:*), Read, Task
argument-hint: <path-or-pattern>
---

## Context
- Target: $ARGUMENTS
- Project root: !`git rev-parse --show-toplevel 2>/dev/null || pwd`

## Task
Analyze code focusing on:

1. Architecture and organization
2. Key dependencies and imports
3. Notable patterns or conventions
4. Potential issues or improvements

Use Task tool with Explore agent for multi-file analysis.
Keep findings concise and actionable.
