# Migration History

Read this reference before changing compatibility guarantees, restoring retired
behavior, or replacing a setup boundary. Add an entry when a breaking change is
intentional, alongside focused migration tests.

## 2026-08-29 — Require physical destination parents and no-replace renames

Managed mutations now validate every destination parent through a descriptor
walk. A symlinked ancestor of a managed destination, such as a synced
`~/.config`, fails with an unsafe-parent error. Replace the symlink with a
real directory before you install.

Atomic replacement now uses no-replace renames. Linux needs `renameat2` with
`RENAME_NOREPLACE` filesystem support. macOS needs `renameatx_np`. A
filesystem without support fails with `ENOTSUP`. Move the managed
destinations to a filesystem with no-replace support.

Created directories now install with mode `0755` by default; a caller may
declare a stricter mode. The transactional rewrite had created
`~/.local/bin` and `~/.local/lib` with mode `0700`. Replace those
directories if the restrictive mode matters to you.

## 2026-08-29 — Reject inactive checkout profile elements

Profile setup now upgrades only an active element from the current checkout.
If the matching element is inactive, remove it with `nix profile remove NAME`.
Then run `./bootstrap.sh profile` to add a new active element. This prevents an
inactive profile record from hiding the active installation state.

## 2026-08-29 — Retain verified legacy skill quarantines

Legacy skill cleanup now moves each accepted tree to a hidden quarantine in
the same directory. It does not delete the accepted contents. Inspect the
reported paths after cleanup. Move retained trees to the platform trash only
after the shared catalog passes `./bootstrap.sh agent-skills --check`.

## 2026-08-10 — Move global instructions to shared agent configuration

`config/agents/AGENTS.md` is now the authoritative global instruction source.
The managed inventory links it to both `~/.agents/AGENTS.md` and
`${CODEX_HOME:-~/.codex}/AGENTS.md`, deduplicating the destination when
`CODEX_HOME` is `~/.agents`. `config/codex/AGENTS.md` remains a compatibility
link, while `config/codex/config.toml` retains its machine-local template
behavior. Existing physical destinations continue to use the standard backup
before replacement.

## 2026-08-08 — Retire the dotfiles-owned global skill catalog

The repository stopped linking or validating its former Codex skill catalog,
custom agents, and Claude configuration. Dotfiles-specific operating skills
remain under `.agents/skills/`; reusable source moved to the dedicated
`agent-skills` repository.

## 2026-08-09 — Consume a pinned external agent-skill catalog

The explicit `./bootstrap.sh agent-skills` command consumes
`agent-skills.lock.toml`, uses `gh skill install` for Codex user scope, refuses
conflicting same-name skills, and verifies source plus pin. Installed copies and
GitHub CLI tracking state are machine-local. The command remains outside the
default install, and skills removed upstream require separate review because
GitHub CLI does not prune them.

## 2026-08-09 — Move the shared catalog to the Agent Skills user directory

GitHub CLI's Codex host profile still maps user installs to `~/.codex/skills`,
but Codex now documents `~/.agents/skills` as the shared user discovery root.
The consumer lock moved to schema version 2 with a portable relative directory,
and the installer now supplies that directory with `gh skill install --dir` and
verifies it with `gh skill list --dir`. A guarded, explicit legacy cleanup is
available only after the shared catalog verifies. It quarantines exact matching
legacy copies and does not prune foreign or stale skills.

## 2026-08-09 — Replace setup orchestration with Python

`bootstrap.sh` became the supported setup entry point. It obtains Nix only when
explicitly authorized on Linux/WSL, enters `nix develop`, and runs `uv run
--locked python -m dotfiles_setup`. The default install leaves Bash and zsh
startup files unchanged; shell handoff is explicit.

## 2026-08-09 — Separate advisory and strict verification

`doctor` is advisory and exits successfully after reporting host or
not-yet-installed warnings. `verify` is strict, read-only post-installation
acceptance, and `install` runs it last. Ambient development-shell health checks
use `doctor`.

## 2026-08-09 — Add the transactional setup boundary

Mutating setup commands are serialized by a fail-fast per-user lock and write a
content-free operation manifest under XDG state. Link, npm, Codex-template, and
shell-file changes are journaled and atomic. Interrupted operations block later
mutations until recovery is inspected; applying recovery requires `--apply
--yes`. External profile and agent-skill state is inspected and acknowledged,
not automatically reversed.

## 2026-08-09 — Make repository targets canonical CI acceptance

Linux CI invokes repository Make targets for locked quality, syntax,
four-system evaluation, and the Docker runtime matrix. Documentation builds on
pull requests and deploys only from `main`. Native Apple Silicon runs weekly or
manually; Intel macOS runs manually. Workflows remain bounded, least-privilege,
SHA-pinned, report-retaining, and cleanliness-checking.
