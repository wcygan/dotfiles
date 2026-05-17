#!/usr/bin/env bash
set -euo pipefail

if [[ -f /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh ]]; then
  # shellcheck disable=SC1091
  source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
fi

export PATH="$HOME/.nix-profile/bin:/nix/var/nix/profiles/default/bin:$PATH"

if ! command -v rustup >/dev/null 2>&1; then
  echo "rustup not found in PATH; run scripts/install-packages.sh first"
  exit 1
fi

default_toolchain="$(rustup default 2>/dev/null | awk 'NR == 1 { print $1 }' || true)"

if [[ -z "$default_toolchain" ]]; then
  default_toolchain="stable"
  echo "No rustup default toolchain configured; installing $default_toolchain"
  rustup toolchain install "$default_toolchain" --profile default --component rust-analyzer
  rustup default "$default_toolchain"
else
  echo "Ensuring rust-analyzer is installed for $default_toolchain"
  rustup component add rust-analyzer --toolchain "$default_toolchain"
fi

resolved_rust_analyzer="$(
  RUSTUP_TOOLCHAIN="$default_toolchain" rustup which rust-analyzer
)"

echo "rust-analyzer resolved to $resolved_rust_analyzer"
