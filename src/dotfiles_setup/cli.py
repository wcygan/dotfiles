from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from pathlib import Path

from dotfiles_setup.agent_skills import (
    cleanup_legacy_agent_skills,
    install_agent_skills,
    verify_agent_skills,
)
from dotfiles_setup.cleanup import cleanup_links
from dotfiles_setup.doctor import run_doctor
from dotfiles_setup.errors import SetupError
from dotfiles_setup.git_user import configure_git_user
from dotfiles_setup.installer import run_install, run_mutation, run_recovery_workflow
from dotfiles_setup.links import link_config
from dotfiles_setup.nix_profile import ensure_profile
from dotfiles_setup.rustup import setup_rustup
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
    subcommands.add_parser(
        "rustup", help="Install rust-analyzer for the repository-pinned toolchain"
    )

    agent_skills_parser = subcommands.add_parser(
        "agent-skills",
        help="Install the repository-pinned shared Codex user skill catalog",
    )
    agent_skills_parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the pinned shared user skill catalog without changing it",
    )
    agent_skills_parser.add_argument(
        "--cleanup-legacy",
        action="store_true",
        help="Remove the verified legacy Codex user-scope catalog after migration",
    )
    agent_skills_parser.add_argument(
        "--yes",
        action="store_true",
        help="Authorize legacy user-scope skill removal",
    )

    link_parser = subcommands.add_parser("link", help="Link repository configuration")
    link_parser.add_argument("--dry-run", action="store_true", help="Preview filesystem changes")

    uninstall_parser = subcommands.add_parser("uninstall", help="Remove managed symlinks")
    uninstall_parser.add_argument("--dry-run", action="store_true", help="Preview removals")
    uninstall_parser.add_argument("--yes", action="store_true", help="Skip confirmation")

    recover_parser = subcommands.add_parser("recover", help="Inspect interrupted setup recovery")
    recover_parser.add_argument("--apply", action="store_true", help="Apply the recovery plan")
    recover_parser.add_argument("--yes", action="store_true", help="Authorize recovery mutation")

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
    handlers: dict[str, Callable[[argparse.Namespace], int]] = {
        "doctor": lambda _args: run_doctor(),
        "verify": lambda _args: run_verify(REPO_ROOT),
        "profile": lambda _args: run_mutation(
            "profile", REPO_ROOT, lambda _journal: print(ensure_profile(REPO_ROOT))
        ),
        "rustup": lambda _args: run_mutation(
            "rustup", REPO_ROOT, lambda _journal: print(setup_rustup(REPO_ROOT))
        ),
        "agent-skills": _handle_agent_skills,
        "link": _handle_link,
        "recover": _handle_recover,
        "uninstall": _handle_uninstall,
        "shell-handoff": _handle_shell_handoff,
        "git-user": _handle_git_user,
        "install": _handle_install,
    }
    return handlers[args.command](args)


def _handle_agent_skills(args: argparse.Namespace) -> int:
    if args.check and args.cleanup_legacy:
        print("agent-skills --check cannot be combined with --cleanup-legacy.")
        return 2
    if args.yes and not args.cleanup_legacy:
        print("agent-skills --yes is only valid with --cleanup-legacy.")
        return 2
    if args.check:
        try:
            print(verify_agent_skills(REPO_ROOT))
            return 0
        except SetupError as error:
            print(f"agent-skills check failed: {error}")
            return 1
    if args.cleanup_legacy:
        if not args.yes:
            print("Legacy cleanup requires --yes.")
            return 2
        return run_mutation(
            "agent-skills",
            REPO_ROOT,
            lambda _journal: print(cleanup_legacy_agent_skills(REPO_ROOT)),
        )
    return run_mutation(
        "agent-skills", REPO_ROOT, lambda _journal: print(install_agent_skills(REPO_ROOT))
    )


def _handle_link(args: argparse.Namespace) -> int:
    if args.dry_run:
        try:
            link_config(REPO_ROOT, dry_run=True)
        except SetupError as error:
            print(f"Link setup failed: {error}")
            return 1
        return 0
    return run_mutation(
        "link", REPO_ROOT, lambda journal: link_config(REPO_ROOT, journal=journal)
    )


def _handle_recover(args: argparse.Namespace) -> int:
    if args.yes and not args.apply:
        print("Recovery --yes is only valid with --apply.")
        return 2
    return run_recovery_workflow(apply=args.apply, yes=args.yes)


def _handle_uninstall(args: argparse.Namespace) -> int:
    if not args.dry_run and not args.yes:
        try:
            confirmed = input("Remove symlinks managed by this repository? [y/N] ")
        except EOFError:
            print("Confirmation required; rerun with --yes for non-interactive use.")
            return 2
        if confirmed.lower() != "y":
            print("No changes made.")
            return 0
    if args.dry_run:
        try:
            cleanup_links(REPO_ROOT, dry_run=True)
            return 0
        except SetupError as error:
            print(f"Uninstall preview failed: {error}")
            return 1
    return run_mutation(
        "uninstall",
        REPO_ROOT,
        lambda journal: cleanup_links(REPO_ROOT, dry_run=False, journal=journal),
    )


def _handle_shell_handoff(_args: argparse.Namespace) -> int:
    def shell_handoff(journal: object) -> None:
        result = configure_shell_handoff(journal=journal)
        print(f"Updated {len(result.updated_files)} shell configuration file(s).")

    return run_mutation("shell-handoff", REPO_ROOT, shell_handoff)


def _handle_git_user(args: argparse.Namespace) -> int:
    def git_user(_journal: object) -> None:
        result = configure_git_user(
            name=args.name,
            email=args.email,
            remove_global=args.remove_global,
        )
        action = "Updated" if result.updated else "Preserved"
        print(f"{action} Git identity at {result.path}")

    return run_mutation("git-user", REPO_ROOT, git_user)


def _handle_install(args: argparse.Namespace) -> int:
    return run_install(REPO_ROOT, shell_handoff=args.shell_handoff)
