---
title: Updating PRs after review
source: https://steveklabnik.github.io/jujutsu-tutorial/sharing-code/updating-prs.html
tags: [prs, review, update, bookmarks, force-push]
---

# Updating PRs After Review

The central rhythm of PR feedback loops in jj:

> **The workflow is not: Make change → Update branch → Make change → Update branch → Push.**
> **It is: Make change → Make change → Update branch → Push.**

Unlike git, jj separates commit creation from branch positioning. Bookmarks don't automatically follow your commits — you explicitly position them before pushing.

## Commands

```
# jj new -m "message"
jnm "message"                                  # create new change
# jj bookmark set <branch-name>
jbs <branch-name>                              # move branch to current commit
# jj git push
jgp                                            # push tracked branches
# jj bookmark set <branch> -r @- --allow-backwards
jbs <branch> -r @- --allow-backwards           # move branch backward
# jj edit <commit-hash>
jed <commit-hash>                              # switch working copy to a commit
# jj abandon <commit-hash>
jab <commit-hash>                              # delete a commit
# jj next --edit
jnx                                            # move to next commit in stack
# jj git push -b <branch-name>
jgp -b <branch-name>                           # push a specific branch
# jj st
js                                             # check status
# jj log
jl                                             # view commit graph
```

## Two ways to respond to feedback

### Adding commits (history-preserving)

1. `jj new -m "address review: fix X"` — create a new change on top
2. Edit files
3. `jj bookmark set my-feature` — move bookmark to the new @
4. `jj git push`

**Effect:** review comments on the original commit persist because that commit is unchanged. Good for projects that value discussion history.

### Rewriting commits (clean-history)

1. `jj edit <the-commit-the-review-touched>` — jump into it
2. Edit files
3. jj auto-rebases descendants: *"Rebased 1 descendant commits onto updated working copy."*
4. `jj bookmark set my-feature -r <latest-rev>`
5. `jj git push` — this force-pushes

**Effect:** clean history, but review comments show as "outdated" on GitHub. Good for projects that prefer squash-merge or linear history.

## Aha moments

- **Silent-success gotcha.** `jj git push` without any bookmark movement succeeds with *"Nothing changed"*. Klabnik: "the worst case is that nothing gets pushed, which is a reminder." If your push does nothing, you probably forgot `jj bookmark set`.
- **Asterisks signal divergence.** When a local bookmark and its remote counterpart disagree, `jj log` shows the bookmark name with an asterisk (`main*`) — visual feedback that you need to push or fetch.
- **The mental flip.** Stop thinking "where does this commit go?" Start thinking "where should the branch point when I push?" The latter is a deliberate, one-time decision instead of a continuous tax.

## Connection to broader workflow

This pattern is the foundation of stacked PRs: you maintain multiple dependent bookmarks, and each time you update a chain, you reposition them all before a single `jj git push`. See [simultaneous-edits.md](simultaneous-edits.md) for the advanced version.

**Canonical source:** https://steveklabnik.github.io/jujutsu-tutorial/sharing-code/updating-prs.html
