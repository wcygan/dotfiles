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
| The repo has no `.jj` directory | Adopt jj first (see below), then use jj |

## Adopting jj in an existing git repo

When you land in a plain-git repo and want to switch to jj, run the three steps below. Everything is local until the final push; nothing affects teammates who stay on git. Assumes a clean working tree — stash or commit in-progress work with git first if needed.

```bash
# 1. Colocate jj into the existing .git (no history is modified)
jj git init --colocate

# 2. Add .jj/ to the repo's .gitignore with context for teammates
cat >> .gitignore <<'EOF'

# Jujutsu (jj) local state — present only for contributors using jj.
# See https://jj-vcs.dev. Safe to ignore; git users are unaffected.
.jj/
EOF

# 3. Track main, commit the gitignore change via jj, advance the bookmark, push
jj bookmark track main --remote=origin     # only needed the first time
jj commit -m "chore: gitignore .jj/ (jujutsu local state)"
jj bookmark set main -r @-
jj git push
```

**Alternative — skip the repo change entirely.** If you don't want to touch the shared `.gitignore`, add `.jj/` to your global gitignore once and every future repo you colocate will just work:

```bash
mkdir -p ~/.config/git
echo '.jj/' >> ~/.config/git/ignore
git config --global core.excludesfile ~/.config/git/ignore
```

**Back out of colocation** at any time with `rm -rf .jj` — git is untouched, so the repo reverts to a plain git repo.

See [git-interop § Adopting jj in an existing git repo](references/git-interop.md#initializing-on-an-existing-git-repo) for the gotchas (submodules, LFS, clean-tree assumption, etc.) and [workflows § Adopting jj in a git repo](references/workflows.md#adopting-jj-in-an-existing-git-repo) for the narrated recipe.

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
- [Common workflows](references/workflows.md) — adopt, split, squash, stacked rebase, conflict resolution, undo, pushing, recovering from a bad op

## Learning mode only

- [jj-tutorial router](references/jj-tutorial/INDEX.md) — local summaries of Steve Klabnik's [jj tutorial](https://steveklabnik.github.io/jujutsu-tutorial/). **Load this only when the user is explicitly learning jj or reflecting on the tutorial** — e.g., "help me learn jj", "explain the squash workflow", "I'm reading the tutorial and...", "what's the difference between squash and edit workflows?". For daily jj operations, the four references above are sufficient; do not preload the tutorial router.
