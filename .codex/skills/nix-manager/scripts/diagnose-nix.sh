#!/usr/bin/env bash
# Diagnose Nix installation health

set -euo pipefail

echo "🔍 Nix Installation Diagnostics"
echo "================================"
echo ""

# Check Nix installation
echo "1. Nix Installation"
if command -v nix &> /dev/null; then
    echo "   ✅ Nix installed: $(nix --version)"
else
    echo "   ❌ Nix not found in PATH"
    exit 1
fi

# Check Nix daemon
echo ""
echo "2. Nix Daemon"
if [[ -d "/nix/var/nix/daemon-socket" ]] || [[ -S "/nix/var/nix/daemon-socket/socket" ]]; then
    echo "   ✅ Nix daemon socket exists"
else
    echo "   ⚠️  Nix daemon socket not found (single-user install?)"
fi

# Check Nix store
echo ""
echo "3. Nix Store"
if [[ -d "/nix/store" ]]; then
    STORE_SIZE=$(du -sh /nix/store 2>/dev/null | cut -f1 || echo "unknown")
    echo "   ✅ Nix store exists: $STORE_SIZE"
else
    echo "   ❌ /nix/store not found"
    exit 1
fi

# Check experimental features
echo ""
echo "4. Experimental Features"
if grep -q "experimental-features.*nix-command.*flakes" ~/.config/nix/nix.conf 2>/dev/null; then
    echo "   ✅ Flakes enabled in user config"
elif nix show-config | grep -q "experimental-features.*nix-command.*flakes"; then
    echo "   ✅ Flakes enabled in system config"
else
    echo "   ❌ Flakes not enabled"
fi

# Check profiles
echo ""
echo "5. Nix Profiles"
if nix profile list &> /dev/null; then
    PROFILE_COUNT=$(nix profile list | wc -l)
    echo "   ✅ Profiles accessible: $PROFILE_COUNT installed"
else
    echo "   ⚠️  No profiles or profile access issue"
fi

# Check binary cache
echo ""
echo "6. Binary Cache Configuration"
if nix show-config | grep -q "cache.nixos.org"; then
    echo "   ✅ Official cache configured"
else
    echo "   ⚠️  Official cache not found"
fi

if nix show-config | grep -q "cache.flakehub.com"; then
    echo "   ✅ FlakeHub cache configured (Determinate Systems)"
else
    echo "   ℹ️  FlakeHub cache not configured"
fi

# Check for flake in current directory
echo ""
echo "7. Current Directory Flake"
if [[ -f "flake.nix" ]]; then
    echo "   ✅ flake.nix found"
    if [[ -f "flake.lock" ]]; then
        echo "   ✅ flake.lock found"
        LAST_MODIFIED=$(grep -A 1 '"lastModified"' flake.lock | head -1 | grep -o '[0-9]*')
        if [[ -n "$LAST_MODIFIED" ]]; then
            LOCK_DATE=$(date -r "$LAST_MODIFIED" 2>/dev/null || date -d "@$LAST_MODIFIED" 2>/dev/null || echo "unknown")
            echo "   ℹ️  Lock file last modified: $LOCK_DATE"
        fi
    else
        echo "   ⚠️  flake.lock missing (run: nix flake update)"
    fi
else
    echo "   ℹ️  No flake.nix in current directory"
fi

# Quick validation
echo ""
echo "8. Quick Validation"
if [[ -f "flake.nix" ]]; then
    if nix flake metadata --no-write-lock-file &> /dev/null; then
        echo "   ✅ Flake metadata accessible"
    else
        echo "   ❌ Flake metadata check failed"
    fi
fi

# Store statistics
echo ""
echo "9. Store Statistics"
if command -v nix &> /dev/null; then
    nix store info || echo "   ⚠️  Unable to get store info"
fi

echo ""
echo "================================"
echo "✅ Diagnostic complete!"
echo ""
echo "For more details:"
echo "  - Check Nix config: nix show-config"
echo "  - List profiles: nix profile list"
echo "  - Store gc dry-run: nix store gc --dry-run"
