#!/usr/bin/env bash
# Shell configuration for Nix package manager
# Source this file in your .bashrc/.zshrc

# PATH priority matches config/fish/conf.d/10-nix.fish:
# Nix profiles > language and user bins > Homebrew > system paths.
_dotfiles_path_prepend() {
    [ -d "$1" ] || return 0
    case ":$PATH:" in
        *":$1:"*) PATH=$(printf '%s' ":$PATH:" | sed "s|:$1:|:|g; s|^:||; s|:\$||") ;;
    esac
    PATH="$1:$PATH"
}

if [ -f "$HOME/.nix-profile/etc/ssl/certs/ca-bundle.crt" ]; then
    export NIX_SSL_CERT_FILE="${NIX_SSL_CERT_FILE-$HOME/.nix-profile/etc/ssl/certs/ca-bundle.crt}"
    export SSL_CERT_FILE="${SSL_CERT_FILE-$HOME/.nix-profile/etc/ssl/certs/ca-bundle.crt}"
    export SSL_CERT_DIR="${SSL_CERT_DIR-$HOME/.nix-profile/etc/ssl/certs}"
fi

# Nix single-user installation
if [ -e "$HOME/.nix-profile/etc/profile.d/nix.sh" ]; then
    . "$HOME/.nix-profile/etc/profile.d/nix.sh"
fi

# Nix multi-user installation (daemon mode)
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
    . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi

# Lowest priority first; each call moves its directory to the front.
if [ -d /opt/homebrew/bin ]; then
    _dotfiles_path_prepend /opt/homebrew/bin
else
    _dotfiles_path_prepend /usr/local/bin
fi
_dotfiles_path_prepend "$HOME/.bun/bin"
_dotfiles_path_prepend "$HOME/.local/bin"
_dotfiles_path_prepend "$HOME/bin"
_dotfiles_path_prepend "$HOME/.tiup/bin"
_dotfiles_path_prepend "$HOME/.cargo/bin"
_dotfiles_path_prepend "$HOME/go/bin"
_dotfiles_path_prepend /nix/var/nix/profiles/default/bin
_dotfiles_path_prepend "$HOME/.nix-profile/bin"
export PATH
unset -f _dotfiles_path_prepend

# Nix flakes configuration
export NIX_CONFIG="experimental-features = nix-command flakes"

# Useful Nix aliases
alias nix-search='nix search nixpkgs'
alias nix-list='nix profile list'
alias nix-clean='nix-collect-garbage -d'
alias nix-shell-pure='nix-shell --pure'
alias nix-build-dry='nix build --dry-run --no-write-lock-file'

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
        nix profile add "nixpkgs#$1"
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
