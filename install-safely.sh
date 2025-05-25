#!/usr/bin/env bash

# Safe Dotfiles Installation Script
# This script backs up existing dotfiles before installing new ones

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="$HOME/.dotfiles-backup-$(date +%Y%m%d-%H%M%S)"
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Files to manage
DOTFILES=(
    ".zshrc"
    ".bashrc" 
    ".bash_profile"
    ".path"
    ".exports"
    ".aliases"
    ".functions"
    ".extra"
    ".vimrc"
)

# Optional files that might exist
OPTIONAL_FILES=(
    ".platform"
    ".fzf.zsh"
)

echo -e "${BLUE}🔧 Safe Dotfiles Installation${NC}"
echo -e "${BLUE}===============================${NC}"
echo
echo -e "📁 Dotfiles source: ${YELLOW}$DOTFILES_DIR${NC}"
echo -e "💾 Backup location: ${YELLOW}$BACKUP_DIR${NC}"
echo

# Function to print status
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "$DOTFILES_DIR/.zshrc" ] || [ ! -f "$DOTFILES_DIR/.aliases" ]; then
    print_error "Not in dotfiles directory or files missing!"
    echo "Please run this script from the dotfiles repository directory."
    exit 1
fi

# Create backup directory
echo -e "${BLUE}📦 Creating backup directory...${NC}"
mkdir -p "$BACKUP_DIR"
print_status "Created backup directory: $BACKUP_DIR"

# Function to backup existing file
backup_file() {
    local file="$1"
    local home_file="$HOME/$file"
    
    if [ -f "$home_file" ] || [ -L "$home_file" ]; then
        cp "$home_file" "$BACKUP_DIR/" 2>/dev/null || true
        print_status "Backed up $file"
        return 0
    else
        echo -e "   ${YELLOW}No existing $file found${NC}"
        return 1
    fi
}

# Backup existing dotfiles
echo
echo -e "${BLUE}💾 Backing up existing dotfiles...${NC}"
for file in "${DOTFILES[@]}"; do
    backup_file "$file"
done

# Backup optional files
echo
echo -e "${BLUE}🔍 Checking for optional files...${NC}"
for file in "${OPTIONAL_FILES[@]}"; do
    backup_file "$file"
done

# Show current shell
echo
echo -e "${BLUE}🐚 Current shell information:${NC}"
echo -e "   Shell: ${YELLOW}$SHELL${NC}"
echo -e "   User: ${YELLOW}$USER${NC}"

# Detect shell and confirm
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_TYPE="zsh"
    BOOTSTRAP_SCRIPT="bootstrap-zsh.sh"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_TYPE="bash" 
    BOOTSTRAP_SCRIPT="bootstrap-bash.sh"
else
    print_warning "Unknown shell: $SHELL"
    echo "Please manually choose bootstrap script:"
    echo "  - bootstrap-zsh.sh for zsh"
    echo "  - bootstrap-bash.sh for bash"
    exit 1
fi

echo -e "   Detected: ${GREEN}$SHELL_TYPE${NC}"
echo -e "   Will use: ${GREEN}$BOOTSTRAP_SCRIPT${NC}"

# Confirm installation
echo
echo -e "${YELLOW}⚠️  This will replace your current dotfiles with the repository versions.${NC}"
echo -e "${YELLOW}   Your existing files are safely backed up in: $BACKUP_DIR${NC}"
echo
read -p "Continue with installation? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Installation cancelled by user"
    echo -e "Your backups are still available in: ${YELLOW}$BACKUP_DIR${NC}"
    exit 0
fi

# Update repository
echo
echo -e "${BLUE}🔄 Updating dotfiles repository...${NC}"
if [ -d ".git" ]; then
    git pull origin main || print_warning "Could not update repository (continuing anyway)"
    print_status "Repository updated"
else
    print_warning "Not a git repository, skipping update"
fi

# Install dotfiles using the appropriate bootstrap script
echo
echo -e "${BLUE}🚀 Installing dotfiles...${NC}"
if [ -f "$BOOTSTRAP_SCRIPT" ]; then
    source "$BOOTSTRAP_SCRIPT" --force
    print_status "Dotfiles installed successfully!"
else
    print_error "Bootstrap script $BOOTSTRAP_SCRIPT not found!"
    exit 1
fi

# Reload shell configuration
echo
echo -e "${BLUE}🔃 Reloading shell configuration...${NC}"
if [ "$SHELL_TYPE" = "zsh" ]; then
    source ~/.zshrc || print_warning "Could not reload .zshrc automatically"
else
    source ~/.bash_profile || print_warning "Could not reload .bash_profile automatically"
fi
print_status "Shell configuration reloaded"

# Installation complete
echo
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo
echo -e "${BLUE}📋 What was done:${NC}"
echo -e "   ✅ Backed up existing dotfiles to: ${YELLOW}$BACKUP_DIR${NC}"
echo -e "   ✅ Installed new dotfiles from repository"
echo -e "   ✅ Reloaded shell configuration"
echo
echo -e "${BLUE}🧪 Test your installation:${NC}"
echo -e "   • Try: ${YELLOW}d${NC} (should open development workspace in Cursor)"
echo -e "   • Try: ${YELLOW}k get nodes${NC} (kubectl shortcut)"
echo -e "   • Try: ${YELLOW}cgr${NC} (cargo run)"
echo -e "   • Try: ${YELLOW}mm${NC} (git main branch helper)"
echo
echo -e "${BLUE}🔄 If you need to rollback:${NC}"
echo -e "   ${YELLOW}./rollback.sh $BACKUP_DIR${NC}"
echo
echo -e "${GREEN}Enjoy your new dotfiles setup! 🎊${NC}" 