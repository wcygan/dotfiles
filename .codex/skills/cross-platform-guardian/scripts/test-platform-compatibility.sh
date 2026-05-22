#!/usr/bin/env bash
# test-platform-compatibility.sh
# Tests Nix flake builds across all supported platforms
# Requires: nix with flakes enabled

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO_ROOT"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🧪 Testing Nix Flake Platform Compatibility"
echo "============================================"
echo ""

PLATFORMS=(
  "x86_64-linux"
  "aarch64-linux"
  "x86_64-darwin"
  "aarch64-darwin"
)

CURRENT_SYSTEM=$(nix eval --impure --raw --expr 'builtins.currentSystem')
echo "Current system: $CURRENT_SYSTEM"
echo ""

FAILED_PLATFORMS=()

for platform in "${PLATFORMS[@]}"; do
  echo "Testing $platform..."

  # Try to build the package for this platform
  if nix build ".#packages.$platform.default" --dry-run 2>/dev/null; then
    echo -e "${GREEN}✅ $platform: Build plan valid${NC}"
  else
    echo -e "${RED}❌ $platform: Build plan failed${NC}"
    FAILED_PLATFORMS+=("$platform")

    # Try to get more details
    echo "  Checking package availability..."
    nix eval ".#packages.$platform.default.name" 2>&1 | head -n5 || true
  fi
  echo ""
done

# Summary
echo "============================================"
if [[ ${#FAILED_PLATFORMS[@]} -eq 0 ]]; then
  echo -e "${GREEN}✅ All platforms pass compatibility checks!${NC}"
  exit 0
else
  echo -e "${RED}❌ Failed platforms:${NC}"
  for platform in "${FAILED_PLATFORMS[@]}"; do
    echo "  - $platform"
  done
  echo ""
  echo "💡 Possible causes:"
  echo "  1. Package not available for this platform in nixpkgs"
  echo "  2. Platform not in flake.nix allSystems list"
  echo "  3. Syntax error in flake.nix"
  echo ""
  echo "🔧 Debugging steps:"
  echo "  nix flake show  # View all outputs"
  echo "  nix eval .#packages.<platform>.default.name  # Check specific platform"
  echo "  nix search nixpkgs <package-name>  # Verify package availability"
  exit 1
fi
