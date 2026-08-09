# Dotfiles

Modern developer configuration with safe installation and Nix package management.

## Installation

```bash
git clone https://github.com/wcygan/dotfiles.git
cd dotfiles
./bootstrap.sh
```

`bootstrap.sh` is the supported entry point. With Nix available, it enters the
repository development shell and runs the locked Python CLI:

```bash
nix develop --no-write-lock-file .#default --command uv run --locked python -m dotfiles_setup install
```

The default install upgrades or adds this repository's Nix profile, links the
managed configuration (backing up existing files), prepares Rust tooling, and
verifies the result. It does **not** edit Bash or zsh startup files. Opt in to
that behavior only when wanted:

```bash
./bootstrap.sh install --shell-handoff
```

On macOS, if Nix is missing, `./bootstrap.sh` opens the Determinate macOS
installer package and exits; finish that installer, start a fresh shell, then
rerun the command. On Linux or WSL, explicitly authorize the Determinate Nix
install instead:

```bash
./bootstrap.sh --install-nix --yes
```

Full documentation available at: https://wcygan.github.io/dotfiles/

## What You Get

- **🚀 Modern CLI tools**: ripgrep, fd, bat, eza, fzf, delta, and more
- **🐟 Fish shell**: Full configuration with functions and abbreviations
- **⭐ Starship prompt**: Beautiful, fast, and informative
- **📦 Nix packages**: Reproducible across macOS, Ubuntu, and Fedora
- **🔗 Safe symlinks**: Automatic backups before any changes

## Project Structure

```
dotfiles/
├── .agents/             # Project-local operating skills
├── config/             # Configuration files
│   ├── fish/           # Fish shell config
│   ├── codex/          # Codex config template and global instructions
│   ├── zed/            # Zed config
│   ├── ghostty/        # Ghostty config
│   ├── starship.toml   # Starship prompt
│   └── shell-nix.sh    # Bash/zsh compatibility
├── src/dotfiles_setup/  # Locked Python setup CLI
├── tests/               # Python and platform test suites
├── flake.nix           # Nix package definitions
├── bootstrap.sh         # Nix bootstrap and Python CLI bridge
├── pyproject.toml       # Python project metadata and tool configuration
├── uv.lock              # Locked Python dependencies
└── docs/               # Documentation site
```

## Post-Install Extras

### Peon Ping (Claude Code sound notifications)

[Peon Ping](https://github.com/PeonPing/peon-ping) plays Warcraft-style sound cues when Claude Code needs attention. Not managed by Nix — install separately via Homebrew:

```bash
brew install PeonPing/tap/peon-ping && peon-ping-setup
```

This adds hooks to your local `~/.claude/` config. It is not managed by this
repository.

### Agent Skills

Dotfiles-specific operating skills live in `.agents/skills/`; reusable skills
are authored and published from the dedicated `agent-skills` repository, which
is authoritative. This repository neither vendors nor installs a global skill
catalog. Codex is managed narrowly:
`config/codex/config.toml` is a portable template copied to
`${CODEX_HOME:-~/.codex}/config.toml` only when missing, and
`config/codex/AGENTS.md` points to `${CODEX_HOME:-~/.codex}/AGENTS.md`. Skills,
custom agents, and the rest of `CODEX_HOME` remain machine-local state. Codex
may write machine-specific `[projects]` trust entries into the local config;
keep those out of the tracked template.

Pi credentials, sessions, models, and global catalogs remain machine-local
state.

### npm Global Tools

The installer configures npm's user prefix and a one-day dependency release
cooldown in `~/.npmrc`:

```ini
prefix=${HOME}/.local
min-release-age=1
```

That keeps `npm install -g` writable when npm comes from Nix, lets package
releases settle for 24 hours before install, and exposes global binaries
through `~/.local/bin`, which the shell config already adds to `PATH` behind
Nix-managed tools.

Example:

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

### Dependency Install Cooldowns

The repo's docs site uses npm (`docs/package-lock.json`). The installer manages
dependency release-age settings for npm, Bun, and Deno:

- Bun: links `config/bunfig.toml` to global bunfig locations with
  `minimumReleaseAge = 259200`.
- npm: manages `min-release-age=1` in `~/.npmrc`. npm does not currently expose
  a documented package or scope exemption key for this setting.
- Deno: links `config/deno/deno.jsonc` and shell wrappers apply it to
  `deno install`, `deno add`, `deno update`, `deno outdated`, and `deno x` when
  no project `deno.json` or `deno.jsonc` is already active. Its dependency age
  is set to one day so package releases settle for 24 hours before install.

Bun exempts the `@wcygan/*` workspace scope from the cooldown. Deno keeps the
same exemption entries in its config for future nonzero cooldowns.

## Per-Project Dev Environments (nix-direnv)

For reproducible per-project tool versions, use [nix-direnv](https://determinate.systems/blog/nix-direnv/).

### One-time machine setup

1. Ensure `direnv` is in `flake.nix` packages
2. Fish hook is preconfigured at `config/fish/conf.d/20-direnv.fish`
3. Global direnv config allows nix-direnv

### Per-repository setup

1. Create `.envrc`:

   ```bash
   use flake
   ```

2. Create `flake.nix` with a dev shell:

   ```nix
   {
     inputs.nixpkgs.url = "github:NixOS/nixpkgs";
     outputs = { self, nixpkgs }: {
       devShells.x86_64-darwin.default = nixpkgs.legacyPackages.x86_64-darwin.mkShell {
         packages = [ /* project-specific tools */ ];
       };
     };
   }
   ```

3. `direnv allow` to trust the environment.

Commit `.envrc` and `flake.nix`; gitignore `.direnv/`. Use cases: language toolchains (Node 20 vs 18), pinned database clients, exact build tool versions, locked cloud CLIs.

For troubleshooting concurrent direnv rebuilds and Nix daemon issues, the agent has a dedicated `nix-direnv-perf` skill.

## Nix Installation (macOS)

Use the **Determinate Systems macOS Installer**. When Nix is absent,
`./bootstrap.sh` opens its package URL and tells you to rerun after the package
installation completes. The package handles macOS integration, automatic
updates, and Apple Silicon optimization.

For Linux and WSL, the bootstrapper only invokes the official Determinate
installer after the explicit `--install-nix --yes` confirmation shown above.

## Setup and Verification

Use the Make targets for the common workflow, or pass the matching command to
`./bootstrap.sh` directly:

```bash
make install                 # ./bootstrap.sh
make link                    # ./bootstrap.sh link
make link-dry                # ./bootstrap.sh link --dry-run
make git-user                # ./bootstrap.sh git-user
make setup-shell-handoff     # ./bootstrap.sh shell-handoff
make setup-rustup-components # ./bootstrap.sh rustup
make verify                  # ./bootstrap.sh verify
make doctor                  # ./bootstrap.sh doctor
make uninstall               # ./bootstrap.sh uninstall
make uninstall-dry           # ./bootstrap.sh uninstall --dry-run
./bootstrap.sh recover       # inspect interrupted-operation recovery
```

`doctor` is advisory: it reports the host and development-shell environment as
`PASS` or `WARN` without treating not-yet-installed state as an acceptance
failure. `verify` is strict and read-only. It requires an active Nix profile
element sourced from this exact checkout, required binaries in that element's
store output, Python 3.13, every managed link at its platform-specific
destination, and a regular machine-local Codex `config.toml`. A full `install`
always ends with strict verification and fails when a required operation was
failed or skipped.

Mutating commands share a fail-fast per-user lock under the XDG cache home, so
two setup processes cannot race. Link setup preflights its complete inventory,
uses atomic replacements, restores physical destinations if replacement fails,
and journals recovery metadata under
`${XDG_STATE_HOME:-$HOME/.local/state}/dotfiles/`. `doctor`, `verify`, dry runs,
and the default `recover` inspection remain read-only and do not take the
mutation lock. If an interrupted operation is recorded, inspect it first:

```bash
./bootstrap.sh recover
./bootstrap.sh recover --apply --yes  # explicit, guarded mutation
```

Recovery restores only recorded backups or links whose current state still
matches the interrupted operation. It refuses to overwrite later user changes
and leaves the recovery manifest in place when manual intervention is needed.
The manifest records paths, link targets, statuses, timestamps, and one-way
content hashes only; it never records Git identity values, Codex trust
contents, or file contents. Shell startup-file and `.npmrc` symlink referents
must remain inside `HOME`; setup refuses external referents with manual
guidance instead of modifying an unexpected file.

Rust is pinned in `rust-toolchain.toml` to the exact
[1.97.1 corrective release](https://blog.rust-lang.org/2026/07/16/Rust-1.97.1/),
including rust-analyzer. `./bootstrap.sh rustup` installs and resolves that
toolchain explicitly and never changes the global rustup default. Update the
pin intentionally after reviewing an official Rust release, then rerun the
Rust and strict-verification tests.

Committed CI and local Docker acceptance use full GitHub Action SHAs and
multi-platform image manifest digests, so pull requests test exactly the
reviewed inputs. A separate scheduled/manual upstream-freshness workflow strips
the committed image digests in a temporary runner file and builds the current
Ubuntu 24.04, Fedora 43, and Nix 2.30.3 tags. It reports compatibility drift but
never edits the repository. Dependabot proposes weekly Action and Docker digest
updates for human review; no automatic merge is configured. Platform refreshes
are evaluated against the official [Ubuntu release lifecycle](https://wiki.ubuntu.com/Releases)
and [Fedora release lifecycle](https://fedoraproject.org/wiki/User%3AJkurik/Fedora_Release_Life_Cycle).

Pull-request CI calls the same repository targets used locally: locked quality
and syntax checks, four-system flake evaluation, and the canonical Ubuntu/Fedora
Docker driver. Docker builds use separate GitHub Actions cache scopes, load the
resulting image, and run strict installation plus Fish/direnv runtime smoke.
Pytest JUnit reports are retained on both success and failure. Documentation
changes build on pull requests, but Pages deployment is restricted to a push to
`main`. Native macOS 15 arm64 acceptance runs weekly or manually in an isolated
temporary home; Intel macOS 15 acceptance is manual so routine pull requests
remain Linux-only and economical.

The Python package lives in `src/dotfiles_setup/`: `cli.py` owns command
parsing, while focused modules own profile management, linking and cleanup,
advisory diagnostics, strict verification, Rust setup, shell handoff, and Git
identity. Run a command
inside the Nix development environment with `uv run --locked python -m
dotfiles_setup <command>`; normally, prefer `bootstrap.sh` so the Nix boundary
is applied consistently.

To roll back a package change, use `nix profile rollback`. Configuration links
are safe to rerun and pre-existing files are kept as timestamped backups. The
annotated `pre-transactional-setup-recovery` tag is the rollback point before
the transactional setup boundary. Keep a known-good Git tag before any later
configuration migration so the repository state itself is also easy to
restore.

## Quick Reference

```bash
# Update the flake and managed profile
make update

# Add new packages
# Edit flake.nix, then update the managed profile:
make profile

# Run the locked Python checks
make test-pre      # Ruff plus the complete pytest suite
make test-local    # ephemeral-HOME-focused pytest suite
make test-shell    # shell-handoff pytest suite
make test-syntax   # Bash and Fish parsing
make test-eval     # all four flake systems, evaluation only
make test-docker   # Python Ubuntu/Fedora driver
make test           # every non-Docker test

# Documentation
make docs-build    # clean install and production build
make docs
```
