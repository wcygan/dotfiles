# AGENTS.md

## Mission

Reproducible tools with Nix; portable, editable configs via symlinks; fast onboarding and deterministic CI. Do **not** migrate dotfiles to Home Manager; keep them repo-driven and linked into `~/.config`.

## Principles

* **Idempotent**: every script safe to run twice.
* **Cross‑platform**: macOS, Ubuntu, Fedora all green. CI runs Linux only (cost); macOS compatibility is verified ad-hoc on the maintainer's machine.
* **Minimal surface area**: configs live under `config/**`; packages live in `flake.nix`.
* **Test-first ops**: `make test-pre` (locked Ruff + pytest) → `make test-local` (ephemeral HOME) → `make test-shell` → `make test-docker` (Ubuntu/Fedora driver). macOS-specific changes: run the relevant non-Docker checks on a Mac before merging.
* **Rollbackable**: links backed up, package generations garbage-collectable.
* **Minimal shell bridge**: `bootstrap.sh` is the only root setup shell entry point. Shell helpers under `.agents/skills/**/scripts` are project-local skill implementation details, not installation entry points.

## Authority & Guardrails

**You may** edit: `bootstrap.sh`, `flake.nix`, `pyproject.toml`, `uv.lock`, `src/dotfiles_setup/**`, `config/**`, `Makefile`, `README.md`, `AGENTS.md`, `tests/**`, CI workflows.

**You must not**: commit secrets, hard-code machine paths, or regress OS coverage.

**Breaking changes**: require a migration note in this file and a `tests/` update.

## Decision Tree

* **Need a tool?** Add it to `flake.nix` → `./bootstrap.sh profile` (or `make profile`).
* **Need a config?** Add under `config/**` → wire it into `src/dotfiles_setup/links.py`.
  * Only symlink to `~/.config/` for XDG-compliant programs (fish, starship, zed). Legacy programs like tmux expect `~/.tmux.conf` — check before symlinking.
* **Need per-project dev environment?** Use the nix-direnv pattern — see README.md.
* **Need a dotfiles operating skill?** Add it under `.agents/skills/` so it is project-local and versioned with this repository.
* **Need a reusable agent skill?** Own it in the dedicated `agent-skills` repository. Keep Pi credentials, sessions, models, and other runtime state machine-local.
* **Unsure?** Prefer plain files + symlinks over bespoke derivations.

## Workflow

1. Branch `feat/<slug>` or `fix/<slug>`.
2. Make the smallest change that passes `make test-pre` locally.
3. Run the relevant focused suite (`make test-local` for links, `make test-shell` for handoff); use `make test-docker` for cross-platform changes.
4. Open PR with: scope/motivation, screens/logs of tests, rollback plan.
5. Merge only when CI *summary* job is ✅.

Rollback: rerun `./bootstrap.sh link` (managed links back up physical paths), or use `nix profile rollback` if a package regressed. Keep a known-good Git tag before a broader config migration.

## Quality Bar (PR Checklist)

* [ ] Idempotent (re-run safe)
* [ ] Cross‑platform verified — Linux via CI; macOS locally when the change could be platform-sensitive (shell init, paths, package availability)
* [ ] Tests updated (pre-flight + relevant suite)
* [ ] Docs updated (README/AGENTS)
* [ ] Rollback path obvious

## Contributor Playbooks

**Add a CLI tool + shortcut**: add package to `flake.nix`; add alias/abbr in `40-aliases.fish` guarded with `type -q <tool>`; extend tests; run `make test-pre` then `make test-local`.

**Bump package set**: `make update`; verify with `make test-pre && make test-local`; push and let the CI matrix run.

**Add a fish function**: create `config/fish/functions/<name>.fish`; reference in docs; add a small test if relevant.

## Pointers

* **Nix install / dev environments tutorial** → `README.md`
* **Fish aliases & abbreviations policy** → `fish-aliases-policy` skill
* **nix-direnv perf, concurrent rebuilds, Nix daemon troubleshooting** → `nix-direnv-perf` skill

## Migrations

* **2026-08-08 — Retire global agent-skill installation**: this repository no longer links or validates Codex skills, custom agents, or Claude configuration, and it does not install global agent skills. Dotfiles-specific operating skills live under `.agents/skills/`; reusable skills belong in the dedicated `agent-skills` repository.
* **2026-08-09 — Python setup migration**: `bootstrap.sh` is the supported setup entry point. It obtains Nix when explicitly authorized on Linux/WSL, enters `nix develop`, and runs `uv run --locked python -m dotfiles_setup`. The default `install` workflow does not alter Bash/zsh startup files; use `install --shell-handoff` or the separate `shell-handoff` command to opt in. Do not restore the retired shell setup path; update Python tests and the applicable Make targets for breaking changes.
* **2026-08-09 — Strict verification contract**: `doctor` is advisory and exits successfully after reporting host or not-yet-installed warnings. `verify` is strict, read-only post-installation acceptance, and `install` runs it last. Automation that previously used `verify` as an ambient development-shell health check must use `doctor` instead.
* **2026-08-09 — Transactional setup boundary**: mutating setup commands are serialized by a fail-fast per-user lock and write a content-free operation manifest under XDG state. Link, npm, Codex-template, and shell-file mutations are journaled and atomic, and an interrupted operation blocks later mutations until `./bootstrap.sh recover` is inspected. Applying recovery requires `recover --apply --yes`; doctor, verify, dry runs, and recovery inspection remain lock-free. Install now runs link and Rust setup serially so the manifest describes one deterministic mutation order. Shell startup-file and `.npmrc` symlink referents outside `HOME` are rejected rather than modified.
* **2026-08-09 — Canonical CI acceptance**: Linux CI invokes repository Make targets for locked quality, syntax, four-system evaluation, and the Docker runtime matrix. Docker acceptance is owned by `tests/docker_matrix.py`; the retired Fish counter script must not be restored. Docs build on pull requests but deploy only from `main`, while native macOS arm64 runs weekly/manual and Intel runs manually. Keep every workflow bounded, least-privilege, SHA-pinned, report-retaining, and cleanliness-checking.
