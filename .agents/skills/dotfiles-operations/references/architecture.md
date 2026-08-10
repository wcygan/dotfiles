# Architecture Reference

## Mission and Invariants

This repository provides reproducible tools with Nix and editable,
repository-owned configuration through managed links. It intentionally does not
use Home Manager. The key invariants are:

- one root setup entry point: `bootstrap.sh`;
- locked Python orchestration inside the Nix development shell;
- package definitions in `flake.nix` and configurations in `config/**`;
- exact, read-only post-install verification;
- serialized, journaled, recoverable mutations;
- four-system evaluation and economical platform acceptance;
- machine-local credentials and mutable application state.

## Layered Setup Flow

```text
user / Make target
        |
        v
bootstrap.sh
  - establishes the Nix boundary
  - handles explicit Nix-install handoff
  - enters nix develop without rewriting flake.lock
        |
        v
uv run --locked python -m dotfiles_setup <command>
        |
        +--> cli.py: parsing, command routing, lock/journal boundary
        +--> installer.py: serial install orchestration and PASS/FAIL/SKIP
        +--> nix_profile.py: exact checkout profile add/upgrade/inspection
        +--> links.py / cleanup.py: managed config and uninstall inventory
        +--> rustup.py: exact repository Rust pin and rust-analyzer
        +--> agent_skills.py: exact external skill pin and Codex user-scope install
        +--> shell_handoff.py / git_user.py: explicit optional host changes
        +--> doctor.py: advisory environment diagnostics
        +--> verify.py: strict read-only acceptance
        +--> locking.py / manifest.py / recovery.py: mutation safety
```

The default install sequence is serial:

```text
preflight/recovery check -> mutation lock -> profile -> links -> rustup
    -> optional shell handoff -> strict verification -> journal completion
```

A failed dependency produces explicit skipped operations, but strict
verification still runs so the final report describes the actual host state.

## Technology Stack

| Layer | Technology | Source of truth |
| --- | --- | --- |
| Package graph | Nix flakes / pinned nixpkgs | `flake.nix`, `flake.lock` |
| Supported systems | x86_64/aarch64 Linux and Darwin | `flake.nix` |
| Setup runtime | Python 3.13 standard library | `src/dotfiles_setup/**` |
| Python environment | uv locked environment | `pyproject.toml`, `uv.lock` |
| Tests and lint | pytest and Ruff | `tests/**`, `pyproject.toml` |
| Shell bridge | Bash bootstrap; Fish configuration | `bootstrap.sh`, `config/fish/**` |
| Rust tools | rustup with exact numeric pin | `rust-toolchain.toml`, `rustup.py` |
| Configuration | repository files plus managed links | `config/**`, `links.py` |
| Linux acceptance | Docker Buildx, Ubuntu, Fedora | `Dockerfile.*`, `tests/docker_matrix.py` |
| Automation | GitHub Actions pinned to commit SHAs | `.github/workflows/**` |
| Documentation | Docusaurus / npm lock | `docs/**`, `docs/package-lock.json` |

The production Python package has no third-party runtime dependencies. pytest
and Ruff are development-only dependencies. Nix supplies the operational
Python interpreter, uv, shell tools, and user-facing CLI package closure.

## Agent Skills Provider/Consumer Boundary

`$agent-skills-integration` owns the detailed operating contract for global
skills. The architecture has three deliberately separate owners:

```text
wcygan/agent-skills       dotfiles                     GitHub CLI / Codex
reusable skill source -> repository + commit lock  -> shared user-scope installed copies
provider validation      command + verification      machine-local tracking state
```

Dotfiles never mirrors the provider catalog. `agent-skills.lock.toml` records a
full immutable commit and a relative shared user directory;
`src/dotfiles_setup/agent_skills.py` delegates discovery and installation to
`gh skill install --dir`, rejects conflicting installed names, and verifies
GitHub CLI metadata. The runtime destination is derived from the lock's current
`HOME` plus its portable relative directory and then confirmed by `gh skill
list --dir`; it is not inferred from GitHub CLI's stale Codex host mapping.
Installation is an explicit journaled command and remains outside the default
install workflow; its `--check` form is read-only.

## State Ownership

### Repository-owned

- `flake.nix`, `flake.lock`, `rust-toolchain.toml`;
- `agent-skills.lock.toml` and the pinned external catalog contract;
- `bootstrap.sh`, `src/dotfiles_setup/**`, and tests;
- portable configuration under `config/**`;
- project-local operating skills under `.agents/skills/**`;
- Dockerfiles, Make targets, workflows, and documentation.

### User-owned but managed

- platform-specific links defined only by `links.managed_links(...)`;
- npm prefix and release-age settings in `~/.npmrc`;
- the optional Bash/zsh Fish handoff blocks;
- the local Git identity file when explicitly configured;
- the shared and Codex `AGENTS.md` links sourced from `config/agents/AGENTS.md`;
- the pinned Codex shared user-scope skill copies installed by the current
  GitHub CLI under `~/.agents/skills`.

Existing physical destinations are backed up before replacement. The managed
inventory, platform path resolvers, and HOME/XDG/CODEX overrides are part of the
tested contract.

### Machine-local and not repository-managed

- credentials, tokens, SSH keys, and secrets;
- Codex custom agents, project trust entries, sessions, and caches;
- GitHub CLI skill tracking state under `~/.agents/.skill-lock.json`;
- Pi credentials, sessions, models, and global catalogs;
- the mutable Codex `config.toml` after its initial template copy;
- rustup downloads under `RUSTUP_HOME` and Cargo state under `CARGO_HOME`.

## Verification Contract

`doctor` answers "is this environment plausibly usable?" and exits
successfully with advisory warnings. `verify` answers "does this exact checkout
own a complete installation?" and fails if any required postcondition is
missing.

Strict verification checks:

- an active user-profile element whose local origin resolves to this checkout;
- required and representative executables in the matched profile store output;
- Python 3.13 from that store output;
- rust-analyzer resolved by the profile's rustup executable for the exact
  numeric repository pin;
- each platform-specific managed link resolves to its repository source;
- `${CODEX_HOME:-$HOME/.codex}/config.toml` is a regular local file.

It does not trust the ambient `PATH`, a profile element name, a global Rust
default, or file-content equivalence for managed links.

## Mutation and Recovery Model

Mutating commands acquire a fail-fast per-user lock under
`${XDG_CACHE_HOME:-$HOME/.cache}/dotfiles/`. A durable operation journal lives
under `${XDG_STATE_HOME:-$HOME/.local/state}/dotfiles/`.

Before a filesystem mutation, setup records intent and prior identity, then
checkpoints progress after each entry. Atomic temporary files or links are
renamed into place. Recovery validates the command, normalized destinations,
managed allowlist, backup identity, and current result before undoing anything.
It refuses to overwrite later user changes.

The manifest records paths, state, timestamps, link targets, inode identities,
and one-way content hashes. It must never record Git identity values, Codex
trust contents, credentials, or file contents.
