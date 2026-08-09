"""Create and maintain the user-specific Git identity file."""

from __future__ import annotations

import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

CommandRunner = Callable[..., subprocess.CompletedProcess[str]]
InputFunction = Callable[[str], str]


class GitUserError(RuntimeError):
    """Raised when Git identity setup cannot complete safely."""


@dataclass(frozen=True)
class GitUserConfig:
    """The resulting local identity and any global identity cleanup."""

    path: Path
    name: str | None
    email: str | None
    updated: bool
    removed_global: bool


def configure_git_user(
    *,
    home: Path | None = None,
    name: str | None = None,
    email: str | None = None,
    update: bool | None = None,
    remove_global: bool | None = None,
    input_func: InputFunction = input,
    run: CommandRunner = subprocess.run,
) -> GitUserConfig:
    """Configure ``~/.config/git/config.local`` without leaking identity data.

    With no controls supplied, this keeps the prompt flow from
    ``scripts/setup-git-user.sh``.  Supplying any control selects
    non-interactive mode: a write then requires both a name and an email, so a
    CI process never waits for stdin unexpectedly.
    """
    home_directory = Path.home() if home is None else home.expanduser()
    path = home_directory / ".config" / "git" / "config.local"
    interactive = all(value is None for value in (name, email, update, remove_global))
    exists = path.is_file()
    existing_name = _get_config(run, ("--file", str(path)), "user.name") if exists else None
    existing_email = _get_config(run, ("--file", str(path)), "user.email") if exists else None

    if exists:
        should_update = _should_update(update, interactive, input_func)
        if not should_update:
            return GitUserConfig(path, existing_name, existing_email, False, False)

    global_name = _get_config(run, ("--global",), "user.name")
    global_email = _get_config(run, ("--global",), "user.email")
    selected_name, selected_email = _identity_values(
        name,
        email,
        global_name,
        global_email,
        interactive,
        input_func,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    _set_config(run, ("--file", str(path)), "user.name", selected_name)
    _set_config(run, ("--file", str(path)), "user.email", selected_email)

    should_remove_global = _should_remove_global(
        remove_global,
        global_name,
        global_email,
        interactive,
        input_func,
    )
    if should_remove_global:
        _unset_config(run, "user.name")
        _unset_config(run, "user.email")

    return GitUserConfig(path, selected_name, selected_email, True, should_remove_global)


def _should_update(
    update: bool | None,
    interactive: bool,
    input_func: InputFunction,
) -> bool:
    if update is not None:
        return update
    if not interactive:
        return True
    return _prompt("Do you want to update it? [y/N] ", input_func).lower() == "y"


def _identity_values(
    name: str | None,
    email: str | None,
    global_name: str | None,
    global_email: str | None,
    interactive: bool,
    input_func: InputFunction,
) -> tuple[str, str]:
    if not interactive:
        if name is None or email is None:
            raise GitUserError("non-interactive Git identity setup requires both name and email")
        return name, email

    selected_name = _prompt_identity("name", global_name, input_func)
    selected_email = _prompt_identity("email", global_email, input_func)
    return selected_name, selected_email


def _prompt_identity(
    label: str,
    default: str | None,
    input_func: InputFunction,
) -> str:
    prompt = f"Enter your {label} [{default}]: " if default else f"Enter your {label}: "
    entered = _prompt(prompt, input_func)
    return default if not entered and default is not None else entered


def _should_remove_global(
    remove_global: bool | None,
    global_name: str | None,
    global_email: str | None,
    interactive: bool,
    input_func: InputFunction,
) -> bool:
    if remove_global is not None:
        return remove_global and (global_name is not None or global_email is not None)
    if not interactive or (global_name is None and global_email is None):
        return False
    prompt = "Remove global git user config (now redundant)? [Y/n] "
    return _prompt(prompt, input_func).lower() != "n"


def _prompt(prompt: str, input_func: InputFunction) -> str:
    try:
        return input_func(prompt)
    except EOFError as error:
        raise GitUserError(
            "interactive Git identity setup reached EOF; pass name and email "
            "for non-interactive setup"
        ) from error


def _get_config(
    run: CommandRunner,
    scope: Sequence[str],
    key: str,
) -> str | None:
    result = _run(run, ("git", "config", *scope, "--get", key))
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None


def _set_config(run: CommandRunner, scope: Sequence[str], key: str, value: str) -> None:
    _require_success(_run(run, ("git", "config", *scope, key, value)))


def _unset_config(run: CommandRunner, key: str) -> None:
    # The legacy script intentionally treats an already-absent key as success.
    _run(run, ("git", "config", "--global", "--unset", key))


def _run(run: CommandRunner, command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    try:
        return run(list(command), capture_output=True, check=False, text=True)
    except OSError as error:
        raise GitUserError(f"could not run {' '.join(command)}: {error}") from error


def _require_success(result: subprocess.CompletedProcess[str]) -> None:
    if result.returncode == 0:
        return
    detail = result.stderr.strip() or result.stdout.strip() or "no diagnostic output"
    raise GitUserError(f"{' '.join(str(part) for part in result.args)} failed: {detail}")
