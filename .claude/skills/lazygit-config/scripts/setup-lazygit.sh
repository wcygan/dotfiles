#!/usr/bin/env bash
# Setup script for lazygit with delta integration
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

success() {
    echo -e "${GREEN}✓${NC} $*"
}

warn() {
    echo -e "${YELLOW}⚠${NC} $*"
}

error() {
    echo -e "${RED}✗${NC} $*"
}

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Darwin)
            echo "macos"
            ;;
        Linux)
            echo "linux"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Get lazygit config directory
get_config_dir() {
    local os="$1"
    case "$os" in
        macos)
            echo "$HOME/Library/Application Support/lazygit"
            ;;
        linux)
            echo "$HOME/.config/lazygit"
            ;;
        windows)
            echo "$LOCALAPPDATA/lazygit"
            ;;
        *)
            error "Unknown OS: $os"
            exit 1
            ;;
    esac
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check lazygit installation
check_lazygit() {
    info "Checking lazygit installation..."
    if command_exists lazygit; then
        success "lazygit is installed ($(lazygit --version))"
        return 0
    else
        error "lazygit is not installed"
        info "Install with: brew install lazygit (macOS) or nix profile install nixpkgs#lazygit"
        return 1
    fi
}

# Check delta installation
check_delta() {
    info "Checking delta installation..."
    if command_exists delta; then
        success "delta is installed ($(delta --version | head -n1))"
        return 0
    else
        warn "delta is not installed (optional but recommended)"
        info "Install with: brew install git-delta (macOS) or nix profile install nixpkgs#delta"
        return 1
    fi
}

# Create config directory
create_config_dir() {
    local config_dir="$1"
    info "Creating config directory: $config_dir"
    mkdir -p "$config_dir"
    success "Config directory created"
}

# Backup existing config
backup_config() {
    local config_file="$1"
    if [ -f "$config_file" ]; then
        local backup_file="${config_file}.backup.$(date +%Y%m%d_%H%M%S)"
        info "Backing up existing config to: $backup_file"
        cp "$config_file" "$backup_file"
        success "Backup created"
        return 0
    fi
    return 1
}

# Install config template
install_config() {
    local template="$1"
    local config_dir="$2"
    local config_file="$config_dir/config.yml"

    backup_config "$config_file" || true

    info "Installing $template config..."
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local template_file="$script_dir/../templates/$template.yml"

    if [ ! -f "$template_file" ]; then
        error "Template not found: $template_file"
        return 1
    fi

    cp "$template_file" "$config_file"
    success "Config installed: $config_file"
}

# Configure delta in gitconfig
configure_delta() {
    info "Configuring delta in ~/.gitconfig..."

    if ! git config --global core.pager >/dev/null 2>&1 || [ "$(git config --global core.pager)" != "delta" ]; then
        git config --global core.pager delta
        success "Set core.pager = delta"
    else
        info "core.pager already set to delta"
    fi

    if ! git config --global interactive.diffFilter >/dev/null 2>&1; then
        git config --global interactive.diffFilter "delta --color-only"
        success "Set interactive.diffFilter"
    else
        info "interactive.diffFilter already configured"
    fi

    # Basic delta settings
    git config --global delta.navigate true
    git config --global delta.line-numbers true
    git config --global delta.dark true
    git config --global delta.syntax-theme "Monokai Extended"

    success "Delta configured in ~/.gitconfig"
}

# Test delta integration
test_delta() {
    info "Testing delta integration..."

    # Create a temporary git repo
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"
    git init >/dev/null 2>&1
    echo "line 1" > test.txt
    git add test.txt
    git commit -m "Initial commit" >/dev/null 2>&1
    echo "line 2" >> test.txt

    info "Running: git diff"
    if git diff | delta >/dev/null 2>&1; then
        success "Delta is working correctly"
    else
        error "Delta test failed"
    fi

    cd - >/dev/null
    rm -rf "$temp_dir"
}

# Main setup function
main() {
    echo "================================"
    echo "Lazygit + Delta Setup"
    echo "================================"
    echo

    local os=$(detect_os)
    info "Detected OS: $os"

    # Check installations
    local has_lazygit=0
    local has_delta=0
    check_lazygit && has_lazygit=1 || true
    check_delta && has_delta=1 || true

    if [ $has_lazygit -eq 0 ]; then
        error "Please install lazygit first"
        exit 1
    fi

    # Get config directory
    local config_dir=$(get_config_dir "$os")
    info "Config directory: $config_dir"

    # Create config directory
    create_config_dir "$config_dir"

    # Ask which template to install
    echo
    info "Which config template would you like to install?"
    echo "  1) Minimal (basic delta integration)"
    echo "  2) Advanced (multiple pagers, custom commands)"
    read -p "Enter choice [1-2]: " choice

    case "$choice" in
        1)
            install_config "config-minimal" "$config_dir"
            ;;
        2)
            install_config "config-advanced" "$config_dir"
            ;;
        *)
            error "Invalid choice: $choice"
            exit 1
            ;;
    esac

    # Configure delta if installed
    if [ $has_delta -eq 1 ]; then
        echo
        read -p "Configure delta in ~/.gitconfig? [Y/n]: " configure_delta_choice
        case "$configure_delta_choice" in
            [Nn]*)
                info "Skipping delta configuration"
                ;;
            *)
                configure_delta
                test_delta
                ;;
        esac
    else
        warn "Delta not installed - skipping delta configuration"
        info "Install delta to get syntax-highlighted diffs"
    fi

    echo
    echo "================================"
    success "Setup complete!"
    echo "================================"
    echo
    info "Next steps:"
    echo "  1. Run 'lazygit' to test the configuration"
    echo "  2. Press 'e' in lazygit to edit the config"
    echo "  3. Press '|' to cycle between pagers (if multiple configured)"
    echo "  4. Visit https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md for more options"
    echo
}

main "$@"
