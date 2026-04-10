---
title: jj CLI reference
description: jj subcommands grouped by purpose with key flags and usage notes
tags: [jj, cli, reference, commands, flags]
---

# jj CLI reference

Subcommands grouped by purpose. For exhaustive detail, run `jj <cmd> --help` or visit https://www.jj-vcs.dev/latest/cli-reference/.

## Table of contents

- [Working copy](#working-copy)
- [History and inspection](#history-and-inspection)
- [Rewriting and reorganizing](#rewriting-and-reorganizing)
- [Navigation](#navigation)
- [Bookmarks and tags](#bookmarks-and-tags)
- [Git integration](#git-integration)
- [Operations (undo/redo)](#operations-undoredo)
- [Configuration](#configuration)
- [Utilities](#utilities)
- [Shared flags and revsets](#shared-flags-and-revsets)

## Working copy

| Command | Purpose |
|---|---|
| `jj st` (`status`) | Current working-copy change, parents, changed files |
| `jj new [<rev>]` | Create a new empty change on top of `<rev>` (default: `@`). Use this instead of `git checkout` |
| `jj edit <rev>` | Point the working copy at an existing change. Rare — prefer `jj new <rev>` |
| `jj restore [<paths>]` | Restore paths from another revision (default: parent) |
| `jj file track <path>` / `jj file untrack <path>` | Manage which paths are tracked |
| `jj file list [-r <rev>]` | List files in a revision |
| `jj file show -r <rev> <path>` | Dump file contents at a revision |

## History and inspection

| Command | Purpose |
|---|---|
| `jj log [-r <revset>]` | Revision graph. Default revset is configurable; `jj log -r 'all()'` shows everything |
| `jj show [<rev>]` | Description and diff for a revision |
| `jj diff [-r <rev>]` | Diff for `@` (default) or `<rev>`. Use `--from A --to B` for a range |
| `jj diffedit [-r <rev>]` | Interactively edit a commit's diff in a merge tool |
| `jj describe [<rev>] [-m <msg>]` | Set a description. Opens `$EDITOR` if `-m` omitted |
| `jj commit [-m <msg>]` | Describe `@` and start a fresh empty change on top. Equivalent to `jj describe -m ...; jj new` |
| `jj evolog -r <rev>` | Show how a change evolved through rewrites |

## Rewriting and reorganizing

| Command | Purpose |
|---|---|
| `jj squash [-i] [--into <rev>] [--from <rev>] [<paths>]` | Move changes into another revision. Default: `@` into `@-`. `--into` picks any ancestor. `-i` for interactive hunks |
| `jj split [-r <rev>] [-i] [<paths>]` | Split a change into two. `-i` for interactive selection |
| `jj absorb [-r <rev>]` | Automatically move working-copy changes into the mutable ancestor that last touched each line. Replaces `git commit --fixup` workflows |
| `jj duplicate <rev> [-A <after>] [-B <before>]` | Copy a change. Cherry-pick equivalent |
| `jj rebase -s <src> -d <dest>` | Move `<src>` and its descendants onto `<dest>` |
| `jj rebase -r <rev> -d <dest>` | Move a single change (descendants stay put) |
| `jj rebase -b <branch> -d <dest>` | Move an entire branch (everything reachable from `<branch>` but not `<dest>`) onto `<dest>` |
| `jj rebase -r <rev> --before <other>` / `--after <other>` | Reorder a change in a stack |
| `jj abandon [<rev>]` | Drop a change; descendants rebase automatically. Reversible via `jj undo` |

## Navigation

| Command | Purpose |
|---|---|
| `jj next [<n>]` | Move working copy `n` children forward |
| `jj prev [<n>]` | Move working copy `n` parents back |
| `jj resolve [<paths>]` | Open merge tool on conflicted paths in `@` |

## Bookmarks and tags

Bookmarks are jj's name for branches. They are optional and must be moved manually.

| Command | Purpose |
|---|---|
| `jj bookmark list` / `jj b l` | List bookmarks |
| `jj bookmark create <name> -r <rev>` | Create a bookmark at a revision |
| `jj bookmark set <name> -r <rev>` | Move (or create) a bookmark. Force by default |
| `jj bookmark delete <name>` | Delete locally |
| `jj bookmark rename <old> <new>` | Rename |
| `jj bookmark move <name> --to <rev>` | Explicit move |
| `jj bookmark track <name>@<remote>` | Start tracking a remote branch |
| `jj bookmark untrack <name>@<remote>` | Stop tracking |
| `jj tag list` / `jj tag set <name> -r <rev>` / `jj tag delete <name>` | Tag management |

## Git integration

| Command | Purpose |
|---|---|
| `jj git init [--colocate] [--git-repo=<path>]` | Create a jj repo. `--colocate` shares a working copy with git. `--git-repo` adopts an existing git repo |
| `jj git clone <url> [<dir>] [--colocate]` | Clone a git remote |
| `jj git fetch [--remote <name>] [--all-remotes] [--tracked]` | Fetch from a remote |
| `jj git push [--remote <name>] [--bookmark <name>] [--all] [-c <rev>]` | Push bookmarks. `-c <rev>` creates an auto-named bookmark at `<rev>` and pushes it |
| `jj git remote add <name> <url>` | Add a git remote |
| `jj git remote list` / `remove` / `rename` / `set-url` | Manage remotes |
| `jj git colocation status` / `enable` / `disable` | Toggle git colocation on an existing repo |
| `jj git import` / `jj git export` | Manually sync refs to/from git. Only needed in standalone mode |

## Operations (undo/redo)

Every jj command is an **operation** — an atomic update to all refs and working-copy state. The operation log is the real undo.

| Command | Purpose |
|---|---|
| `jj undo` | Revert the last operation |
| `jj redo` | Redo a previously-undone operation |
| `jj op log` | Show the full operation log |
| `jj op show <op-id>` | Show what an operation changed |
| `jj op diff --from <a> --to <b>` | Diff between operations |
| `jj op restore <op-id>` | Jump the entire repo state back to an operation |
| `jj op revert <op-id>` | Revert a specific past operation (newer ops stay) |
| `jj op abandon <op-id>..` | Permanently drop operation log entries (reclaim space) |

## Configuration

| Command | Purpose |
|---|---|
| `jj config list` | Show current config |
| `jj config get <key>` | Read one value |
| `jj config set --user <key> <value>` | Set a user-level value |
| `jj config set --repo <key> <value>` | Set a repo-level value |
| `jj config edit --user` | Open config in `$EDITOR` |
| `jj config path --user` | Print config file path |

Common keys: `user.name`, `user.email`, `ui.default-command`, `ui.diff.format`, `ui.pager`, `revset-aliases."trunk()"`, `git.auto-local-bookmark`, `git.colocate`.

## Utilities

| Command | Purpose |
|---|---|
| `jj fix [-r <rev>]` | Run configured formatters on files in a revision |
| `jj bisect run <cmd>` | Binary search through history with a test command |
| `jj workspace add <path>` | Create an additional workspace (like git worktrees) |
| `jj workspace list` / `remove` / `root` | Manage workspaces |
| `jj util gc` | Garbage-collect unreachable objects (esp. in large colocated repos) |
| `jj util completion <shell>` | Print shell completions |

## Shared flags and revsets

**Common flags:**
- `-r, --revision <revset>` — target revision(s)
- `-i, --interactive` — hunk-level selection via merge tool
- `-f, --from <rev>` / `-t, --to <rev>` — source/destination for `squash`, `diff`
- `-m, --message <msg>` — inline commit/change description
- `-d, --destination <rev>` — target of a rebase
- `-s, --source <rev>` — source subtree for a rebase
- `-b, --branch <rev>` — branch root for a rebase
- `--at-op <op-id>` — run a read command as if at a past operation

**Revset basics** (jj's selector language, used wherever a command takes `-r`):

| Revset | Meaning |
|---|---|
| `@` | Working-copy change |
| `@-` | Parent of `@` |
| `@--` | Grandparent |
| `<change-id-prefix>` | Any prefix unique enough to identify a change |
| `main` | The bookmark named `main` |
| `trunk()` | Configured trunk revset (defaults to `main`/`master`) |
| `A..B` | Ancestors of `B` that are not ancestors of `A` |
| `A::B` | Range including both endpoints |
| `::A` | All ancestors of `A` |
| `A::` | All descendants of `A` |
| `mutable()` / `immutable()` | Everything not yet pushed / already pushed |
| `description("foo")` | Changes whose description matches |
| `author("alice")` | Changes by author |
| `heads(...)` | Leaf changes of a set |
| `all()` | Literally all visible changes |

Combine with `&` (and), `|` (or), `~` (not): `jj log -r 'mutable() & author(exact:"me@example.com")'`.
