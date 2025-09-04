#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ============================================================================
# Pre-flight checks
# ============================================================================
echo -e "${BLUE}=== Pre-flight checks ===${NC}"

# Check OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo -e "${GREEN}✓${NC} macOS detected"
elif [[ -f /etc/fedora-release ]]; then
    OS="fedora"
    echo -e "${GREEN}✓${NC} Fedora detected"
elif [[ -f /etc/lsb-release ]] && grep -q "Ubuntu" /etc/lsb-release; then
    OS="ubuntu"
    echo -e "${GREEN}✓${NC} Ubuntu detected"
else
    echo -e "${YELLOW}⚠${NC} Unsupported OS detected. Proceeding with caution..."
fi

# Check for required commands
MISSING_DEPS=()
for cmd in curl git; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        MISSING_DEPS+=("$cmd")
    else
        echo -e "${GREEN}✓${NC} $cmd found"
    fi
done

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo -e "${RED}✗${NC} Missing required dependencies: ${MISSING_DEPS[*]}"
    echo "Please install them first:"
    case "$OS" in
        macos)
            echo "  brew install ${MISSING_DEPS[*]}"
            ;;
        ubuntu)
            echo "  sudo apt update && sudo apt install -y ${MISSING_DEPS[*]}"
            ;;
        fedora)
            echo "  sudo dnf install -y ${MISSING_DEPS[*]}"
            ;;
    esac
    exit 1
fi

# Check sudo access for Linux
if [[ "$OS" == "ubuntu" || "$OS" == "fedora" ]]; then
    if ! sudo -n true 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC} This script may require sudo access for Nix installation"
        echo "Testing sudo access..."
        if sudo true; then
            echo -e "${GREEN}✓${NC} Sudo access confirmed"
        else
            echo -e "${RED}✗${NC} Unable to get sudo access"
            exit 1
        fi
    else
        echo -e "${GREEN}✓${NC} Sudo access available"
    fi
fi

echo ""

# ============================================================================
# Installation
# ============================================================================
echo -e "${BLUE}=== Starting installation ===${NC}"

echo -e "\n${BLUE}Step 1: Installing Nix (if needed)${NC}"
if ! command -v nix >/dev/null 2>&1; then
    echo "Nix not found. Installing via Determinate Systems installer..."
    "$ROOT/scripts/install-nix.sh"

    # Source daemon profile for multi-user installations
    if [ -f /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh ]; then
        echo "Sourcing Nix daemon..."
        . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
    fi

    # Verify Nix installation
    if command -v nix >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Nix installed successfully ($(nix --version))"
    else
        echo -e "${RED}✗${NC} Nix installation failed"
        echo "Please try opening a new terminal or manually source the Nix profile"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} Nix already installed ($(nix --version))"
fi

echo -e "\n${BLUE}Step 2: Installing packages from flake${NC}"
if "$ROOT/scripts/install-packages.sh"; then
    echo -e "${GREEN}✓${NC} Packages installed successfully"
else
    echo -e "${RED}✗${NC} Package installation failed"
    exit 1
fi

echo -e "\n${BLUE}Step 3: Linking configuration files${NC}"
if "$ROOT/scripts/link-config.sh"; then
    echo -e "${GREEN}✓${NC} Configurations linked successfully"
else
    echo -e "${RED}✗${NC} Configuration linking failed"
    exit 1
fi

echo ""

# ============================================================================
# Post-flight checks
# ============================================================================
echo -e "${BLUE}=== Post-flight verification ===${NC}"

# Check if key tools are available
TOOLS_TO_CHECK=(rg fd bat eza fzf git gh starship fish)
MISSING_TOOLS=()

for tool in "${TOOLS_TO_CHECK[@]}"; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $tool installed"
    else
        MISSING_TOOLS+=("$tool")
        echo -e "${YELLOW}⚠${NC} $tool not found in PATH"
    fi
done

# Check config files
echo -e "\n${BLUE}Configuration files:${NC}"
CONFIG_FILES=(
    "$HOME/.config/fish/config.fish"
    "$HOME/.config/starship.toml"
)

for file in "${CONFIG_FILES[@]}"; do
    if [ -L "$file" ] || [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${YELLOW}⚠${NC} $file not found"
    fi
done

echo ""

# ============================================================================
# Next steps
# ============================================================================
echo -e "${GREEN}=== Installation complete! ===${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""

# Check if we're in a container
if [ -f /.dockerenv ] || [ -n "${container:-}" ] || ! command -v systemctl &>/dev/null; then
    echo "1. Source Nix environment first:"
    echo -e "   ${YELLOW}source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh${NC}"
    echo ""
    echo "2. Then start fish shell:"
    echo -e "   ${YELLOW}make fish${NC} or ${YELLOW}fish${NC}"
else
    # Shell-specific instructions
    CURRENT_SHELL=$(basename "$SHELL")
    case "$CURRENT_SHELL" in
        fish)
            echo "1. Restart your shell or run:"
            echo -e "   ${YELLOW}exec fish -l${NC}"
            ;;
        bash|zsh)
            echo "1. Add this line to your ~/.${CURRENT_SHELL}rc:"
            echo -e "   ${YELLOW}source ~/.config/shell-nix.sh${NC}"
            echo ""
            echo "2. Then restart your shell or run:"
            echo -e "   ${YELLOW}source ~/.${CURRENT_SHELL}rc${NC}"
            echo ""
            echo "3. (Optional) Switch to fish shell:"
            echo -e "   ${YELLOW}fish${NC}"
            ;;
        *)
            echo "1. For bash/zsh, add to your shell rc file:"
            echo -e "   ${YELLOW}source ~/.config/shell-nix.sh${NC}"
            echo ""
            echo "2. Or try fish shell:"
            echo -e "   ${YELLOW}fish${NC}"
            ;;
    esac
fi

if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
    echo ""
    echo -e "${YELLOW}Note:${NC} Some tools were not found in PATH: ${MISSING_TOOLS[*]}"
    echo "They may become available after restarting your shell."
fi

echo ""
echo -e "${GREEN}Enjoy your new development environment!${NC}"
echo ""
echo "For more information, see: https://wcygan.github.io/dotfiles/"
