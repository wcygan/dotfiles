# Migration History

Read this reference before changing compatibility guarantees, restoring retired
behavior, or replacing a setup boundary. Add an entry when a breaking change is
intentional, alongside focused migration tests.

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
