---
allowed-tools: TodoWrite, Bash(git:*), Read
description: Start working on a new task or project
---

## Context

- Target task: $ARGUMENTS
- Current directory: !`pwd`
- Git status: !`git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0"` uncommitted files
- Current branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`

## Your task

Help start working on the specified task:

1. **Understand the Task** - Clarify what needs to be accomplished
2. **Check Prerequisites** - Ensure environment and dependencies are ready
3. **Create Todo List** - Break down the work into manageable steps
4. **Set Up Workspace** - Prepare any necessary files or branch setup
5. **Begin Implementation** - Start with the first actionable step

**Common Workflows:**

- **New Feature**: Create branch, write tests first, implement incrementally
- **Bug Fix**: Reproduce issue, identify root cause, create minimal fix
- **Refactoring**: Ensure tests exist, make small safe changes, verify
- **Research**: Define questions, gather information, document findings

Focus on getting started quickly with a clear plan of action.
