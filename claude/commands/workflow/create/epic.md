---
allowed-tools: Read, Write, Bash(git:*), Bash(gh:*), Bash(fd:*)
description: Plan and coordinate large-scale development epics
---

## Context

- Epic target: $ARGUMENTS
- Current repository: !`git remote get-url origin 2>/dev/null | sed 's/.*\///' | sed 's/\.git$//' || echo "unknown"`
- Current branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- Organization repos: !`gh repo list --limit 5 --json name 2>/dev/null | jq -r '.[].name' | head -5 || echo "GitHub CLI not configured"`

## Your task

Plan and coordinate a large-scale development epic:

1. **Epic Analysis** - Break down the epic into manageable components
2. **Repository Impact** - Identify which repos/services will be affected
3. **Dependencies** - Map out task dependencies and critical path
4. **Execution Plan** - Create a phased implementation strategy
5. **Coordination** - Define communication and tracking approach

**Epic Planning Process:**

- Scope definition and success criteria
- Technical design and architecture decisions
- Task breakdown with effort estimates
- Risk assessment and mitigation strategies
- Resource allocation and timeline

**Common Epic Types:**

- **Feature Rollouts**: Multi-service feature development
- **Infrastructure Migration**: Technology stack changes
- **Architecture Refactoring**: System-wide improvements
- **Security Initiatives**: Cross-cutting security improvements

Start by analyzing the epic scope and identifying the key components that need to be addressed.
