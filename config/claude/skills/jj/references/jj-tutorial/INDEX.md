---
title: jj tutorial router (Steve Klabnik)
description: Index of locally-summarized pages from Steve Klabnik's jujutsu tutorial. Load individual pages on demand during learning sessions.
source: https://steveklabnik.github.io/jujutsu-tutorial/
tags: [tutorial, learning, router, steveklabnik]
---

# jj Tutorial — Local Router

Summaries of selected pages from [Steve Klabnik's Jujutsu Tutorial](https://steveklabnik.github.io/jujutsu-tutorial/). Each file captures the core lesson, commands, and aha moments. **Load them only when the user is explicitly learning jj, reflecting on a tutorial concept, or asking "how do I X" where X is one of the workflows below.** For daily jj work, the main SKILL.md and the sibling reference files (`git-to-jj.md`, `cli-reference.md`, `git-interop.md`, `workflows.md`) are the right place to look.

**Canonical source:** https://steveklabnik.github.io/jujutsu-tutorial/ — if the local summary is thin, send the user to the original.

## When to read what

| If the user... | Read |
|---|---|
| Is brand new to jj and wants "where do I start" | [00-overview.md](00-overview.md) then [squash-workflow.md](squash-workflow.md) |
| Asks "how do I actually commit things day-to-day" | [squash-workflow.md](squash-workflow.md) or [edit-workflow.md](edit-workflow.md) |
| Is choosing between the two daily-driver workflows | Both squash and edit — they contrast directly |
| Hits a merge conflict and is confused by jj's behavior | [conflicts.md](conflicts.md) |
| Is surprised that bookmarks don't move automatically | [named-branches.md](named-branches.md) |
| Is setting up a remote or fork | [remotes.md](remotes.md) |
| Got PR feedback and needs to update their branch | [updating-prs.md](updating-prs.md) |
| Wants to work on several PRs at once | [simultaneous-edits.md](simultaneous-edits.md) |

## Suggested learning path (from zero)

1. **[00-overview.md](00-overview.md)** — what the tutorial covers, the author's stance
2. **[squash-workflow.md](squash-workflow.md)** — canonical daily-driver (Martin's preferred)
3. **[edit-workflow.md](edit-workflow.md)** — alternative daily-driver, for contrast
4. **[conflicts.md](conflicts.md)** — committable-conflict model
5. **[named-branches.md](named-branches.md)** — bookmarks basics and the "branches don't move" surprise
6. **[remotes.md](remotes.md)** — git remote interop
7. **[updating-prs.md](updating-prs.md)** — the change → position-bookmark → push cadence
8. **[simultaneous-edits.md](simultaneous-edits.md)** — advanced parallel-PR work

## Pages in this router

- [00-overview.md](00-overview.md) — tutorial landing page, scope, author's goals
- [squash-workflow.md](squash-workflow.md) — describe-first, `jj squash` daily flow
- [edit-workflow.md](edit-workflow.md) — navigate-the-stack, `jj edit` / `jj next --edit` flow
- [conflicts.md](conflicts.md) — conflicts are committable; rebases never stop
- [named-branches.md](named-branches.md) — bookmarks as interop handles, not working state
- [remotes.md](remotes.md) — `jj git remote add`, `jj git push -c @`, `--allow-backwards`
- [updating-prs.md](updating-prs.md) — adding-commits vs rewriting flows for PR feedback
- [simultaneous-edits.md](simultaneous-edits.md) — merge commits with multiple parents, `jj absorb`

## Progressive disclosure rule

Do not preload these files during normal jj operations. This router exists specifically for **learning mode** — when the user is studying jj rather than using it. Triggers: "help me learn jj", "I don't understand X", "how does the squash workflow work", "what's the edit workflow", "I'm reading the tutorial and...", "reflect on what I just read".
