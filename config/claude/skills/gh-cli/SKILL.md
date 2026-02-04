---
name: gh-cli
description: Work with GitHub from the command line using the GitHub CLI (gh). Use when managing repositories, pull requests, issues, releases, GitHub Actions, or any GitHub operations. Keywords: github, gh, pull request, PR, issue, release, workflow, actions, repository, fork, clone, merge
---

# GitHub CLI (gh)

Use the `gh` CLI to interact with GitHub directly from the terminal. Prefer `gh` over raw git commands or API calls for GitHub-specific operations.

## Quick Reference

### Authentication
```bash
gh auth login                    # Interactive login
gh auth status                   # Check authentication
gh auth token                    # Print current token
```

### Repository Operations
```bash
gh repo clone owner/repo         # Clone repository
gh repo view                     # View current repo details
gh repo create name --public     # Create new repository
gh repo fork owner/repo --clone  # Fork and clone
gh repo sync                     # Sync fork with upstream
```

### Pull Requests
```bash
gh pr create                     # Create PR interactively
gh pr list                       # List open PRs
gh pr view 123                   # View PR details
gh pr checkout 123               # Checkout PR branch
gh pr merge 123 --squash         # Merge with squash
gh pr diff 123                   # View PR diff
gh pr checks 123 --watch         # Watch CI checks
```

### Issues
```bash
gh issue create                  # Create issue interactively
gh issue list                    # List open issues
gh issue view 123                # View issue details
gh issue close 123               # Close issue
gh issue comment 123 --body "x"  # Add comment
```

### GitHub Actions
```bash
gh run list                      # List workflow runs
gh run view 123456               # View run details
gh run watch 123456              # Watch run in real-time
gh run rerun 123456              # Rerun failed run
gh workflow run ci.yml           # Trigger workflow manually
```

### Releases
```bash
gh release list                  # List releases
gh release create v1.0.0         # Create release
gh release download v1.0.0       # Download release assets
```

## Instructions

When the user needs to interact with GitHub:

1. **Verify authentication** if operations fail:
   ```bash
   gh auth status
   ```

2. **Use appropriate subcommands** based on the task:
   - Repository management → `gh repo`
   - Pull requests → `gh pr`
   - Issues → `gh issue`
   - CI/CD → `gh run`, `gh workflow`
   - Releases → `gh release`

3. **Prefer JSON output** for parsing:
   ```bash
   gh pr list --json number,title,author
   gh issue view 123 --json title,body,labels
   ```

4. **Use jq for filtering**:
   ```bash
   gh pr list --json number,title --jq '.[] | select(.title | contains("fix"))'
   ```

5. **Open in browser when useful**:
   ```bash
   gh pr view 123 --web
   gh issue view 123 --web
   gh browse
   ```

## Common Workflows

### Create PR from Current Branch
```bash
gh pr create --title "Feature: Add X" --body "Description" --draft
```

### Review and Merge PR
```bash
gh pr checkout 123
# Review code...
gh pr review 123 --approve
gh pr merge 123 --squash --delete-branch
```

### Check CI Status
```bash
gh pr checks 123 --watch
gh run list --workflow ci.yml --limit 5
```

### Link Issue to PR
```bash
gh pr create --title "Fix #123" --body "Closes #123"
```

For detailed reference, see [REFERENCE.md](REFERENCE.md).
