---
title: Tutorial overview (landing page)
source: https://steveklabnik.github.io/jujutsu-tutorial/
tags: [tutorial, overview, author, scope]
---

# jj Tutorial — Overview

Steve Klabnik's tutorial is a learning-as-I-go document he started writing while teaching himself jj. He explicitly disclaims authority ("no claim that this tutorial is good, complete, or even accurate") and encourages corrections. The tone is exploratory, opinionated, and grounded in real experimentation rather than abstract theory.

## Scope (8 chapters)

1. **Introduction** — what jj is, why you might care
2. **Hello World** — install, init, status, describe
3. **Real-world Workflows** — the squash workflow and the edit workflow
4. **Branching, Merging, Conflicts** — including the committable-conflict model
5. **Sharing Code** — named branches (bookmarks), remotes, PRs, Gerrit
6. **Advanced Workflows** — simultaneous edits, stacked PRs, workspaces
7. **Fixing Problems** — undo, revert, the operation log
8. **Customization** — config and output templates

## Author's stance

Learning-in-public. "You only get to look at a problem as a beginner once" — Klabnik writes each chapter while discovering the topic, so the explanations retain the fresh confusion and realization patterns of someone coming from git. That makes it especially effective for git veterans learning jj.

## Pedagogical approach

**Hands-on first.** Commands and concrete workflows come before deep conceptual explanations. You run things, observe the output, then understand why. This suits git users who learn by doing rather than reading a manual.

## How to use this router

Each page under `jj-tutorial/` is a dense local summary of one tutorial chapter. Load only the ones relevant to the current learning question — don't page through all of them at once. The canonical URL is at the top of each local file; if the summary is thin or the user wants the full walkthrough with sample output, link them to the original.

**Canonical source:** https://steveklabnik.github.io/jujutsu-tutorial/
