#!/usr/bin/env bash
# Shell configuration for Nix package manager
# Source this file in your .bashrc/.zshrc

# Priority PATH setup - system packages take precedence over Nix
# First, ensure system and user paths are prioritized

# macOS: Add Homebrew paths with higher priority
if [ -d "/opt/homebrew/bin" ]; then
    export PATH="/opt/homebrew/bin:$PATH"
elif [ -d "/usr/local/bin" ]; then
    export PATH="/usr/local/bin:$PATH"
fi

# User-specific binary locations (for manual installs)
[ -d "$HOME/.local/bin" ] && export PATH="$HOME/.local/bin:$PATH"
[ -d "$HOME/bin" ] && export PATH="$HOME/bin:$PATH"

# Language-specific paths
[ -d "$HOME/.cargo/bin" ] && export PATH="$HOME/.cargo/bin:$PATH"
[ -d "$HOME/go/bin" ] && export PATH="$HOME/go/bin:$PATH"

# Now add Nix paths at the END (lower priority)
# Store original PATH to avoid duplication
if [ -z "${_ORIGINAL_PATH_BEFORE_NIX+x}" ]; then
    export _ORIGINAL_PATH_BEFORE_NIX="$PATH"
fi

# Nix single-user installation
if [ -e "$HOME/.nix-profile/etc/profile.d/nix.sh" ]; then
    . "$HOME/.nix-profile/etc/profile.d/nix.sh"
fi

# Nix multi-user installation (daemon mode)
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
    . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi

# Append Nix profile binaries to PATH (instead of prepending)
# This ensures system packages take precedence
export PATH="${_ORIGINAL_PATH_BEFORE_NIX}:$HOME/.nix-profile/bin:/nix/var/nix/profiles/default/bin"

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

# Function to show which version of a command will be used
which-version() {
    if [ -z "$1" ]; then
        echo "Usage: which-version <command>"
        echo "Shows which version of a command will be used (system vs Nix)"
        return 1
    fi

    local cmd="$1"
    local path=$(which "$cmd" 2>/dev/null)

    if [ -z "$path" ]; then
        echo "Command '$cmd' not found"
        return 1
    fi

    echo "Active: $path"

    # Check if it's from Nix
    if [[ "$path" == *"/nix/"* ]] || [[ "$path" == *"/.nix-profile/"* ]]; then
        echo "Source: Nix package"
    elif [[ "$path" == *"/opt/homebrew/"* ]] || [[ "$path" == *"/usr/local/"* ]]; then
        echo "Source: Homebrew"
    elif [[ "$path" == "$HOME/.local/bin"* ]] || [[ "$path" == "$HOME/bin"* ]]; then
        echo "Source: User install"
    else
        echo "Source: System package"
    fi

    # Show all available versions
    echo ""
    echo "All available:"
    type -a "$cmd" 2>/dev/null | sed 's/^/  /'
}
