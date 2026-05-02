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
├── config/             # Configuration files
|   ├── zed/            # Zed config
|   ├── ghostty/        # Ghostty config
│   ├── fish/           # Fish shell config
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

This adds hooks and skills to your local `~/.claude/` config. These files are gitignored and will need to be reinstalled on new machines.

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

# Uninstall (configs only, keeps Nix)
make uninstall

# Run tests
make test-pre
make test-local

# Start documentation dev server
make docs
```