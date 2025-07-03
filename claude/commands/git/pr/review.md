---
allowed-tools: Bash(gh pr view:*), Bash(gh pr list:*), Bash(gh pr review:*), Bash(gh pr diff:*), Bash(gh pr checks:*), Bash(gh pr edit:*), Bash(gh api:*), Bash(git branch:*), Bash(rg:*), Bash(delta:*)
description: Review and manage pull requests
---

# /pr-review

Reviews and manages pull requests using the GitHub CLI (`gh`) with comprehensive analysis and feedback tools.

## Usage

```
/pr-review [PR_NUMBER]
/pr-review approve [PR_NUMBER]
/pr-review comment [PR_NUMBER] "Your comment here"
/pr-review request-changes [PR_NUMBER]
/pr-review diff [PR_NUMBER]
/pr-review checks [PR_NUMBER]
/pr-review files [PR_NUMBER]
```

## Description

This command provides comprehensive PR review capabilities through the `gh` CLI, enabling efficient code review workflows directly from the command line.

### Core Workflow

#### 1. PR Discovery

If no PR number is provided, the command automatically detects relevant PRs:

```bash
# Check for PR associated with current branch
gh pr list --head $(git branch --show-current) --json number,title,state

# List all open PRs assigned for review
gh pr list --search "review-requested:@me" --json number,title,author,createdAt

# List PRs where you're mentioned
gh pr list --search "mentions:@me" --json number,title,state
```

#### 2. PR Analysis

The command runs these analyses in parallel:

```bash
# Get PR details
gh pr view $PR_NUMBER --json title,body,state,author,assignees,labels,milestone

# Check review status
gh pr view $PR_NUMBER --json reviews,reviewDecision,statusCheckRollup

# Get diff statistics
gh pr diff $PR_NUMBER --stat

# List changed files
gh pr view $PR_NUMBER --json files --jq '.files[].path'
```

#### 3. Code Review Actions

##### View PR Details

```bash
# Full PR information
gh pr view $PR_NUMBER

# PR comments and review threads
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/comments --jq '.[].body'

# Review comments on specific lines
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews
```

##### Submit Reviews

```bash
# Approve PR
gh pr review $PR_NUMBER --approve --body "LGTM! Great work on the implementation."

# Request changes
gh pr review $PR_NUMBER --request-changes --body "Please address the following concerns..."

# Add review comment
gh pr review $PR_NUMBER --comment --body "Thanks for the PR! I have a few suggestions..."
```

##### Interactive Diff Review

```bash
# View full diff with syntax highlighting
gh pr diff $PR_NUMBER | delta

# View specific file diff
gh pr diff $PR_NUMBER -- path/to/file.js

# View diff in browser
gh pr view $PR_NUMBER --web
```

### Advanced Features

#### Smart Review Suggestions

The command analyzes the PR and suggests review focus areas:

```bash
# Check for common issues
gh pr diff $PR_NUMBER | rg -i "TODO|FIXME|XXX|HACK"

# Security-sensitive patterns
gh pr diff $PR_NUMBER | rg -i "password|secret|token|api_key"

# Large file changes
gh pr view $PR_NUMBER --json files --jq '.files[] | select(.additions > 500 or .deletions > 500)'
```

#### CI/CD Status Monitoring

```bash
# Check all status checks
gh pr checks $PR_NUMBER

# Watch CI status until completion
gh pr checks $PR_NUMBER --watch

# Get detailed check run information
gh api repos/{owner}/{repo}/commits/$(gh pr view $PR_NUMBER --json headRefOid -q .headRefOid)/check-runs
```

#### Review Collaboration

```bash
# See who else is reviewing
gh pr view $PR_NUMBER --json reviewRequests,reviews

# Check review history
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews --jq '.[] | {user: .user.login, state: .state, submitted_at: .submitted_at}'

# Add additional reviewers
gh pr edit $PR_NUMBER --add-reviewer alice,bob
```

## Examples

### Basic Review Flow

```bash
# Review PR #123
/pr-review 123

# After reviewing, approve it
/pr-review approve 123
```

### Detailed Code Review

```bash
# View diff with specific focus
/pr-review diff 123

# Add inline comment (opens editor)
gh pr review 123 --comment

# Request specific changes
/pr-review request-changes 123
```

### Review Current Branch PR

```bash
# Automatically finds PR for current branch
/pr-review

# Check CI status for current branch PR
/pr-review checks
```

### Batch Review Operations

```bash
# List all PRs needing review
gh pr list --search "review-requested:@me" --json number,title

# Review multiple PRs
for pr in 123 456 789; do
  /pr-review $pr
done
```

## Review Best Practices

### Automated Checks

The command performs these checks automatically:

1. **Code Quality**
   - Linting violations
   - Test coverage changes
   - Documentation updates

2. **Security Scanning**
   - Hardcoded credentials
   - Vulnerable dependencies
   - Insecure patterns

3. **Performance Impact**
   - Bundle size changes
   - Database query patterns
   - API response time estimates

### Review Comment Templates

```bash
# Positive feedback
"Great implementation! The error handling is particularly well thought out."

# Constructive suggestions
"Consider extracting this logic into a separate function for better testability."

# Security concerns
"This could potentially expose sensitive data. Please add input validation."

# Performance suggestions
"This might cause N+1 queries. Consider using eager loading here."
```

## Integration with Other Commands

- Use after `/pr` to review your own PRs before requesting reviews
- Combine with `/test` to verify test results locally
- Use `/pr-check` to monitor CI/CD status during review
- Follow up with `/pr-update` to address review feedback

## Error Handling

- **PR not found**: Lists available PRs and suggests correct number
- **No review permissions**: Checks if you have access to the repository
- **Merge conflicts**: Alerts about conflicts and suggests resolution
- **Failed checks**: Shows which checks are failing and why

## Keyboard Shortcuts

When viewing diffs in the terminal:

- `j/k` - Navigate between files
- `n/p` - Next/previous comment
- `q` - Quit review mode
- `?` - Show help

## See Also

- `/pr` - Create pull requests
- `/pr-update` - Update existing pull requests
- `/pr-check` - Check PR and CI/CD status
