---
allowed-tools: Bash(gh pr edit:*), Bash(gh pr view:*), Bash(gh pr list:*), Bash(gh pr ready:*), Bash(gh pr close:*), Bash(gh pr reopen:*), Bash(gh label list:*), Bash(git branch:*), Bash(date:*)
description: Update existing pull requests
---

# /pr-update

Updates existing pull requests using the GitHub CLI (`gh`) with support for title, description, labels, and metadata changes.

## Usage

```
/pr-update [PR_NUMBER]
/pr-update title="New PR title" [PR_NUMBER]
/pr-update body="Updated description" [PR_NUMBER]
/pr-update add-label=bug,priority-high [PR_NUMBER]
/pr-update remove-label=wip [PR_NUMBER]
/pr-update add-reviewer=alice,bob [PR_NUMBER]
/pr-update milestone=v2.0 [PR_NUMBER]
/pr-update ready [PR_NUMBER]
/pr-update draft [PR_NUMBER]
```

## Description

This command provides comprehensive PR update capabilities through the `gh` CLI, allowing you to modify pull requests after creation without using the web interface.

### Core Workflow

#### 1. PR Identification

If no PR number provided, automatically detects current branch PR:

```bash
# Get PR for current branch
CURRENT_PR=$(gh pr list --head $(git branch --show-current) --json number -q '.[0].number')

# Verify PR exists and is open
gh pr view $PR_NUMBER --json state,number,title
```

#### 2. Update Operations

##### Title and Description

```bash
# Update PR title
gh pr edit $PR_NUMBER --title "feat: improved user authentication flow"

# Update PR body/description
gh pr edit $PR_NUMBER --body "$(cat <<'EOF'
## Summary
Updated implementation based on review feedback

## Changes
- Improved error handling
- Added comprehensive tests
- Updated documentation

## Review Notes
All previous comments have been addressed
EOF
)"

# Update both title and body
gh pr edit $PR_NUMBER --title "New title" --body "New description"
```

##### Label Management

```bash
# Add labels
gh pr edit $PR_NUMBER --add-label "bug" --add-label "priority-high"

# Remove labels
gh pr edit $PR_NUMBER --remove-label "wip" --remove-label "draft"

# Replace all labels
gh label list --json name -q '.[].name' | grep -E "^(bug|enhancement)$" | xargs -I {} gh pr edit $PR_NUMBER --add-label {}
```

##### Reviewer Management

```bash
# Add reviewers
gh pr edit $PR_NUMBER --add-reviewer alice,bob,@frontend-team

# Remove reviewers
gh pr edit $PR_NUMBER --remove-reviewer charlie

# Request review from CODEOWNERS
gh pr edit $PR_NUMBER --add-reviewer @CODEOWNERS
```

##### State Changes

```bash
# Convert draft to ready
gh pr ready $PR_NUMBER

# Convert to draft
gh pr edit $PR_NUMBER --draft

# Close PR
gh pr close $PR_NUMBER

# Reopen PR
gh pr reopen $PR_NUMBER
```

### Advanced Features

#### Smart Description Updates

The command can intelligently append to existing descriptions:

```bash
# Get current body
CURRENT_BODY=$(gh pr view $PR_NUMBER --json body -q .body)

# Append update section
UPDATED_BODY="$CURRENT_BODY

## Update $(date +%Y-%m-%d)
- Addressed review feedback
- Fixed failing tests
- Updated documentation"

gh pr edit $PR_NUMBER --body "$UPDATED_BODY"
```

#### Bulk Updates

```bash
# Update all PRs with a specific label
gh pr list --label "needs-update" --json number -q '.[].number' | \
  xargs -I {} gh pr edit {} --remove-label "needs-update" --add-label "updated"

# Add milestone to multiple PRs
for pr in $(gh pr list --author @me --json number -q '.[].number'); do
  gh pr edit $pr --milestone "v2.0"
done
```

#### Review Response Automation

```bash
# After addressing review comments
/pr-update ready remove-label=changes-requested add-label=ready-for-review

# Mark PR as WIP while making changes
/pr-update draft add-label=wip title="WIP: $(gh pr view --json title -q .title)"
```

## Examples

### Basic Updates

```bash
# Update current branch PR title
/pr-update title="feat: add user profile management"

# Update PR #123 description
/pr-update body="Updated with review feedback" 123
```

### Label Management

```bash
# Add bug label to current PR
/pr-update add-label=bug

# Remove WIP and add ready labels
/pr-update remove-label=wip add-label=ready-for-review
```

### Reviewer Updates

```bash
# Add reviewers to PR #456
/pr-update add-reviewer=alice,bob 456

# Request review from team
/pr-update add-reviewer=@backend-team
```

### State Transitions

```bash
# Mark PR as ready for review
/pr-update ready

# Convert back to draft
/pr-update draft
```

### Comprehensive Update

```bash
# Update everything at once
/pr-update \
  title="feat: complete authentication system" \
  add-label=enhancement,security \
  remove-label=wip \
  add-reviewer=@security-team \
  milestone=Q4-2024 \
  ready
```

## Update Patterns

### Post-Review Updates

After addressing review feedback:

```bash
# 1. Update PR description with changes made
/pr-update body="$(cat <<'EOF'
[Previous description...]

## Updates Based on Review

- ✅ Fixed error handling as suggested by @alice
- ✅ Added comprehensive test coverage
- ✅ Updated documentation
- ✅ Refactored authentication logic

All review comments have been addressed.
EOF
)"

# 2. Update labels and request re-review
/pr-update remove-label=changes-requested add-label=ready-for-review
```

### Work-in-Progress Updates

```bash
# Mark as WIP
/pr-update draft add-label=wip title="WIP: $(gh pr view --json title -q .title)"

# When ready
/pr-update ready remove-label=wip title="$(gh pr view --json title -q .title | sed 's/WIP: //')"
```

### Milestone and Project Updates

```bash
# Assign to milestone
/pr-update milestone="v2.0-release"

# Add to project (requires project ID)
gh pr edit $PR_NUMBER --project "MyProject"
```

## Integration with CI/CD

The command can trigger CI/CD actions through description updates:

```bash
# Trigger specific tests
/pr-update body="$(gh pr view --json body -q .body)

/test integration
/test performance"

# Trigger deployment
/pr-update body="$(gh pr view --json body -q .body)

/deploy staging"
```

## Error Handling

- **PR not found**: Lists PRs and helps identify correct number
- **Permission denied**: Checks if you have write access
- **Invalid labels**: Shows available labels for the repository
- **Reviewer not found**: Validates reviewer usernames/teams
- **Conflicting states**: Prevents invalid state transitions

## Best Practices

1. **Always explain updates**: When updating description, add context about what changed
2. **Use semantic labels**: Follow team conventions for label naming
3. **Batch related updates**: Combine multiple updates in single command
4. **Preserve history**: Append to descriptions rather than replacing
5. **Communicate changes**: Mention significant updates in PR comments

## See Also

- `/pr` - Create pull requests
- `/pr-review` - Review pull requests
- `/pr-check` - Check PR and CI/CD status
