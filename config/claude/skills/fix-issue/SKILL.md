---
name: fix-issue
description: Take a GitHub issue number, investigate it, implement a fix, write tests, and open a PR. End-to-end workflow from assigned issue to merged PR. Use when you want to fix a specific GitHub issue. Keywords: fix issue, github issue, resolve issue, close issue, implement issue, issue to PR, bug fix
disable-model-invocation: true
argument-hint: [issue-number]
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Fix Issue: End-to-End Issue-to-PR Pipeline

Take a GitHub issue number, investigate the problem, implement a fix with tests, and open a PR. Follows TDD workflow: test first, implement, verify, commit, push.

## Prerequisites

- Current directory is a git repository with a GitHub remote
- `gh` CLI is installed and authenticated
- Working tree is clean (commit or stash changes first)

## Workflow

### 1. Read the Issue

Fetch the full issue details from GitHub.

```bash
gh issue view $ISSUE_NUMBER --json title,body,labels,comments,assignees
```

Extract from the issue:
- **Title and description**: What's the problem?
- **Reproduction steps**: How to trigger it?
- **Expected behavior**: What should happen instead?
- **Labels**: Bug? Feature? Enhancement?
- **Comments**: Any additional context from discussion?

### 2. Assess Clarity

Before proceeding, evaluate whether the issue is actionable:

**Proceed if:**
- The problem is clearly described
- You can identify which code area is affected
- The expected behavior is unambiguous
- The scope is bounded (single bug or small feature)

**STOP and ask the user if:**
- The issue description is vague or contradictory
- Multiple interpretations are possible
- The scope is too broad for a single PR
- You cannot determine what "fixed" looks like
- The issue references external systems you cannot test

When stopping, explain specifically what is unclear and suggest how the user could clarify.

### 3. Create a Feature Branch

```bash
# Generate branch name from issue number and title
ISSUE_TITLE=$(gh issue view $ISSUE_NUMBER --json title -q .title)
SLUG=$(echo "$ISSUE_TITLE" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '-' | head -c 40 | sed 's/-$//')
BRANCH="fix/${ISSUE_NUMBER}-${SLUG}"

git checkout -b "$BRANCH"
```

### 4. Investigate the Codebase

Before writing any code, understand the context:

1. **Find affected code**: Use Grep and Glob to locate relevant files
   - Search for keywords from the issue
   - Trace error messages or stack traces
   - Find the module or component mentioned

2. **Understand existing patterns**: Read surrounding code
   - How is the module structured?
   - What conventions are used (naming, error handling, etc.)?
   - Where do similar fixes exist for reference?

3. **Find existing tests**: Locate test files for the affected code
   - What testing framework is used?
   - What patterns do existing tests follow?
   - What test utilities or helpers exist?

### 5. Write Tests First (TDD)

Following the project's test conventions:

1. **Write a failing test** that demonstrates the bug or verifies the new behavior
   - The test should fail with the current code (proving the bug exists)
   - Use the same patterns as existing tests in the project
   - Name the test clearly: it should describe the expected behavior

2. **Run the test** to confirm it fails for the right reason
   ```bash
   # Run just the new test to verify it fails
   # (use project-appropriate test command)
   ```

3. If the test doesn't fail, re-examine whether you've correctly identified the issue

### 6. Implement the Fix

Write the minimal solution that makes the test pass:

- **Change only what's necessary**: Don't refactor, don't "improve" nearby code
- **Follow existing patterns**: Match the code style around you
- **Stay in scope**: If you discover related issues, note them but don't fix them

### 7. Verify

```bash
# Run the specific test
# Run the full test suite to check for regressions
# Run linter/formatter if the project has one
```

All tests must pass. If the full suite fails on something unrelated, note it but don't fix it in this PR.

### 8. Commit

Create an atomic commit referencing the issue:

```bash
git add [specific files]
git commit -m "fix: [description of what was fixed]

Closes #$ISSUE_NUMBER

[Brief explanation of the root cause and fix approach]"
```

**Commit message rules:**
- First line: `fix:` prefix with concise description
- Reference the issue with `Closes #N`
- If helpful, explain the root cause in the body
- Only include files related to this fix

### 9. Push and Create PR

```bash
git push -u origin HEAD

gh pr create \
  --title "Fix #${ISSUE_NUMBER}: [description]" \
  --body "Closes #${ISSUE_NUMBER}

## Summary
[What was wrong and what this PR does to fix it]

## Root Cause
[Brief explanation of why the bug existed]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [x] New test added that reproduces the issue
- [x] All existing tests pass
- [x] Manually verified (if applicable)"
```

### 10. Present Results

Give the user a concise summary:

```
PR: [URL]
Branch: fix/[number]-[slug]
Issue: #[number]

Changes:
- [file1]: [what changed]
- [file2]: [what changed]

Tests: [N] new, [M] total passing
```

## Guard Rails

### Scope Discipline

- Fix ONLY what the issue describes
- Don't add features, refactor surrounding code, or "improve" things
- If you notice other issues, mention them to the user but don't fix them
- One issue = one PR = one logical change

### When Things Go Wrong

**Tests fail after your fix:**
- Check if your fix introduced a regression
- If the failure is pre-existing, note it in the PR body
- Never skip or delete existing tests to make the suite pass

**Issue is more complex than expected:**
- Stop and explain the complexity to the user
- Suggest breaking it into smaller issues
- Implement only the part that's clear

**Can't reproduce the bug:**
- Document what you tried
- Ask the user for more reproduction details
- Don't submit a speculative fix

### Quality Checks Before PR

1. Tests pass (new + existing)
2. Code follows project conventions
3. Commit message references the issue
4. PR description explains the fix
5. No unrelated changes included
6. No debug code or temporary hacks left in

## Example Session

User runs: `/fix-issue 47`

1. **Read issue #47**: "Login button unresponsive on mobile when keyboard is open"
2. **Assess**: Clear bug, reproducible, scoped to login component
3. **Branch**: `fix/47-login-button-unresponsive-mobile`
4. **Investigate**: Find `LoginForm.tsx`, trace the submit handler, find the click target overlaps with keyboard dismiss area
5. **Test**: Write test simulating mobile viewport with keyboard
6. **Fix**: Adjust click handler to account for viewport resize
7. **Verify**: New test passes, full suite green
8. **PR**: "Fix #47: Login button unresponsive on mobile with keyboard open"

## Key Principles

- **TDD**: Test first, always
- **Minimal**: Fix the issue, nothing more
- **Traceable**: Every PR references an issue, every commit explains why
- **Honest**: If you can't fix it, say so and explain what you found
