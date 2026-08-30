"""Configure bash and zsh to retain Nix paths and hand interactive shells to fish."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotfiles_setup.errors import ShellHandoffError
from dotfiles_setup.manifest import OperationJournal
from dotfiles_setup.mutations import (
    FileInputState,
    FileMutation,
    MutationExecutionError,
    execute_mutations,
)
from dotfiles_setup.paths import UserPathContext
from dotfiles_setup.scoped_file_input import (
    FileInputOutsideScopeError,
    capture_scoped_file_input,
)

_SETUP_SOURCE = "Python shell-handoff setup"

_BASH_EXEC_FISH = """
if case $- in *i*) true;; *) false;; esac && [ -t 1 ]; then
  if command -v fish >/dev/null 2>&1; then
    exec fish -l
  fi
fi
"""
_BASH_PROFILE_SOURCE_BASHRC = """
# Source .bashrc for login shells
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi"""
_BASH_PROFILE_SOURCE_PROFILE = """
# Source .profile for other env setup (deno, cargo, etc.)
if [ -f ~/.profile ]; then
    . ~/.profile
fi"""
_ZSH_EXEC_FISH = """
if [[ -o interactive && -t 1 ]] && command -v fish >/dev/null 2>&1; then
  exec fish -l
fi
"""
_ZSHENV_PATH = (
    "\n"
    'export PATH="$HOME/.nix-profile/bin:/nix/var/nix/profiles/default/bin:'
    '/opt/homebrew/bin:$HOME/.cargo/bin:$HOME/go/bin:$HOME/.local/bin:$PATH"'
)


@dataclass(frozen=True)
class ShellHandoffResult:
    """The files changed and preserved while configuring a shell handoff."""

    updated_files: tuple[Path, ...]
    backups: tuple[Path, ...]


@dataclass
class _ShellPlan:
    visible_path: Path
    effective_path: Path
    updated: str
    mode: int | None
    precondition: FileInputState


def configure_shell_handoff(
    *,
    home: Path | None = None,
    shell: str | None = None,
    backup_timestamp: int | None = None,
    journal: OperationJournal | None = None,
) -> ShellHandoffResult:
    """Idempotently apply the legacy shell-handoff blocks to a home directory.

    ``home`` and ``shell`` are arguments so callers can configure a temporary
    home without changing process-wide environment variables.  No interactive
    input is requested.
    """
    home_directory = UserPathContext.from_environment(home=home).home
    requested = _requested_shell_blocks(home_directory, shell)
    plans = _plan_shell_files(requested, home_directory)
    mutations = tuple(
        FileMutation(
            destination=plan.effective_path,
            visible_destination=plan.visible_path,
            source="shell-handoff",
            contents=plan.updated.encode(),
            mode=plan.mode,
            precondition=plan.precondition,
        )
        for plan in plans
    )
    try:
        results = execute_mutations(
            mutations,
            journal=journal,
            timestamp=backup_timestamp,
            authority_roots=(home_directory,),
        )
    except MutationExecutionError as error:
        status = "prior files restored" if error.restored else "recovery manifest preserved"
        raise ShellHandoffError(
            f"cannot atomically complete shell handoff: {error}; {status}"
        ) from error
    return ShellHandoffResult(
        tuple(plan.visible_path for plan in plans),
        tuple(result.backup for result in results if result.backup is not None),
    )


def _requested_shell_blocks(
    home: Path,
    shell: str | None,
) -> dict[Path, list[tuple[str, str]]]:
    requested: dict[Path, list[tuple[str, str]]] = {}

    def ensure(path: Path, marker: str, content: str) -> None:
        requested.setdefault(path, []).append((marker, content))

    bashrc = home / ".bashrc"
    ensure(
        bashrc,
        "DOTFILES:NIX_SHELL_HELPERS",
        'source "$HOME/.config/shell-nix.sh" 2>/dev/null || true',
    )
    ensure(bashrc, "DOTFILES:EXEC_FISH", _BASH_EXEC_FISH)
    active_shell = os.environ.get("SHELL", "") if shell is None else shell
    if Path(active_shell).name == "bash":
        bash_profile = home / ".bash_profile"
        ensure(bash_profile, "DOTFILES:BASH_PROFILE_SOURCE_BASHRC", _BASH_PROFILE_SOURCE_BASHRC)
        ensure(bash_profile, "DOTFILES:BASH_PROFILE_SOURCE_PROFILE", _BASH_PROFILE_SOURCE_PROFILE)
    zshrc = home / ".zshrc"
    ensure(
        zshrc,
        "DOTFILES:NIX_SHELL_HELPERS",
        'source "$HOME/.config/shell-nix.sh" 2>/dev/null || true',
    )
    ensure(zshrc, "DOTFILES:EXEC_FISH", _ZSH_EXEC_FISH)
    ensure(home / ".zshenv", "DOTFILES:NIX_PATH", _ZSHENV_PATH)
    return requested


def _plan_shell_files(
    requested: dict[Path, list[tuple[str, str]]],
    home: Path,
) -> list[_ShellPlan]:
    plans: list[_ShellPlan] = []
    for visible_path, blocks in requested.items():
        try:
            selected = capture_scoped_file_input(visible_path, scope_root=home)
            captured = selected.captured
            existing = captured.contents.decode() if captured.contents is not None else ""
        except FileInputOutsideScopeError as error:
            raise ShellHandoffError(
                "shell file symlink resolves outside HOME: "
                f"{error.visible_path} -> {error.effective_path}; "
                "preserved without changes"
            ) from error
        except (MutationExecutionError, OSError) as error:
            raise ShellHandoffError(f"cannot inspect shell file {visible_path}: {error}") from error
        effective_path = selected.effective_path
        updated = existing
        for marker, content in blocks:
            if marker not in updated:
                updated += f"\n# Added by dotfiles {_SETUP_SOURCE} ({marker})\n{content}\n"
        if updated == existing:
            continue
        ancestor = effective_path.parent
        while not ancestor.exists() and ancestor.parent != ancestor:
            ancestor = ancestor.parent
        if not ancestor.is_dir() or not os.access(ancestor, os.W_OK | os.X_OK):
            raise ShellHandoffError(
                f"cannot create or update shell file {visible_path}; "
                f"parent {ancestor} is not writable"
            )
        plans.append(
            _ShellPlan(
                visible_path,
                effective_path,
                updated,
                captured.state.mode,
                captured.state,
            )
        )
    return plans
