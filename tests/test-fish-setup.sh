#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🐠 Fish Configuration Integration Test"
echo "======================================"
echo ""

PASS_COUNT=0
FAIL_COUNT=0
WARNINGS=""

pass() {
    echo -e "${GREEN}✓${NC} $1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    WARNINGS="${WARNINGS}\n  - FAILED: $1"
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS="${WARNINGS}\n  - $1"
}

section() {
    echo ""
    echo "[$1]"
    echo "---"
}

# Test 1: Check fish is in flake.nix
section "Nix Package Definition"
if grep -qE '^\s+fish\s*$' ../flake.nix; then
    pass "fish is defined in flake.nix"
else
    fail "fish is NOT in flake.nix - need to add it"
fi

if grep -qE '^\s+nodejs\s*$' ../flake.nix; then
    pass "nodejs is defined in flake.nix for npm"
else
    fail "nodejs is NOT in flake.nix - npm will be unavailable"
fi

if grep -q 'self.packages.${pkgs.stdenv.hostPlatform.system}.default' ../flake.nix; then
    pass "dev shell includes the default package set"
else
    fail "dev shell missing default package set - direnv may not expose npm"
fi

# Test 2: Check fish config structure
section "Fish Config Structure"
EXPECTED_FILES=(
    "../config/fish/config.fish"
    "../config/fish/conf.d/10-nix.fish"
    "../config/fish/conf.d/20-direnv.fish"
    "../config/fish/conf.d/30-starship.fish"
    "../config/fish/functions/nix-try.fish"
    "../config/fish/functions/nix-install.fish"
    "../config/fish/functions/qmd.fish"
)

for file in "${EXPECTED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        pass "$file exists"
    else
        fail "$file missing"
    fi
done

# Test 3: Validate fish syntax (if fish is available)
section "Fish Syntax Validation"
if command -v fish &> /dev/null; then
    # Use find to recursively locate fish files, excluding broken symlinks
    while IFS= read -r -d '' file; do
        # Skip broken symlinks (e.g., OrbStack completions on non-macOS)
        if [[ -L "$file" ]] && [[ ! -e "$file" ]]; then
            warn "$(basename "$file") is a broken symlink (skipping)"
            continue
        fi

        if fish -n "$file" 2>/dev/null; then
            pass "$(basename "$file") syntax valid"
        else
            fail "$(basename "$file") has syntax errors"
        fi
    done < <(find ../config/fish -name "*.fish" \( -type f -o -type l \) -print0)
else
    warn "fish not installed yet - can't validate syntax"
fi

# Test 4: Check link-config.sh will link fish
section "Symlink Configuration"
if grep -q 'link "$CFG_SRC/fish"' ../scripts/link-config.sh; then
    pass "link-config.sh configured to symlink fish"
else
    fail "link-config.sh missing fish symlink command"
fi

if [[ -d "../config/codex/skills" ]]; then
    pass "config/codex/skills exists for Codex skills"
else
    fail "config/codex/skills missing"
fi

if grep -q 'GGML_METAL_NO_RESIDENCY=1' ../config/fish/functions/qmd.fish && \
   grep -q 'GGML_METAL_TENSOR_DISABLE=1' ../config/fish/functions/qmd.fish && \
   grep -q 'command qmd' ../config/fish/functions/qmd.fish; then
    pass "qmd fish wrapper applies stable macOS Metal settings"
else
    fail "qmd fish wrapper missing stable macOS Metal settings"
fi

if [[ -f "../config/codex/config.toml" ]]; then
    pass "config/codex/config.toml exists as the Codex config template"
else
    fail "config/codex/config.toml missing"
fi

if [[ -f "../config/codex/AGENTS.md" ]]; then
    pass "config/codex/AGENTS.md exists for global Codex instructions"
else
    fail "config/codex/AGENTS.md missing"
fi

if grep -q 'link_codex_skills' ../scripts/link-config.sh && \
   grep -q 'CODEX_HOME' ../scripts/link-config.sh; then
    pass "link-config.sh configured to symlink Codex skills"
else
    fail "link-config.sh missing Codex skills symlink command"
fi

if grep -q 'install_codex_config_toml' ../scripts/link-config.sh && \
   grep -q 'Preserved existing local Codex config' ../scripts/link-config.sh; then
    pass "link-config.sh configured to install local Codex config.toml"
else
    fail "link-config.sh missing Codex config.toml install command"
fi

if grep -q 'link_codex_agents_md' ../scripts/link-config.sh && \
   grep -q 'AGENTS.md' ../scripts/link-config.sh; then
    pass "link-config.sh configured to symlink global Codex instructions"
else
    fail "link-config.sh missing Codex AGENTS.md symlink command"
fi

# Test 5: Check for potential conflicts
section "Conflict Detection"
if [[ -e "$HOME/.config/fish" ]]; then
    if [[ -L "$HOME/.config/fish" ]]; then
        TARGET=$(readlink "$HOME/.config/fish")
        warn "~/.config/fish exists as symlink → $TARGET (will be replaced)"
    else
        warn "~/.config/fish exists as directory (will be backed up)"
    fi
else
    pass "No existing ~/.config/fish - clean install"
fi

# Test 6: Check Nix environment
section "Nix Environment"
if command -v nix &> /dev/null; then
    pass "Nix is installed"

    if [[ -d "$HOME/.nix-profile" ]]; then
        pass "Nix profile directory exists"
    else
        warn "Nix profile directory missing - might be multi-user install"
    fi

    if [[ -f "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh" ]]; then
        pass "Nix daemon profile script found (multi-user)"
    else
        warn "No Nix daemon script - likely single-user install"
    fi
else
    fail "Nix not installed - install.sh needs to run first"
fi

if grep -q 'fish_add_path --path --move --prepend $HOME/.nix-profile/bin' ../config/fish/conf.d/10-nix.fish && \
   grep -q 'fish_add_path --path --move --prepend /nix/var/nix/profiles/default/bin' ../config/fish/conf.d/10-nix.fish; then
    pass "fish prefers Nix profile paths"
else
    fail "fish does not prefer Nix profile paths"
fi

if grep -q 'fish_add_path --path --move --prepend $HOME/.tiup/bin' ../config/fish/conf.d/10-nix.fish && \
   grep -q 'test -d $HOME/.tiup/bin; and set new_path $HOME/.tiup/bin $new_path' ../config/fish/functions/fix-paths.fish; then
    pass "fish includes TiUP binaries in PATH"
else
    fail "fish does not include TiUP binaries in PATH"
fi

bun_path_line="$(grep -nF 'fish_add_path --path --move --prepend $HOME/.bun/bin' ../config/fish/conf.d/10-nix.fish | cut -d: -f1)"
local_path_line="$(grep -nF 'fish_add_path --path --move --prepend $HOME/.local/bin' ../config/fish/conf.d/10-nix.fish | cut -d: -f1)"
bun_repair_line="$(grep -nF 'test -d $HOME/.bun/bin; and set new_path $HOME/.bun/bin $new_path' ../config/fish/functions/fix-paths.fish | cut -d: -f1)"
local_repair_line="$(grep -nF 'test -d $HOME/.local/bin; and set new_path $HOME/.local/bin $new_path' ../config/fish/functions/fix-paths.fish | cut -d: -f1)"

if [[ -n "$bun_path_line" && -n "$local_path_line" && "$bun_path_line" -lt "$local_path_line" && \
      -n "$bun_repair_line" && -n "$local_repair_line" && "$bun_repair_line" -lt "$local_repair_line" ]]; then
    pass "fish prefers the repo-managed npm prefix over Bun for duplicate CLIs"
else
    fail "fish does not prefer ~/.local/bin over ~/.bun/bin"
fi

# Test 7: Check other tools in flake
section "Companion Tools"
for tool in direnv starship; do
    if grep -qE "^\s+${tool}\s*$" ../flake.nix; then
        pass "$tool is in flake.nix"
    else
        warn "$tool not in flake.nix (optional but recommended)"
    fi
done

# Test 8: Dry run the symlink
section "Symlink Dry Run"
echo "Would create symlinks:"
echo "  ~/.config/fish → $(dirname $(pwd))/config/fish"
echo "  ~/.config/shell-nix.sh → $(dirname $(pwd))/config/shell-nix.sh"
echo "  \${CODEX_HOME:-~/.codex}/config.toml copied from $(dirname $(pwd))/config/codex/config.toml if missing"
echo "  \${CODEX_HOME:-~/.codex}/AGENTS.md → $(dirname $(pwd))/config/codex/AGENTS.md"
echo "  \${CODEX_HOME:-~/.codex}/skills → $(dirname $(pwd))/config/codex/skills"

if [[ -e "$HOME/.config/fish" ]]; then
    if [[ -L "$HOME/.config/fish" ]]; then
        echo "  (replacing existing symlink)"
    else
        echo "  (backing up existing directory to ~/.config/fish.backup.$(date +%s))"
    fi
fi

# Test 9: Check .envrc
section "Direnv Configuration"
if [[ -f "../.envrc" ]]; then
    if grep -q "use flake" ../.envrc; then
        pass ".envrc configured for flake"
    else
        warn ".envrc exists but doesn't use flake"
    fi
else
    warn "No .envrc file - direnv won't auto-activate"
fi

# Summary
echo ""
echo "======================================"
echo "Test Summary"
echo "======================================"
echo -e "${GREEN}Passed:${NC} $PASS_COUNT"
echo -e "${RED}Failed:${NC} $FAIL_COUNT"

if [[ -n "$WARNINGS" ]]; then
    echo -e "${YELLOW}Warnings:${NC}$WARNINGS"
fi

echo ""
if [[ $FAIL_COUNT -eq 0 ]]; then
    echo -e "${GREEN}✓ All critical tests passed!${NC}"
    echo ""
    echo "Ready to install. Run:"
    echo "  ../scripts/link-config.sh  # Create symlinks"
    echo "  exec fish -l              # Start fish session"
    echo ""
    echo "Or for full setup:"
    echo "  ../install.sh              # Full installation"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Fix issues before installing.${NC}"
    exit 1
fi
