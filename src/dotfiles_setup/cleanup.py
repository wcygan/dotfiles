"""Remove only symlinks managed by :mod:`dotfiles_setup.links`."""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping
from pathlib import Path

from dotfiles_setup.errors import CleanupError
from dotfiles_setup.links import (
    Link,
    managed_links,
    resolve_codex_home,
    resolve_config_home,
    resolve_home,
)
from dotfiles_setup.manifest import OperationJournal

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
    home = resolve_home(values)
    config_home = resolve_config_home(home, values)
    codex_home = resolve_codex_home(home, values)
    platform_name = system or os.uname().sysname

    inventory = managed_links(
        repo_root,
        home=home,
        config_home=config_home,
        codex_home=codex_home,
        system=platform_name,
    )
    actions: list[tuple[Link, str]] = []
    for link in inventory:
        if _is_managed(link):
            try:
                actions.append((link, os.readlink(link.destination)))
            except OSError as error:
                raise CleanupError(
                    f"cannot inspect managed link {link.destination}: {error}; no links removed"
                ) from error
        elif link.destination.is_symlink():
            output(f"Skipping unmanaged symlink: {link.destination}")
        elif link.destination.exists():
            output(f"Skipping local file: {link.destination}")

    journal_indices: list[int | None] = []
    for link, prior_target in actions:
        if dry_run:
            output(f"[DRY] Would remove symlink: {link.destination}")
            journal_indices.append(None)
        elif journal is not None:
            journal_indices.append(
                journal.add_link_entry(
                    {
                        "destination": str(link.destination),
                        "source": str(link.source),
                        "prior_kind": "symlink",
                        "prior_target": prior_target,
                        "backup": None,
                        "result_kind": "absent",
                        "result_target": None,
                        "mutation_started": False,
                        "applied": False,
                        "recovered": False,
                    }
                )
            )
        else:
            journal_indices.append(None)

    if dry_run:
        return
    for (link, _prior_target), journal_index in zip(actions, journal_indices, strict=True):
        try:
            if journal is not None and journal_index is not None:
                journal.update_link_entry(journal_index, mutation_started=True)
            link.destination.unlink()
            if journal is not None and journal_index is not None:
                journal.update_link_entry(journal_index, applied=True)
        except OSError as error:
            raise CleanupError(
                f"cannot remove managed link {link.destination}: {error}; "
                "run ./bootstrap.sh recover before retrying"
            ) from error
        output(f"Removed symlink: {link.destination}")
