# Authoring Workflow

Use this reference when deciding how a uv-backed Python script should be created, run, and shaped for maintainers.

## Script Shape Decision

| Situation | Prefer | Command |
| --- | --- | --- |
| No third-party dependencies | Plain `.py` script | `uv run --no-project script.py` |
| Quick experiment with one dependency | Per-invocation dependency | `uv run --with rich --no-project script.py` |
| Reusable script with dependencies | PEP 723 inline metadata | `uv add --script script.py rich` then `uv run --script script.py` |
| Script should be executable from shell | uv shebang plus inline metadata | `./script-name` |
| Needs the repo package and project deps | Project command | `uv run python -m package.module` or the repo's existing task |
| Must run in CI predictably | Inline metadata plus lockfile | `uv lock --script script.py` |
| One-off shell-piped Python | stdin script | `uv run --no-project -` |

Use `--no-project` when a script lives inside a repo but should not install the current project or inherit its dependencies.

## Maintainable Script Skeleton

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Do one clear job.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def run(input_path: Path, output_path: Path | None) -> int:
    if not input_path.exists():
        print(f"missing input: {input_path}", file=sys.stderr)
        return 2

    # Keep the main path boring: read, transform, write/report.
    text = input_path.read_text()
    result = text.strip()

    if output_path is None:
        print(result)
    else:
        output_path.write_text(result + "\n")

    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    return run(args.input, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
```

## Authoring Rules

- Start with `argparse` unless the CLI has subcommands, rich validation, prompts, or completion needs.
- Keep business logic in functions that can be imported and tested without spawning a process.
- Use `Path` for filesystem inputs and avoid hard-coded home directories, absolute machine paths, and implicit cwd assumptions.
- Print machine-readable output when the script feeds another tool; use pretty terminal output only for human-facing scripts.
- Put errors on stderr and return explicit exit codes.
- Use network timeouts and handle non-2xx responses deliberately.
- Write files atomically when partial output would be harmful: write to a temp file in the same directory, then replace.
- Make reruns idempotent. Existing output should be overwritten intentionally, skipped intentionally, or backed up explicitly.
- Keep the single blessed run command in the script header comment, README, `Justfile`, or surrounding handoff.

## Common Command Forms

```sh
# Plain script, isolated from any project in the cwd.
uv run --no-project script.py input.txt

# One-off dependency without committing metadata.
uv run --with rich --no-project script.py input.txt

# Create metadata, then add reusable dependencies.
uv init --script script.py --python 3.12
uv add --script script.py httpx rich

# Run a metadata-bearing script.
uv run --script script.py input.txt

# Run a short stdin script.
uv run --no-project - <<'PY'
print("hello")
PY
```

## Source

- https://docs.astral.sh/uv/guides/scripts/
