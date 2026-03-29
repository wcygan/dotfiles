---
title: Autonomous Loop Protocol
description: The 8 critical rules governing each iteration of the autoresearch loop
tags: [loop, protocol, iteration, rules]
---

# Loop Protocol

## Critical Rules

1. **One change per iteration.** Add one test, fix one lint error, optimize one function. Not multiple.
2. **Read before write.** Every iteration starts with `git log --oneline -5` and reading the target code.
3. **Mechanical verification only.** No subjective "looks better." Command exits 0 or it doesn't.
4. **Commit before verifying.** Use `experiment: <desc>` prefix. Revert is cheap; losing work isn't.
5. **Automatic rollback.** Verify fails or metric regresses → `git revert HEAD --no-edit`. Never leave the repo broken.
6. **Simplicity wins.** Same metric improvement with less code → keep the simpler version.
7. **Git is memory.** Read `git log` each iteration. Don't repeat reverted approaches.
8. **When stuck, change strategy.** After 2 consecutive reverts: re-read all attempts, try a radically different approach. After 3: stop.
