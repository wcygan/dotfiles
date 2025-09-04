# Dotfiles

Modern developer configuration with safe installation and Nix package management.

## Installation

```bash
git clone https://github.com/wcygan/dotfiles.git
cd dotfiles
./install.sh
```

That's it! The installer handles everything:
- ✅ Pre-flight checks (OS detection, dependencies)
- ✅ Nix installation (if needed)
- ✅ Package installation from flake
- ✅ Configuration symlinking
- ✅ Post-flight verification

## What You Get

- **🚀 Modern CLI tools**: ripgrep, fd, bat, eza, fzf, delta, and more
- **🐟 Fish shell**: Full configuration with functions and abbreviations
- **⭐ Starship prompt**: Beautiful, fast, and informative
- **📦 Nix packages**: Reproducible across macOS, Ubuntu, and Fedora
- **🔗 Safe symlinks**: Automatic backups before any changes

## Supported Platforms

- macOS (Intel & Apple Silicon)
- Ubuntu (20.04+)
- Fedora (38+)

## Documentation

Full documentation available at: https://wcygan.github.io/dotfiles/

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
```

## Project Structure

```
dotfiles/
├── config/              # Configuration files
│   ├── fish/           # Fish shell config
│   ├── starship.toml   # Starship prompt
│   └── shell-nix.sh    # Bash/zsh compatibility
├── scripts/            # Installation scripts
├── flake.nix          # Nix package definitions
├── install.sh         # One-command installer
└── docs/              # Documentation site
```

## Contributing

PRs welcome! Please ensure:
- Changes work on all supported platforms
- Tests pass (`make test-pre`)
- Idempotent operations (safe to run multiple times)

## License

MIT