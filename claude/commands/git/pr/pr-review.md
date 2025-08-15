---
allowed-tools: Bash(gh:*), Bash(git:*), Bash(delta:*), Read
description: Review a GitHub pull request
---

## Context

- Target PR: $ARGUMENTS (PR number or leave empty for current branch PR)
- Current branch: !`git branch --show-current 2>/dev/null || echo "detached"`
- Current PR: !`gh pr list --head "$(git branch --show-current 2>/dev/null)" --json number,title --jq '.[0].number // "none"' 2>/dev/null || echo "none"`
- PRs awaiting review: !`gh pr list --search "review-requested:@me" --json number,title --jq 'length' 2>/dev/null || echo "0"`
- Repository: !`gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null || echo "unknown"`

**PR Details (if specific PR provided):**
!`if [ -n "$ARGUMENTS" ]; then gh pr view $ARGUMENTS --json title,author,state,mergeable,reviewDecision; fi`

## Your task

Conduct a focused pull request review:

1. **Get PR Details** - Show PR title, author, changes summary, and current status
2. **Analyze Changes** - Review the diff for code quality, logic, and potential issues
3. **Check Tests** - Verify test coverage and CI status
4. **Security Review** - Look for security concerns or sensitive data exposure
5. **Provide Feedback** - Suggest specific improvements or approve if ready

**Review Process:**

- If no PR specified, review the current branch PR or list PRs awaiting review
- Focus on logic errors, code style, security issues, and maintainability
- Provide constructive, actionable feedback
- Consider both the code changes and their impact on the overall system

Start by fetching and displaying the PR details and diff.
