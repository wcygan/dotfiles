---
title: Git Worktrees
canonical_url: https://code.claude.com/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees
fetch_before_acting: true
---

# Git Worktrees

> Before setting up worktrees, WebFetch https://code.claude.com/docs/en/common-workflows for the latest.

## Summary

Git worktrees give each Claude session its own isolated copy of the codebase — separate working directory, separate branch, shared repository history. Essential for running many Claude sessions in parallel without conflicts.

### Quick Start

```bash
# Start Claude in a named worktree
claude -w feature-auth

# Auto-generated name (e.g., "bright-running-fox")
claude -w

# Open in tmux pane alongside
claude -w feature-auth --tmux
```

Worktrees are created at `<repo>/.claude/worktrees/<name>` and branch from `origin/HEAD`.

### Desktop App

In the Desktop app, click **+ New session** — each session automatically gets its own worktree. Configure worktree location and branch prefix in Settings → Claude Code.

### Key Behaviors

- **Branch naming**: `worktree-<name>` (e.g., `worktree-feature-auth`)
- **Base branch**: `origin/HEAD` (re-sync with `git remote set-head origin -a`)
- **Cleanup on exit**:
  - No changes → worktree and branch removed automatically
  - Changes exist → prompted to keep or remove
- **Gitignored files**: create `.worktreeinclude` in project root to copy files like `.env`:

```text
.env
.env.local
config/secrets.json
```

### Subagent Worktrees

Subagents can use worktree isolation too:

```yaml
# In agent frontmatter
isolation: worktree
```

Or ask Claude: "use worktrees for your agents". Each subagent gets its own worktree, auto-cleaned when it finishes without changes.

### WorktreeCreate Hook

For non-git VCS or custom worktree logic, configure a `WorktreeCreate` hook that replaces the default git behavior:

```json
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/create-worktree.sh"
          }
        ]
      }
    ]
  }
}
```

When configured, `.worktreeinclude` is not processed — handle file copying in your script.

### Running Dozens of Parallel Sessions

The power pattern for heavy parallel work:

1. Use `claude -w` for each independent task
2. Each session gets its own branch and working directory
3. Changes in one session never affect another
4. Merge branches independently when ready

Combine with `claude remote-control --spawn worktree` to run a server that creates a new worktree for each incoming remote session.

### Manual Worktree Management

```bash
# Create with specific branch
git worktree add ../project-feature-a -b feature-a

# List all worktrees
git worktree list

# Clean up
git worktree remove ../project-feature-a
```

### Tips

- Add `.claude/worktrees/` to `.gitignore`
- Run dependency installation in each new worktree (`npm install`, etc.)
- Each worktree needs its own dev environment setup
- Re-sync base branch after remote default changes: `git remote set-head origin -a`
