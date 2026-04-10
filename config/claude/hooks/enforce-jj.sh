#!/usr/bin/env bash
# enforce-jj.sh — PreToolUse Bash hook that nudges git commands toward jj
# equivalents inside jj-managed repos.
#
# Behavior:
#   - Runs only for Bash tool calls whose first token is `git`.
#   - No-op if jj is not installed, or the working directory is not a jj repo
#     (no reachable workspace root), or the git subcommand has no clean jj
#     equivalent (submodule, lfs, worktree, hooks, etc.).
#   - Blocks with exit 2 + a helpful hint on mutating subcommands that do have
#     a jj equivalent, so the model can retry with the jj form.
#   - Escape hatch: if the command is prefixed with `JJ_OVERRIDE=1`, allow it.
#
# Hook wiring lives in settings.json under hooks.PreToolUse. See CLAUDE.md for
# the rationale.

set -euo pipefail

INPUT=$(cat)
COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')
CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // empty')

[[ -z "$COMMAND" ]] && exit 0

# Escape hatch for cases where git is genuinely the right tool.
if [[ "$COMMAND" =~ (^|[[:space:]])JJ_OVERRIDE=1([[:space:]]|$) ]]; then
  exit 0
fi

# Walk tokens, skipping leading env-var assignments, to find the invoked binary.
first_token=""
for tok in $COMMAND; do
  case "$tok" in
    *=*) continue ;;
    *) first_token="$tok"; break ;;
  esac
done
case "$(basename "${first_token:-}" 2>/dev/null)" in
  git) ;;
  *) exit 0 ;;
esac

command -v jj >/dev/null 2>&1 || exit 0

if [[ -z "$CWD" ]] || ! (cd "$CWD" && jj workspace root >/dev/null 2>&1); then
  exit 0
fi

# Extract git subcommand, skipping git's own global flags.
subcmd=""
saw_git=false
skip_next=false
for tok in $COMMAND; do
  if [[ "$skip_next" == true ]]; then skip_next=false; continue; fi
  if [[ "$saw_git" == false ]]; then
    if [[ "$(basename "$tok" 2>/dev/null)" == "git" ]]; then
      saw_git=true
    fi
    continue
  fi
  case "$tok" in
    -c|-C|--git-dir|--work-tree|--namespace|--super-prefix|--exec-path|--config-env)
      skip_next=true; continue ;;
    --git-dir=*|--work-tree=*|--namespace=*|--super-prefix=*|--exec-path=*|--config-env=*)
      continue ;;
    -p|--paginate|-P|--no-pager|--bare|--no-replace-objects|--no-optional-locks|\
    --literal-pathspecs|--glob-pathspecs|--noglob-pathspecs|--icase-pathspecs)
      continue ;;
    --version|--help) subcmd="$tok"; break ;;
    -*) continue ;;
    *) subcmd="$tok"; break ;;
  esac
done

[[ -z "$subcmd" ]] && exit 0

# Read-only or jj-doesn't-support list — always allow.
case "$subcmd" in
  status|log|show|diff|blame|grep|ls-files|ls-tree|ls-remote|cat-file|\
  rev-parse|rev-list|shortlog|reflog|check-ignore|config|help|version|\
  --version|--help|name-rev|for-each-ref|symbolic-ref|show-ref|show-branch|\
  describe|archive|bundle|gc|fsck|count-objects|verify-pack|verify-commit|\
  verify-tag|whatchanged|remote|submodule|lfs|worktree|notes|\
  filter-branch|filter-repo|bisect|daemon|var|check-mailmap|credential|\
  credential-cache|credential-store|credential-osxkeychain|mailinfo|mailsplit|\
  maintenance|prune|pack-objects|pack-refs|repack|update-index|update-ref|\
  write-tree|read-tree|commit-tree|hash-object|mktree|mktag)
    exit 0
    ;;
esac

# Mutating subcommands: block with a targeted hint.
case "$subcmd" in
  commit)
    hint="Use 'jj commit -m \"...\"' (describes @ and starts a fresh change on top) or 'jj describe -m \"...\"' (updates @ in place). For 'git commit --amend', use 'jj squash' to move @ into its parent." ;;
  add)
    hint="jj tracks files automatically — there is no staging step. Just edit files and run 'jj st' to confirm. Use 'jj file untrack <path>' to stop tracking a file." ;;
  rebase)
    hint="Use 'jj rebase -b @ -d <dest>' for the whole branch, or 'jj rebase -s <src> -d <dest>' for a subtree. Conflicts do not stop the rebase — they are recorded in the resulting commits." ;;
  merge)
    hint="Use 'jj new @ <branch>' to create a merge change with both parents." ;;
  reset)
    hint="Use 'jj abandon' to drop a change (reversible via 'jj undo'), 'jj squash --from @-' for a soft-reset equivalent, or 'jj restore <paths>' to discard file changes." ;;
  restore)
    hint="Use 'jj restore <paths>' (same name) to discard working-copy changes, or 'jj restore --from <rev> <paths>' to pull content from another revision." ;;
  checkout|switch)
    hint="Use 'jj new <rev>' to start a new change on top of <rev>, 'jj new <branch>@origin' for a remote branch, or 'jj edit <rev>' to point the working copy at an existing change." ;;
  stash)
    hint="jj has no stash — just start a new change: 'jj new @-' leaves the old change as a sibling you can return to with 'jj edit <change-id>'." ;;
  cherry-pick)
    hint="Use 'jj duplicate <rev> --destination @' to copy a change onto the current one." ;;
  revert)
    hint="Use 'jj revert -r <rev> -B @' to create a revert change before @." ;;
  push)
    hint="Use 'jj git push' (pushes tracked bookmarks) or 'jj git push --bookmark <name>'. 'jj git push -c @' auto-creates a bookmark at @ and pushes it." ;;
  pull)
    hint="jj has no pull. Run 'jj git fetch', then rebase onto the updated remote: 'jj rebase -d <branch>@origin'." ;;
  fetch)
    hint="Use 'jj git fetch' (add '--all-remotes' to fetch every remote)." ;;
  clone)
    hint="Use 'jj git clone <url>' (add '--colocate' if you also need git tooling in the clone)." ;;
  init)
    hint="Use 'jj git init --colocate' to adopt an existing git repo (or start a fresh one). Full adoption: 'jj git init --colocate' → append '.jj/' to .gitignore with a teammate-friendly comment (see jj skill) → 'jj bookmark track main --remote=origin' → 'jj commit -m \"chore: gitignore .jj/ (jujutsu local state)\"' → 'jj bookmark set main -r @-' → 'jj git push'. Alternative: add '.jj/' to the global gitignore (\$HOME/.config/git/ignore) once and skip the repo change entirely." ;;
  branch)
    hint="jj uses bookmarks. 'jj bookmark list', 'jj bookmark create <name> -r <rev>', 'jj bookmark set <name> -r <rev>' (move), 'jj bookmark delete <name>'." ;;
  tag)
    hint="Use 'jj tag set <name> -r <rev>' to create, 'jj tag list' to list, 'jj tag delete <name>' to delete." ;;
  mv|rm)
    hint="jj tracks files automatically — use plain 'mv' or 'rm' and jj will pick up the change on the next command." ;;
  clean)
    hint="jj has no index, so there is nothing to clean. Use plain 'rm' or your shell to remove untracked files." ;;
  apply|am|format-patch|cherry)
    hint="Apply patches by editing files directly inside a 'jj new' change, then 'jj describe -m \"...\"'. For mailbox flows jj has no direct equivalent — if you truly need this, re-run with 'JJ_OVERRIDE=1 git $subcmd ...'." ;;
  *)
    exit 0 ;;
esac

cat >&2 <<EOF
Blocked 'git $subcmd' — this repo is jj-managed; prefer jj over git.

→ $hint

If jj genuinely cannot do what you need (e.g. signed push to a protected
branch, LFS, git submodules, .gitattributes, git hooks), re-run the same
command prefixed with 'JJ_OVERRIDE=1' and it will pass through.

If you are unsure which jj command to use, load the jj skill via /jj or ask
about jj workflows — the skill covers the full git→jj translation, common
workflows, and git interop gotchas.
EOF
exit 2
