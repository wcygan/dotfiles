---
name: jj
description: Use jj (Jujutsu) as the default VCS for git-backed repositories. Covers jj commands, git interop in colocated repos, common workflows (split, squash, rebase, resolve), and the git-to-jj translation for users migrating from git. Use when working with version control, making commits, rebasing, resolving conflicts, pushing branches, or when a repo has a .git directory. Keywords: jj, jujutsu, version control, vcs, git, bookmark, rebase, squash, split, conflict, operation log, colocated
---

# jj (Jujutsu)

Use `jj` as the default VCS in git-backed repositories. Jujutsu is git-compatible — it reads and writes a standard `.git` directory — so teammates using git are unaffected. Fall back to `git` only when jj lacks the feature (LFS, submodules, hooks, signed push to protected branches) or when the repo is not jj-initialized.

## Mental model (the parts that matter)

- **Working copy is a commit.** There is no index. Editing a file automatically updates the current change. Shape commits with `jj split` / `jj squash`, not `git add`.
- **Change ID ≠ commit ID.** Change IDs (`k`, `q`, `z`…) are stable across rewrites. Commit IDs change when content changes. Prefer change IDs in commands.
- **Bookmarks, not branches.** Bookmarks are optional, manually-moved labels. You don't need one to start work. They only matter when pushing to a git remote.
- **Conflicts are committable.** `jj rebase` never stops. Conflicts are recorded in commits and resolved later with `jj resolve` or a normal edit.
- **Descendants auto-rebase.** Rewriting any commit (amend, describe, squash, reorder) automatically rebases everything on top.
- **Operation log is the real undo.** `jj undo` reverts the last operation atomically. `jj op log` shows every state change; `jj op restore <id>` jumps back.
- **`@` is the working-copy change.** `@-` is its parent. `@--` is two back. Most commands take `-r <rev>` to target a different change.

## When to reach for jj vs git

| Situation | Use |
|---|---|
| Any local history rewrite (amend, rebase, reorder, split) | `jj` |
| Inspecting state, committing, resolving conflicts | `jj` |
| Pushing/pulling with a remote | `jj git push` / `jj git fetch` |
| Running pre-commit hooks, LFS, submodules, signed commits to protected branches | `git` (see [git-interop](references/git-interop.md)) |
| The repo has no `.jj` directory | `git`, or run `jj git init --colocate` first |

## Daily cheat sheet

```bash
# Status & history
jj st                              # status
jj log                             # graph of revisions (default revset is fine)
jj log -r 'trunk()..@'             # what's on my stack vs main
jj show @                          # current change
jj diff                            # diff of working-copy change
jj diff -r @-                      # diff of parent
jj diff --from main --to @         # range diff

# Making changes
jj new                             # start a new empty change on top of @
jj new main                        # start a new change on top of main
jj describe -m "msg"               # set/update description of current change
jj commit -m "msg"                 # describe @ and start a fresh new change on top

# Rewriting
jj squash                          # move @ into its parent (like amend)
jj squash -i                       # interactively pick hunks to move into parent
jj squash --into <rev>             # move @ into an arbitrary ancestor (autosquash replacement)
jj split                           # split @ into two changes
jj split -r <rev>                  # split any change, not just @
jj describe <rev> -m "msg"         # edit message of any change
jj abandon <rev>                   # drop a change (descendants rebase automatically)
jj rebase -s <src> -d <dest>       # move a subtree
jj rebase -b <branch> -d main      # rebase the whole branch onto main

# Navigating
jj edit <rev>                      # point working copy at an existing change (rarely; prefer `new`)
jj new <rev>                       # start a new change on top of <rev>
jj next / jj prev                  # walk the stack

# Bookmarks (only for pushing)
jj bookmark list
jj bookmark set <name> -r @        # create or move a bookmark to current change
jj bookmark delete <name>

# Git remotes
jj git fetch                       # fetch all tracked remotes
jj git push                        # push tracked bookmarks
jj git push --bookmark <name>      # push one bookmark
jj git push -c @                   # create a bookmark and push current change

# Undo / history recovery
jj undo                            # undo the last operation
jj op log                          # full operation log
jj op restore <op-id>              # jump back to any previous repo state
```

## Rules of thumb

- **Default to `jj new` instead of `git checkout -b`.** Give it a description with `jj describe -m` when the intent becomes clear, or use `jj commit -m` to close out a change and start a fresh one.
- **Don't mix `jj` and `git` mutating commands in a colocated repo.** Reads are fine; writes can cause branch conflicts. See [git-interop](references/git-interop.md) for details.
- **When a rebase "fails" in jj, it didn't — the conflict is in the commit.** Run `jj log` to see the conflicted change marker, then `jj resolve` or edit the files directly.
- **Prefer `jj squash --into <rev>` over `git commit --fixup` + autosquash.** It's one step and descendants rebase for free.
- **`jj abandon` is reversible.** It's not `git reset --hard`. Recover with `jj undo` or `jj op restore`.
- **Never force-push without confirming.** `jj git push` only pushes what changed, but bookmark moves are still force updates from the remote's perspective.

## References

- [git-to-jj command table](references/git-to-jj.md) — one-to-one translations for every common git workflow
- [jj CLI reference](references/cli-reference.md) — subcommands grouped by purpose, important flags
- [git interoperability](references/git-interop.md) — colocated vs standalone, init/clone/push, compatibility matrix, known gotchas
- [Common workflows](references/workflows.md) — split, squash, stacked rebase, conflict resolution, undo, pushing, recovering from a bad op
