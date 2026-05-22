#!/usr/bin/env bash
# audit-compatibility.sh
# Scans dotfiles repository for cross-platform compatibility issues
# Exit code: 0 = no issues, 1 = issues found

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO_ROOT"

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

ISSUES_FOUND=0

echo "🔍 Cross-Platform Compatibility Audit"
echo "======================================="
echo ""

# Check 1: Hardcoded user paths
echo "📁 Checking for hardcoded paths..."
HARDCODED_PATHS=$(grep -r "/Users/wcygan" scripts/ config/ 2>/dev/null || true)
if [[ -n "$HARDCODED_PATHS" ]]; then
  echo -e "${RED}❌ Found hardcoded user paths:${NC}"
  echo "$HARDCODED_PATHS" | while read -r line; do
    echo "  $line"
  done
  ISSUES_FOUND=1
else
  echo -e "${GREEN}✅ No hardcoded user paths${NC}"
fi
echo ""

# Check 2: Platform-specific commands without conditionals
echo "🖥️  Checking for platform-specific commands..."
MACOS_OPEN=$(grep -rn "open " scripts/ | grep -v "xdg-open" | grep -v "#" | grep -v "opener" || true)
if [[ -n "$MACOS_OPEN" ]]; then
  echo -e "${YELLOW}⚠️  Found 'open' command (macOS-specific):${NC}"
  echo "$MACOS_OPEN" | while read -r line; do
    echo "  $line"
  done
  echo "  💡 Consider: if [[ \$OSTYPE == darwin* ]]; then open; else xdg-open; fi"
  ISSUES_FOUND=1
else
  echo -e "${GREEN}✅ No unguarded platform-specific commands${NC}"
fi
echo ""

# Check 3: Shebang correctness
echo "🔧 Checking shebang lines..."
WRONG_SHEBANG=$(find scripts/ -type f -name "*.sh" -exec sh -c '
  for file; do
    if head -n1 "$file" | grep -q "^#!/bin/sh"; then
      if grep -q "declare -a\|local -a\|\[\[" "$file"; then
        echo "$file: Uses bash features with #!/bin/sh"
      fi
    fi
  done
' sh {} + || true)

if [[ -n "$WRONG_SHEBANG" ]]; then
  echo -e "${RED}❌ Found bash-isms in sh scripts:${NC}"
  echo "$WRONG_SHEBANG" | while read -r line; do
    echo "  $line"
  done
  echo "  💡 Change shebang to: #!/usr/bin/env bash"
  ISSUES_FOUND=1
else
  echo -e "${GREEN}✅ Shebang lines correct${NC}"
fi
echo ""

# Check 4: Fish configs assume tools exist
echo "🐟 Checking Fish configs for missing guards..."
UNGUARDED_FISH=$(find config/fish -name "*.fish" -exec sh -c '
  for file; do
    # Check for common tools without type -q guard
    if grep -q "eval (starship init fish)" "$file" && ! grep -B2 "eval (starship init fish)" "$file" | grep -q "type -q starship"; then
      echo "$file: starship init without guard"
    fi
    if grep -q "eval (direnv hook fish)" "$file" && ! grep -B2 "eval (direnv hook fish)" "$file" | grep -q "type -q direnv"; then
      echo "$file: direnv hook without guard"
    fi
  done
' sh {} + || true)

if [[ -n "$UNGUARDED_FISH" ]]; then
  echo -e "${YELLOW}⚠️  Found unguarded tool usage in Fish configs:${NC}"
  echo "$UNGUARDED_FISH" | while read -r line; do
    echo "  $line"
  done
  echo "  💡 Add: if type -q <tool>; <command>; end"
  ISSUES_FOUND=1
else
  echo -e "${GREEN}✅ Fish configs properly guarded${NC}"
fi
echo ""

# Check 5: Nix flake has all architectures
echo "📦 Checking Nix flake architecture support..."
if [[ -f flake.nix ]]; then
  REQUIRED_SYSTEMS=("x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin")
  MISSING_SYSTEMS=()

  for sys in "${REQUIRED_SYSTEMS[@]}"; do
    if ! grep -q "\"$sys\"" flake.nix; then
      MISSING_SYSTEMS+=("$sys")
    fi
  done

  if [[ ${#MISSING_SYSTEMS[@]} -gt 0 ]]; then
    echo -e "${RED}❌ Missing architecture support:${NC}"
    for sys in "${MISSING_SYSTEMS[@]}"; do
      echo "  $sys"
    done
    ISSUES_FOUND=1
  else
    echo -e "${GREEN}✅ All required architectures supported${NC}"
  fi
else
  echo -e "${YELLOW}⚠️  No flake.nix found${NC}"
fi
echo ""

# Check 6: CI matrix coverage
echo "🔄 Checking CI test matrix..."
if [[ -f .github/workflows/ci.yml ]]; then
  CI_PLATFORMS=$(grep -A5 "matrix:" .github/workflows/ci.yml | grep "os:" || true)

  if echo "$CI_PLATFORMS" | grep -q "ubuntu" && echo "$CI_PLATFORMS" | grep -q "macos"; then
    echo -e "${GREEN}✅ CI tests both Ubuntu and macOS${NC}"
  else
    echo -e "${YELLOW}⚠️  CI may be missing platform coverage${NC}"
    ISSUES_FOUND=1
  fi

  # Check for Docker matrix
  if grep -q "docker-matrix" .github/workflows/ci.yml; then
    echo -e "${GREEN}✅ Docker matrix tests configured${NC}"
  else
    echo -e "${YELLOW}⚠️  No Docker matrix found in CI${NC}"
    ISSUES_FOUND=1
  fi
else
  echo -e "${YELLOW}⚠️  No CI workflow found${NC}"
fi
echo ""

# Summary
echo "======================================="
if [[ $ISSUES_FOUND -eq 0 ]]; then
  echo -e "${GREEN}✅ All compatibility checks passed!${NC}"
  exit 0
else
  echo -e "${RED}❌ Compatibility issues found - review above${NC}"
  echo ""
  echo "💡 Quick fixes:"
  echo "  1. Replace hardcoded paths with dynamic detection"
  echo "  2. Add platform conditionals for OS-specific commands"
  echo "  3. Fix shebang lines for bash scripts"
  echo "  4. Add 'type -q' guards in Fish configs"
  echo "  5. Update flake.nix to support all architectures"
  exit 1
fi
