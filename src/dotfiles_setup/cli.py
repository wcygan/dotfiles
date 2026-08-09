from __future__ import annotations

import argparse
from collections.abc import Sequence

from dotfiles_setup.doctor import run_doctor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dotfiles-setup",
        description="Install and verify the dotfiles repository.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("doctor", help="Run read-only environment diagnostics")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "doctor":
        return run_doctor()

    raise AssertionError(f"Unhandled command: {args.command}")
