#!/usr/bin/env bash
# setup-hermes-skills.sh
#
# Registers this repo's config/hermes/skills/ directory as a Hermes external
# skills directory by adding it to ~/.hermes/config.yaml under
# skills.external_dirs. Idempotent: running twice is a no-op.
#
# Hermes treats external_dirs as read-only, so git stays the source of truth
# and the Hermes agent cannot mutate dotfile-tracked skills.
#
# Docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/config/hermes/skills"
HERMES_DIR="$HOME/.hermes"
CONFIG="$HERMES_DIR/config.yaml"

echo -e "${BLUE}=== Hermes skills setup ===${NC}"

# 1. Make sure the dotfiles skills directory exists
if [ ! -d "$SKILLS_DIR" ]; then
    echo -e "${YELLOW}⚠${NC}  $SKILLS_DIR does not exist yet — creating empty directory"
    mkdir -p "$SKILLS_DIR"
fi

# 2. If Hermes isn't installed at all, skip silently. This script is
#    non-essential; users who don't use Hermes shouldn't see a failure.
if [ ! -d "$HERMES_DIR" ]; then
    echo -e "${YELLOW}⚠${NC}  $HERMES_DIR not found — Hermes Agent not installed. Skipping."
    echo "   When you install Hermes, re-run this script:"
    echo "     $REPO_ROOT/scripts/setup-hermes-skills.sh"
    exit 0
fi

# 3. Idempotency check: is the skills dir already registered?
#    A literal substring match is sufficient — if the path string appears
#    anywhere in config.yaml, it is almost certainly under external_dirs.
if [ -f "$CONFIG" ] && grep -qF "$SKILLS_DIR" "$CONFIG"; then
    echo -e "${GREEN}✓${NC} $SKILLS_DIR already registered in $CONFIG"
    exit 0
fi

# 4. We need to write. Require yq (Python yq from the flake, version 3.x).
if ! command -v yq >/dev/null 2>&1; then
    echo -e "${RED}✗${NC} yq not found — install nix packages first (scripts/install-packages.sh)"
    exit 1
fi

# 5. Ensure config.yaml exists with at least an empty object so yq can read it.
if [ ! -f "$CONFIG" ]; then
    echo -e "${BLUE}ℹ${NC}  $CONFIG does not exist — creating a minimal one"
    # Start with just the skills block we're about to add. Hermes will fill in
    # the rest on first run.
    cat > "$CONFIG" <<'EOF'
# Hermes Agent configuration
# https://hermes-agent.nousresearch.com/docs/user-guide/configuration
skills:
  external_dirs: []
EOF
fi

# 6. Back up before rewriting — yq (Python) does not preserve comments, and
#    this is a user-owned config file.
BACKUP="$CONFIG.backup.$(date +%s)"
cp "$CONFIG" "$BACKUP"
echo -e "${BLUE}ℹ${NC}  Backed up $CONFIG → $BACKUP"

# 7. Merge: ensure .skills.external_dirs exists as a list, then append our
#    path if missing. Using Python yq syntax (jq filter + YAML I/O via -y).
TMP="$(mktemp)"
# shellcheck disable=SC2016
yq -y --arg p "$SKILLS_DIR" '
    .skills = ((.skills // {}) | .external_dirs = ((.external_dirs // []) |
      if index($p) then . else . + [$p] end))
' "$CONFIG" > "$TMP"

# Sanity check: confirm the path is now present before replacing the original.
if ! grep -qF "$SKILLS_DIR" "$TMP"; then
    echo -e "${RED}✗${NC} yq merge did not produce expected output; refusing to overwrite $CONFIG"
    echo "   Failed output kept at: $TMP"
    echo "   Original is still in place (and backed up at $BACKUP)"
    exit 1
fi

mv "$TMP" "$CONFIG"
echo -e "${GREEN}✓${NC} Added $SKILLS_DIR to skills.external_dirs in $CONFIG"

# 8. Show a hint for verification
if command -v hermes >/dev/null 2>&1; then
    echo ""
    echo -e "${BLUE}Verify with:${NC}"
    echo "  hermes skills list"
fi
