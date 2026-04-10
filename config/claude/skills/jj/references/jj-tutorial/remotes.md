---
title: Working with remotes
source: https://steveklabnik.github.io/jujutsu-tutorial/sharing-code/remotes.html
tags: [remotes, git-interop, push, fetch, auto-bookmarks]
---

# Remotes

jj abstracts branches away from local work. Remote branches (`trunk@origin`) exist separately from local bookmarks (`trunk`). When you're ready to share, jj can auto-generate bookmark names from your change ID — you never need to come up with a feature-branch name.

## Core mental model

> **Work locally without thinking about branches. Push when ready for collaboration.**

## Commands

```
# jj git remote add origin git@github.com:you/repo.git
jj git remote add origin git@github.com:you/repo.git   # (no alias)
# jj git push
jgp                                       # push all tracked bookmarks that moved
# jj git push -c @
jgp -c @                                  # create a bookmark at @ and push it
# jj git fetch
jgf                                       # sync with the remote
# jj new trunk
jn trunk                                  # start a new change on top of trunk
# jj describe -m "add a comment to main"
jde "add a comment to main"
# jj bookmark set trunk --allow-backwards
jbs trunk --allow-backwards               # move a bookmark backward (guarded)
# jj abandon pzkrzopz
jab pzkrzopz                              # discard an unwanted change
```

## Aha moments

### `jj git push -c @` auto-generates a bookmark name

Instead of agonizing over `feature/add-rate-limiter-v2-final`, you run `jj git push -c @` and jj creates a branch named something like `push-vmunwxsksqvk` — derived from your stable change ID. The auto-name is tied to the change, not the content, so it stays meaningful across rewrites.

This is the single biggest ergonomic win over git's branch-first mental model.

### `--allow-backwards` guards against dangerous moves

Moving a bookmark *backward* (to an earlier commit) is dangerous **only if the current position has already been pushed**. Locally it's safe, but jj requires the `--allow-backwards` flag as a speed bump to make sure you meant it.

### Working copy auto-moves after push

After `jj git push`, jj warns: *"the working-copy commit became immutable, so a new commit has been created on top of it."* Your `@` is automatically moved to a fresh empty child. No manual `jj new` needed — jj protects the pushed commit from further in-place modification.

## Git-interop pattern

The natural progression:

1. **Make changes locally** — tracked by change ID, no branch name
2. **`jj git push -c @`** — auto-creates a remote-tracking bookmark
3. **Open a PR** from the auto-generated branch on GitHub
4. **Fetch updates with `jj git fetch`**, then `jj new trunk@origin` to start fresh work on top

No "which branch am I on?" No "what should I name this?" jj tracks your changes internally and exposes branch names to the remote only when needed.

## Configuration

You can set default push/fetch targets in `.jj/repo/config.toml`:

```toml
[git]
push = "origin"
fetch = "upstream"
```

This enables fork-based workflows without explicit `--remote` flags every time.

**Canonical source:** https://steveklabnik.github.io/jujutsu-tutorial/sharing-code/remotes.html
