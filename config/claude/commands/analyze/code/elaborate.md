---
allowed-tools: Read, Bash(fd:*), Bash(rg:*), Bash(git:*)
description: Detailed technical analysis of code or concept
---

## Context

- Analysis target: $ARGUMENTS
- Current directory: !`pwd`
- Code files: !`fd "\.(rs|go|java|py|js|ts|cpp|c)$" . | wc -l | tr -d ' ' || echo "0"` files
- Project type: !`fd "(package.json|Cargo.toml|go.mod|pom.xml|deno.json)" . -d 2 | head -1 | xargs basename 2>/dev/null || echo "unknown"`
- Git status: !`git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0"` uncommitted files
- Recent commits: !`git log --oneline -3 2>/dev/null | head -3 || echo "No git history"`

## Your task

Provide a comprehensive technical analysis of the specified target:

1. **Overview** - What is this code/concept and its primary purpose?
2. **Architecture** - How is it structured and organized?
3. **Key Components** - What are the main parts and how do they interact?
4. **Implementation Details** - Important patterns, algorithms, or design decisions
5. **Dependencies & Integration** - How it connects to other systems/components
6. **Considerations** - Performance, security, maintainability aspects

**Analysis Approach:**

- If analyzing code: Read the target files and trace through the logic
- If analyzing a concept: Research and explain the technical implementation
- Focus on practical, actionable insights
- Include code examples where relevant
- Identify potential improvements or concerns

Start by determining what specifically should be analyzed from the target argument.
