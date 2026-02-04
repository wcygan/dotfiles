---
name: create-pr
description: Create a pull request using git and GitHub CLI. Handles the full workflow from committing changes to opening a PR. Use when creating a PR, opening a pull request, submitting changes for review, or pushing a branch for review. Keywords: pull request, PR, create PR, open PR, submit PR, push for review, code review
---

# Create Pull Request Workflow

End-to-end workflow for creating a pull request from local changes.

## Pre-flight Checks

Before creating a PR, verify:

```bash
# Check for uncommitted changes
git status

# Verify on correct branch (not main/master)
git branch --show-current

# Check remote is set
git remote -v
```

## Workflow Steps

### 1. Ensure Clean Working State

```bash
# Stage all changes (or specific files)
git add -A
# Or selectively:
git add src/feature.ts tests/feature.test.ts

# Commit with descriptive message
git commit -m "feat: add user authentication flow"
```

**Commit message conventions:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance

### 2. Create Feature Branch (if not already on one)

```bash
# Create and switch to new branch
git checkout -b feat/user-auth

# Or from a specific base
git checkout -b feat/user-auth origin/main
```

**Branch naming:**
- `feat/description` - Features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Refactoring

### 3. Push Branch to Remote

```bash
# Push and set upstream
git push -u origin HEAD

# Or explicit branch name
git push -u origin feat/user-auth
```

### 4. Create Pull Request

**Interactive (recommended for first-time):**
```bash
gh pr create
```

**With options:**
```bash
gh pr create \
  --title "feat: Add user authentication" \
  --body "## Summary
Adds user authentication flow with JWT tokens.

## Changes
- Add login endpoint
- Add session management
- Add auth middleware

## Testing
- [x] Unit tests pass
- [x] Manual testing complete

Closes #123"
```

**As draft:**
```bash
gh pr create --draft --title "WIP: User authentication"
```

**With reviewers and labels:**
```bash
gh pr create \
  --title "feat: Add user auth" \
  --reviewer teammate1,teammate2 \
  --label enhancement,auth \
  --assignee @me
```

### 5. Verify PR Created

```bash
# View the PR
gh pr view --web

# Or check status
gh pr status
```

## Quick One-Liner

For simple changes when already on a feature branch:

```bash
git add -A && git commit -m "feat: description" && git push -u origin HEAD && gh pr create --fill
```

The `--fill` flag auto-populates title from commit and body from commit messages.

## Common Scenarios

### From Issue

```bash
# Create branch from issue
gh issue develop 123 --checkout

# Make changes, then...
git add -A && git commit -m "fix: resolve issue #123"
git push -u origin HEAD
gh pr create --title "Fix #123: Description" --body "Closes #123"
```

### Update Existing PR

```bash
# Make more changes
git add -A && git commit -m "address review feedback"
git push
# PR updates automatically
```

### Rebase Before PR

```bash
# Update with latest main
git fetch origin
git rebase origin/main

# Force push if needed (only on feature branches!)
git push --force-with-lease
```

## Checklist Before Creating PR

1. ✅ Tests pass locally
2. ✅ Code is formatted/linted
3. ✅ Commit messages are clear
4. ✅ Branch is up-to-date with base
5. ✅ No unintended files staged
6. ✅ PR title describes the change
7. ✅ PR body explains why, not just what

## Error Recovery

**Wrong branch:**
```bash
# Move commits to new branch
git checkout -b correct-branch
git checkout main
git reset --hard origin/main
```

**Forgot to branch:**
```bash
# Already committed to main? Move to feature branch
git branch feat/my-feature
git reset --hard origin/main
git checkout feat/my-feature
```

**Need to amend last commit:**
```bash
git add -A
git commit --amend --no-edit
git push --force-with-lease  # If already pushed
```
