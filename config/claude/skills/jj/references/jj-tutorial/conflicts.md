---
title: Conflicts are committable
source: https://steveklabnik.github.io/jujutsu-tutorial/branching-merging-and-conflicts/conflicts.html
tags: [conflicts, rebase, committable-conflicts, mental-model]
---

# Conflicts in jj

The single biggest mental shift from git. In jj, **conflicts are committable**. A rebase or merge never halts. jj records the conflict inside the resulting commit and keeps going. You resolve whenever you feel like it.

> "If there's a conflict, it doesn't make you stop and fix it, it records that there's a conflict and still performs the rest of the rebase. This is *very* powerful." — Klabnik

## Commands

```
# jj new -m "message"
jnm "message"                    # create new change
# jj new <commit_id> -m "message"
jnm <commit_id> "message"        # branch from a specific commit
# jj rebase -r <commit> -o @
jj rebase -r <commit> -o @       # rebase a single commit onto current (no alias)
# jj edit <commit>
jed <commit>                     # jump into a conflicted commit to fix it
# jj st
js                               # check status (shows conflict markers)
# jj log --limit N
jl --limit N                     # view history (conflicts shown as "(conflict)")
# jj undo
ju                               # undo the previous operation
# jj abandon <commit>
jab <commit>                     # delete an unwanted change
# jj resolve
jres                             # resolve conflicts interactively
```

## Aha moments

### 1. Rebases always succeed

When `jj rebase -r povouosx -o @` produces a conflict, the rebase *still completes*. The resulting commit appears in `jj log` marked `(conflict)`. There's no "rebase in progress" state to abort or continue. You can keep working on unrelated things and come back to the conflict later.

### 2. Automatic descendant rebase

After you fix a conflicted parent, jj automatically rebases its children:

```
Rebased 1 descendant commits onto updated working copy.
```

A resolution at one level propagates through the DAG without you re-running anything. If a descendant was *only* conflicted because of the parent, it often clears automatically.

### 3. Richer conflict markers

jj's conflict markers are more expressive than git's `<<<<`/`====`/`>>>>` three-way format:

- `<<<<<<<` — start of conflict
- `+++++++` — snapshot start
- `%%%%%%%` — diff start
- `>>>>>>>` — end of conflict

The snapshot + diff combination gives jj enough info to automatically recompute conflicts after rewrites (this is what makes auto-rebase of descendants work).

## How jj differs from git

| Aspect | git | jj |
|---|---|---|
| Conflict handling | Halts; requires immediate resolution | Records conflict, continues |
| Rebasing children | Manual re-execution | Automatic propagation |
| Workflow | Linear problem-solving | Can stack more work on conflicted commits |
| Markers | 3-way only | Snapshots + diffs |
| Recovery | `git rebase --abort` | `jj undo` or `jj op restore` |

## Broader implication

This unlocks **stacked PR** workflows that are painful in git. You can develop multiple dependent changes even when intermediate commits have unresolved conflicts, resolving strategically when you're ready rather than reactively every time git complains.

**Canonical source:** https://steveklabnik.github.io/jujutsu-tutorial/branching-merging-and-conflicts/conflicts.html
