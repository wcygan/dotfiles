from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from dotfiles_setup.cleanup import cleanup_links
from dotfiles_setup.doctor import run_doctor
from dotfiles_setup.links import link_config
from dotfiles_setup.nix_profile import NixProfileError, ensure_profile
from dotfiles_setup.rustup import RustupError, setup_rustup

REPO_ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dotfiles-setup",
        description="Install and verify the dotfiles repository.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("doctor", help="Run read-only environment diagnostics")
    subcommands.add_parser("profile", help="Install or upgrade the Nix package profile")
    subcommands.add_parser("rustup", help="Install rust-analyzer for the default toolchain")

    link_parser = subcommands.add_parser("link", help="Link repository configuration")
    link_parser.add_argument("--dry-run", action="store_true", help="Preview filesystem changes")

    uninstall_parser = subcommands.add_parser("uninstall", help="Remove managed symlinks")
    uninstall_parser.add_argument("--dry-run", action="store_true", help="Preview removals")
    uninstall_parser.add_argument("--yes", action="store_true", help="Skip confirmation")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "doctor":
        return run_doctor()
    if args.command == "profile":
        try:
            print(ensure_profile(REPO_ROOT))
        except NixProfileError as error:
            print(f"Profile setup failed: {error}")
            return 1
        return 0
    if args.command == "rustup":
        try:
            resolved_path = setup_rustup()
        except RustupError as error:
            print(f"Rustup setup failed: {error}")
            return 1
        print(f"rust-analyzer resolved to {resolved_path}")
        return 0
    if args.command == "link":
        link_config(REPO_ROOT, dry_run=args.dry_run)
        return 0
    if args.command == "uninstall":
        if not args.dry_run and not args.yes:
            try:
                confirmed = input("Remove symlinks managed by this repository? [y/N] ")
            except EOFError:
                print("Confirmation required; rerun with --yes for non-interactive use.")
                return 2
            if confirmed.lower() != "y":
                print("No changes made.")
                return 0
        cleanup_links(REPO_ROOT, dry_run=args.dry_run)
        return 0

    raise AssertionError(f"Unhandled command: {args.command}")
