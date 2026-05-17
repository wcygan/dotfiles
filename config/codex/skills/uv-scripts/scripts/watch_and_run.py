#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "rich>=13,<15",
#   "watchfiles>=0.24,<2",
# ]
# ///
"""Gold-standard watch-and-rerun local automation loop.

Run:
    uv run --script watch_and_run.py --demo
    uv run --script watch_and_run.py src tests -- pytest -q
"""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from watchfiles import Change, watch

console = Console()
error_console = Console(stderr=True)


def run_command(command: list[str]) -> int:
    console.print(f"[cyan]running[/cyan] {shlex.join(command)}")
    result = subprocess.run(command, check=False)
    if result.returncode == 0:
        console.print("[green]command passed[/green]")
    else:
        error_console.print(f"[red]command failed[/red] exit={result.returncode}")
    return result.returncode


def render_changes(changes: set[tuple[Change, str]]) -> None:
    for change, path in sorted(changes, key=lambda item: item[1]):
        console.print(f"[dim]{change.name.lower():>8}[/dim] {path}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watch paths and rerun a command.",
        epilog="Use -- before the command, for example: watch_and_run.py src -- pytest -q",
    )
    parser.add_argument("args", nargs="*", help="Paths followed by -- and command.")
    parser.add_argument("--debounce-ms", type=int, default=500)
    parser.add_argument(
        "--run-initial", action="store_true", help="Run command before watching."
    )
    parser.add_argument(
        "--demo", action="store_true", help="Run a one-shot demo command."
    )
    parsed = parser.parse_args(argv)

    if parsed.demo:
        parsed.paths = [Path.cwd()]
        parsed.command = [sys.executable, "-c", "print('demo command ran')"]
        return parsed

    if "--" not in parsed.args:
        parser.error("expected paths followed by -- and a command")
    separator = parsed.args.index("--")
    parsed.paths = [Path(value) for value in parsed.args[:separator]]
    parsed.command = parsed.args[separator + 1 :]
    if not parsed.paths:
        parser.error("expected at least one path before --")
    if not parsed.command:
        parser.error("expected command after --")
    return parsed


def run(args: argparse.Namespace) -> int:
    missing = [path for path in args.paths if not path.exists()]
    if missing:
        for path in missing:
            error_console.print(f"[red]missing path[/red] {path}")
        return 2

    if args.demo:
        return run_command(args.command)

    if args.run_initial:
        run_command(args.command)

    console.print(
        f"[green]watching[/green] {', '.join(str(path) for path in args.paths)}"
    )
    try:
        for changes in watch(*args.paths, debounce=args.debounce_ms):
            render_changes(changes)
            run_command(args.command)
    except KeyboardInterrupt:
        error_console.print("[red]interrupted[/red]")
        return 130
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except FileNotFoundError as exc:
        error_console.print(f"[red]command not found[/red] {exc.filename}")
        return 127


if __name__ == "__main__":
    raise SystemExit(main())
