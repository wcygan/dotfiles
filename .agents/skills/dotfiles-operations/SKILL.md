---
name: dotfiles-operations
description: "Operate, maintain, upgrade, troubleshoot, and review this dotfiles repository. Use for architecture questions, installation and verification, interrupted setup recovery, Nix/profile maintenance, managed links, Rust pins, CI workflows, Docker or macOS acceptance, documentation operations, and repository-wide setup changes."
---

# Dotfiles Operations

## Outcome

Keep this repository's Nix-backed setup path reproducible, recoverable, and
portable while preserving the repo-driven configuration model.

Success means the requested operation uses the supported entry point, respects
state and authority boundaries, runs validation proportional to its blast
radius, and reports both evidence and residual risk.

## Start Here

1. Read the nearest `AGENTS.md` and inspect `git status --short`.
2. Read [references/architecture.md](references/architecture.md) for component
   boundaries, state ownership, and the install sequence.
3. Read the relevant section of
   [references/operations.md](references/operations.md) before mutating or
   diagnosing setup state.
4. Read [references/migrations.md](references/migrations.md) before changing a
   compatibility guarantee, restoring retired behavior, or making a breaking
   setup change.
5. For reusable-skill source, pin, installation, verification, collision, or
   recovery work, also read `$agent-skills-integration` before acting.
6. Recheck current repository files and live state. The references describe the
   intended architecture; `bootstrap.sh`, `Makefile`, `flake.nix`,
   `src/dotfiles_setup/**`, and `.github/workflows/**` remain authoritative.

## Operating Rules

- Use `./bootstrap.sh` as the only root setup entry point. Do not add another
  installer or restore retired setup scripts.
- Keep configuration under `config/**`, package selection in `flake.nix`, and
  operational behavior in focused modules under `src/dotfiles_setup/**`.
- Keep the default install free of Bash/zsh startup-file changes. Shell handoff
  is explicit through `--shell-handoff` or `shell-handoff`.
- Treat `doctor` as advisory and `verify` as the strict, read-only acceptance
  contract. Never weaken `verify` to accommodate a broken install.
- Preserve exact checkout identity: profile acceptance must match the resolved
  local origin, not an element name or ambient `PATH`.
- Preserve lockfile discipline. Consumer commands use committed locks without
  rewriting them; only explicit update workflows may change a lockfile.
- Record intentional breaking changes in `references/migrations.md` and add
  focused migration tests.
- Preserve the per-user mutation lock, preflight, operation journal, atomic
  replacements, and guarded recovery protocol for every managed mutation.
- Do not put credentials, machine-local Codex state, Git identity values, file
  contents, or secret-bearing diagnostics in manifests, tests, or CI logs.
- Preserve macOS, Ubuntu, Fedora, and Linux/WSL behavior. Do not infer macOS
  acceptance from Linux or Docker evidence.
- Preserve unrelated worktree changes. Do not stage, commit, push, deploy, pull,
  update locks, install Nix, apply recovery, or change shell startup files
  without authority for that action.

## Request Routing

Use this skill for the repository-wide operating model, then route specialized
work when appropriate:

- Nix package-set update: use `$nix-update` for the lock update and version
  comparison; use `$nix-manager` for Nix mechanics.
- Cross-platform/bootstrap change: also use `$cross-platform-guardian`.
- Fish, Ghostty, Neovim, Starship, Zed, Zellij, or lazygit config: route through
  `$config-change` and the matching focused skill.
- Dotfiles-local skill design: use `$brainstorm-skills`.
- Reusable/global skill source, catalog pin, installation, verification,
  collision, or recovery: use `$agent-skills-integration`. Keep source in the
  authoritative `agent-skills` repository and consume it here through the
  pinned GitHub CLI integration.

## Standard Workflow

1. Classify the request as read-only diagnosis, installation, configuration,
   dependency update, recovery, CI maintenance, or cleanup.
2. Inspect the authoritative files and the exact live state in scope. For setup
   incidents, begin with:

   ```bash
   git status --short
   ./bootstrap.sh doctor
   ./bootstrap.sh verify
   ./bootstrap.sh recover
   nix profile list --json
   ```

3. Select the smallest supported command or code change. Preview links and
   cleanup where available before applying them.
4. For code changes, update focused pytest coverage and repository-policy tests
   when changing a cross-file invariant.
5. Run the narrow validation first, then expand according to the matrix in the
   operations reference.
6. Confirm relevant lockfiles and tracked inputs did not change unexpectedly:

   ```bash
   git diff --exit-code -- flake.lock uv.lock
   git diff --check
   git status --short
   ```

7. Report changed interfaces, commands run, platform evidence, skipped checks,
   recovery or rollback path, residual risks, Git state, and whether anything
   was published.

## Stop Conditions

Stop and explain the next safe action when:

- recovery is pending and the current destination no longer matches the
  recorded interrupted operation;
- another mutating setup process owns the per-user lock;
- strict verification identifies a profile from another checkout;
- a requested mutation crosses `HOME`, the managed inventory, or the stated
  authority boundary;
- a lock update, Nix installation, shell handoff, recovery apply, Git pull,
  push, deployment, or destructive cleanup lacks explicit authorization;
- platform evidence is unavailable for a platform-sensitive change.
