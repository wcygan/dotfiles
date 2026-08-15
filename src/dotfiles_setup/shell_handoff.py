"""Configure bash and zsh to retain Nix paths and hand interactive shells to fish."""

from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from dotfiles_setup.errors import ManifestError, ShellHandoffError
from dotfiles_setup.manifest import OperationJournal

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
    existing: str
    updated: str
    mode: int | None
    backup: Path | None
    prior_kind: str
    prior_hash: str | None
    result_hash: str
    journal_index: int | None = None


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
    home_directory = (Path.home() if home is None else home).expanduser()
    suffix = int(time.time()) if backup_timestamp is None else backup_timestamp
    requested = _requested_shell_blocks(home_directory, shell)
    plans = _plan_shell_files(requested, home_directory, suffix)
    _journal_shell_plans(plans, journal)
    staged = _stage_shell_plans(plans)
    updated_files, backups = _apply_shell_plans(staged, journal=journal)
    return ShellHandoffResult(tuple(updated_files), tuple(backups))


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
    suffix: int,
) -> list[_ShellPlan]:
    plans: list[_ShellPlan] = []
    home_scope = home.resolve()
    for visible_path, blocks in requested.items():
        effective_path = (
            visible_path.resolve(strict=False) if visible_path.is_symlink() else visible_path
        )
        if not effective_path.is_relative_to(home_scope):
            raise ShellHandoffError(
                f"shell file symlink resolves outside HOME: {visible_path} -> {effective_path}; "
                "preserved without changes"
            )
        try:
            existing = effective_path.read_text() if effective_path.exists() else ""
            mode = effective_path.stat().st_mode & 0o777 if effective_path.exists() else None
        except OSError as error:
            raise ShellHandoffError(f"cannot inspect shell file {visible_path}: {error}") from error
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
        backup = None
        prior_kind = "absent"
        prior_hash = None
        if effective_path.exists() and effective_path.is_file():
            backup = _backup_path(effective_path, suffix)
            prior_kind = "file"
            prior_hash = _content_hash(existing)
        plans.append(
            _ShellPlan(
                visible_path,
                effective_path,
                existing,
                updated,
                mode,
                backup,
                prior_kind,
                prior_hash,
                _content_hash(updated),
            )
        )
    return plans


def _journal_shell_plans(
    plans: list[_ShellPlan],
    journal: OperationJournal | None,
) -> None:
    if journal is None:
        return
    for plan in plans:
        plan.journal_index = journal.add_link_entry(
            {
                "entry_type": "file",
                "destination": str(plan.effective_path),
                "visible_destination": str(plan.visible_path),
                "source": "shell-handoff",
                "prior_kind": plan.prior_kind,
                "prior_target": None,
                "prior_hash": plan.prior_hash,
                "backup": str(plan.backup) if plan.backup is not None else None,
                "result_kind": "file",
                "result_target": None,
                "result_hash": plan.result_hash,
                "mutation_started": False,
                "applied": False,
                "recovered": False,
            }
        )


def _stage_shell_plans(plans: list[_ShellPlan]) -> list[tuple[_ShellPlan, Path, int, int]]:
    staged: list[tuple[_ShellPlan, Path, int, int]] = []
    try:
        for plan in plans:
            plan.effective_path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{plan.effective_path.name}.handoff.",
                dir=plan.effective_path.parent,
            )
            temporary = Path(temporary_name)
            identity = os.fstat(descriptor)
            staged.append((plan, temporary, identity.st_dev, identity.st_ino))
            with os.fdopen(descriptor, "w") as file:
                file.write(plan.updated)
                file.flush()
                os.fsync(file.fileno())
            if plan.mode is not None:
                temporary.chmod(plan.mode)
    except OSError as error:
        for _plan, temporary, device, inode in staged:
            _unlink_owned_temporary(temporary, device=device, inode=inode)
        raise ShellHandoffError(f"cannot stage shell handoff update: {error}") from error
    return staged


def _apply_shell_plans(
    staged: list[tuple[_ShellPlan, Path, int, int]],
    *,
    journal: OperationJournal | None,
) -> tuple[list[Path], list[Path]]:
    updated_files: list[Path] = []
    backups: list[Path] = []
    applied: list[_ShellPlan] = []
    moved_temporaries: set[Path] = set()
    try:
        for plan, temporary, _device, _inode in staged:
            if journal is not None and plan.journal_index is not None:
                journal.update_link_entry(plan.journal_index, mutation_started=True)
            if plan.backup is not None:
                if plan.backup.exists() or plan.backup.is_symlink():
                    raise ShellHandoffError(
                        f"shell backup path appeared before apply: {plan.backup}"
                    )
                shutil.copy2(plan.effective_path, plan.backup)
                backups.append(plan.backup)
            os.replace(temporary, plan.effective_path)
            moved_temporaries.add(temporary)
            applied.append(plan)
            if journal is not None and plan.journal_index is not None:
                journal.update_link_entry(plan.journal_index, applied=True)
            updated_files.append(plan.visible_path)
    except (OSError, ManifestError, ShellHandoffError) as error:
        rolled_back = _rollback_shell_plans(applied, journal=journal)
        if journal is not None:
            journal.transition("failed" if rolled_back else "recovery-needed")
        raise ShellHandoffError(
            f"cannot atomically complete shell handoff: {error}; "
            f"{'prior files restored' if rolled_back else 'recovery manifest preserved'}"
        ) from error
    finally:
        for _plan, temporary, device, inode in staged:
            if temporary not in moved_temporaries:
                _unlink_owned_temporary(temporary, device=device, inode=inode)
    return updated_files, backups


def _content_hash(contents: str) -> str:
    return hashlib.sha256(contents.encode()).hexdigest()


def _unlink_owned_temporary(path: Path, *, device: int, inode: int) -> None:
    try:
        metadata = path.lstat()
        if metadata.st_dev == device and metadata.st_ino == inode:
            path.unlink()
    except OSError:
        return


def _rollback_shell_plans(applied: list[_ShellPlan], *, journal: OperationJournal | None) -> bool:
    complete = True
    for plan in reversed(applied):
        try:
            current = plan.effective_path.read_text() if plan.effective_path.exists() else None
            if current is None or _content_hash(current) != plan.result_hash:
                complete = False
                continue
            if plan.backup is not None and plan.backup.exists():
                os.replace(plan.backup, plan.effective_path)
            elif plan.prior_kind == "absent":
                plan.effective_path.unlink()
            else:
                complete = False
                continue
            if journal is not None and plan.journal_index is not None:
                journal.update_link_entry(plan.journal_index, recovered=True)
        except (OSError, ManifestError):
            complete = False
    return complete


def _backup_path(path: Path, timestamp: int) -> Path:
    candidate = path.with_name(f"{path.name}.backup.{timestamp}")
    suffix = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = path.with_name(f"{path.name}.backup.{timestamp}.{suffix}")
        suffix += 1
    return candidate
