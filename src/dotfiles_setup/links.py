"""Link repository-managed configuration into a user's home directory."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

Output = Callable[[str], None]
CommandRunner = Callable[..., subprocess.CompletedProcess[str]]
Timestamp = Callable[[], int]


@dataclass(frozen=True)
class Link:
    """A repository source and the location where it is managed."""

    source: Path
    destination: Path


def resolve_home(environ: Mapping[str, str] | None = None) -> Path:
    """Return HOME, respecting an explicitly supplied environment."""

    values = os.environ if environ is None else environ
    return Path(values.get("HOME", str(Path.home()))).expanduser().resolve()


def resolve_config_home(home: Path, environ: Mapping[str, str] | None = None) -> Path:
    """Return XDG_CONFIG_HOME, with the conventional HOME fallback."""

    values = os.environ if environ is None else environ
    return Path(values.get("XDG_CONFIG_HOME", str(home / ".config"))).expanduser()


def resolve_codex_home(home: Path, environ: Mapping[str, str] | None = None) -> Path:
    """Return CODEX_HOME, with the conventional HOME fallback."""

    values = os.environ if environ is None else environ
    return Path(values.get("CODEX_HOME", str(home / ".codex"))).expanduser()


def vscode_config_home(home: Path, config_home: Path, system: str) -> Path:
    """Return VS Code's user settings directory for the current platform."""

    if system.lower() == "darwin":
        return home / "Library" / "Application Support" / "Code" / "User"
    return config_home / "Code" / "User"


def managed_links(
    repo_root: Path,
    *,
    home: Path,
    config_home: Path,
    codex_home: Path,
    system: str,
) -> tuple[Link, ...]:
    """Build the complete, platform-aware set of managed symlinks."""

    config = repo_root.resolve() / "config"
    vscode_home = vscode_config_home(home, config_home, system)
    return (
        Link(config / "git", config_home / "git"),
        Link(config / "tmux" / "tmux.conf", home / ".tmux.conf"),
        Link(config / "shell-nix.sh", config_home / "shell-nix.sh"),
        Link(config / "fish", config_home / "fish"),
        Link(config / "starship.toml", config_home / "starship.toml"),
        Link(config / "zed", config_home / "zed"),
        Link(config / "bunfig.toml", home / ".bunfig.toml"),
        Link(config / "bunfig.toml", config_home / ".bunfig.toml"),
        Link(config / "deno", config_home / "deno"),
        Link(config / "ghostty", config_home / "ghostty"),
        Link(config / "codex" / "AGENTS.md", codex_home / "AGENTS.md"),
        Link(config / "zellij", config_home / "zellij"),
        Link(config / "vscode" / "settings.json", vscode_home / "settings.json"),
        Link(config / "vscode" / "keybindings.json", vscode_home / "keybindings.json"),
    )


def _backup_path(path: Path, timestamp: int) -> Path:
    candidate = path.with_name(f"{path.name}.backup.{timestamp}")
    suffix = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = path.with_name(f"{path.name}.backup.{timestamp}.{suffix}")
        suffix += 1
    return candidate


def _link_one(link: Link, *, dry_run: bool, output: Output, now: Timestamp) -> None:
    destination = link.destination
    if dry_run:
        output(f"[DRY] Would link: {destination} -> {link.source}")
        if destination.is_symlink():
            output("      (would replace existing symlink)")
        elif destination.exists():
            output(f"      (would backup existing {destination})")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        destination.unlink()
    elif destination.exists():
        backup = _backup_path(destination, now())
        shutil.move(str(destination), str(backup))
        output(f"-> Backed up {destination} to {backup}")
    destination.symlink_to(link.source, target_is_directory=link.source.is_dir())
    output(f"-> {destination} -> {link.source}")


def _copy_codex_template(
    repo_root: Path,
    codex_home: Path,
    *,
    dry_run: bool,
    output: Output,
) -> None:
    source = repo_root.resolve() / "config" / "codex" / "config.toml"
    destination = codex_home / "config.toml"
    if dry_run:
        if destination.is_symlink():
            output(f"[DRY] Would migrate Codex config symlink to local file: {destination}")
        elif destination.exists():
            output(f"[DRY] Would preserve existing local Codex config: {destination}")
        else:
            output(f"[DRY] Would copy Codex config template: {source} -> {destination}")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.migration.",
            dir=destination.parent,
        )
        os.close(descriptor)
        temporary = Path(temporary_name)
        try:
            shutil.copy2(destination if destination.exists() else source, temporary)
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)
        output(f"-> Migrated Codex config symlink to local file: {destination}")
    elif destination.exists():
        output(f"-> Preserved existing local Codex config: {destination}")
    else:
        shutil.copy2(source, destination)
        output(f"-> Copied Codex config template to local file: {destination}")


def _normalised_npmrc(contents: str) -> str:
    prefix = "prefix=${HOME}/.local"
    minimum_age = "min-release-age=1"
    lines: list[str] = []
    wrote_prefix = False
    wrote_minimum_age = False
    for line in contents.splitlines():
        key = line.lstrip().split("=", 1)[0].rstrip()
        if "=" in line and key == "prefix":
            if not wrote_prefix:
                lines.append(prefix)
                wrote_prefix = True
        elif "=" in line and key == "min-release-age":
            if not wrote_minimum_age:
                lines.append(minimum_age)
                wrote_minimum_age = True
        else:
            lines.append(line)
    if not wrote_prefix:
        lines.append(prefix)
    if not wrote_minimum_age:
        lines.append(minimum_age)
    return "\n".join(lines) + "\n"


def _configure_npm(
    home: Path,
    *,
    dry_run: bool,
    output: Output,
    now: Timestamp,
) -> None:
    npmrc = home / ".npmrc"
    if dry_run:
        output(f"[DRY] Would ensure npm global prefix in {npmrc}: ${{HOME}}/.local")
        output("[DRY] Would ensure npm minimum release age: 1 day")
        output(f"[DRY] Would ensure npm global directories exist under: {home / '.local'}")
        return

    (home / ".local" / "bin").mkdir(parents=True, exist_ok=True)
    (home / ".local" / "lib").mkdir(parents=True, exist_ok=True)
    if not npmrc.exists():
        npmrc.write_text("prefix=${HOME}/.local\nmin-release-age=1\n")
        output(f"-> Configured npm settings in {npmrc}")
        return

    updated = _normalised_npmrc(npmrc.read_text())
    if updated == npmrc.read_text():
        output(f"-> npm settings already configured in {npmrc}")
        return
    backup = _backup_path(npmrc, now())
    shutil.copy2(npmrc, backup)
    npmrc.write_text(updated)
    output(f"-> Updated npm settings in {npmrc}")


def link_config(
    repo_root: Path,
    *,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
    dry_run: bool = False,
    output: Output = print,
    now: Timestamp = lambda: int(time.time()),
    find_command: Callable[[str], str | None] = shutil.which,
    run_command: CommandRunner = subprocess.run,
) -> None:
    """Install managed links and preserve mutable, local configuration state."""

    values = os.environ if environ is None else environ
    home = resolve_home(values)
    config_home = resolve_config_home(home, values)
    codex_home = resolve_codex_home(home, values)
    platform_name = system or os.uname().sysname

    for link in managed_links(
        repo_root,
        home=home,
        config_home=config_home,
        codex_home=codex_home,
        system=platform_name,
    ):
        _link_one(link, dry_run=dry_run, output=output, now=now)

    _configure_npm(home, dry_run=dry_run, output=output, now=now)
    _copy_codex_template(repo_root, codex_home, dry_run=dry_run, output=output)

    if values.get("DOTFILES_SKIP_FISH_GREETING") == "1" or find_command("fish") is None:
        return
    if dry_run:
        output("[DRY] Would disable fish greeting")
        return
    run_command(
        ["fish", "-c", "set -U fish_greeting"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    output("-> Disabled fish greeting")
