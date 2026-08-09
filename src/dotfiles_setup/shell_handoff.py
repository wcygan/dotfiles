"""Configure bash and zsh to retain Nix paths and hand interactive shells to fish."""

from __future__ import annotations

import os
import shutil
import time
from dataclasses import dataclass
from pathlib import Path

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


def configure_shell_handoff(
    *,
    home: Path | None = None,
    shell: str | None = None,
    backup_timestamp: int | None = None,
) -> ShellHandoffResult:
    """Idempotently apply the legacy shell-handoff blocks to a home directory.

    ``home`` and ``shell`` are arguments so callers can configure a temporary
    home without changing process-wide environment variables.  No interactive
    input is requested.
    """
    home_directory = (Path.home() if home is None else home).expanduser()
    home_directory.joinpath(".config").mkdir(parents=True, exist_ok=True)
    suffix = int(time.time()) if backup_timestamp is None else backup_timestamp
    updated_files: list[Path] = []
    backups: list[Path] = []
    backed_up_files: set[Path] = set()
    original_regular_files: set[Path] = set()
    inspected_files: set[Path] = set()

    def ensure(path: Path, marker: str, content: str) -> None:
        if path not in inspected_files:
            inspected_files.add(path)
            if _needs_backup(path):
                original_regular_files.add(path)
        if _ensure_block(
            path,
            marker,
            suffix,
            original_regular_files,
            backed_up_files,
            backups,
            content,
        ):
            updated_files.append(path)

    bashrc = home_directory / ".bashrc"
    ensure(
        bashrc,
        "DOTFILES:NIX_SHELL_HELPERS",
        'source "$HOME/.config/shell-nix.sh" 2>/dev/null || true',
    )
    ensure(bashrc, "DOTFILES:EXEC_FISH", _BASH_EXEC_FISH)

    active_shell = os.environ.get("SHELL", "") if shell is None else shell
    if Path(active_shell).name == "bash":
        bash_profile = home_directory / ".bash_profile"
        ensure(
            bash_profile,
            "DOTFILES:BASH_PROFILE_SOURCE_BASHRC",
            _BASH_PROFILE_SOURCE_BASHRC,
        )
        ensure(
            bash_profile,
            "DOTFILES:BASH_PROFILE_SOURCE_PROFILE",
            _BASH_PROFILE_SOURCE_PROFILE,
        )

    zshrc = home_directory / ".zshrc"
    ensure(
        zshrc,
        "DOTFILES:NIX_SHELL_HELPERS",
        'source "$HOME/.config/shell-nix.sh" 2>/dev/null || true',
    )
    ensure(zshrc, "DOTFILES:EXEC_FISH", _ZSH_EXEC_FISH)

    ensure(home_directory / ".zshenv", "DOTFILES:NIX_PATH", _ZSHENV_PATH)
    return ShellHandoffResult(tuple(updated_files), tuple(backups))


def _ensure_block(
    path: Path,
    marker: str,
    backup_timestamp: int,
    original_regular_files: set[Path],
    backed_up_files: set[Path],
    backups: list[Path],
    content: str,
) -> bool:
    existing = path.read_text() if path.exists() else ""
    if marker in existing:
        return False

    if path in original_regular_files and path not in backed_up_files:
        backup = path.with_name(f"{path.name}.backup.{backup_timestamp}")
        shutil.copy2(path, backup)
        backed_up_files.add(path)
        backups.append(backup)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as file:
        file.write(f"\n# Added by dotfiles {_SETUP_SOURCE} ({marker})\n{content}\n")
    return True


def _needs_backup(path: Path) -> bool:
    return path.exists() and path.is_file() and not path.is_symlink()
