---
title: Error Recovery
description: How to handle verify failures, crashes, metric command errors, and git conflicts during the loop
tags: [error, recovery, revert, crash, conflict]
---

# Error Recovery

## Verify command fails (non-zero exit)

1. Attempt ONE quick fix (missing import, typo, syntax)
2. If fix works → amend the experiment commit, continue
3. If fix fails → `git revert HEAD --no-edit`, log failure, next iteration

## Verify command crashes (segfault, OOM, timeout)

Revert immediately. Do not attempt to fix crashes. Log as `crashed`.

## Metric command fails to produce a number

Check if your change broke the metric tooling. If yes → revert. If tool was already broken → stop and report.

## Git revert conflict

```bash
git revert --abort
git reset --hard HEAD~1
```

Log as `conflict` and continue to next iteration.
