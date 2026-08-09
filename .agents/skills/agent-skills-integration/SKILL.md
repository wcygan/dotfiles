---
name: agent-skills-integration
description: "Maintain the pinned agent-skills provider/consumer integration. Use when changing the external skill repository or pin, installing or verifying the Codex user catalog, troubleshooting skill collisions or recovery, or changing the dotfiles integration contract."
---

# Agent Skills Integration

## Outcome

Preserve one explicit boundary for reusable skills:

```text
wcygan/agent-skills       dotfiles                     GitHub CLI / Codex
source and validation -> exact consumer lock       -> machine-local user copies
                           supported orchestration     and tracking state
```

Success means reusable skill source remains in `wcygan/agent-skills`, this
repository consumes one reviewed commit through `agent-skills.lock.toml`, and
GitHub CLI installs and reports the complete Codex user-scope catalog at that
exact commit.

## Ownership Contract

- The `agent-skills` repository owns reusable skill contents, dependencies,
  packaging, and provider-side validation.
- This repository owns only the external repository identifier, immutable
  commit pin, supported command, collision policy, recovery boundary, and
  consumer-side verification.
- GitHub CLI owns fetching, installing, and tracking machine-local copies.
  Derive their destination from `gh skill list`; do not encode a CLI-specific
  installation path in implementation logic.
- Project-specific operating skills remain under `.agents/skills/` here and
  are not part of the global catalog.

## Invariants

- Pin a full lowercase 40-character commit SHA. Mutable branches, tags, and
  abbreviated SHAs are not an installation contract.
- Invoke `gh skill install` with `--agent codex --scope user --all --pin`.
  Keep catalog discovery and installation in GitHub CLI instead of adding a
  second clone, copy, vendoring, or synchronization implementation.
- Keep installation explicit through `./bootstrap.sh agent-skills`; the default
  dotfiles install does not mutate the global skill catalog.
- Serialize and journal installation as a dotfiles mutation. Keep
  `./bootstrap.sh agent-skills --check` read-only and lock-free.
- Refuse same-name user skills from another source or duplicate user-scope
  locations before using `--force`.
- Verify every expected skill's source, scope, pinned flag, exact version, and
  installed path after installation.
- Keep installed copies and GitHub CLI tracking state untracked and
  machine-local. Never write credentials or remote contents to the operation
  journal.
- Judge unchanged reruns by durable catalog state. Because installation uses
  `--force`, GitHub CLI refreshes `updatedAt` for managed entries in
  `~/.agents/.skill-lock.json` even when source, pin, paths, and contents are
  unchanged. A timestamp-only tracking diff is expected; any inventory,
  duplicate-name, source, scope, pin, path, or file-content change is not.
- Treat removal separately when advancing a pin: GitHub CLI installation does
  not prove that skills removed upstream were pruned locally.

## Workflow

1. Read `agent-skills.lock.toml`, `src/dotfiles_setup/agent_skills.py`, the
   `agent-skills` CLI branch in `src/dotfiles_setup/cli.py`, recovery handling,
   focused tests, and the pinned-skills section of the operations runbook.
2. Inspect `git status --short` in both repositories and inspect the live user
   inventory with `gh skill list --agent codex --scope user --json
   skillName,sourceURL,scope,version,pinned,path`.
3. Classify the change:
   - author or modify a reusable skill in `wcygan/agent-skills`;
   - advance the dotfiles consumer pin after reviewing the provider change;
   - install, reconcile, or verify the currently pinned catalog;
   - change the consumer integration, collision rules, or recovery behavior;
   - explicitly review stale local skills removed from the provider catalog.
4. Make the change only in the owning layer. A provider-source change does not
   belong in dotfiles, and a consumer pin or setup-policy change does not belong
   in the provider repository.
5. For a pin advance, use the reviewed provider commit's full SHA, update only
   `agent-skills.lock.toml`, run the explicit installer, then run the read-only
   check. Inspect removed or renamed skills before any cleanup.
6. For integration code changes, preserve the root `bootstrap.sh` entry point,
   mutation journal, recovery behavior, and metadata-based verification; add
   focused tests for each changed invariant.

## Acceptance

Run the narrow checks first, then the repository gate appropriate to the
change:

```bash
uv tool run --from skills-ref agentskills validate \
  .agents/skills/agent-skills-integration
make agent-skills-check
make test-pre
git diff --check
git diff --exit-code -- flake.lock uv.lock
git status --short
```

For a live installation or pin advance, also confirm that `gh skill list`
reports one source, one exact version, `scope=user`, and `pinned=true` for the
complete expected catalog. For an unchanged rerun, compare the normalized
inventory and installed file contents; do not use the raw tracking-lock digest
as the idempotency oracle. For Python setup or recovery changes, follow the
broader setup validation matrix in `$dotfiles-operations`.

Report the provider commit, catalog count, actual destination reported by
GitHub CLI, validation evidence, stale-skill review, recovery state, worktree
state, and whether either repository was committed or published.
