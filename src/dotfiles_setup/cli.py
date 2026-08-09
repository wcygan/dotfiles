from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from dotfiles_setup.cleanup import cleanup_links
from dotfiles_setup.doctor import run_doctor
from dotfiles_setup.git_user import GitUserError, configure_git_user
from dotfiles_setup.installer import run_install
from dotfiles_setup.links import link_config
from dotfiles_setup.nix_profile import NixProfileError, ensure_profile
from dotfiles_setup.rustup import RustupError, setup_rustup
from dotfiles_setup.shell_handoff import configure_shell_handoff
from dotfiles_setup.verify import run_verify

REPO_ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dotfiles-setup",
        description="Install and verify the dotfiles repository.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("doctor", help="Run read-only environment diagnostics")
    subcommands.add_parser("verify", help="Verify the configured environment")
    subcommands.add_parser("profile", help="Install or upgrade the Nix package profile")
    subcommands.add_parser("rustup", help="Install rust-analyzer for the default toolchain")

    link_parser = subcommands.add_parser("link", help="Link repository configuration")
    link_parser.add_argument("--dry-run", action="store_true", help="Preview filesystem changes")

    uninstall_parser = subcommands.add_parser("uninstall", help="Remove managed symlinks")
    uninstall_parser.add_argument("--dry-run", action="store_true", help="Preview removals")
    uninstall_parser.add_argument("--yes", action="store_true", help="Skip confirmation")

    subcommands.add_parser(
        "shell-handoff",
        help="Configure interactive Bash and zsh sessions to launch Fish",
    )

    git_user_parser = subcommands.add_parser("git-user", help="Configure local Git identity")
    git_user_parser.add_argument("--name", help="Git user name for non-interactive setup")
    git_user_parser.add_argument("--email", help="Git email for non-interactive setup")
    git_user_parser.add_argument(
        "--remove-global",
        action="store_const",
        const=True,
        default=None,
        help="Remove redundant global Git identity after writing the local file",
    )

    install_parser = subcommands.add_parser("install", help="Run the complete setup workflow")
    install_parser.add_argument(
        "--shell-handoff",
        action="store_true",
        help="Opt in to editing Bash and zsh startup files",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "doctor":
        return run_doctor()
    if args.command == "verify":
        return run_verify(REPO_ROOT)
    if args.command == "profile":
        try:
            print(ensure_profile(REPO_ROOT))
        except NixProfileError as error:
            print(f"Profile setup failed: {error}")
            return 1
        return 0
    if args.command == "rustup":
        try:
            result = setup_rustup(REPO_ROOT)
        except RustupError as error:
            print(f"Rustup setup failed: {error}")
            return 1
        print(result)
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
    if args.command == "shell-handoff":
        try:
            result = configure_shell_handoff()
        except OSError as error:
            print(f"Shell handoff setup failed: {error}")
            return 1
        print(f"Updated {len(result.updated_files)} shell configuration file(s).")
        return 0
    if args.command == "git-user":
        try:
            result = configure_git_user(
                name=args.name,
                email=args.email,
                remove_global=args.remove_global,
            )
        except GitUserError as error:
            print(f"Git identity setup failed: {error}")
            return 1
        action = "Updated" if result.updated else "Preserved"
        print(f"{action} Git identity at {result.path}")
        return 0
    if args.command == "install":

        def link_output(line: str) -> None:
            print(f"[links] {line}")

        return run_install(
            profile=lambda: ensure_profile(REPO_ROOT),
            links=lambda: link_config(REPO_ROOT, output=link_output),
            rustup=lambda: setup_rustup(REPO_ROOT),
            shell_handoff=configure_shell_handoff if args.shell_handoff else None,
            verify=lambda: run_verify(REPO_ROOT),
        )

    raise AssertionError(f"Unhandled command: {args.command}")
