---
allowed-tools: Read, Bash(rg:*), Bash(fd:*), Bash(git:*)
description: Comprehensive code review with architectural insights
---

## Context

- Project type: !`fd "(package.json|deno.json|Cargo.toml|go.mod|pom.xml)" . -d 1 | head -1 | xargs basename 2>/dev/null || echo "unknown"`
- Git status: !`git status --porcelain | wc -l | tr -d ' ' || echo "0"` uncommitted files
- Recent commits: !`git log --oneline -3 2>/dev/null | head -3 || echo "No git history"`
- Current branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- Code files: !`fd "\.(ts|js|rs|go|java|py)$" . | wc -l | tr -d ' ' || echo "0"` files

## Your task

Conduct a comprehensive code review focusing on:

1. **Architecture & Design** - Overall structure, patterns, and design decisions
2. **Code Quality** - Readability, maintainability, and adherence to best practices
3. **Performance** - Potential bottlenecks, inefficiencies, or optimization opportunities
4. **Security** - Vulnerability scanning, input validation, and security best practices
5. **Testing** - Test coverage, test quality, and missing test scenarios

**Review Process:**

- Analyze the overall project structure and architecture
- Review recent changes and commits for context
- Identify code smells, anti-patterns, and technical debt
- Suggest specific improvements with examples
- Prioritize findings by impact and effort required

**Focus Areas:**

- Error handling and edge cases
- Resource management and cleanup
- API design and consistency
- Documentation completeness
- Configuration and environment handling

Provide actionable feedback with specific file references and improvement suggestions.
