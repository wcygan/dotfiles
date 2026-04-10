---
title: Git to jj command translation
description: One-to-one translation table from common git commands to their jj equivalents
tags: [git, translation, commands, migration]
---

# Git → jj translation

Concrete mappings for users migrating muscle memory from git. When two jj forms exist, the first is preferred.

## Table of contents

- [Repository setup](#repository-setup)
- [Inspecting state](#inspecting-state)
- [Files](#files)
- [Creating and modifying changes](#creating-and-modifying-changes)
- [Undoing changes](#undoing-changes)
- [Bookmarks and navigation](#bookmarks-and-navigation)
- [Rebasing and reordering](#rebasing-and-reordering)
- [Conflicts, merges, reverts](#conflicts-merges-reverts)
- [Tags](#tags)
- [History recovery (no git equivalent)](#history-recovery-no-git-equivalent)
- [Utilities](#utilities)

## Repository setup

| Task | git | jj |
|---|---|---|
| New repo (colocated with git) | `git init` | `jj git init --colocate` |
| New repo (standalone) | — | `jj git init` |
| Adopt an existing git repo | — | `jj git init --git-repo=.` (run inside the repo) |
| Clone | `git clone <url> <dir>` | `jj git clone <url> <dir>` |
| Add remote | `git remote add <name> <url>` | `jj git remote add <name> <url>` |
| List remotes | `git remote -v` | `jj git remote list` |
| Fetch | `git fetch` / `git fetch <remote>` | `jj git fetch` / `jj git fetch --remote <remote>` |
| Fetch all | `git fetch --all` | `jj git fetch --all-remotes` |
| Push all bookmarks | `git push --all` | `jj git push --all` |
| Push one bookmark | `git push <remote> <name>` | `jj git push --bookmark <name>` |

## Inspecting state

| Task | git | jj |
|---|---|---|
| Status | `git status` | `jj st` |
| Log (graph) | `git log --oneline --graph --all` | `jj log` |
| Log of your stack | `git log main..HEAD` | `jj log -r 'trunk()..@'` |
| Show a commit | `git show <rev>` | `jj show <rev>` |
| Diff working copy | `git diff HEAD` | `jj diff` |
| Diff one commit | `git diff <rev>^ <rev>` | `jj diff -r <rev>` |
| Range diff | `git diff A B` | `jj diff --from A --to B` |
| Blame | `git blame <file>` | `jj file annotate <file>` |

## Files

| Task | git | jj |
|---|---|---|
| Add new file | `git add <file>` | Just create it — tracked automatically |
| Remove file | `git rm <file>` | `rm <file>` (tracked automatically) |
| Untrack (keep on disk) | `git rm --cached <file>` | `jj file untrack <file>` (must match `.gitignore`) |
| List tracked files | `git ls-files` | `jj file list` |
| Show file at rev | `git show <rev>:<file>` | `jj file show -r <rev> <file>` |

## Creating and modifying changes

| Task | git | jj |
|---|---|---|
| Commit staged changes | `git commit` | `jj commit -m "msg"` |
| Commit with message | `git commit -am "msg"` | `jj commit -m "msg"` |
| Amend message | `git commit --amend -m "msg"` | `jj describe -m "msg"` (current) or `jj describe <rev> -m "msg"` |
| Amend content | `git commit --amend -a` | `jj squash` (moves @ into @-) |
| Amend hunks only | `git add -p && git commit --amend` | `jj squash -i` |
| Fixup into ancestor | `git commit --fixup=<rev> && git rebase -i --autosquash` | `jj squash --into <rev>` |
| Split a commit | `git reset HEAD^ && git add -p && git commit` | `jj split` (or `jj split -r <rev>` for any change) |
| Interactively edit a diff | — | `jj diffedit -r <rev>` |
| Start new work on top of main | `git switch -c topic main` | `jj new main` |
| Checkout a commit | `git checkout <rev>` | `jj new <rev>` (creates empty change on top; don't use `jj edit` unless you mean it) |

## Undoing changes

| Task | git | jj |
|---|---|---|
| Discard working-copy edits to file | `git restore <file>` | `jj restore <file>` |
| Drop the current change | `git reset --hard HEAD^` | `jj abandon` (reversible) |
| Drop an arbitrary change | `git rebase --onto <rev>^ <rev>` | `jj abandon <rev>` |
| Soft reset (keep changes, drop commit) | `git reset --soft HEAD^` | `jj squash --from @-` (moves parent's content into @) |
| Stash | `git stash` | `jj new @-` (old change stays as a sibling; return via `jj edit <prev-change>`) |
| Undo the last operation | — | `jj undo` |

## Bookmarks and navigation

In jj, branches are called **bookmarks** and are optional. You do not need one to work.

| Task | git | jj |
|---|---|---|
| List branches | `git branch` | `jj bookmark list` (`jj b l`) |
| Create branch at rev | `git branch <name> <rev>` | `jj bookmark create <name> -r <rev>` |
| Move branch (force) | `git branch -f <name> <rev>` | `jj bookmark set <name> -r <rev>` |
| Delete branch | `git branch -d <name>` | `jj bookmark delete <name>` |
| Current branch | `git branch --show-current` | n/a — jj has no "current" bookmark |
| Switch branch | `git switch <name>` | `jj new <name>` (start new change on top of the bookmark) |
| Checkout remote branch | `git switch -t origin/<name>` | `jj bookmark track <name>@origin` |

## Rebasing and reordering

| Task | git | jj |
|---|---|---|
| Rebase current branch onto main | `git rebase main` | `jj rebase -b @ -d main` |
| Rebase a subtree | `git rebase --onto <dest> <src>^ <src>` | `jj rebase -s <src> -d <dest>` |
| Rebase a single commit | `git rebase --onto <dest> <rev>^ <rev>` | `jj rebase -r <rev> -d <dest>` |
| Interactive reorder | `git rebase -i` | Rewrite change by change — rebase individual revs with `jj rebase -r <rev> --before <other>` or `--after <other>` |
| Move a diff into an ancestor | `git commit --fixup && git rebase -i --autosquash` | `jj squash --into <rev>` |
| Absorb working copy into ancestors | — | `jj absorb` (finds the right ancestor by blame) |

## Conflicts, merges, reverts

| Task | git | jj |
|---|---|---|
| Merge two branches | `git merge <branch>` | `jj new @ <branch>` (creates a merge change) |
| Resolve conflicts | `edit; git add; git rebase --continue` | Edit files; conflict markers disappear on save, or use `jj resolve` |
| Revert a commit | `git revert <rev>` | `jj revert -r <rev> -B @` |
| Cherry-pick | `git cherry-pick <rev>` | `jj duplicate <rev> --destination @` |
| Reuse past resolution | `git rerere` | Built in — rebasing a resolved conflict keeps the resolution |

**Key difference:** jj never stops a rebase or merge on conflict. The conflicted state is stored in the commit; you resolve at your leisure. `jj log` marks conflicted changes.

## Tags

| Task | git | jj |
|---|---|---|
| List tags | `git tag -l` | `jj tag list` |
| Create tag | `git tag <name> <rev>` | `jj tag set <name> -r <rev>` |
| Delete tag | `git tag -d <name>` | `jj tag delete <name>` |
| Tags containing rev | `git tag --contains <rev>` | `jj tag list -r '<rev>::'` |

## History recovery (no git equivalent)

| Task | jj |
|---|---|
| See every operation ever performed | `jj op log` |
| Undo the last operation | `jj undo` |
| Redo | `jj redo` |
| Restore repo to a past operation | `jj op restore <op-id>` |
| Diff between operations | `jj op diff --from <a> --to <b>` |
| See how a change evolved | `jj evolog -r <rev>` |

## Utilities

| Task | git | jj |
|---|---|---|
| Repo root | `git rev-parse --show-toplevel` | `jj workspace root` |
| Search tracked content | `git grep <pattern>` | `rg <pattern>` (rg respects `.gitignore` automatically) |
| Pickaxe (search in diffs) | `git log -G <regex>` | `jj log -r 'diff_contains(regex:<regex>)'` |
| Bisect | `git bisect start/good/bad/run` | `jj bisect run` |
