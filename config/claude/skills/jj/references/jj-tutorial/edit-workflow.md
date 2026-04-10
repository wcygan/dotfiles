---
title: The edit workflow
source: https://steveklabnik.github.io/jujutsu-tutorial/real-world-workflows/the-edit-workflow.html
tags: [workflow, edit, daily-driver, stack-navigation]
---

# The Edit Workflow

The other daily-driver workflow in jj. Where the [squash workflow](squash-workflow.md) builds up one change, the edit workflow treats each change as a discrete unit that you explicitly navigate between. Work on one change at a time; move back and forth through your stack as needed.

## The rhythm

1. `jj new -m "first thing"` — start a change on top of main, describe it
2. Edit files. Content lives in `@`.
3. `jj new -m "second thing"` — start a new change on top
4. Edit files. Content lives in the new `@`.
5. Realize the second change should come first? `jj new -B @ -m "..."` inserts a change *before* `@`
6. `jj edit <rev>` or `jj next --edit` to jump back into an earlier change and tweak it — descendants auto-rebase

## Commands

```
# jj new -m "message"
jnm "message"                    # create new change on top of @
# jj describe -m "message"
jde "message"                    # describe (or re-describe) current change
# jj new -B @ -m "message"
jnm -B @ "message"               # create change BEFORE current @ (inserts in stack)
# jj edit <revision>
jed <revision>                   # point working copy at a specific change
# jj next --edit
jnx                              # move to child change, in edit mode
# jj st
js                               # check status
# jj log
jl                               # see the stack
```

## Aha moments

- **Automatic descendant rebase, always.** When you insert a change mid-stack with `jj new -B @`, every dependent commit automatically rebases. Klabnik: "this operation will *always* succeed" — no conflicts, no intervention, no `git rebase --continue` dance.
- **Change IDs are stable.** The change ID stays the same even when the underlying commit hash shifts during rebases. That's what lets you refer to "that change I was working on" across rewrites.
- **Working copy follows you.** `jj next --edit` physically moves the files on disk to reflect the target change's content — no stash, no checkout.

## Who this suits

Developers who prefer explicit, structured decomposition of work across multiple changes. Those who think sequentially about dependencies ("this should come before that"). People who realize mid-task that they want to break work up differently and want the VCS to support retroactive reorganization without losing work.

## Contrast with the squash workflow

| | Squash | Edit |
|---|---|---|
| Where you work | Always on top of @ in a scratch commit | Wherever you navigate in the stack |
| Canonical command | `jj squash` | `jj new -B @` / `jj edit` / `jj next --edit` |
| Mental model | `git add -p` applied to commits | Rebase-as-you-go with zero friction |
| When it shines | Refining one commit until done | Decomposing work mid-task |

Both are valid. Most jj users pick one as their default and reach for the other situationally.

**Canonical source:** https://steveklabnik.github.io/jujutsu-tutorial/real-world-workflows/the-edit-workflow.html
