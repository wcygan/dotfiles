---
description: Create conventional commit with staged changes
allowed-tools: Bash(git:*), Bash(gh:*)
---

## Context
- Branch: !`git branch --show-current`
- Status: !`git status -sb`
- Recent commits: !`git log --oneline -3`

## Task
Create a conventional commit following this repo's style:

1. Review staged changes with `git diff --staged`
2. Generate semantic commit message (feat:/fix:/docs:/chore:)
3. Focus on "why" not "what"
4. Keep subject line under 72 chars
5. Run `git commit -m "message"`

