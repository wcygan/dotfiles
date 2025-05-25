#!/usr/bin/env bash

# Dotfiles Rollback Script
# Restores dotfiles from a backup directory

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

echo -e "${BLUE}🔄 Dotfiles Rollback${NC}"
echo -e "${BLUE}==================${NC}"
echo

# Check if backup directory is provided
if [ $# -eq 0 ]; then
    print_error "No backup directory specified!"
    echo
    echo "Usage: $0 <backup_directory>"
    echo
    echo "Available backups:"
    ls -la "$HOME"/.dotfiles-backup-* 2>/dev/null || echo "  No backups found"
    exit 1
fi

BACKUP_DIR="$1"

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    print_error "Backup directory does not exist: $BACKUP_DIR"
    exit 1
fi

echo -e "📂 Backup directory: ${YELLOW}$BACKUP_DIR${NC}"
echo -e "🏠 Home directory: ${YELLOW}$HOME${NC}"
echo

# List files in backup
echo -e "${BLUE}📋 Files in backup:${NC}"
ls -la "$BACKUP_DIR"
echo

# Confirm rollback
echo -e "${YELLOW}⚠️  This will restore your dotfiles from the backup directory.${NC}"
echo -e "${YELLOW}   Current dotfiles will be overwritten!${NC}"
echo
read -p "Continue with rollback? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Rollback cancelled by user"
    exit 0
fi

# Perform rollback
echo -e "${BLUE}🔄 Restoring files...${NC}"

restored_count=0
for file in "$BACKUP_DIR"/*; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        destination="$HOME/$filename"
        
        # Copy file back
        cp "$file" "$destination"
        print_status "Restored $filename"
        ((restored_count++))
    fi
done

# Reload shell configuration
echo
echo -e "${BLUE}🔃 Reloading shell configuration...${NC}"
if [[ "$SHELL" == *"zsh"* ]]; then
    source ~/.zshrc || print_warning "Could not reload .zshrc automatically"
    print_status "Reloaded zsh configuration"
elif [[ "$SHELL" == *"bash"* ]]; then
    source ~/.bash_profile || print_warning "Could not reload .bash_profile automatically"
    print_status "Reloaded bash configuration"
fi

# Rollback complete
echo
echo -e "${GREEN}🎉 Rollback completed successfully!${NC}"
echo
echo -e "${BLUE}📋 Summary:${NC}"
echo -e "   ✅ Restored ${GREEN}$restored_count${NC} files from backup"
echo -e "   ✅ Reloaded shell configuration"
echo
echo -e "${BLUE}💡 The backup directory is preserved at:${NC}"
echo -e "   ${YELLOW}$BACKUP_DIR${NC}"
echo
echo -e "${GREEN}Your original dotfiles have been restored! 🔄${NC}" 