#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <plan.dot> [output.png]" >&2
  exit 2
fi

dot_file="$1"
out_png="${2:-}"

if [[ ! -f "$dot_file" ]]; then
  echo "File not found: $dot_file" >&2
  exit 2
fi

if ! command -v dot >/dev/null 2>&1; then
  echo "Graphviz 'dot' not found. Install graphviz, then re-run." >&2
  echo "Alternatively: copy DOT contents to a web-based Graphviz renderer." >&2
  exit 1
fi

if [[ -z "$out_png" ]]; then
  dot "$dot_file" -T png -O
else
  dot "$dot_file" -T png -o "$out_png"
fi

