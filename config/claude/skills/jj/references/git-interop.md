---
title: jj git interoperability
description: Colocated vs standalone backends, init/clone/push semantics, compatibility matrix, and gotchas when using jj on top of an existing git repo
tags: [git, interop, colocated, compatibility, gotchas]
---

# jj git interoperability

jj stores history in a standard `.git` directory by default, so collaborators using git are unaffected. This reference covers how to set up jj on an existing git repo and where the seams show.

## Table of contents

- [Two repository modes](#two-repository-modes)
- [Initializing on an existing git repo](#initializing-on-an-existing-git-repo)
- [Cloning from a git remote](#cloning-from-a-git-remote)
- [Fetching and pushing](#fetching-and-pushing)
- [How bookmarks map to git branches](#how-bookmarks-map-to-git-branches)
- [Compatibility matrix](#compatibility-matrix)
- [Conflicts and git representation](#conflicts-and-git-representation)
- [Gotchas](#gotchas)
- [Recommended config for mixed git/jj teams](#recommended-config-for-mixed-gitjj-teams)

## Two repository modes

**Colocated** (default when using `--colocate`): `.jj/` and `.git/` sit side-by-side in the same working tree. Every jj command automatically imports from and exports to git's refs and index. Other git-aware tools (IDEs, `git` itself, `gh`, `lazygit`) see a normal repo.

**Standalone**: git storage is hidden inside `.jj/`. Other tools cannot see it. You must call `jj git import` / `jj git export` explicitly to sync refs. Best for jj-only workflows.

**Recommendation for this environment:** always use colocated mode on repos the team still treats as git-native. It is the only way existing git tooling (IDE integrations, pre-commit hooks, CI scripts that call `git`) keeps working.

Toggle colocation on an existing repo:

```bash
jj git colocation status
jj git colocation enable     # adopt .git into the current working tree
jj git colocation disable    # move .git back inside .jj/
```

## Initializing on an existing git repo

In a directory that already has a `.git`:

```bash
jj git init --colocate       # preferred — side-by-side .jj/ and .git/
# or
jj git init --git-repo=.     # adopt the existing .git (legacy phrasing)
```

After init:

```bash
jj log                       # should render the existing git history
jj st
jj bookmark track main --remote=origin   # track main against origin (once)
```

No git history is modified. The initial import reads all branches and creates matching bookmarks.

**Gitignore `.jj/` immediately.** jj does **not** add `.jj/` to `.gitignore` for you, and `git status` will happily offer to commit the entire `.jj/` directory. Choose one:

- **Per-repo (shared)** — commit a `.gitignore` entry so every jj user on the team benefits:
  ```bash
  cat >> .gitignore <<'EOF'

  # Jujutsu (jj) local state — present only for contributors using jj.
  # See https://jj-vcs.dev. Safe to ignore; git users are unaffected.
  .jj/
  EOF
  jj commit -m "chore: gitignore .jj/ (jujutsu local state)"
  jj bookmark set main -r @-
  jj git push
  ```
- **Global (personal)** — one-time setup that covers every repo you ever colocate:
  ```bash
  mkdir -p ~/.config/git
  echo '.jj/' >> ~/.config/git/ignore
  git config --global core.excludesfile ~/.config/git/ignore
  ```

The narrated end-to-end recipe is in [workflows § Adopting jj in an existing git repo](workflows.md#adopting-jj-in-an-existing-git-repo).

**Backing out of colocation** is always safe: `rm -rf .jj` restores a plain git repo. Git objects, refs, and history are untouched.

## Cloning from a git remote

```bash
jj git clone <url>                     # colocated by default in recent jj versions
jj git clone <url> <dir> --colocate    # be explicit when in doubt
jj git clone <url> --remote upstream   # custom remote name (default: origin)
```

Cloning non-git remotes is not supported yet.

## Fetching and pushing

```bash
jj git fetch                            # fetch all configured remotes
jj git fetch --remote origin            # one remote
jj git fetch --all-remotes              # explicit
jj git fetch --tracked                  # only bookmarks marked as tracked

jj git push                             # push all tracked bookmarks that changed
jj git push --bookmark <name>           # push one bookmark
jj git push --all                       # all local bookmarks
jj git push -c @                        # create an auto-named bookmark at @ and push it
jj git push --remote origin             # target a specific remote
```

**Force updates:** `jj git push` will refuse to push a bookmark move that rewrites commits that already exist on the remote unless you re-run with `--allow-new` (for brand-new bookmarks) or after moving the bookmark explicitly. jj does not have an independent `--force-with-lease`; it relies on the remote bookmark state it fetched most recently. Re-fetch before pushing if the remote may have changed.

## How bookmarks map to git branches

- Every git branch imported from the remote becomes a **tracked bookmark** named `<branch>@<remote>` plus a local bookmark `<branch>` if `git.auto-local-bookmark = true`.
- Local bookmarks are jj-only until you `jj git push` them.
- `jj bookmark track <branch>@<remote>` starts tracking an existing remote branch.
- A bookmark can be **conflicted** when the local and remote positions disagree. `jj st` and `jj log` mark these — resolve with `jj bookmark set <name> -r <rev>`.
- In colocated mode, jj keeps git's HEAD **detached** because jj has no "current branch" concept. This is expected, not a warning.

## Compatibility matrix

| Feature | Supported | Notes |
|---|---|---|
| `.gitignore` | Yes | Native implementation; a previously-tracked file needs `jj file untrack` before the ignore kicks in |
| `.git/config` | Partial | `[remote "..."]` and `core.excludesFile` are honored; many other sections ignored |
| Authentication | Yes | Git handles credentials via its own helpers (ssh, https, credential manager) |
| Submodules | No | Submodules don't appear in jj's working copy but aren't deleted. Use `git submodule` commands directly |
| Git LFS | No | [upstream issue #80](https://github.com/jj-vcs/jj/issues/80). Use `git lfs` around jj |
| Git hooks | No | jj does not run `.git/hooks/*`. Run them manually or via CI. [#405](https://github.com/jj-vcs/jj/issues/405) |
| `.gitattributes` | No | [#53](https://github.com/jj-vcs/jj/issues/53). Line-ending normalization etc. is not applied |
| Signed commits | Yes | Configure `signing.backend = "gpg"`, `signing.key`, `signing.sign-all`. Or call `jj sign` |
| Shallow clones | Partial | jj can operate on a shallow clone but cannot deepen or unshallow |
| Octopus merges | Yes | jj supports multi-parent merges natively |
| Orphan branches | Yes | jj has a virtual root commit so this case is trivial |
| Staging area (index) | Ignored | jj does not use git's index. `jj diff` is always HEAD↔working copy |
| Reflogs | Superseded | jj has its own operation log, richer than git reflogs |

## Conflicts and git representation

Conflicted jj commits can't be expressed as normal git objects. jj serializes them in git with synthetic directories named `.jjconflict-base-*` and `.jjconflict-side-*`, plus a non-standard `jj:trees` header on the commit. Change IDs are stored in a `change-id` header (behind `git.write-change-id-header`).

**Consequences:**
- `git log` on a conflicted commit shows those synthetic paths. Harmless but ugly.
- Never push a conflicted commit to a shared branch — remote git tools won't know what to do with it. Resolve first.

## Gotchas

1. **Don't mix mutating `jj` and `git` commands.** Reading with `git log` / `git diff` is fine. Running `git commit`, `git rebase`, `git reset` while jj is tracking the working copy can create bookmark conflicts. If it happens, `jj st` will show the conflict and `jj bookmark set` will fix it.
2. **`git switch <branch>` in a colocated repo** moves git's HEAD but leaves jj where it was. Prefer `jj new <branch>` or `jj edit <rev>`.
3. **Large repos can feel slow** because jj imports/exports on every command. Mitigate with `jj util gc` and by keeping the git object store clean (`git gc`).
4. **CI scripts that call `git`** continue to work in colocated mode but will see the detached HEAD. If a script needs a branch name, pass one explicitly.
5. **Pre-commit hooks** won't run on `jj commit`. Options: (a) run `pre-commit run` manually before commit, (b) install a wrapper script, or (c) configure `jj fix` to call the relevant formatters.
6. **LFS files** stored via `git lfs` will be visible in the working copy if smudge/clean filters already ran. jj doesn't manage LFS state, so you must run `git lfs pull` / `git lfs push` yourself around jj operations.
7. **Signed commits on rewrite:** rewriting a signed commit re-signs it only if signing is configured. A rewritten-but-unsigned commit will fail signature checks downstream.
8. **Submodules:** if a repo has submodules, jj ignores them entirely. Use `git submodule update` after `jj git fetch`. Submodule changes must be committed via git.

## Recommended config for mixed git/jj teams

Put this in `~/.config/jj/config.toml` (user) or `.jj/repo/config.toml` (repo):

```toml
[user]
name = "Your Name"
email = "you@example.com"

[git]
auto-local-bookmark = true     # auto-create local bookmarks for imported git branches
colocate = true                # default to colocated mode on `jj git init`

[ui]
default-command = "log"        # `jj` with no args prints the log
diff.format = "git"            # familiar git-style diffs
pager = "delta"                # if delta is installed

[revset-aliases]
"trunk()" = 'latest(remote_bookmarks(exact:"main") | remote_bookmarks(exact:"master") | remote_bookmarks(exact:"trunk"))'

[signing]
backend = "gpg"                # or "ssh"
sign-all = false               # set true only if the team requires it
```

Check settings with `jj config list` and edit with `jj config edit --user`.
