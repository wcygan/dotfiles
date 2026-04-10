---
title: Named branches (bookmarks) — don't move automatically
source: https://steveklabnik.github.io/jujutsu-tutorial/sharing-code/named-branches.html
tags: [bookmarks, branches, interop, mental-model]
---

# Named Branches (Bookmarks)

Named branches in jj are called **bookmarks**, and they exist primarily for interoperability with git-centric tools (GitHub, Gerrit). They are not essential to local workflow. The foundational difference from git:

> **Bookmarks do not move automatically when you create new commits. They stay put until you explicitly move them.**

In git, `HEAD` follows your branch. In jj, there is no "current branch" — there's only `@` (the working-copy change) and a set of bookmarks that you place on whichever change you want them to point to.

## Commands

```
# jj bookmark create <name>
jbc <name>                                 # create a bookmark at current working copy
# jj bookmark set <name>
jbs <name>                                 # move an existing bookmark to current @
# jj bookmark set <name> -r <rev>
jbs <name> -r <rev>                        # move to a specific revision
# jj bookmark delete <name>
jj bookmark delete <name>                  # delete a bookmark (no alias)
# jj bookmark list
jbl                                        # list all bookmarks
# jj log --limit <n>
jl --limit <n>                             # view history
# jj log -r '<revset>'
jl -r '<revset>'                           # query specific revisions
# jj new
jn                                         # create new change (bookmark does NOT follow)
# jj abandon <rev>
jab <rev>                                  # discard unwanted commits
```

## The non-moving branch surprise

```
# jj new
jn
# jj bookmark set trunk
jbs trunk
> Moved 1 bookmarks to pzkrzopz fcf669c5 trunk | (empty) (no description set)
```

After `jj new`, `@` moves to a new empty child — but `trunk` stays where it was. You have to explicitly `jj bookmark set trunk` to advance it. This catches every git user off-guard on day one.

## The practical implication

Rather than updating a branch continuously during development (as git forces you to), experienced jj users **check bookmark status just before pushing**. Bookmarks are treated as remote-tracking references: local developers work with anonymous changes tracked by change ID, and only materialize a bookmark position when they're about to share.

The mental model: "my branch points where the remote branch points until I decide it should move."

## Aha moment

This initially feels like a regression ("why do I have to remember to move the branch?"), but it's actually what enables jj's most powerful feature: **rewriting commits at the tip of a branch without worrying about where the branch label is**. You can do multiple rounds of refinement (amend, reorder, split, squash) with full freedom, and then `jj bookmark set` once when you're ready. In git, every rewrite risks "branch is ahead by N commits" confusion because the label chases you.

## Connection to the sharing workflow

Named branches only matter when you interact with a remote. For local-only work, skip bookmarks entirely. When you're ready to push, `jj bookmark set main -r @-` (or whichever change) and then `jj git push`. See [remotes.md](remotes.md) for the next step.

**Canonical source:** https://steveklabnik.github.io/jujutsu-tutorial/sharing-code/named-branches.html
