---
name: refresh-agent-skills
description: "Refresh the pinned wcygan/agent-skills catalog for this dotfiles checkout, install it into Codex user scope, verify every skill and path, and optionally commit and push the update. Use when asked to update, refresh, reinstall, reconcile, or publish the project's agent skills."
license: MIT
metadata:
  author: wcygan
  version: "0.1.0"
---

# Refresh Agent Skills

Update the repository's pinned reusable-skill catalog and reconcile the local
Codex installation. Keep wcygan/agent-skills as the source of truth and use
the dotfiles bootstrap command as the only consumer-side installer.

## Completion contract

The task is complete only when all of these are true:

- agent-skills.lock.toml contains the reviewed full 40-character lowercase
  commit and portable shared-user directory for wcygan/agent-skills.
- ./bootstrap.sh agent-skills succeeds and reports the installed count and
  destination.
- ./bootstrap.sh agent-skills --check and make agent-skills-check pass.
- gh skill list --dir "$HOME/.agents/skills" reports one source, scope=custom,
  pinned=true, the exact locked version, and one shared user destination for
  every provider skill.
- No provider skill disappeared without a stale-local review.
- make test-pre, git diff --check, and the tracked-lockfile check pass.
- Commit and push happen only when the invocation explicitly asks to publish.

## Boundaries

- Work from /Users/wcygan/Development/dotfiles (or the current checkout
  containing bootstrap.sh and agent-skills.lock.toml).
- Read the nearest AGENTS.md, .agents/skills/dotfiles-operations, and
  .agents/skills/agent-skills-integration before changing state.
- Change only the consumer integration and its focused tests and documentation.
  Do not copy provider files into dotfiles.
- Preserve unrelated worktree changes. Stage named files only.
- Keep installed skills and ~/.agents/.skill-lock.json machine-local.
- Do not run the full dotfiles install, alter Nix inputs, change shell startup
  files, prune stale skills, or publish a branch unless separately requested.

## Workflow

### 1. Inspect state and resolve the provider commit

Start with repository and provider status. The provider checkout is useful for
review, but it is not a second source or installation implementation.

~~~bash
git status --short
git -C ../agent-skills status --short 2>/dev/null || true
sed -n '1,40p' agent-skills.lock.toml
gh skill list --dir "$HOME/.agents/skills" \
  --json skillName,sourceURL,scope,version,pinned,path
~~~

Resolve `origin/main` from the live GitHub remote on every run. Do not use the
local `../agent-skills` checkout, its current branch, or the existing lock as
the latest-version oracle:

~~~bash
remote_refs="$(git ls-remote \
  https://github.com/wcygan/agent-skills.git refs/heads/main)" || exit
if [ "$(printf '%s\n' "$remote_refs" | awk 'NF == 2 { count++ } END { print count + 0 }')" -ne 1 ]; then
  printf '%s\n' "expected exactly one origin/main ref" >&2
  exit 1
fi
latest_sha="$(printf '%s\n' "$remote_refs" | awk 'NR == 1 { print $1 }')"
if ! printf '%s\n' "$latest_sha" | grep -Eq '^[0-9a-f]{40}$'; then
  printf '%s\n' "origin/main did not return a full lowercase SHA" >&2
  exit 1
fi
printf '%s\n' "$latest_sha"
~~~

Require exactly one 40-character lowercase hexadecimal SHA from that command.
If the remote cannot be resolved, or returns no or multiple refs, stop and
report the network/authentication failure. Do not guess a tag, branch, or
abbreviated SHA. If the locked commit equals `latest_sha`, keep the lock
unchanged and continue with install/reconcile. Otherwise replace the lock with
`latest_sha` before discovering or installing the catalog.

Review the provider delta before pinning when a provider checkout is present:

~~~bash
git -C ../agent-skills diff --stat \
  "$(sed -n 's/^commit = "\([0-9a-f]\{40\}\)"$/\1/p' agent-skills.lock.toml)..$latest_sha"
git -C ../agent-skills log --oneline --decorate \
  "$(sed -n 's/^commit = "\([0-9a-f]\{40\}\)"$/\1/p' agent-skills.lock.toml)..$latest_sha"
~~~

### 2. Advance only the consumer pin

Use apply_patch to replace only the commit = "..." line in
agent-skills.lock.toml. If tests/test_agent_skills.py contains a hard-coded
fixture commit, update that fixture to the same full SHA; do not alter the
test's behavior or other files.

Then inspect the diff:

~~~bash
git diff -- agent-skills.lock.toml tests/test_agent_skills.py
git diff --check
~~~

### 3. Review inventory and stale names

The bootstrap installer rejects duplicate or foreign-source collisions. Before
using it, inspect the current inventory and, when possible, compare it with
the provider tree:

~~~bash
gh skill list --dir "$HOME/.agents/skills" \
  --json skillName,sourceURL,scope,version,pinned,path

find ../agent-skills/skills -mindepth 2 -maxdepth 2 -name SKILL.md \
  -print 2>/dev/null | sort
~~~

gh skill install does not prove that removed upstream skills are pruned.
If the provider tree is available, identify installed names absent from that
tree and report them. Do not delete them automatically; removal is a separate
user-authorized cleanup.

### 4. Install through the supported boundary

Run the focused, journaled mutation only:

~~~bash
./bootstrap.sh agent-skills
~~~

Record the reported catalog count and the actual destination. The expected
command uses --dir "$HOME/.agents/skills" --all --pin <full-sha> internally;
do not replace it with a clone, copy, symlink, or direct write to the shared
directory.

### 5. Verify the installation

Run both the strict read-only check and the Make target:

~~~bash
./bootstrap.sh agent-skills --check
make agent-skills-check
~~~

Run this normalized audit so timestamps in GitHub CLI tracking state cannot
mask an inventory or metadata problem:

~~~bash
python3 - <<'PY'
import json
import subprocess
from pathlib import Path
import tomllib

with open("agent-skills.lock.toml", "rb") as f:
    lock = tomllib.load(f)
inventory = json.loads(subprocess.check_output([
    "gh", "skill", "list", "--dir",
    str(Path.home() / lock["directory"]),
    "--json", "skillName,sourceURL,scope,version,pinned,path",
], text=True))

names = [item["skillName"] for item in inventory]
assert len(names) == len(set(names)), "duplicate installed skill names"
assert {item["sourceURL"] for item in inventory} == {
    f"https://github.com/{lock['repository']}"
}
assert {item["scope"] for item in inventory} == {"custom"}
assert {item["version"] for item in inventory} == {lock["commit"]}
assert all(item["pinned"] is True for item in inventory)
parents = {str(Path(item["path"]).resolve().parent) for item in inventory}
assert len(parents) == 1, parents
print(f"verified {len(inventory)} skills at {next(iter(parents))}")
PY
~~~

If the provider checkout is available, validate its source as an additional
provider-side check:

~~~bash
for skill_dir in ../agent-skills/skills/*; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  uv tool run --from skills-ref agentskills validate "$skill_dir" || exit 1
done
gh skill publish --dry-run
~~~

Warnings from the provider's dry run are reportable; validation errors are
blocking.

### 6. Run repository acceptance

~~~bash
make test-pre
git diff --check
git diff --exit-code -- flake.lock uv.lock
git status --short
./bootstrap.sh recover
~~~

recover must report that no interrupted dotfiles operation needs recovery.
Linux, Docker, or evaluation-only results do not establish macOS acceptance;
record the actual platform used.

### 7. Commit and push only in publish mode

When the user explicitly requested commit/push, first confirm the diff contains
only the lock/test expectation and this skill. Stage paths explicitly:

~~~bash
git diff --name-only
git add agent-skills.lock.toml src/dotfiles_setup/agent_skills.py \
  src/dotfiles_setup/cli.py tests/test_agent_skills.py Makefile \
  .agents/skills/agent-skills-integration/SKILL.md \
  .agents/skills/dotfiles-operations/references/{architecture.md,operations.md,migrations.md} \
  .agents/skills/refresh-agent-skills/SKILL.md
git diff --cached --check
git diff --cached --stat
git commit -m "chore(skills): refresh pinned agent skills"
git push origin "$(git branch --show-current)"
~~~
If the pin was unchanged and the skill file is the only change, use a concise
skill-specific commit subject instead. Do not create an empty commit. After a
successful push, report the commit SHA, branch, provider SHA, catalog count,
destination, checks, stale-name review, and any provider warnings.

## Quick cheatsheet

~~~bash
# Resolve the live provider origin/main on every refresh
remote_refs="$(git ls-remote https://github.com/wcygan/agent-skills.git \
  refs/heads/main)" || exit
test "$(printf '%s\n' "$remote_refs" | awk 'NF == 2 { count++ } END { print count + 0 }')" -eq 1
latest_sha="$(printf '%s\n' "$remote_refs" | awk 'NR == 1 { print $1 }')"
printf '%s\n' "$latest_sha" | grep -Eq '^[0-9a-f]{40}$' || exit 1

# Update only agent-skills.lock.toml's commit line with apply_patch

# Reconcile the pinned Codex catalog
./bootstrap.sh agent-skills

# Read-only verification
./bootstrap.sh agent-skills --check
make agent-skills-check

# Full repository gate
make test-pre
git diff --check
git diff --exit-code -- flake.lock uv.lock

# Publish only when explicitly requested
git add agent-skills.lock.toml src/dotfiles_setup/agent_skills.py \
  src/dotfiles_setup/cli.py tests/test_agent_skills.py Makefile \
  .agents/skills/agent-skills-integration/SKILL.md \
  .agents/skills/dotfiles-operations/references/{architecture.md,operations.md,migrations.md} \
  .agents/skills/refresh-agent-skills/SKILL.md
git commit -m "chore(skills): refresh pinned agent skills"
git push origin "$(git branch --show-current)"
~~~
