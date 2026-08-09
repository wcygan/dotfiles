# AGENTS.md

## Mission

Reproducible tools with Nix; portable, editable configs via symlinks; fast onboarding and deterministic CI. Do **not** migrate dotfiles to Home Manager; keep them repo-driven and linked into `~/.config`.

## Principles

* **Idempotent**: every script safe to run twice.
* **Cross‑platform**: macOS, Ubuntu, Fedora all green. CI runs Linux only (cost); macOS compatibility is verified ad-hoc on the maintainer's machine.
* **Minimal surface area**: configs live under `config/**`; packages live in `flake.nix`.
* **Test-first ops**: pre-flight (local) → isolated (ephemeral HOME) → Docker matrix. macOS-specific changes: run `make test-pre` (and `make test-local` if touching fish) on a Mac before merging.
* **Rollbackable**: links backed up, package generations garbage-collectable.

## Authority & Guardrails

**You may** edit: `flake.nix`, `scripts/*.sh`, `config/**`, `Makefile`, `README.md`, `AGENTS.md`, `tests/**`, CI workflows.

**You must not**: commit secrets, hard-code machine paths, or regress OS coverage.

**Breaking changes**: require a migration note in this file and a `tests/` update.

## Decision Tree

* **Need a tool?** Add it to `flake.nix` → `nix profile install .`.
* **Need a config?** Add under `config/**` → wire in `scripts/link-config.sh`.
  * Only symlink to `~/.config/` for XDG-compliant programs (fish, starship, zed). Legacy programs like tmux expect `~/.tmux.conf` — check before symlinking.
* **Need per-project dev environment?** Use the nix-direnv pattern — see README.md.
* **Need a dotfiles operating skill?** Add it under `.agents/skills/` so it is project-local and versioned with this repository.
* **Need a reusable agent skill?** Own it in the dedicated `agent-skills` repository. Keep Pi credentials, sessions, models, and other runtime state machine-local.
* **Unsure?** Prefer plain files + symlinks over bespoke derivations.

## Workflow

1. Branch `feat/<slug>` or `fix/<slug>`.
2. Make the smallest change that passes `make test-pre` locally.
3. If touching fish, run `make test-local` (ephemeral HOME) and `make test-docker` if available.
4. Open PR with: scope/motivation, screens/logs of tests, rollback plan.
5. Merge only when CI *summary* job is ✅.

Rollback: re-link configs (script backs up physical dirs), or `nix profile rollback` if a package regressed.

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
