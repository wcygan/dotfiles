"""Remove only symlinks managed by :mod:`dotfiles_setup.links`."""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping
from pathlib import Path

from dotfiles_setup.errors import CleanupError
from dotfiles_setup.links import Link, managed_links
from dotfiles_setup.manifest import OperationJournal
from dotfiles_setup.mutations import (
    MutationExecutionError,
    SymlinkMutation,
    execute_mutations,
)
from dotfiles_setup.paths import UserPathContext

Output = Callable[[str], None]


def _is_managed(link: Link) -> bool:
    """Return whether a live destination points at its exact repository source."""

    if not link.destination.is_symlink():
        return False
    try:
        return link.destination.resolve(strict=False) == link.source.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise CleanupError(
            f"cannot resolve managed destination {link.destination}: {error}"
        ) from error


def cleanup_links(
    repo_root: Path,
    *,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
    dry_run: bool = False,
    output: Output = print,
    journal: OperationJournal | None = None,
) -> None:
    """Remove installer-managed symlinks while preserving local files and backups."""

    values = os.environ if environ is None else environ
    context = UserPathContext.from_environment(values, system=system)

    inventory = managed_links(
        repo_root,
        home=context.home,
        config_home=context.config_home,
        codex_home=context.codex_home,
        system=context.platform,
    )
    actions: list[Link] = []
    for link in inventory:
        if _is_managed(link):
            actions.append(link)
        elif link.destination.is_symlink():
            output(f"Skipping unmanaged symlink: {link.destination}")
        elif link.destination.exists():
            output(f"Skipping local file: {link.destination}")

    for link in actions:
        if dry_run:
            output(f"[DRY] Would remove symlink: {link.destination}")

    if dry_run:
        return
    mutations = tuple(
        SymlinkMutation(destination=link.destination, source=link.source, present=False)
        for link in actions
    )
    try:
        execute_mutations(
            mutations,
            journal=journal,
            authority_roots=(context.home, context.config_home, context.codex_home),
        )
    except MutationExecutionError as error:
        status = "prior links restored" if error.restored else "recovery manifest preserved"
        raise CleanupError(f"cannot atomically remove managed links: {error}; {status}") from error
    for link in actions:
        output(f"Removed symlink: {link.destination}")
