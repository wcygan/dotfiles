---
title: The squash workflow
source: https://steveklabnik.github.io/jujutsu-tutorial/real-world-workflows/the-squash-workflow.html
tags: [workflow, squash, daily-driver, describe-first, index-replacement]
---

# The Squash Workflow

One of two daily-driver workflows in jj. Martin (jj's creator) prefers this one. It formalizes git's index concept but applied directly to commits: you describe the work first, create an empty "scratch" child, then `jj squash` the scratch's content back into the described parent — like `git add` operating on the commit graph instead of an invisible staging area.

## The rhythm

1. `jj describe -m "what I'm about to do"` — name the work before starting
2. `jj new` — create an empty scratch commit on top
3. Edit files. All edits accumulate in `@` (the scratch).
4. `jj squash` — move all of `@`'s content into the described parent
5. Repeat step 3–4 as you iterate; optionally `jj squash -i` for hunks

## Commands

```
# jj describe -m "message"
jde "message"                   # describe work before implementing
# jj new
jn                              # create empty scratch commit
# jj st
js                              # view working-copy changes
# jj squash
jsq                             # move all changes in @ to its parent
# jj squash src/main.rs
jsq src/main.rs                 # move a specific file to the parent
# jj squash -i
jsq -i                          # interactive hunk selection (TUI)
# jj abandon
jab                             # discard the current change
```

## Aha moments

- **One tool, many targets.** Klabnik writes: "we don't use some tools on the index, and some on commits: we use them all on commits." `jj squash` works on any change, not just the working copy → parent pair. This eliminates git's dual-system (index + commits) overhead.
- **`jj squash` is strictly more powerful than `git add`.** It can move changes between any two adjacent commits, not only working-copy → HEAD.
- **Multiple consecutive empty commits are free.** There's no friction from repeatedly running `jj new` during iteration — empty commits are a normal part of the process.

## Who this suits

Developers deeply familiar with git's index who want that power without managing two separate states. Those who prefer explicit "declare intent first, then do the work" discipline. Those who like interactive patch selection (`jj squash -i`) without context-switching between `git add -p`, `git rebase -i`, and `git commit`.

## Contrast with the edit workflow

Squash keeps you on *one* change, continuously moving content into it. The [edit workflow](edit-workflow.md) has you navigating between discrete changes in a stack. Squash = incremental refinement of one commit; edit = structured decomposition across many.

**Canonical source:** https://steveklabnik.github.io/jujutsu-tutorial/real-world-workflows/the-squash-workflow.html
