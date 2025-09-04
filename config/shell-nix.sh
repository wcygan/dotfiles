#!/usr/bin/env bash
# Shell configuration for Nix package manager
# Source this file in your .bashrc/.zshrc

# Nix single-user installation
if [ -e "$HOME/.nix-profile/etc/profile.d/nix.sh" ]; then
    . "$HOME/.nix-profile/etc/profile.d/nix.sh"
fi

# Nix multi-user installation (daemon mode)
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
    . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi

# Add Nix profile binaries to PATH
export PATH="$HOME/.nix-profile/bin:$PATH"

# Nix flakes configuration
export NIX_CONFIG="experimental-features = nix-command flakes"

# Useful Nix aliases
alias nix-update='nix flake update && nix profile upgrade'
alias nix-search='nix search nixpkgs'
alias nix-list='nix profile list'
alias nix-clean='nix-collect-garbage -d'
alias nix-shell-pure='nix-shell --pure'
alias nix-build-dry='nix build --dry-run'

# Function to quickly test a package without installing
nix-try() {
    if [ -z "$1" ]; then
        echo "Usage: nix-try <package>"
        return 1
    fi
    nix-shell -p "$1" --run "$1 --version || $1 --help || echo 'Package loaded: $1'"
}

# Function to search and install packages interactively
nix-install() {
    if [ -z "$1" ]; then
        echo "Usage: nix-install <package>"
        return 1
    fi
    echo "Searching for package: $1"
    nix search nixpkgs "$1" | head -20
    echo ""
    read -p "Install package? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        nix profile install "nixpkgs#$1"
    fi
}
