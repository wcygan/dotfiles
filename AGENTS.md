# AGENTS.md

## Mission

Provide reproducible tools with Nix and portable, editable configuration through
repository-owned links. Keep Home Manager out of scope and preserve fast
onboarding, deterministic CI, and straightforward rollback.

## Route Before Acting

- **Repository operations:** You **must** use `$dotfiles-operations` for setup,
  installation, verification, recovery, Nix/profile maintenance, managed links,
  CI, Docker, macOS acceptance, or repository-wide changes. Read its relevant
  references before acting; keep it active alongside every more specific route.
- **Agent skills:** For reusable-skill source, catalog pins, user-scope
  installation, verification, collisions, stale copies, or recovery, you
  **must** also use `$agent-skills-integration`.
- **Application configuration:** Route Fish, Ghostty, lazygit, Neovim,
  Starship, Zed, and Zellij changes through `$config-change` and its selected
  focused skill. Edit the repository source in `config/**`; change a host
  destination only through the managed-link workflow.
- **Nix input updates:** Use `$nix-update` for any `flake.lock` update; use
  `$nix-manager` for Nix mechanics. A package-list change is not an input update.

When more than one route applies, use every matching skill. Do not replace the
repository-operation contract with a focused configuration or provider skill.

## Invariants

- `bootstrap.sh` is the only root setup shell entry point; operational behavior
  lives in focused modules under `src/dotfiles_setup/**`.
- Packages live in `flake.nix`, portable configuration in `config/**`, and
  managed-destination inventory in `src/dotfiles_setup/links.py`. Project-only
  skills live in `.agents/skills/**`; reusable skill source belongs in
  `wcygan/agent-skills` and is consumed here only through its exact lock.
- Setup is idempotent and preserves macOS, Ubuntu, Fedora, and Linux/WSL.
  Platform-sensitive work requires evidence from the affected platform; Linux
  or Docker results do not establish macOS compatibility.
- Normal consumers preserve committed lockfiles. Only an explicit update task
  may change `flake.lock`, `uv.lock`, `rust-toolchain.toml`, or
  `agent-skills.lock.toml`.
- Secrets, credentials, Git identity values, and mutable application state stay
  machine-local. Repository paths and behavior remain portable across machines.
- Breaking changes require focused tests and an entry in
  `.agents/skills/dotfiles-operations/references/migrations.md`.

## Change Contract

1. Inspect the nearest instructions, `git status --short`, authoritative source,
   and live state relevant to the request before changing anything.
2. Preserve unrelated work and change only the owning layer. Use a repository
   source plus its supported operation instead of repairing a machine-local
   destination directly.
3. Run the narrowest focused check first, then every applicable gate in the
   `$dotfiles-operations` validation matrix.
4. Finish only when every changed invariant has evidence, unexpected lockfile
   changes are absent, recovery state is understood, and the handoff reports
   residual risk plus commit, push, and deployment status.

## References

- Nix installation and per-project nix-direnv usage: `README.md`; Nix mechanics:
  `$nix-manager`.
- Fish functions, aliases, and abbreviations: `$fish-shell-config`.
