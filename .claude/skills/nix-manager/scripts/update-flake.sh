#!/usr/bin/env bash
# Update flake inputs and apply changes

set -euo pipefail

FLAKE_DIR="${1:-.}"

echo "📦 Updating Nix flake in: $FLAKE_DIR"
cd "$FLAKE_DIR"

# Verify flake.nix exists
if [[ ! -f "flake.nix" ]]; then
    echo "❌ No flake.nix found in $FLAKE_DIR"
    exit 1
fi

echo ""
echo "1. Checking current lock file status..."
if [[ -f "flake.lock" ]]; then
    echo "   Current nixpkgs revision:"
    grep -A 3 '"nixpkgs"' flake.lock | grep '"rev"' | head -1 || echo "   (unable to parse)"
fi

echo ""
echo "2. Updating flake inputs..."
nix flake update

echo ""
echo "3. New nixpkgs revision:"
grep -A 3 '"nixpkgs"' flake.lock | grep '"rev"' | head -1 || echo "   (unable to parse)"

echo ""
echo "4. Validating flake..."
if nix flake check; then
    echo "   ✅ Flake validation passed"
else
    echo "   ❌ Flake validation failed"
    exit 1
fi

echo ""
echo "5. Showing flake outputs..."
nix flake show

echo ""
echo "✅ Flake updated successfully!"
echo ""
echo "To apply changes:"
echo "  nix profile upgrade dotfiles"
echo ""
echo "To review changes:"
echo "  git diff flake.lock"
