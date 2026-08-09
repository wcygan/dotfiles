#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
echo "install.sh is deprecated; use ./bootstrap.sh instead." >&2
exec "$REPO_ROOT/bootstrap.sh" "$@"
