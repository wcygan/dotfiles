---
allowed-tools: Bash(gh pr create:*), Bash(gh pr list:*), Bash(gh auth status:*), Bash(git status:*), Bash(git push:*), Bash(git branch:*), Bash(git diff:*), Bash(git log:*), Bash(gh issue view:*)
description: Create pull requests with intelligent analysis
---

# /pr

Creates high-quality pull requests using the GitHub CLI (`gh`) with intelligent analysis and formatting.

## Usage

```
/pr
/pr draft
/pr template=<name>
/pr reviewers=<user1,user2>
/pr base=<branch>
/pr title="Custom PR title"
/pr labels=<label1,label2>
```

## Description

This command leverages the `gh` CLI to create comprehensive pull requests with proper formatting, context, and metadata. It analyzes your changes and enforces team conventions.

### Core Workflow

#### 1. Pre-flight Checks

```bash
# Check if gh is authenticated
gh auth status

# Verify we're in a git repository
git rev-parse --git-dir

# Check for uncommitted changes
git status --porcelain

# Ensure branch is pushed to remote
git push -u origin $(git branch --show-current)
```

#### 2. Change Analysis

The command runs these `gh` and `git` commands in parallel:

```bash
# Get current branch and base branch
git branch --show-current
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'

# Analyze changes
git diff --name-status origin/main...HEAD
git log --oneline origin/main...HEAD
git diff --stat origin/main...HEAD

# Check for existing PR
gh pr list --head $(git branch --show-current) --json number,state
```

#### 3. Intelligent Title Generation

Based on commit analysis and conventional commit patterns:

```bash
# Analyze commit messages for patterns
git log --pretty=format:"%s" origin/main...HEAD | head -1

# If no clear pattern, analyze file changes
git diff --name-only origin/main...HEAD | head -10
```

**Generated Titles:**

- `feat(api): add user authentication endpoints`
- `fix(auth): resolve token expiration issue`
- `docs: update API documentation`
- `chore(deps): update dependencies`

#### 4. PR Creation with gh

```bash
# Create PR with generated content
gh pr create \
  --title "feat(api): add user authentication" \
  --body "$(cat <<'EOF'
## Summary

Brief description of changes

## Changes
- Added authentication endpoints
- Updated user model
- Added test coverage

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues
Fixes #123
EOF
)" \
  --draft \
  --assignee @me \
  --label "enhancement" \
  --reviewer alice,bob
```

### Advanced Features

#### Smart Reviewer Detection

```bash
# Find CODEOWNERS
if [ -f .github/CODEOWNERS ]; then
  # Parse CODEOWNERS for relevant reviewers
  grep -E "^$(git diff --name-only origin/main...HEAD | head -1)" .github/CODEOWNERS
fi

# Find frequent contributors to changed files
git log --pretty=format:"%an" origin/main...HEAD -- $(git diff --name-only origin/main...HEAD) | \
  sort | uniq -c | sort -rn | head -3
```

#### Issue Linking

```bash
# Extract issue number from branch name
BRANCH=$(git branch --show-current)
ISSUE=$(echo $BRANCH | grep -oE '[0-9]+' | head -1)

# Check if issue exists
if [ -n "$ISSUE" ]; then
  gh issue view $ISSUE --json state,title
fi
```

#### Template Support

```bash
# Check for PR templates
TEMPLATE_DIR=".github/pull_request_template"
if [ -d "$TEMPLATE_DIR" ]; then
  ls -1 "$TEMPLATE_DIR"/*.md
fi

# Use specific template
gh pr create --template .github/pull_request_template/feature.md
```

## Examples

### Basic PR Creation

```bash
/pr
# Runs: gh pr create --title "..." --body "..." --assignee @me
```

### Draft PR with Reviewers

```bash
/pr draft reviewers=alice,bob
# Runs: gh pr create --draft --reviewer alice,bob ...
```

### PR with Custom Base Branch

```bash
/pr base=develop
# Runs: gh pr create --base develop ...
```

### PR with Labels

```bash
/pr labels=bug,priority-high
# Runs: gh pr create --label bug --label priority-high ...
```

## Integration with CI/CD

The command automatically adds CI trigger comments when appropriate:

```markdown
<!-- Added to PR body when test changes detected -->

/test all
/test unit
/test integration

<!-- Added when deployment files changed -->

/deploy preview
```

## Error Handling

- **Not a git repository**: Suggests `git init` or navigating to correct directory
- **No remote**: Offers to add remote with `git remote add origin <url>`
- **Uncommitted changes**: Prompts to commit or stash changes
- **gh not authenticated**: Runs `gh auth login`
- **Branch not pushed**: Automatically pushes with `git push -u origin <branch>`

## See Also

- `/pr-review` - Review and manage pull requests
- `/pr-update` - Update existing pull request
- `/pr-check` - Check PR status and CI/CD state
