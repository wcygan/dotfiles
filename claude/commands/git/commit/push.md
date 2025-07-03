---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(git log:*), Bash(git remote:*), Bash(git rev-parse:*)
description: Create a git commit and push to remote
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Remote tracking branch: !`git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "No upstream branch"`
- Recent commits: !`git log --oneline -10`

## Your task

Generate a conventional commit message following https://www.conventionalcommits.org/en/v1.0.0/ specification, create the commit, and push to the remote repository.

Steps:

1. Analyze the current git changes using `git status` and `git diff --staged`
2. Determine the appropriate commit type (feat, fix, docs, style, refactor, test, chore, etc.)
3. Identify the scope if applicable (component, module, or area affected)
4. Write a concise description in imperative mood (50 chars or less)
5. Add a detailed body if the change is complex (wrap at 72 chars)
6. Include breaking change footer if applicable
7. Format as: `type(scope): description`
8. Create the commit with the generated message
9. Push the commit to the remote repository
   - If no upstream branch exists, set it with `git push -u origin <branch>`
   - Otherwise, use `git push`
   - Handle any push errors (e.g., need to pull first, protected branch)

Example formats:

- `feat(auth): add OAuth2 login support`
- `fix(api): resolve null pointer in user endpoint`
- `docs: update installation instructions`
- `chore(deps): bump lodash to 4.17.21`

Push handling:

- Check if the branch has an upstream before pushing
- If pushing fails due to diverged branches, inform the user they need to pull first
- If pushing to a protected branch, suggest creating a PR instead
- Show the push result and any relevant URLs (PR creation links, etc.)

Generate the most appropriate commit message based on the changes, commit, and push automatically.
