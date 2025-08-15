---
allowed-tools: Read, Bash(fd:*), Bash(rg:*), Bash(git:*)
description: Create comprehensive project development plans
---

## Context

- Target project: $ARGUMENTS
- Current directory: !`pwd`
- Project type: !`fd "(package.json|Cargo.toml|go.mod|pom.xml|deno.json)" . | head -1 | xargs basename 2>/dev/null || echo "unknown"`
- Source files: !`fd "\.(js|ts|rs|go|java|py|c|cpp)" . | wc -l | tr -d ' ' || echo "0"` files
- Documentation: !`fd "(README|CONTRIBUTING|CHANGELOG)" . | head -3 || echo "No docs found"`
- Git status: !`git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0"` uncommitted changes

## Your task

Create a comprehensive development plan for the project:

1. **Project Analysis** - Understand current state, architecture, and goals
2. **Requirements Gathering** - Define objectives and success criteria
3. **Task Breakdown** - Organize work into manageable phases and tasks
4. **Resource Planning** - Estimate effort, identify dependencies, set milestones
5. **Risk Assessment** - Identify potential blockers and mitigation strategies

**Planning Framework:**

- **Discovery Phase**: Understand existing codebase and requirements
- **Design Phase**: Architecture and technical decisions
- **Implementation Phase**: Development tasks and priorities
- **Testing Phase**: Quality assurance and validation
- **Deployment Phase**: Release planning and rollout

**Deliverables:**

- Clear project objectives and scope
- Prioritized task list with estimates
- Technical architecture decisions
- Risk mitigation strategies
- Success metrics and milestones

Focus on creating actionable, realistic plans that can be immediately implemented.
