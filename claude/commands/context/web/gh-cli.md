# context-load-gh-cli

Loads comprehensive GitHub CLI (`gh`) instructions for agent use in pull requests, issues, comments, and reviews.

## Usage

```bash
/context-load-gh-cli
```

## Description

This command loads a comprehensive guide for leveraging the GitHub CLI to:

- Create and manage pull requests
- Create and manage issues
- Add comments to PRs and issues
- Create and view reviews
- Use the API for advanced operations
- Work around current CLI limitations

Perfect for when you need an agent to help with GitHub operations using the command line.

## Implementation

# GitHub CLI (`gh`) Agent Instructions Guide

## Overview

This guide provides comprehensive instructions for leveraging the GitHub CLI (`gh`) to manage pull requests, issues, comments, and reviews.

## Pull Request Management

### Creating Pull Requests

```bash
# Interactive creation (recommended for agents)
gh pr create

# With explicit parameters
gh pr create --title "PR title" --body "PR description"

# Using HEREDOC for multi-line body (best for agents)
gh pr create --title "Fix bug" --body "$(cat <<'EOF'
## Summary
- Fixed the authentication bug
- Updated error handling

## Test plan
- [x] Unit tests pass
- [x] Manual testing completed
EOF
)"

# Additional options
gh pr create --base main --head feature-branch --draft
gh pr create --reviewer username1,username2
gh pr create --assignee @me
gh pr create --label "bug,priority"
gh pr create --project "Roadmap"
```

### Managing Pull Requests

```bash
# List PRs
gh pr list
gh pr list --state closed --limit 10
gh pr list --assignee @me

# View PR details
gh pr view 123
gh pr view --json state,title,body,reviews
gh pr view --web  # Open in browser

# Check PR status
gh pr status

# Check out PR
gh pr checkout 123
gh pr checkout branch-name

# Close/reopen PR
gh pr close 123
gh pr close 123 -d  # Delete branch
gh pr reopen 123

# View PR diff
gh pr diff 123

# Merge PR
gh pr merge --auto --squash
```

## Issue Management

### Creating Issues

```bash
# Interactive creation
gh issue create

# With parameters
gh issue create --title "Bug report" --body "Description"

# With labels and assignees
gh issue create --title "Feature request" --label "enhancement" --assignee username

# Open in browser
gh issue create --web
```

### Managing Issues

```bash
# List issues
gh issue list
gh issue list --state closed --assignee @me
gh issue list -A "username"  # Assigned to specific person

# View issue
gh issue view 123
gh issue view 123 --web

# Check issue status
gh issue status

# Close/reopen issue
gh issue close 123
gh issue reopen 123
```

## Comments

### PR Comments

```bash
# Add comment to current branch's PR
gh pr comment --body "LGTM!"

# Short form
gh pr comment -b "rfm"

# Comment on specific PR
gh pr comment 123 --body "Please update the tests"

# Interactive mode (opens editor)
gh pr comment 123
```

### Issue Comments

```bash
# Comment on issue (opens editor)
gh issue comment 123

# With body flag (not currently supported, use editor mode)
# Note: Issue comments currently require interactive editor
```

## Reviews

### Creating Reviews

```bash
# Approve PR
gh pr review --approve

# Request changes
gh pr review --request-changes --body "Please address the following issues"

# Comment review
gh pr review --comment --body "Some thoughts on this approach"

# Review specific PR
gh pr review 123 --approve
gh pr review 123 -r -b "needs more changes"
```

### Viewing Reviews and Comments

**Current Limitations**: The CLI has limited support for viewing review comments. Use these workarounds:

```bash
# Get reviews (limited info - body, state, author only)
gh pr view 123 --json reviews

# Use API for detailed review data
gh api repos/{owner}/{repo}/pulls/{pull_number}/reviews

# Get review comments
gh api repos/{owner}/{repo}/pulls/{pull_number}/comments

# Get pending review requests for current user
gh api search/issues --raw-field q="is:pr is:open review-requested:@me"
```

## Advanced API Usage

### Fetching Detailed Review Information

```bash
# Get all reviews with comments
gh api repos/{owner}/{repo}/pulls/{pull_number}/reviews

# Get specific review
gh api repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}

# List review comments
gh api repos/{owner}/{repo}/pulls/{pull_number}/comments

# Get comments with HTML formatting
gh api repos/{owner}/{repo}/pulls/{pull_number}/comments \
  --header "Accept: application/vnd.github-commitcomment.html+json"
```

### Working with Reviewers

```bash
# Add reviewers
gh api repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers \
  --method POST \
  --field reviewers[]="user1" \
  --field reviewers[]="user2" \
  --field team_reviewers[]="team-name"

# Remove reviewers
gh api repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers \
  --method DELETE \
  --field reviewers[]="user1"
```

### Creating Pending Reviews

```bash
# Create a pending review (leave event blank)
gh api repos/{owner}/{repo}/pulls/{pull_number}/reviews \
  --method POST \
  --field body="This is a pending review" \
  --field comments[0][path]="file.txt" \
  --field comments[0][position]=1 \
  --field comments[0][body]="Comment on line 1"

# Submit a pending review
gh api repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events \
  --method POST \
  --field event="APPROVE"
```

### Useful API Queries

```bash
# Get all PRs with pending reviews
gh api repos/{owner}/{repo}/pulls \
  --jq '.[] | select(.requested_reviewers | length > 0) | {number, title, requested_reviewers}'

# Search for PRs requesting your review
gh api search/issues \
  --raw-field q="is:pr is:open review-requested:@me"

# Get PR checks status
gh api repos/{owner}/{repo}/commits/{ref}/check-runs
```

## Linking Issues to PRs

Include these keywords in PR body to auto-close issues:

- `Fixes #123`
- `Closes #123`
- `Resolves #123`

Example:

```bash
gh pr create --body "This fixes #123 and closes #456"
```

## Agent Best Practices

1. **Use HEREDOC for multi-line content** to ensure proper formatting:
   ```bash
   gh pr create --title "Feature" --body "$(cat <<'EOF'
   Multi-line
   content here
   EOF
   )"
   ```

2. **Check current state before actions** using view commands:
   ```bash
   gh pr view 123 --json state
   ```

3. **Prefer explicit parameters** over interactive mode for clarity

4. **Use JSON output** for parsing:
   ```bash
   gh pr list --json number,title,state
   ```

5. **Handle errors gracefully** - check if PR/issue exists before commenting

6. **Use the API directly** for complex review operations not supported by CLI commands

7. **Always specify the repo** when not in a git repository:
   ```bash
   gh pr list --repo owner/repo
   ```

## Example Workflow for Agent

```bash
# 1. Check current PR status
gh pr status

# 2. Create PR with comprehensive information
gh pr create --title "Feature: Add authentication" --body "$(cat <<'EOF'
## Summary
- Implemented OAuth2 authentication
- Added user session management

## Test plan
- [x] Unit tests for auth module
- [x] Integration tests for login flow
- [x] Manual testing on staging
EOF
)"

# 3. Add reviewers using API
gh api repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers \
  --method POST \
  --field reviewers[]="senior-dev"

# 4. Monitor reviews
gh pr view --json reviews,state

# 5. Respond to feedback
gh pr comment --body "Thanks for the review! I've addressed all the comments."

# 6. Check CI status
gh pr checks

# 7. After approval, merge
gh pr merge --auto --squash
```

## Common Error Handling

```bash
# Check if PR exists before commenting
if gh pr view 123 &>/dev/null; then
    gh pr comment 123 --body "Comment"
else
    echo "PR #123 does not exist"
fi

# Check if you have permissions
gh api repos/{owner}/{repo} --silent || echo "No access to repo"
```

## Limitations & Workarounds

1. **Cannot view inline review comments directly** - Use `gh pr view --web` or API
2. **Limited support for viewing pending reviews** - Use API queries
3. **Review thread discussions require API access** - Not available in CLI
4. **Issue comments don't support --body flag** - Must use interactive editor

For operations not supported by the CLI, use `gh api` to access the full GitHub REST API.
