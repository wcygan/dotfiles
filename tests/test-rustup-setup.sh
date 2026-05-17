#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pass() {
    echo "✓ $1"
}

fail() {
    echo "✗ $1"
    exit 1
}

echo "Rustup setup integration test"
echo "============================="
echo ""

if grep -qE '^\s+rustup\s*$' "$ROOT/flake.nix"; then
    pass "rustup is defined in flake.nix"
else
    fail "rustup is missing from flake.nix"
fi

if [[ -x "$ROOT/scripts/setup-rustup-components.sh" ]]; then
    pass "setup-rustup-components.sh is executable"
else
    fail "setup-rustup-components.sh is missing or not executable"
fi

if grep -q 'rustup component add rust-analyzer' "$ROOT/scripts/setup-rustup-components.sh"; then
    pass "setup script installs the rust-analyzer component"
else
    fail "setup script does not install the rust-analyzer component"
fi

if grep -q 'rustup toolchain install "$default_toolchain" --profile default --component rust-analyzer' "$ROOT/scripts/setup-rustup-components.sh"; then
    pass "setup script bootstraps stable with rust-analyzer when no default exists"
else
    fail "setup script does not bootstrap stable with rust-analyzer"
fi

if grep -q 'scripts/setup-rustup-components.sh' "$ROOT/install.sh"; then
    pass "install.sh runs Rust component setup"
else
    fail "install.sh does not run Rust component setup"
fi

if grep -q 'rustup which rust-analyzer' "$ROOT/install.sh"; then
    pass "install.sh verifies rust-analyzer through rustup"
else
    fail "install.sh does not verify rust-analyzer through rustup"
fi

if grep -q 'setup-rustup-components:' "$ROOT/Makefile"; then
    pass "Makefile exposes setup-rustup-components target"
else
    fail "Makefile missing setup-rustup-components target"
fi

echo ""
echo "All rustup setup checks passed."
