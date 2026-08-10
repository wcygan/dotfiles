"""Link repository-managed configuration into a user's home directory."""

from __future__ import annotations

import hashlib
import os
import shutil
import stat
import tempfile
import time
import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from dotfiles_setup.errors import LinkError, ManifestError
from dotfiles_setup.manifest import OperationJournal

Output = Callable[[str], None]
Timestamp = Callable[[], int]
Replace = Callable[[Path, Path], None]
Symlink = Callable[[str | Path, Path], None]


@dataclass(frozen=True)
class Link:
    """A repository source and the location where it is managed."""

    source: Path
    destination: Path


@dataclass(frozen=True)
class PlannedLink:
    """A fully classified link mutation produced before any write occurs."""

    link: Link
    prior_kind: str
    prior_target: str | None
    backup: Path | None
    prior_device: int | None
    prior_inode: int | None


@dataclass
class FileMutation:
    """A content-free description of one atomic local-file replacement."""

    source_label: str
    visible_path: Path
    destination: Path
    prior_kind: str
    prior_target: str | None
    backup: Path | None
    prior_hash: str | None
    result_hash: str
    mode: int | None
    journal_index: int | None = None


def resolve_home(environ: Mapping[str, str] | None = None) -> Path:
    """Return HOME, respecting an explicitly supplied environment."""

    values = os.environ if environ is None else environ
    return Path(values.get("HOME", str(Path.home()))).expanduser().resolve()


def resolve_config_home(home: Path, environ: Mapping[str, str] | None = None) -> Path:
    """Return XDG_CONFIG_HOME, with the conventional HOME fallback."""

    values = os.environ if environ is None else environ
    configured = Path(values.get("XDG_CONFIG_HOME", "")).expanduser()
    return configured.resolve(strict=False) if configured.is_absolute() else home / ".config"


def resolve_codex_home(home: Path, environ: Mapping[str, str] | None = None) -> Path:
    """Return CODEX_HOME, with the conventional HOME fallback."""

    values = os.environ if environ is None else environ
    configured = Path(values.get("CODEX_HOME", "")).expanduser()
    return configured.resolve(strict=False) if configured.is_absolute() else home / ".codex"


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


def _backup_path(path: Path, timestamp: int) -> Path:
    candidate = path.with_name(f"{path.name}.backup.{timestamp}")
    suffix = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = path.with_name(f"{path.name}.backup.{timestamp}.{suffix}")
        suffix += 1
    return candidate


def _classify_destination(
    path: Path,
) -> tuple[str, str | None, int | None, int | None]:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return "absent", None, None, None
    except OSError as error:
        raise LinkError(f"cannot inspect managed destination {path}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode):
        try:
            return "symlink", os.readlink(path), metadata.st_dev, metadata.st_ino
        except OSError as error:
            raise LinkError(f"cannot read managed symlink {path}: {error}") from error
    if stat.S_ISREG(metadata.st_mode):
        return "file", None, metadata.st_dev, metadata.st_ino
    if stat.S_ISDIR(metadata.st_mode):
        return "directory", None, metadata.st_dev, metadata.st_ino
    raise LinkError(
        f"unsupported destination type at {path}; no changes made. "
        "Move it aside manually and retry."
    )


def _check_parent(path: Path) -> None:
    ancestor = path.parent
    while not ancestor.exists():
        if ancestor.parent == ancestor:
            raise LinkError(f"cannot find a writable parent for {path}; no changes made")
        ancestor = ancestor.parent
    if not ancestor.is_dir():
        raise LinkError(f"parent path is not a directory for {path}: {ancestor}")
    if not os.access(ancestor, os.W_OK | os.X_OK):
        raise LinkError(f"parent directory is not writable for {path}: {ancestor}")


def _plan_links(
    links: tuple[Link, ...],
    *,
    now: Timestamp,
) -> tuple[PlannedLink, ...]:
    missing = [link.source for link in links if not link.source.exists()]
    if missing:
        rendered = ", ".join(str(path) for path in missing)
        raise LinkError(f"managed source is missing ({rendered}); no destinations were changed")
    plans: list[PlannedLink] = []
    reserved: set[Path] = set()
    for link in links:
        _check_parent(link.destination)
        prior_kind, prior_target, prior_device, prior_inode = _classify_destination(
            link.destination
        )
        backup = None
        if prior_kind in {"file", "directory"}:
            candidate = _backup_path(link.destination, now())
            backup = candidate.with_name(f"{candidate.name}.{uuid.uuid4().hex}")
            while backup in reserved:
                backup = candidate.with_name(f"{candidate.name}.{uuid.uuid4().hex}")
            reserved.add(backup)
        plans.append(
            PlannedLink(
                link,
                prior_kind,
                prior_target,
                backup,
                prior_device,
                prior_inode,
            )
        )
    return tuple(plans)


def _temporary_symlink(
    destination: Path,
    source: Path,
    *,
    symlink: Symlink,
) -> Path:
    for _ in range(20):
        temporary = destination.parent / f".{destination.name}.dotfiles.{uuid.uuid4().hex}"
        try:
            symlink(source, temporary)
            return temporary
        except FileExistsError:
            continue
        except OSError as error:
            raise LinkError(f"cannot create temporary link for {destination}: {error}") from error
    raise LinkError(f"cannot allocate a temporary link for {destination}")


def _link_one(
    plan: PlannedLink,
    *,
    dry_run: bool,
    output: Output,
    replace: Replace,
    symlink: Symlink,
    journal: OperationJournal | None,
    journal_index: int | None,
) -> None:
    link = plan.link
    destination = link.destination
    if dry_run:
        output(f"[DRY] Would link: {destination} -> {link.source}")
        if plan.prior_kind == "symlink":
            output("      (would replace existing symlink)")
        elif plan.prior_kind != "absent":
            output(f"      (would backup existing {destination})")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = _temporary_symlink(destination, link.source, symlink=symlink)
    temporary_identity = temporary.lstat()
    temporary_owned = True
    mutation_started = False
    try:
        if journal is not None and journal_index is not None:
            journal.update_link_entry(journal_index, mutation_started=True)
        if plan.backup is not None:
            if plan.backup.exists() or plan.backup.is_symlink():
                raise LinkError(
                    f"planned backup path appeared before apply: {plan.backup}; "
                    "no destination was overwritten"
                )
            replace(destination, plan.backup)
            mutation_started = True
            output(f"-> Backed up {destination} to {plan.backup}")
        replace(temporary, destination)
        temporary_owned = False
        mutation_started = True
        if journal is not None and journal_index is not None:
            journal.update_link_entry(journal_index, mutation_started=True, applied=True)
    except (OSError, ManifestError, LinkError) as error:
        restored = _restore_plan(plan, replace=replace, symlink=symlink)
        if restored and journal is not None and journal_index is not None:
            try:
                journal.update_link_entry(
                    journal_index,
                    mutation_started=False,
                    restored=True,
                    recovered=True,
                )
            except ManifestError:
                restored = False
        preserved = "prior destination restored" if restored else "recovery manifest preserved"
        raise LinkError(
            f"cannot replace {destination}: {error}; {preserved}. "
            "Run ./bootstrap.sh recover before retrying."
        ) from error
    finally:
        if temporary_owned:
            _unlink_owned_temporary(
                temporary,
                device=temporary_identity.st_dev,
                inode=temporary_identity.st_ino,
            )
    if not mutation_started:
        raise AssertionError("link replacement completed without recording a mutation")
    output(f"-> {destination} -> {link.source}")


def _prior_state_matches(plan: PlannedLink) -> bool:
    destination = plan.link.destination
    if plan.prior_kind == "absent":
        return not (destination.exists() or destination.is_symlink())
    if plan.prior_kind == "symlink":
        try:
            return destination.is_symlink() and os.readlink(destination) == plan.prior_target
        except OSError:
            return False
    try:
        metadata = destination.lstat()
    except (OSError, LinkError):
        return False
    return metadata.st_dev == plan.prior_device and metadata.st_ino == plan.prior_inode


def _restore_plan(
    plan: PlannedLink,
    *,
    replace: Replace,
    symlink: Symlink,
) -> bool:
    destination = plan.link.destination
    if _prior_state_matches(plan):
        return True
    try:
        if plan.backup is not None and plan.backup.exists():
            if destination.exists() or destination.is_symlink():
                if not destination.is_symlink() or os.readlink(destination) != str(
                    plan.link.source
                ):
                    return False
                destination.unlink()
            replace(plan.backup, destination)
        elif plan.prior_kind == "symlink" and plan.prior_target is not None:
            if not destination.is_symlink() or os.readlink(destination) != str(plan.link.source):
                return False
            temporary = _temporary_symlink(
                destination,
                Path(plan.prior_target),
                symlink=symlink,
            )
            temporary_identity = temporary.lstat()
            try:
                replace(temporary, destination)
            except OSError:
                _unlink_owned_temporary(
                    temporary,
                    device=temporary_identity.st_dev,
                    inode=temporary_identity.st_ino,
                )
                raise
        elif plan.prior_kind == "absent":
            if not destination.is_symlink() or os.readlink(destination) != str(plan.link.source):
                return False
            destination.unlink()
        else:
            return False
    except OSError:
        return False
    return _prior_state_matches(plan)


def _unlink_owned_temporary(path: Path, *, device: int, inode: int) -> None:
    try:
        metadata = path.lstat()
        if metadata.st_dev == device and metadata.st_ino == inode:
            path.unlink()
    except OSError:
        return


def _rollback_links(
    applied: list[tuple[PlannedLink, int]],
    *,
    replace: Replace,
    symlink: Symlink,
    journal: OperationJournal,
) -> bool:
    complete = True
    for plan, index in reversed(applied):
        try:
            if not _restore_plan(plan, replace=replace, symlink=symlink):
                complete = False
                continue
            journal.update_link_entry(index, recovered=True)
        except (OSError, ManifestError, LinkError):
            complete = False
    return complete


def _file_hash(path: Path) -> str | None:
    try:
        if not path.is_file() or path.is_symlink():
            return None
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _apply_file_mutation(
    mutation: FileMutation,
    contents: bytes,
    *,
    journal: OperationJournal | None,
) -> None:
    if journal is not None:
        mutation.journal_index = journal.add_link_entry(
            {
                "entry_type": "file",
                "destination": str(mutation.destination),
                "visible_destination": str(mutation.visible_path),
                "source": mutation.source_label,
                "prior_kind": mutation.prior_kind,
                "prior_target": mutation.prior_target,
                "prior_hash": mutation.prior_hash,
                "backup": str(mutation.backup) if mutation.backup is not None else None,
                "result_kind": "file",
                "result_target": None,
                "result_hash": mutation.result_hash,
                "mutation_started": False,
                "applied": False,
                "recovered": False,
            }
        )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{mutation.destination.name}.dotfiles.", dir=mutation.destination.parent
    )
    temporary = Path(temporary_name)
    temporary_identity = os.fstat(descriptor)
    temporary_owned = True
    try:
        if mutation.mode is not None:
            os.fchmod(descriptor, mutation.mode)
        with os.fdopen(descriptor, "wb") as file:
            file.write(contents)
            file.flush()
            os.fsync(file.fileno())
        if journal is not None and mutation.journal_index is not None:
            journal.update_link_entry(mutation.journal_index, mutation_started=True)
        if mutation.backup is not None:
            if mutation.backup.exists() or mutation.backup.is_symlink():
                raise LinkError(f"local-file backup path appeared: {mutation.backup}")
            shutil.copy2(mutation.destination, mutation.backup)
        os.replace(temporary, mutation.destination)
        temporary_owned = False
        if journal is not None and mutation.journal_index is not None:
            journal.update_link_entry(mutation.journal_index, applied=True)
    except (OSError, ManifestError, LinkError) as error:
        restored = _rollback_file_mutation(mutation, journal=journal)
        raise LinkError(
            f"cannot atomically update {mutation.visible_path}: {error}; "
            f"{'prior file restored' if restored else 'recovery manifest preserved'}"
        ) from error
    finally:
        if temporary_owned:
            _unlink_owned_temporary(
                temporary,
                device=temporary_identity.st_dev,
                inode=temporary_identity.st_ino,
            )


def _rollback_file_mutation(mutation: FileMutation, *, journal: OperationJournal | None) -> bool:
    current_hash = _file_hash(mutation.destination)
    if mutation.prior_kind == "file" and current_hash == mutation.prior_hash:
        restored = True
    elif mutation.prior_kind == "symlink" and mutation.destination.is_symlink():
        try:
            restored = os.readlink(mutation.destination) == mutation.prior_target
        except OSError:
            restored = False
    elif mutation.prior_kind == "absent" and not (
        mutation.destination.exists() or mutation.destination.is_symlink()
    ):
        restored = True
    elif current_hash != mutation.result_hash:
        restored = False
    else:
        try:
            if mutation.backup is not None and mutation.backup.exists():
                os.replace(mutation.backup, mutation.destination)
            elif mutation.prior_kind == "symlink" and mutation.prior_target is not None:
                temporary = _temporary_symlink(
                    mutation.destination,
                    Path(mutation.prior_target),
                    symlink=os.symlink,
                )
                temporary_identity = temporary.lstat()
                try:
                    os.replace(temporary, mutation.destination)
                except OSError:
                    _unlink_owned_temporary(
                        temporary,
                        device=temporary_identity.st_dev,
                        inode=temporary_identity.st_ino,
                    )
                    raise
            elif mutation.prior_kind == "absent":
                mutation.destination.unlink()
            else:
                return False
            restored = True
        except OSError:
            restored = False
    if restored and journal is not None and mutation.journal_index is not None:
        try:
            journal.update_link_entry(mutation.journal_index, recovered=True)
        except ManifestError:
            return False
    return restored


def _copy_codex_template(
    repo_root: Path,
    codex_home: Path,
    *,
    dry_run: bool,
    output: Output,
    journal: OperationJournal | None,
) -> FileMutation | None:
    source = repo_root.resolve() / "config" / "codex" / "config.toml"
    destination = codex_home / "config.toml"
    if dry_run:
        if destination.is_symlink():
            output(f"[DRY] Would migrate Codex config symlink to local file: {destination}")
        elif destination.exists():
            output(f"[DRY] Would preserve existing local Codex config: {destination}")
        else:
            output(f"[DRY] Would copy Codex config template: {source} -> {destination}")
        return None

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        contents = (destination if destination.exists() else source).read_bytes()
        mutation = FileMutation(
            "codex-template",
            destination,
            destination,
            "symlink",
            os.readlink(destination),
            None,
            None,
            hashlib.sha256(contents).hexdigest(),
            source.stat().st_mode & 0o777,
        )
        _apply_file_mutation(mutation, contents, journal=journal)
        output(f"-> Migrated Codex config symlink to local file: {destination}")
        return mutation
    elif destination.exists():
        output(f"-> Preserved existing local Codex config: {destination}")
        return None
    else:
        contents = source.read_bytes()
        mutation = FileMutation(
            "codex-template",
            destination,
            destination,
            "absent",
            None,
            None,
            None,
            hashlib.sha256(contents).hexdigest(),
            source.stat().st_mode & 0o777,
        )
        _apply_file_mutation(mutation, contents, journal=journal)
        output(f"-> Copied Codex config template to local file: {destination}")
        return mutation


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
    journal: OperationJournal | None,
) -> FileMutation | None:
    npmrc = home / ".npmrc"
    if dry_run:
        output(f"[DRY] Would ensure npm global prefix in {npmrc}: ${{HOME}}/.local")
        output("[DRY] Would ensure npm minimum release age: 1 day")
        output(f"[DRY] Would ensure npm global directories exist under: {home / '.local'}")
        return None

    (home / ".local" / "bin").mkdir(parents=True, exist_ok=True)
    (home / ".local" / "lib").mkdir(parents=True, exist_ok=True)
    effective_npmrc = npmrc.resolve(strict=False) if npmrc.is_symlink() else npmrc
    if not effective_npmrc.is_relative_to(home.resolve()):
        raise LinkError(
            f"npm config symlink resolves outside HOME: {npmrc} -> {effective_npmrc}; "
            "preserved without changes"
        )
    effective_npmrc.parent.mkdir(parents=True, exist_ok=True)
    original = effective_npmrc.read_text() if effective_npmrc.exists() else ""
    updated = _normalised_npmrc(original)
    if effective_npmrc.exists() and updated == original:
        output(f"-> npm settings already configured in {npmrc}")
        return None
    backup = None
    mode = None
    if effective_npmrc.exists():
        mode = effective_npmrc.stat().st_mode & 0o777
        backup = _backup_path(effective_npmrc, now())
    contents = updated.encode()
    mutation = FileMutation(
        "npmrc",
        npmrc,
        effective_npmrc,
        "file" if effective_npmrc.exists() else "absent",
        None,
        backup,
        hashlib.sha256(original.encode()).hexdigest() if effective_npmrc.exists() else None,
        hashlib.sha256(contents).hexdigest(),
        mode,
    )
    _apply_file_mutation(mutation, contents, journal=journal)
    action = "Updated" if backup is not None else "Configured"
    output(f"-> {action} npm settings in {npmrc}")
    return mutation


def link_config(
    repo_root: Path,
    *,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
    dry_run: bool = False,
    output: Output = print,
    now: Timestamp = lambda: int(time.time()),
    journal: OperationJournal | None = None,
    replace: Replace = os.replace,
    symlink: Symlink = os.symlink,
) -> None:
    """Install managed links and preserve mutable, local configuration state."""

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
    try:
        plans = _plan_links(inventory, now=now)
    except LinkError:
        if journal is not None:
            journal.transition("failed")
        raise
    owns_journal = journal is None and not dry_run
    if owns_journal:
        journal = OperationJournal("link", repo_root, environ=values)
    journal_indices: list[int | None] = []
    for plan in plans:
        if journal is None:
            journal_indices.append(None)
            continue
        journal_indices.append(
            journal.add_link_entry(
                {
                    "destination": str(plan.link.destination),
                    "source": str(plan.link.source),
                    "prior_kind": plan.prior_kind,
                    "prior_target": plan.prior_target,
                    "prior_device": plan.prior_device,
                    "prior_inode": plan.prior_inode,
                    "backup": str(plan.backup) if plan.backup is not None else None,
                    "result_kind": "symlink",
                    "result_target": str(plan.link.source),
                    "mutation_started": False,
                    "applied": False,
                    "recovered": False,
                }
            )
        )
    if owns_journal and journal is not None:
        journal.transition("applying")

    applied: list[tuple[PlannedLink, int]] = []
    file_mutations: list[FileMutation] = []
    try:
        for plan, journal_index in zip(plans, journal_indices, strict=True):
            _link_one(
                plan,
                dry_run=dry_run,
                output=output,
                replace=replace,
                symlink=symlink,
                journal=journal,
                journal_index=journal_index,
            )
            if journal_index is not None:
                applied.append((plan, journal_index))

        npm_mutation = _configure_npm(
            home,
            dry_run=dry_run,
            output=output,
            now=now,
            journal=journal,
        )
        if npm_mutation is not None:
            file_mutations.append(npm_mutation)
        codex_mutation = _copy_codex_template(
            repo_root,
            codex_home,
            dry_run=dry_run,
            output=output,
            journal=journal,
        )
        if codex_mutation is not None:
            file_mutations.append(codex_mutation)
    except (LinkError, OSError, ManifestError) as error:
        if journal is not None:
            files_rolled_back = True
            for mutation in reversed(file_mutations):
                if not _rollback_file_mutation(mutation, journal=journal):
                    files_rolled_back = False
            rolled_back = _rollback_links(
                applied,
                replace=replace,
                symlink=symlink,
                journal=journal,
            )
            entries = journal.data["entries"]
            assert isinstance(entries, list)
            pending = any(
                isinstance(entry, dict)
                and entry.get("mutation_started")
                and not entry.get("recovered")
                and not entry.get("restored")
                for entry in entries
            )
            journal.transition(
                "failed" if files_rolled_back and rolled_back and not pending else "recovery-needed"
            )
        if isinstance(error, LinkError):
            raise
        raise LinkError(f"link setup failed: {error}") from error

    if owns_journal and journal is not None:
        journal.record_operation("links", "completed")
        journal.transition("completed")
