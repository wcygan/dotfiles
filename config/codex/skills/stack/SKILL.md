---
name: stack
description: Use for guarded stacked pull request workflows with kitlangton/stack in GitHub squash-merge repos, especially PR-base sync, root merges, undo, and stacked PR repair.
---

# Stack

Use `kitlangton/stack` only for dependent GitHub pull requests in repositories
that squash-merge and may delete merged branches. It is a stack repair and
metadata tool, not a replacement for normal `git`.

Keep normal editing, staging, commits, branch creation, and one-off inspection on
plain `git` and `gh`. Use `stack` only to inspect stack intent, infer PR-base
links, sync/repair descendants, merge stack roots, refresh PR stack blocks, and
undo the last stack mutation.

## Preflight

Before any mutating `stack` command:

1. Confirm this is a GitHub repo and `gh auth status` works.
2. Confirm `stack --version`, or use a one-shot trial command:
   `npm exec --yes --package @kitlangton/stack@0.1.5 -- stack --version`.
3. Run `git status --short --branch`; stop if the worktree is dirty.
4. Confirm the trunk branch is `dev`, `main`, or `master`, and the writable
   remote is `origin`.
5. Run `stack doctor` when the repo state is unfamiliar.

Do not commit `.git/stack/state.json`, `.git/stack/undo.json`, backup branches,
local trust tables, secrets, generated runtime state, or one-off cache files.

## Workflow

Create the stack with ordinary GitHub PR bases:

```bash
git switch -c stack-a
# edit, test, commit
git push -u origin stack-a
gh pr create --base main --head stack-a

git switch -c stack-b
# edit, test, commit
git push -u origin stack-b
gh pr create --base stack-a --head stack-b
```

Then preview and apply stack sync:

```bash
stack sync --dry-run
stack sync
stack status
```

Only run `stack sync` after the dry-run tree, inferred links, planned rebases,
PR retargets, and PR-body updates look correct. Use `stack sync <branch>` when
you want to scope the operation to one stack from an off-stack branch.

For root merges, preview first:

```bash
stack merge
stack merge --apply
```

Use `stack merge --auto` only when waiting for GitHub merge requirements is the
desired behavior. Use `stack merge --auto --through <branch-or-pr>` only for a
bounded range, not as a default whole-stack merge.

## Recovery

After any mutating sync or merge, keep the printed undo path visible:

```bash
stack history
stack undo
stack undo --apply
```

Use `stack undo` as the preview and `stack undo --apply` as the recovery path.
Undo restores branch tips from backup branches, restores PR bases, closes PRs
created by the mutation, and restores stack metadata.

## Risk Rules

- `stack sync` is mutating even though it has no `--apply` flag.
- `stack merge` is dry-run by default; `--apply`, `--auto`, and `--admin` are
  mutating.
- Mutating workflows may retarget PR bases, edit PR bodies, create PRs, close
  PRs during undo, replay commits with cherry-pick, rewrite descendant branch
  tips, and push with `--force-with-lease`.
- Never run mutating commands on trunk branches, protected shared branches,
  dirty worktrees, ambiguous multi-remote/fork setups, or repos that are not
  using GitHub PRs.
- Do not use this for independent PRs, merge-commit/rebase-merge workflows,
  stacks whose PR bases intentionally do not encode the stack, or repos where
  force-with-lease pushes are not acceptable.
- Do not edit `.git/stack/state.json` or `.git/stack/undo.json` by hand. Use
  `stack sync --dry-run`, `stack track`, `stack history`, and `stack undo`.
- If the preview is unclear, stop and inspect with `git log --graph --decorate`,
  `gh pr view`, `stack status`, and `stack doctor` before applying.

## Agent Behavior

When acting as an agent, print or summarize the dry-run plan before applying.
Do not run a mutating `stack` command unless the user has explicitly asked for
that mutation in the current task, or has already approved the matching preview.
