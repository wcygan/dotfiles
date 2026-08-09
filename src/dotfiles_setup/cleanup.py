"""Remove only symlinks managed by :mod:`dotfiles_setup.links`."""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping
from pathlib import Path

from dotfiles_setup.links import (
    Link,
    managed_links,
    resolve_codex_home,
    resolve_config_home,
    resolve_home,
)

Output = Callable[[str], None]


def _is_managed(link: Link) -> bool:
    """Return whether a live destination points at its exact repository source."""

    if not link.destination.is_symlink():
        return False
    return link.destination.resolve(strict=False) == link.source.resolve(strict=False)


def cleanup_links(
    repo_root: Path,
    *,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
    dry_run: bool = False,
    output: Output = print,
) -> None:
    """Remove installer-managed symlinks while preserving local files and backups."""

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
        if _is_managed(link):
            if dry_run:
                output(f"[DRY] Would remove symlink: {link.destination}")
            else:
                link.destination.unlink()
                output(f"Removed symlink: {link.destination}")
        elif link.destination.is_symlink():
            output(f"Skipping unmanaged symlink: {link.destination}")
        elif link.destination.exists():
            output(f"Skipping local file: {link.destination}")
