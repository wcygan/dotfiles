---
title: Change Priorities
description: How to choose what to change next when iterating on code quality metrics
tags: [prioritization, strategy, changes]
---

# Change Priorities

When choosing what to change, prefer (in order):

1. **Low-hanging fruit** — unused imports, dead code, trivial lint fixes
2. **Missing test coverage** — functions with no tests at all
3. **Uncovered edge cases** — existing tests that miss boundary conditions
4. **Performance** — obvious O(n^2) → O(n) opportunities
5. **Refactoring** — extract duplicated code, simplify complex functions
6. **Type safety** — add annotations, fix type errors

Always check git history and `.autoresearch-results.tsv` before choosing. Never repeat an approach that was already reverted.
