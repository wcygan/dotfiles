from __future__ import annotations

import argparse
import os
from collections.abc import Callable, Sequence
from contextlib import suppress
from pathlib import Path

from dotfiles_setup.cleanup import cleanup_links
from dotfiles_setup.doctor import run_doctor
from dotfiles_setup.errors import SetupError
from dotfiles_setup.git_user import GitUserError, configure_git_user
from dotfiles_setup.installer import OperationResult, run_install
from dotfiles_setup.links import link_config
from dotfiles_setup.locking import mutation_lock
from dotfiles_setup.manifest import OperationJournal
from dotfiles_setup.nix_profile import NixProfileError, ensure_profile
from dotfiles_setup.recovery import run_recovery
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
    subcommands.add_parser(
        "rustup", help="Install rust-analyzer for the repository-pinned toolchain"
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

    if args.command == "doctor":
        return run_doctor()
    if args.command == "verify":
        return run_verify(REPO_ROOT)
    if args.command == "profile":
        return _run_mutation("profile", lambda _journal: print(ensure_profile(REPO_ROOT)))
    if args.command == "rustup":
        return _run_mutation("rustup", lambda _journal: print(setup_rustup(REPO_ROOT)))
    if args.command == "link":
        if args.dry_run:
            try:
                link_config(REPO_ROOT, dry_run=True)
            except SetupError as error:
                print(f"Link setup failed: {error}")
                return 1
            return 0
        return _run_mutation("link", lambda journal: link_config(REPO_ROOT, journal=journal))
    if args.command == "recover":
        if args.yes and not args.apply:
            print("Recovery --yes is only valid with --apply.")
            return 2
        if not args.apply:
            try:
                return run_recovery()
            except SetupError as error:
                print(f"Recovery failed: {error}")
                return 1
        try:
            with mutation_lock("recover"):
                return run_recovery(apply=True, yes=args.yes)
        except (SetupError, OSError) as error:
            print(f"Recovery failed: {error}")
            return 1
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
        if args.dry_run:
            try:
                cleanup_links(REPO_ROOT, dry_run=True)
                return 0
            except SetupError as error:
                print(f"Uninstall preview failed: {error}")
                return 1
        return _run_mutation(
            "uninstall",
            lambda journal: cleanup_links(REPO_ROOT, dry_run=False, journal=journal),
        )
    if args.command == "shell-handoff":

        def shell_handoff(journal: OperationJournal) -> None:
            result = configure_shell_handoff(journal=journal)
            journal.record_operation("shell-handoff", "completed")
            print(f"Updated {len(result.updated_files)} shell configuration file(s).")

        return _run_mutation("shell-handoff", shell_handoff)
    if args.command == "git-user":

        def git_user(journal: OperationJournal) -> None:
            result = configure_git_user(
                name=args.name,
                email=args.email,
                remove_global=args.remove_global,
            )
            journal.record_operation("git-user", "completed")
            action = "Updated" if result.updated else "Preserved"
            print(f"{action} Git identity at {result.path}")

        return _run_mutation("git-user", git_user)
    if args.command == "install":

        def link_output(line: str) -> None:
            print(f"[links] {line}")

        try:
            with mutation_lock("install"):
                journal = OperationJournal("install", REPO_ROOT, environ=os.environ)
                journal.transition("applying")

                def observe(result: OperationResult) -> None:
                    status = (
                        "skipped"
                        if result.skipped
                        else "completed"
                        if result.succeeded
                        else "failed"
                    )
                    journal.record_operation(result.name, status)

                exit_code = run_install(
                    profile=lambda: ensure_profile(REPO_ROOT),
                    links=lambda: link_config(REPO_ROOT, output=link_output, journal=journal),
                    rustup=lambda: setup_rustup(REPO_ROOT),
                    shell_handoff=(
                        (lambda: configure_shell_handoff(journal=journal))
                        if args.shell_handoff
                        else None
                    ),
                    verify=lambda: run_verify(REPO_ROOT),
                    observer=observe,
                )
                if journal.data["state"] not in {"failed", "recovery-needed"}:
                    if exit_code == 0:
                        journal.transition("completed")
                    else:
                        operations = journal.data["operations"]
                        assert isinstance(operations, list)
                        mutation_may_be_partial = any(
                            isinstance(operation, dict) and operation.get("status") == "failed"
                            for operation in operations
                        )
                        journal.transition(
                            "recovery-needed" if mutation_may_be_partial else "failed"
                        )
                return exit_code
        except (SetupError, NixProfileError, RustupError, GitUserError, OSError) as error:
            if "journal" in locals() and journal.data["state"] == "applying":
                with suppress(SetupError):
                    journal.transition("recovery-needed")
            print(f"Install failed: {error}")
            return 1

    raise AssertionError(f"Unhandled command: {args.command}")


def _run_mutation(command: str, operation: Callable[[OperationJournal], object]) -> int:
    try:
        with mutation_lock(command):
            journal = OperationJournal(command, REPO_ROOT, environ=os.environ)
            journal.transition("applying")
            operation(journal)
            journal.record_operation(command, "completed")
            journal.transition("completed")
        return 0
    except (SetupError, NixProfileError, RustupError, GitUserError, OSError) as error:
        if "journal" in locals() and journal.data["state"] not in {
            "failed",
            "recovery-needed",
        }:
            try:
                journal.record_operation(command, "failed")
                journal.transition("recovery-needed")
            except SetupError:
                pass
        print(f"{command} failed: {error}")
        return 1
