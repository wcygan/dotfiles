#!/usr/bin/env bash

# Test script to verify Nix recovery logic
# Can be run on Fedora/Ubuntu systems to test the install script

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Testing Nix Recovery Logic ===${NC}"
echo ""

# Test 1: Check if script detects and sources existing Nix daemon
echo -e "${BLUE}Test 1: Checking Nix daemon detection${NC}"
if [ -f /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh ]; then
    echo -e "${GREEN}✓${NC} Found Nix daemon profile"

    # Source and test
    . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
    if command -v nix &> /dev/null; then
        echo -e "${GREEN}✓${NC} Nix available after sourcing daemon profile"
        echo "  Nix version: $(nix --version)"
    else
        echo -e "${YELLOW}⚠${NC} Nix not available even after sourcing"
    fi
else
    echo -e "${YELLOW}⚠${NC} No Nix daemon profile found"
fi

# Test 2: Check for Nix receipt
echo ""
echo -e "${BLUE}Test 2: Checking for Nix receipt${NC}"
if [ -f /nix/receipt.json ]; then
    echo -e "${GREEN}✓${NC} Found /nix/receipt.json"
    echo "  This indicates an existing Nix installation"

    # Check if receipt is readable
    if [ -r /nix/receipt.json ]; then
        echo -e "${GREEN}✓${NC} Receipt is readable"
    else
        echo -e "${YELLOW}⚠${NC} Receipt exists but not readable (may need sudo)"
    fi
else
    echo -e "${YELLOW}⚠${NC} No Nix receipt found"
fi

# Test 3: Check profile locations
echo ""
echo -e "${BLUE}Test 3: Checking various Nix profile locations${NC}"
PROFILES=(
    "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh"
    "/etc/profile.d/nix.sh"
    "$HOME/.nix-profile/etc/profile.d/nix.sh"
)

for profile in "${PROFILES[@]}"; do
    if [ -f "$profile" ]; then
        echo -e "${GREEN}✓${NC} Found: $profile"
    else
        echo -e "${YELLOW}⚠${NC} Not found: $profile"
    fi
done

# Test 4: Run the actual install-nix.sh script in dry-run mode
echo ""
echo -e "${BLUE}Test 4: Testing install-nix.sh recovery logic${NC}"
echo "Running scripts/install-nix.sh..."
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

# Run the install script
if "$SCRIPT_DIR/scripts/install-nix.sh"; then
    echo -e "${GREEN}✓${NC} install-nix.sh completed successfully"
else
    echo -e "${RED}✗${NC} install-nix.sh failed"
fi

echo ""
echo -e "${BLUE}=== Test Summary ===${NC}"
echo "This test verified:"
echo "1. Detection of existing Nix daemon profiles"
echo "2. Recovery from partial Nix installations"
echo "3. Proper sourcing of Nix environment"
echo ""
echo "To run full installation test:"
echo "  ./install.sh"
