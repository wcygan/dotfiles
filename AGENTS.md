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
  Rex, Starship, Zed, and Zellij changes through `$config-change` and its selected
  focused skill. Edit the repository source in `config/**`; change a host
  destination only through the managed-link workflow.
- **Nix input updates:** Use `$nix-update` for any `flake.lock` update; use
  `$nix-manager` for Nix mechanics. A package-list change is not an input update.
- **User questions:** Use `request_user_input` for structured questions when the tool is available.

When more than one route applies, use every matching skill. Do not replace the
repository-operation contract with a focused configuration or provider skill.

## Agent skills: ownership and flow

- `wcygan/agent-skills` owns reusable skill source and provider-side validation.
  Edit reusable skills there, not in installed copies or this repository.
- Dotfiles owns project-specific skills in `.agents/skills/**` and the consumer
  integration. `agent-skills.lock.toml` pins the provider repository and full
  commit SHA, plus the agent and portable shared user directory. Dotfiles does
  not vendor the reusable catalog.
- GitHub CLI installs the pinned catalog into the shared Codex user scope
  (`~/.agents/skills` with the current lock). Installed copies and tracking
  state are machine-local, not source of truth.

To update a reusable skill, change and validate it in the provider repository;
then, in an explicit update task, advance the dotfiles lock to the reviewed
provider commit. Installing or reconciling the pin is a separate, mutating
operation: `./bootstrap.sh agent-skills`. It is not part of the default install.
Use `./bootstrap.sh agent-skills --check` for read-only verification. Do not
assume a pin update authorizes installation, pruning, or a full reset.

For collision handling, stale copies, recovery, and verification, follow
[$agent-skills-integration](.agents/skills/agent-skills-integration/SKILL.md)
and the [pinned skills runbook](.agents/skills/dotfiles-operations/references/operations.md#pinned-global-agent-skills).
Keep `$dotfiles-operations` active for repository operations.

## Writing and repeated UI text

Use `$write-clearly` for prose and repeated UI text. For feeds, cards, table
summaries, notifications, or session titles, read its repeated-item guidance and
review the collection together. Put distinguishing information early, use
consistent structure and terminology within comparable groups, and make variation
reflect meaningful differences. Preserve factual status, uncertainty, and mixed
feedback; never imply progress, completion, or sentiment without evidence.

Keep descriptive headings for explanations and action labels for controls. Check
wrapping and truncation in the actual layout, and retain essential labels, units,
constraints, and recovery guidance. Keep reusable writing rules in the provider
skill rather than duplicating its checklist here.

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
