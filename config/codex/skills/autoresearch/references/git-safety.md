# Git Safety

Use this reference before making any autoresearch iteration change.

## Preflight

Run and inspect:

```sh
git rev-parse --show-toplevel
git status --short
git branch --show-current
git log --oneline -5
```

Proceed with an edit loop only when the repo is under git and rollback boundaries are clear.

## Working Tree Rules

- Clean tree: a loop may use local `experiment:` commits or patch snapshots.
- Dirty tree with unrelated user changes: preserve the user's changes and ask before any loop that needs rollback.
- Dirty tree containing only current task edits: summarize them, then continue if rollback can target only autoresearch-owned files.
- Detached HEAD: ask before committing or create a safe branch only with user approval.

## Rollback Modes

Prefer these modes in order:

1. **Experiment branch or worktree**: best for long loops or high-risk changes.
2. **Local experiment commits**: acceptable when the user asked for a loop, the tree is clean, and commits are local.
3. **Patch snapshots**: acceptable for short loops where commits are inappropriate.

Experiment commits use:

```text
experiment: <short hypothesis>
```

Revert only commits or patches created by the current autoresearch run.

## Commit Handling

When using experiment commits:

1. Commit one coherent iteration.
2. Run verify and guard.
3. Keep the commit if the metric improves and guard passes.
4. Revert the commit if the metric regresses, parsing fails, verify fails, or guard fails.
5. Record the commit SHA in the run artifact before any cleanup.

Do not squash, rebase, push, tag, publish, or deploy as part of the loop. Treat those as separate shipping actions that require explicit user approval.

## User Work Boundary

Before rollback, compare the candidate changes to the run log. If a file was modified by the user during the run or is outside scope, stop and report the conflict instead of reverting.
