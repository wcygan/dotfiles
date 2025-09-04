#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

build() {
  local df="$1" tag="$2"
  echo "🧱 Building ${tag} from ${df}…"
  docker build --pull -f "${ROOT}/${df}" -t "${tag}" "${ROOT}"
  echo ""
}

smoke_run() {
  local tag="$1"
  echo "🧪 Smoke run in ${tag} (fish -lc './tests/docker-test-commands.fish')…"
  docker run --rm -e TERM="${TERM:-xterm-256color}" "${tag}" \
    /bin/bash -lc ". /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh && fish -lc './tests/docker-test-commands.fish'"
  echo ""
}

echo "🐳 Docker test matrix start"
echo "==========================="
echo ""

build Dockerfile.ubuntu nixdotfiles:test-ubuntu
smoke_run nixdotfiles:test-ubuntu

build Dockerfile.fedora nixdotfiles:test-fedora
smoke_run nixdotfiles:test-fedora

echo "✅ Matrix ok"
