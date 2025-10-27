---
description: Create pull request with summary
allowed-tools: Bash(git:*), Bash(gh:*)
---

## Context
- Current branch: !`git branch --show-current`
- Base branch: !`git remote show origin | grep 'HEAD branch' | cut -d' ' -f5`
- Changes: !`git diff $(git merge-base HEAD origin/$(git remote show origin | grep 'HEAD branch' | cut -d' ' -f5))...HEAD --stat`

## Task
Create PR with `gh pr create`:

1. Review all commits in this branch (not just latest)
2. Generate concise summary (2-3 bullet points)
3. Include test plan if applicable
4. Push branch if needed with `git push -u origin HEAD`
5. Return PR URL

Template:
```
## Summary
- Key change 1
- Key change 2

## Test Plan
- [ ] Steps to verify
```
