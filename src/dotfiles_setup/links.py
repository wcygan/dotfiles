"""Link repository-managed configuration into a user's home directory."""

from __future__ import annotations

import os
import stat
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from dotfiles_setup.errors import LinkError
from dotfiles_setup.manifest import OperationJournal
from dotfiles_setup.mutations import (
    DirectoryMutation,
    FileMutation,
    Mutation,
    MutationExecutionError,
    MutationResult,
    SymlinkMutation,
    capture_file_input,
    execute_mutations,
)
from dotfiles_setup.paths import UserPathContext
from dotfiles_setup.scoped_file_input import (
    FileInputOutsideScopeError,
    capture_scoped_file_input,
)

Output = Callable[[str], None]
Timestamp = Callable[[], int]


@dataclass(frozen=True)
class Link:
    """A repository source and the location where it is managed."""

    source: Path
    destination: Path


@dataclass(frozen=True)
class _PreparedFile:
    """A local-file mutation and its success message."""

    mutation: FileMutation
    success_message: str


def resolve_home(environ: Mapping[str, str] | None = None) -> Path:
    """Return HOME, respecting an explicitly supplied environment."""

    return UserPathContext.from_environment(environ).home


def resolve_config_home(home: Path, environ: Mapping[str, str] | None = None) -> Path:
    """Return XDG_CONFIG_HOME, with the conventional HOME fallback."""

    values = os.environ if environ is None else environ
    if not Path(values.get("XDG_CONFIG_HOME", "")).expanduser().is_absolute():
        return home / ".config"
    return UserPathContext.from_environment(environ, home=home).config_home


def resolve_codex_home(home: Path, environ: Mapping[str, str] | None = None) -> Path:
    """Return CODEX_HOME, with the conventional HOME fallback."""

    values = os.environ if environ is None else environ
    if not Path(values.get("CODEX_HOME", "")).expanduser().is_absolute():
        return home / ".codex"
    return UserPathContext.from_environment(environ, home=home).codex_home


def vscode_config_home(home: Path, config_home: Path, system: str) -> Path:
    """Return VS Code's user settings directory for the current platform."""

    context = UserPathContext(
        home=home,
        config_home=config_home,
        state_home=home / ".local" / "state",
        cache_home=home / ".cache",
        codex_home=home / ".codex",
        platform=system,
    )
    return context.vscode_config_home


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
    agents_source = config / "agents" / "AGENTS.md"
    shared_agents = home / ".agents" / "AGENTS.md"
    codex_agents = codex_home / "AGENTS.md"
    agents_links = [Link(agents_source, shared_agents)]
    if codex_agents != shared_agents:
        agents_links.append(Link(agents_source, codex_agents))
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
        *agents_links,
        Link(config / "zellij", config_home / "zellij"),
        Link(config / "vscode" / "settings.json", vscode_home / "settings.json"),
        Link(config / "vscode" / "keybindings.json", vscode_home / "keybindings.json"),
    )


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


def _prepare_npm(home: Path, *, output: Output) -> _PreparedFile | None:
    npmrc = home / ".npmrc"
    try:
        selected = capture_scoped_file_input(npmrc, scope_root=home)
    except FileInputOutsideScopeError as error:
        raise LinkError(
            "npm config symlink resolves outside HOME: "
            f"{error.visible_path} -> {error.effective_path}; "
            "preserved without changes"
        ) from error
    effective_npmrc = selected.effective_path
    captured = selected.captured
    original = captured.contents.decode() if captured.contents is not None else ""
    updated = _normalised_npmrc(original)
    if captured.state.kind != "absent" and updated == original:
        output(f"-> npm settings already configured in {npmrc}")
        return None
    existed = captured.state.kind != "absent"
    mutation = FileMutation(
        destination=effective_npmrc,
        visible_destination=npmrc,
        source="npmrc",
        contents=updated.encode(),
        mode=captured.state.mode,
        precondition=captured.state,
    )
    action = "Updated" if existed else "Configured"
    return _PreparedFile(mutation, f"-> {action} npm settings in {npmrc}")


def _prepare_codex_template(repo_root: Path, codex_home: Path) -> _PreparedFile | str:
    source = repo_root.resolve() / "config" / "codex" / "config.toml"
    destination = codex_home / "config.toml"
    captured = capture_file_input(destination)
    if captured.state.kind == "symlink":
        contents = captured.contents if captured.contents is not None else source.read_bytes()
        message = f"-> Migrated Codex config symlink to local file: {destination}"
    elif captured.state.kind == "file":
        return f"-> Preserved existing local Codex config: {destination}"
    else:
        contents = source.read_bytes()
        message = f"-> Copied Codex config template to local file: {destination}"
    return _PreparedFile(
        FileMutation(
            destination=destination,
            visible_destination=destination,
            source="codex-template",
            contents=contents,
            mode=source.stat().st_mode & 0o777,
            precondition=captured.state,
        ),
        message,
    )


def _dry_destination_kind(path: Path) -> str:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return "absent"
    except OSError as error:
        raise LinkError(f"cannot inspect managed destination {path}: {error}") from error
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    raise LinkError(f"unsupported destination type at {path}; no changes made")


def _show_dry_run(
    inventory: tuple[Link, ...],
    repo_root: Path,
    codex_home: Path,
    home: Path,
    *,
    output: Output,
) -> None:
    missing = [link.source for link in inventory if not link.source.exists()]
    if missing:
        rendered = ", ".join(str(path) for path in missing)
        raise LinkError(f"managed source is missing ({rendered}); no destinations were changed")
    for link in inventory:
        kind = _dry_destination_kind(link.destination)
        output(f"[DRY] Would link: {link.destination} -> {link.source}")
        if kind == "symlink":
            output("      (would replace existing symlink)")
        elif kind != "absent":
            output(f"      (would backup existing {link.destination})")
    npmrc = home / ".npmrc"
    output(f"[DRY] Would ensure npm global prefix in {npmrc}: ${{HOME}}/.local")
    output("[DRY] Would ensure npm minimum release age: 1 day")
    output(f"[DRY] Would ensure npm global directories exist under: {home / '.local'}")
    destination = codex_home / "config.toml"
    source = repo_root.resolve() / "config" / "codex" / "config.toml"
    if destination.is_symlink():
        output(f"[DRY] Would migrate Codex config symlink to local file: {destination}")
    elif destination.exists():
        output(f"[DRY] Would preserve existing local Codex config: {destination}")
    else:
        output(f"[DRY] Would copy Codex config template: {source} -> {destination}")


def _report_results(
    inventory: tuple[Link, ...],
    results: tuple[MutationResult, ...],
    prepared_files: tuple[_PreparedFile, ...],
    preserved_codex_message: str | None,
    *,
    output: Output,
) -> None:
    link_results = {
        result.mutation.destination: result
        for result in results
        if isinstance(result.mutation, SymlinkMutation)
    }
    for link in inventory:
        result = link_results.get(link.destination)
        if result is not None and result.backup is not None:
            output(f"-> Backed up {link.destination} to {result.backup}")
        output(f"-> {link.destination} -> {link.source}")
    for prepared in prepared_files:
        output(prepared.success_message)
    if preserved_codex_message is not None:
        output(preserved_codex_message)


def link_config(
    repo_root: Path,
    *,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
    dry_run: bool = False,
    output: Output = print,
    now: Timestamp = lambda: int(time.time()),
    journal: OperationJournal | None = None,
) -> None:
    """Install managed links and preserve mutable, local configuration state."""

    values = os.environ if environ is None else environ
    context = UserPathContext.from_environment(values, system=system)
    home = context.home
    codex_home = context.codex_home
    inventory = managed_links(
        repo_root,
        home=home,
        config_home=context.config_home,
        codex_home=codex_home,
        system=context.platform,
    )
    if dry_run:
        _show_dry_run(inventory, repo_root, codex_home, home, output=output)
        return

    missing = [link.source for link in inventory if not link.source.exists()]
    if missing:
        rendered = ", ".join(str(path) for path in missing)
        raise LinkError(f"managed source is missing ({rendered}); no destinations were changed")
    try:
        prepared_npm = _prepare_npm(home, output=output)
        prepared_codex = _prepare_codex_template(repo_root, codex_home)
    except (MutationExecutionError, OSError) as error:
        raise LinkError(f"cannot prepare link setup: {error}") from error
    prepared_files = tuple(
        prepared
        for prepared in (prepared_npm, prepared_codex)
        if isinstance(prepared, _PreparedFile)
    )
    preserved_codex_message = prepared_codex if isinstance(prepared_codex, str) else None
    mutations: tuple[Mutation, ...] = (
        *(SymlinkMutation(destination=link.destination, source=link.source) for link in inventory),
        *(prepared.mutation for prepared in prepared_files),
        DirectoryMutation(destination=home / ".local" / "bin"),
        DirectoryMutation(destination=home / ".local" / "lib"),
    )

    owns_journal = journal is None
    if owns_journal:
        journal = OperationJournal("link", repo_root, environ=values)
        journal.transition("applying")
    try:
        results = execute_mutations(
            mutations,
            journal=journal,
            timestamp=now(),
            authority_roots=(home, context.config_home, codex_home),
        )
    except MutationExecutionError as error:
        if journal is not None and journal.state not in {"failed", "recovery-needed"}:
            journal.transition("failed")
        status = "prior destination restored" if error.restored else "recovery manifest preserved"
        raise LinkError(f"cannot atomically update link setup: {error}; {status}") from error

    _report_results(
        inventory,
        results,
        prepared_files,
        preserved_codex_message,
        output=output,
    )
    if owns_journal and journal is not None:
        journal.record_operation("links", "completed")
        journal.transition("completed")
