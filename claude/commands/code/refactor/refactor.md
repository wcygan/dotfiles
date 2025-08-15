---
allowed-tools: Read, Edit, MultiEdit, Bash(fd:*), Bash(rg:*)
description: Identify and apply specific refactoring improvements to code
---

## Context

- Target: $ARGUMENTS
- Project type: !`fd "(deno.json|package.json|Cargo.toml|go.mod|pom.xml)" . | head -1 | xargs basename 2>/dev/null || echo "unknown"`
- Code files: !`fd "\.(java|go|rs|py|ts|js|cpp|c)$" $ARGUMENTS -t f | wc -l | tr -d ' ' || echo "0"` files
- Large files (>200 lines): !`fd "\.(java|go|rs|py|ts|js|cpp|c)$" $ARGUMENTS -x wc -l {} \; 2>/dev/null | awk '{if($1>200) print FILENAME ": " $1 " lines"}' | head -3`
- Git status: !`git status --porcelain $ARGUMENTS 2>/dev/null | head -3 || echo "Clean or not in git"`

## Your task

Analyze the target code for refactoring opportunities and apply improvements:

1. **Identify Code Smells** - Look for long methods, duplicate code, complex conditionals, or large classes
2. **Suggest 2-3 High-Impact Improvements** - Focus on the most valuable refactorings first
3. **Apply One Refactoring** - Make one focused improvement with user confirmation
4. **Verify No Regressions** - Ensure tests still pass after changes

**Common Refactoring Patterns:**

- Extract method from long functions (>20 lines)
- Extract constants from magic numbers/strings
- Simplify complex conditional logic
- Remove duplicate code
- Improve variable/function naming

Start by reading the target file(s) and identifying the most impactful refactoring opportunity.
