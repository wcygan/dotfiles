#!/usr/bin/env bash
# install-skills.sh
#
# Installs vendor-published agent skills from the open skills ecosystem
# (https://skills.sh/). The CLI keeps the canonical content in
# ~/.agents/skills, which Pi discovers directly.
#
# Uses bunx (bun is provisioned by flake.nix) so this works on a fresh
# install without requiring Node.js. Idempotent: re-running upgrades any
# skills that have new versions and is a no-op for those already current.
#
# To update later: scripts/install-skills.sh --update  (or 'make update-skills')

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Curated list of trusted, official-publisher skills. Add to this list as
# new vendor skills become useful. Format: <owner>/<repo>@<skill>
SKILLS=(
    "astral-sh/claude-code-plugins@uv"
    "planetscale/database-skills@mysql"
    "vercel-labs/portless@portless"
)

MODE="install"
if [[ "${1:-}" == "--update" ]]; then
    MODE="update"
fi

echo -e "${BLUE}=== Vendor skills $MODE ===${NC}"

# Skip gracefully if bun isn't available yet (e.g. install order, or fresh
# system before Nix profile is on PATH). install.sh treats this as non-fatal.
if ! command -v bunx >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠${NC}  bunx not found on PATH — skipping skill $MODE."
    echo "   bun is provided by flake.nix; ensure packages are installed and"
    echo "   the Nix profile is sourced, then re-run:"
    echo "     scripts/install-skills.sh"
    exit 0
fi

# Install/update path: iterate the curated list. The skills CLI handles
# already-installed skills cleanly with -y (skips prompts, upgrades if newer).
# Do not select an agent target: Pi discovers the canonical shared catalog,
# avoiding duplicate ~/.pi/agent/skills links.
FAILED=()
for skill in "${SKILLS[@]}"; do
    echo -e "\n${BLUE}→${NC} $skill"
    if bunx skills add "$skill" -g -y; then
        echo -e "${GREEN}✓${NC} $skill"
    else
        echo -e "${RED}✗${NC} $skill failed"
        FAILED+=("$skill")
    fi
done

echo ""
if [ ${#FAILED[@]} -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All ${#SKILLS[@]} skills installed/updated"
else
    echo -e "${YELLOW}⚠${NC}  ${#FAILED[@]} of ${#SKILLS[@]} skills failed: ${FAILED[*]}"
    exit 1
fi
