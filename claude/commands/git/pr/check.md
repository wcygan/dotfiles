---
allowed-tools: Bash(gh pr view:*), Bash(gh pr checks:*), Bash(gh pr list:*), Bash(gh api:*), Bash(gh run list:*), Bash(gh run view:*), Bash(gh workflow run:*), Bash(git fetch:*), Bash(git checkout:*), Bash(git merge:*), Bash(git diff:*), Bash(jq:*), Bash(osascript:*)
description: Check PR status and CI/CD state
---

# /pr-check

Checks pull request status, CI/CD state, and merge readiness using the GitHub CLI (`gh`).

## Usage

```
/pr-check [PR_NUMBER]
/pr-check status [PR_NUMBER]
/pr-check checks [PR_NUMBER]
/pr-check conflicts [PR_NUMBER]
/pr-check reviews [PR_NUMBER]
/pr-check mergeable [PR_NUMBER]
/pr-check watch [PR_NUMBER]
```

## Description

This command provides comprehensive PR status monitoring through the `gh` CLI, helping you track CI/CD progress, review status, and merge readiness.

### Core Workflow

#### 1. PR Status Overview

```bash
# Get comprehensive PR status
gh pr view $PR_NUMBER --json state,mergeable,mergeStateStatus,statusCheckRollup

# Check review status
gh pr view $PR_NUMBER --json reviewDecision,reviews

# Check merge readiness
gh pr view $PR_NUMBER --json mergeable,mergeStateStatus
```

#### 2. CI/CD Monitoring

##### Check Status

```bash
# List all checks
gh pr checks $PR_NUMBER

# Get detailed check information
gh api repos/{owner}/{repo}/commits/$(gh pr view $PR_NUMBER --json headRefOid -q .headRefOid)/check-runs \
  --jq '.check_runs[] | {name: .name, status: .status, conclusion: .conclusion}'

# Watch checks until completion
gh pr checks $PR_NUMBER --watch
```

##### Failing Checks Analysis

```bash
# Get details of failing checks
gh pr checks $PR_NUMBER --json name,state,conclusion | \
  jq -r '.[] | select(.conclusion == "failure") | .name'

# Get logs from failed checks
gh run list --branch $(gh pr view $PR_NUMBER --json headRefName -q .headRefName) --json databaseId,status,conclusion | \
  jq -r '.[] | select(.conclusion == "failure") | .databaseId' | \
  xargs -I {} gh run view {} --log-failed
```

#### 3. Merge Conflict Detection

```bash
# Check for merge conflicts
gh pr view $PR_NUMBER --json mergeable,mergeStateStatus

# Get conflict details
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER --jq '.mergeable_state'

# Show files with conflicts
git fetch origin pull/$PR_NUMBER/head:pr-$PR_NUMBER
git checkout pr-$PR_NUMBER
git merge origin/main --no-commit --no-ff
git diff --name-only --diff-filter=U
```

### Advanced Features

#### Comprehensive Status Report

The command generates a detailed status report:

```bash
echo "=== PR #$PR_NUMBER Status Report ==="
echo

# Basic info
gh pr view $PR_NUMBER --json title,author,state,createdAt | \
  jq -r '"Title: \(.title)\nAuthor: \(.author.login)\nState: \(.state)\nCreated: \(.createdAt)"'

echo -e "\n--- Reviews ---"
gh pr view $PR_NUMBER --json reviews,reviewDecision | \
  jq -r '.reviews[] | "\(.author.login): \(.state)"'

echo -e "\n--- Checks ---"
gh pr checks $PR_NUMBER

echo -e "\n--- Merge Status ---"
gh pr view $PR_NUMBER --json mergeable,mergeStateStatus | \
  jq -r '"Mergeable: \(.mergeable)\nStatus: \(.mergeStateStatus)"'
```

#### Real-time Monitoring

```bash
# Watch PR status with auto-refresh
while true; do
  clear
  echo "PR #$PR_NUMBER - $(date)"
  echo "=================="
  
  # Show check status
  gh pr checks $PR_NUMBER | head -10
  
  # Show review status
  echo -e "\nReviews:"
  gh pr view $PR_NUMBER --json reviewDecision -q .reviewDecision
  
  sleep 30
done
```

#### Merge Readiness Checklist

```bash
# Automated merge readiness check
echo "Merge Readiness Checklist for PR #$PR_NUMBER"
echo "==========================================="

# Required reviews
REVIEWS=$(gh pr view $PR_NUMBER --json reviewDecision -q .reviewDecision)
[ "$REVIEWS" = "APPROVED" ] && echo "✅ Reviews approved" || echo "❌ Pending reviews"

# CI checks
CHECKS=$(gh pr checks $PR_NUMBER --json state -q '.[] | select(.state != "SUCCESS") | .state' | wc -l)
[ $CHECKS -eq 0 ] && echo "✅ All checks passing" || echo "❌ $CHECKS checks failing"

# Merge conflicts
MERGEABLE=$(gh pr view $PR_NUMBER --json mergeable -q .mergeable)
[ "$MERGEABLE" = "true" ] && echo "✅ No merge conflicts" || echo "❌ Has merge conflicts"

# Branch protection
gh api repos/{owner}/{repo}/branches/main/protection --jq '.required_status_checks.contexts[]' 2>/dev/null
```

## Examples

### Basic Status Check

```bash
# Check current branch PR
/pr-check

# Check specific PR
/pr-check 123
```

### CI/CD Monitoring

```bash
# View all checks
/pr-check checks 456

# Watch checks until completion
/pr-check watch 456
```

### Review Status

```bash
# Check review status
/pr-check reviews 789

# Full merge readiness report
/pr-check mergeable 789
```

### Conflict Resolution

```bash
# Check for conflicts
/pr-check conflicts 123

# Get detailed conflict information
gh pr view 123 --json mergeable,mergeStateStatus,potentialMergeCommit
```

## Status Indicators

### PR States

- `OPEN` - PR is open and active
- `CLOSED` - PR was closed without merging
- `MERGED` - PR was successfully merged

### Check States

- `PENDING` - Check is queued or running
- `SUCCESS` - Check passed
- `FAILURE` - Check failed
- `NEUTRAL` - Check completed with warnings
- `CANCELLED` - Check was cancelled
- `SKIPPED` - Check was skipped
- `TIMED_OUT` - Check exceeded time limit

### Review States

- `APPROVED` - PR has required approvals
- `CHANGES_REQUESTED` - Changes requested by reviewers
- `REVIEW_REQUIRED` - Awaiting required reviews
- `COMMENTED` - Reviews with comments only

### Merge States

- `MERGEABLE` - Ready to merge
- `CONFLICTING` - Has merge conflicts
- `UNKNOWN` - GitHub is still calculating

## Troubleshooting

### Common Issues

#### Stuck Checks

```bash
# Re-run failed checks
gh pr checks $PR_NUMBER --json name,state | \
  jq -r '.[] | select(.state == "FAILURE") | .name' | \
  xargs -I {} gh workflow run {} --ref $(gh pr view $PR_NUMBER --json headRefName -q .headRefName)
```

#### Missing Required Checks

```bash
# List required checks
gh api repos/{owner}/{repo}/branches/main/protection/required_status_checks

# Trigger missing checks
gh pr comment $PR_NUMBER --body "/test all"
```

#### Review Dismissal

```bash
# Check why reviews were dismissed
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews | \
  jq '.[] | select(.dismissed_at != null) | {user: .user.login, dismissed_at: .dismissed_at}'
```

## Integration with Other Commands

- Use after `/pr` to monitor your new PR
- Use during `/pr-review` to check CI status
- Use before merging to ensure all requirements met
- Combine with `/pr-update` to fix failing checks

## Automation Scripts

### PR Health Dashboard

```bash
# Check all your open PRs
gh pr list --author @me --json number,title --jq '.[] | .number' | \
  xargs -I {} sh -c 'echo "PR #{}: " && gh pr checks {} | grep -E "(SUCCESS|FAILURE)" | wc -l'
```

### Notification on Completion

```bash
# Wait for checks and notify
gh pr checks $PR_NUMBER --watch && \
  osascript -e 'display notification "All checks passed!" with title "PR #'$PR_NUMBER'"'
```

## See Also

- `/pr` - Create pull requests
- `/pr-review` - Review pull requests
- `/pr-update` - Update pull requests
