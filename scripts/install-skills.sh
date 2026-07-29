#!/usr/bin/env bash
# install-skills.sh
#
# Installs vendor-published agent skills from the open skills ecosystem
# (https://skills.sh/) for pi. The CLI keeps canonical content in
# ~/.agents/skills/ and links only the selected agent target.
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

# Keep .gitignore in sync with the SKILLS array. The skills CLI installs real
# files into ~/.agents/skills/ and symlinks them into the repo-backed Pi skill
# directory. Without these ignores, every vendor symlink shows up as untracked
# and points outside the work tree.
sync_gitignore() {
    local repo_root gitignore tmp begin end
    repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    gitignore="$repo_root/.gitignore"
    [[ -f "$gitignore" ]] || return 0

    begin="# BEGIN vendor-skill-symlinks (managed by scripts/install-skills.sh)"
    end="# END vendor-skill-symlinks"

    tmp="$(mktemp)"
    # Strip any prior managed block; preserve everything else verbatim.
    awk -v B="$begin" -v E="$end" '
        $0 == B { skip = 1; next }
        skip && $0 == E { skip = 0; next }
        !skip { print }
    ' "$gitignore" > "$tmp"

    # Trim trailing blank lines so we re-emit exactly one separator before the block.
    while [[ -s "$tmp" ]] && [[ -z "$(tail -n 1 "$tmp")" ]]; do
        sed -i.bak -e '$d' "$tmp" && rm -f "$tmp.bak"
    done

    {
        cat "$tmp"
        printf '\n%s\n' "$begin"
        printf '%s\n' "# Symlinks created by 'bunx skills add'. Real content lives in ~/.agents/skills/;"
        printf '%s\n' "# the CLI links them into the repo-backed Pi skill directory."
        for skill in "${SKILLS[@]}"; do
            printf 'config/pi/skills/%s\n' "${skill##*@}"
        done
        printf '%s\n' "$end"
    } > "$gitignore"

    rm -f "$tmp"
}

sync_gitignore

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
# Pinning the agent prevents the CLI from recreating ~/.claude/skills.
FAILED=()
for skill in "${SKILLS[@]}"; do
    echo -e "\n${BLUE}→${NC} $skill"
    if bunx skills add "$skill" -g -a pi -y; then
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
