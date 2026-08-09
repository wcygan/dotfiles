# Dotfiles

Modern developer configuration with safe installation and Nix package management.

## Installation

```bash
git clone https://github.com/wcygan/dotfiles.git
cd dotfiles
./install.sh
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
├── scripts/            # Installation scripts
├── flake.nix           # Nix package definitions
├── install.sh          # One-command installer
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
belong in the dedicated `agent-skills` repository. Codex is managed narrowly:
`config/codex/config.toml` is a portable template copied to
`${CODEX_HOME:-~/.codex}/config.toml` only when missing, and
`config/codex/AGENTS.md` points to `${CODEX_HOME:-~/.codex}/AGENTS.md`. Skills,
custom agents, and the rest of `CODEX_HOME` remain machine-local state. Codex
may write machine-specific `[projects]` trust entries into the local config;
keep those out of the tracked template.

This repository does not install or link global agent skills. Pi credentials,
sessions, models, and any global catalog remain machine-local state.

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

Use the **Determinate Systems macOS Installer** rather than the shell script. Download it from [docs.determinate.systems](https://docs.determinate.systems/), run the installer, then `./install.sh` to set up dotfiles. The installer handles macOS integration, automatic updates, and Apple Silicon optimization.

## Quick Reference

```bash
# Update packages
nix flake update
nix profile upgrade '.*'

# Add new packages
# Edit flake.nix, then:
nix profile install .

# Repair Rust editor components
make setup-rustup-components

# Uninstall (configs only, keeps Nix)
make uninstall

# Run tests
make test-pre
make test-local

# Start documentation dev server
make docs
```
