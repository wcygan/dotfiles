---
title: Common jj workflows
description: End-to-end recipes for the workflows that come up daily — starting work, splitting, squashing, rebasing stacks, resolving conflicts, undoing, and pushing to a git remote
tags: [jj, workflows, recipes, rebase, conflict, undo, stacked-diffs]
---

# Common jj workflows

Recipes for the situations that come up every day. Each one is a concrete sequence, not prose.

## Table of contents

- [Starting new work](#starting-new-work)
- [Committing and describing](#committing-and-describing)
- [Splitting a change](#splitting-a-change)
- [Squashing into an ancestor (fixup)](#squashing-into-an-ancestor-fixup)
- [Stacked diffs](#stacked-diffs)
- [Rebasing onto updated main](#rebasing-onto-updated-main)
- [Resolving conflicts](#resolving-conflicts)
- [Undoing mistakes](#undoing-mistakes)
- [Pushing to a git remote](#pushing-to-a-git-remote)
- [Merging a PR locally](#merging-a-pr-locally)
- [Recovering from a bad rebase](#recovering-from-a-bad-rebase)
- [Working with multiple workspaces](#working-with-multiple-workspaces)
- [Bisecting](#bisecting)

## Starting new work

No branch required. Just start.

```bash
jj git fetch
jj new main                          # new empty change on top of main
# ... edit files ...
jj describe -m "add rate limiter"    # name it when the intent is clear
```

If you want a bookmark right away (e.g. to share a branch name with a PR):

```bash
jj bookmark create rate-limiter -r @
```

## Committing and describing

There are two related commands:

- `jj describe -m "msg"` — set the description of the current change. Content stays in `@`.
- `jj commit -m "msg"` — describe `@` and start a fresh empty change on top of it. Use when you want to "close out" a commit and move on.

```bash
jj describe -m "add rate limiter middleware"
# keep editing — still the same change

jj commit -m "add rate limiter middleware"
# now @ is a new empty change; previous work is in @-
```

## Splitting a change

Break a big change into two. jj opens a merge tool; what you select goes into the **first** (earlier) change; what remains goes into the **second**.

```bash
jj split                             # interactive split of @
jj split -r <rev>                    # split any change, not just @
jj split path/to/file.rs             # move only that path into the new change
```

After splitting, both changes are on your stack and descendants (if any) follow automatically.

## Squashing into an ancestor (fixup)

You're working on `@` and realize a hunk belongs two commits back. No fixup commits, no autosquash.

```bash
jj squash --into <rev>               # move all of @ into <rev>
jj squash -i --into <rev>            # pick specific hunks
jj squash path/to/file.rs --into <rev>
```

All descendants automatically rebase. If the change you targeted has been pushed, jj refuses by default — override only if you know it's safe.

## Stacked diffs

jj is great at stacked changes because rewriting any ancestor auto-rebases its descendants.

```bash
jj new main   -m "1 refactor helpers"
# ... edit ...
jj new        -m "2 add new feature"
# ... edit ...
jj new        -m "3 wire it up"
# ... edit ...

jj log -r 'trunk()..@'               # see the stack
```

Editing change 1 retroactively:

```bash
jj edit <change-id-of-1>             # point working copy at it
# ... edit ...
jj next                              # walk back toward @
```

Reordering:

```bash
jj rebase -r <id-of-2> --after <id-of-3>
```

## Rebasing onto updated main

```bash
jj git fetch
jj rebase -b @ -d main               # rebase the whole current branch onto main
```

Or move just your current stack off its old base:

```bash
jj rebase -s <root-of-stack> -d main
```

Conflicts do not stop the rebase — they're recorded in the resulting commits. Check `jj log` for conflict markers.

## Resolving conflicts

After a rebase or merge, `jj log` marks conflicted changes. There's no "rebase in progress" state to abort.

**Option A — edit files directly:**

```bash
jj edit <conflicted-rev>             # point working copy at it
# open the files; conflict markers look like git's <<<<<<<
# edit until clean
jj st                                # marker disappears when resolved
```

**Option B — use a merge tool:**

```bash
jj resolve                           # opens configured merge tool on @
jj resolve path/to/file.rs           # specific file
```

**Option C — give up on the rebase:**

```bash
jj undo                              # revert the rebase entirely
```

When a conflicted ancestor is resolved, descendants recompute. If they were also conflicted *only because* of that ancestor, they often clear automatically.

## Undoing mistakes

```bash
jj undo                              # revert the last operation
jj op log                            # see everything that's happened
jj op restore <op-id>                # jump repo state back to an earlier point
jj op diff --from <a> --to <b>       # what changed between two ops
```

`jj undo` is the first thing to try after any "oh no" moment — rebase gone wrong, wrong change abandoned, bad squash. It's atomic over all refs and the working copy.

Recovering a change you rewrote (not operation-level, but change-level):

```bash
jj evolog -r <change-id>             # see prior versions of this change
jj restore --from <older-commit-id>  # pull old content into current change
```

## Pushing to a git remote

```bash
jj git fetch                         # sync remote state first
jj bookmark set my-feature -r @      # point bookmark at what you want to push
jj git push --bookmark my-feature
```

Shortcut: create a bookmark named after the change and push in one step:

```bash
jj git push -c @                     # auto-names a bookmark and pushes
```

To push *all* tracked bookmarks that moved:

```bash
jj git push
```

## Merging a PR locally

To test someone's remote branch without polluting your own work:

```bash
jj git fetch
jj new their-feature@origin          # new empty change on top of their branch
# ... test ...
```

To merge two local branches into a third:

```bash
jj new feature-a feature-b -m "merge feature-a and feature-b"
```

Merge conflicts land in the new commit; resolve as above.

## Recovering from a bad rebase

```bash
jj op log -n 10                      # find the operation before the rebase
jj op restore <op-id-before>         # entire repo jumps back
```

Or the lighter-weight:

```bash
jj undo
```

Both are reversible. Nothing is lost from the operation log until `jj op abandon` is run.

## Working with multiple workspaces

jj has a native alternative to `git worktree`:

```bash
jj workspace add ../feature-b        # new workspace sharing the same repo
cd ../feature-b
jj new main
# ... work in parallel with the original workspace ...

jj workspace list
jj workspace remove <name>
```

Each workspace has its own `@` but shares the underlying commit graph.

## Bisecting

```bash
jj bisect run -r 'trunk()..@' -- <test-command>
```

Example — find the commit that broke a test:

```bash
jj bisect run -r 'v1.0..@' -- cargo test --test my_test
```

jj jumps between revisions, runs the command, and reports the first bad change. Unlike `git bisect`, there's no mode to enter or exit — it's a single operation, reversible via `jj undo`.
