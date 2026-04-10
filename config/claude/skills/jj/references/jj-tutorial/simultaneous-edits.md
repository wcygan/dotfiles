---
title: Simultaneous edits across branches
source: https://steveklabnik.github.io/jujutsu-tutorial/advanced/simultaneous-edits.html
tags: [advanced, parallel, stacked-prs, merge-commits, absorb]
---

# Simultaneous Branch Edits

An advanced pattern that inverts git's model. Instead of switching between branches, you **merge them together**, make changes that logically belong to different branches in one working tree, then distribute those edits back to the right parent branches using `jj absorb` or `jj squash`.

## Core mental model

A jj commit can have many parents. If you create a single change whose parents are all your in-flight feature branches, your working tree shows the union of them. Edit what you want. Then use `jj absorb` to route each hunk back to whichever parent's history it belongs in.

This is impossible to do cleanly in git without complex scripting.

## Commands

```
# jj new trunk
jn trunk                                          # start new change from trunk
# jj new ym z r yx m -m "merge: combine PRs"
jnm ym z r yx m "merge: combine PRs"              # commit with 5 parents
# jj new xn
jn xn                                             # create child on the merge
# jj rebase -r xn -o m -o ym -o yx -o r -o kv
jj rebase -r xn -o m -o ym -o yx -o r -o kv       # rebase to multiple parents (no alias — jrb only covers -d)
# jj rebase -s 'all:roots(trunk..@)' -o trunk
jj rebase -s 'all:roots(trunk..@)' -o trunk       # rebase all PR roots after upstream update
# jj absorb
jj absorb                                         # auto-distribute edits to the right parents (no alias)
# jj abandon push-vmunwxsksqvk
jab push-vmunwxsksqvk                             # clean up temporary bookmarks
```

## Aha moments

### Multiple parents = parallel editing

When a commit has N parents, its working tree is the merge of all N. If those parents are five in-progress feature branches, you're simultaneously "on" all of them. Make a fix that spans three features → `jj absorb` figures out where each line actually belongs and distributes it.

### The `all:` revset prefix

`all:roots(trunk..@)` tells jj "I intentionally want a set, not a single revision." Without the `all:` prefix, ambiguous selectors error out. With it, you can operate on every PR root reachable from your merge commit at once.

### `-s` vs `-r` in rebase

- `-s <rev>` — rebase `<rev>` **and all its descendants**. Matches git's `rebase --onto` intuition.
- `-r <rev>` — "rip out" a single commit, leaving descendants in place. No git equivalent without plumbing.

The distinction matters when you want to move one change without dragging its stack along.

### `jj absorb` as a smart squash

`jj absorb` reads the blame history of each modified line and moves the change into the mutable ancestor that last touched it. It replaces the git workflow of `git commit --fixup` + autosquash — and it's automatic rather than manual.

### Cleanup after upstream rebase

When upstream lands changes, `jj rebase -s 'all:roots(trunk..@)' -o trunk` moves every PR simultaneously. This leaves behind empty `@` commits that need a `jj new` + `jj abandon` cleanup pass. Worth the cost when you're managing 5+ parallel PRs.

## When this pattern shines

- Managing several stacked or parallel PRs
- Making a single fix that touches multiple in-flight features
- Keeping your PRs cleanly separated while still coding them as one cohesive change locally
- Bulk-rebasing after an upstream update

## When to skip it

For one or two PRs, this is overkill. Use the simpler [squash-workflow](squash-workflow.md) or [edit-workflow](edit-workflow.md) and reach for this only when the parallel PR count crosses 3–4.

**Canonical source:** https://steveklabnik.github.io/jujutsu-tutorial/advanced/simultaneous-edits.html
