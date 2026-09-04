"""Install the repository-pinned shared Codex skill catalog with GitHub CLI."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tomllib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from dotfiles_setup.errors import SetupError
from dotfiles_setup.mutations import (
    MutationExecutionError,
    VerifiedDirectory,
    VerifiedDirectoryEntry,
    capture_verified_directory,
    remove_verified_directories,
)
from dotfiles_setup.paths import UserPathContext

CommandRunner = Callable[..., subprocess.CompletedProcess[str]]
CommandLocator = Callable[[str], str | None]

_EXACT_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_LIST_FIELDS = "skillName,sourceURL,scope,version,pinned,path"


class AgentSkillsError(SetupError):
    """The pinned user-scope agent skill catalog could not be installed or verified."""


@dataclass(frozen=True)
class AgentSkillsLock:
    repository: str
    commit: str
    agent: str
    directory: str


@dataclass(frozen=True)
class InstalledSkill:
    """One typed GitHub CLI installed-skill inventory record."""

    name: str
    source: str | None
    scope: str | None
    version: str | None
    pinned: bool | None
    path: Path | None


@dataclass(frozen=True)
class _GitTreeEntry:
    """One validated entry from the pinned Git tree."""

    path: PurePosixPath
    kind: str
    mode: str
    object_id: str


@dataclass(frozen=True)
class _LegacyCleanupPlan:
    """Bound identities for one exact legacy catalog cleanup."""

    directories: tuple[VerifiedDirectory, ...]
    parent_identity: tuple[int, int]
    parent_parent_identity: tuple[int, int]

    @property
    def parent(self) -> Path:
        return self.directories[0].path.parent


@dataclass(frozen=True)
class AgentSkillsResult:
    repository: str
    commit: str
    count: int
    destination: Path
    local_content_digest: str = field(default="", compare=False, repr=False)

    def __str__(self) -> str:
        return (
            f"{self.count} pinned Codex shared-user skills from "
            f"{self.repository}@{self.commit} at {self.destination}"
        )


@dataclass(frozen=True)
class AgentSkillsCleanupResult:
    count: int
    destination: Path | None
    quarantines: tuple[Path, ...] = ()

    def __post_init__(self) -> None:
        if self.count != len(self.quarantines):
            raise ValueError("cleanup count must match the retained quarantine paths")
        if (self.destination is None) != (self.count == 0):
            raise ValueError("cleanup destination must match the quarantine result")
        if self.destination is not None and any(
            path.parent != self.destination for path in self.quarantines
        ):
            raise ValueError("cleanup quarantines must use the reported destination")

    def __str__(self) -> str:
        if self.destination is None:
            return "No legacy Codex user skills required cleanup."
        retained = ", ".join(str(path) for path in self.quarantines)
        return (
            f"Quarantined {self.count} legacy Codex user skills from "
            f"{self.destination}; retained at: {retained}"
        )


@dataclass(frozen=True)
class GitHubSkillRegistry:
    """Adapt GitHub CLI skill commands to typed catalog operations."""

    executable: str
    run: CommandRunner = field(default=subprocess.run, repr=False, compare=False)
    environment: Mapping[str, str] = field(default_factory=dict, repr=False, compare=False)

    def discover(self, lock: AgentSkillsLock) -> tuple[str, ...]:
        """Return the sorted skill names from the pinned provider catalog."""

        result = self._execute(
            [
                "skill",
                "install",
                lock.repository,
                "--pin",
                lock.commit,
            ],
            "list the pinned agent skill catalog",
        )
        names: list[str] = []
        for line in result.stdout.splitlines():
            if "\t" not in line:
                continue
            name = line.split("\t", 1)[0].strip()
            if _SKILL_NAME.fullmatch(name) is None:
                raise AgentSkillsError(f"gh returned an invalid skill name: {name!r}")
            names.append(name)
        if not names:
            raise AgentSkillsError(
                f"gh found no skills in {lock.repository} at pinned commit {lock.commit}"
            )
        if len(names) != len(set(names)):
            raise AgentSkillsError("gh returned duplicate skill names for the pinned catalog")
        return tuple(sorted(names))

    def install(self, lock: AgentSkillsLock, destination: Path) -> None:
        """Install the complete pinned catalog into one custom directory."""

        self._execute(
            [
                "skill",
                "install",
                lock.repository,
                "--all",
                "--pin",
                lock.commit,
                "--force",
                "--dir",
                str(destination),
            ],
            "install pinned agent skills",
        )

    def list_shared(self, destination: Path) -> tuple[InstalledSkill, ...]:
        """Return the typed custom-directory inventory."""

        return self._list(
            [
                "skill",
                "list",
                "--dir",
                str(destination),
                "--json",
                _LIST_FIELDS,
            ],
            "inspect installed agent skills",
        )

    def list_legacy(self, lock: AgentSkillsLock) -> tuple[InstalledSkill, ...]:
        """Return the typed legacy Codex user-scope inventory."""

        return self._list(
            [
                "skill",
                "list",
                "--agent",
                lock.agent,
                "--scope",
                "user",
                "--json",
                _LIST_FIELDS,
            ],
            "inspect legacy Codex skills",
        )

    def pinned_tree(self, lock: AgentSkillsLock) -> tuple[_GitTreeEntry, ...]:
        """Return the complete Git tree for the exact provider commit."""

        result = self._execute(
            [
                "api",
                f"repos/{lock.repository}/git/trees/{lock.commit}?recursive=1",
            ],
            "inspect the pinned agent skill source tree",
        )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise AgentSkillsError("gh api returned an invalid pinned Git tree") from error
        if not isinstance(payload, dict) or payload.get("truncated") is not False:
            raise AgentSkillsError("gh api returned an incomplete pinned Git tree")
        tree = payload.get("tree")
        if not isinstance(tree, list) or not all(isinstance(item, dict) for item in tree):
            raise AgentSkillsError("gh api returned an invalid pinned Git tree")
        return tuple(self._parse_tree_entry(item) for item in tree)

    def _list(self, arguments: list[str], action: str) -> tuple[InstalledSkill, ...]:
        result = self._execute(arguments, action)
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise AgentSkillsError("gh skill list returned invalid JSON") from error
        if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
            raise AgentSkillsError("gh skill list returned an invalid skill inventory")
        # Namespaced entries (e.g. Codex built-ins ".system/imagegen") are
        # agent-internal skills, never members of the user catalog; skip them.
        return tuple(
            self._parse_installed_skill(item)
            for item in payload
            if "/" not in str(item.get("skillName", ""))
        )

    @staticmethod
    def _parse_installed_skill(item: dict[object, object]) -> InstalledSkill:
        name = item.get("skillName")
        if not isinstance(name, str) or _SKILL_NAME.fullmatch(name) is None:
            raise AgentSkillsError("gh skill list returned an invalid skill name")
        source = _optional_string(item.get("sourceURL"), "sourceURL")
        scope = _optional_string(item.get("scope"), "scope")
        version = _optional_string(item.get("version"), "version")
        pinned_value = item.get("pinned")
        if pinned_value is not None and not isinstance(pinned_value, bool):
            raise AgentSkillsError("gh skill list returned invalid pinned metadata")
        path_value = _optional_string(item.get("path"), "path")
        return InstalledSkill(
            name=name,
            source=source,
            scope=scope,
            version=version,
            pinned=pinned_value,
            path=Path(path_value) if path_value is not None else None,
        )

    @staticmethod
    def _parse_tree_entry(item: dict[object, object]) -> _GitTreeEntry:
        path_value = item.get("path")
        kind = item.get("type")
        mode = item.get("mode")
        object_id = item.get("sha")
        if not isinstance(path_value, str):
            raise AgentSkillsError("gh api returned an invalid pinned Git tree path")
        path = PurePosixPath(path_value)
        if (
            path.is_absolute()
            or path.as_posix() != path_value
            or any(part in {"", ".", ".."} for part in path.parts)
        ):
            raise AgentSkillsError("gh api returned an unsafe pinned Git tree path")
        if kind not in {"blob", "tree", "commit"} or not isinstance(mode, str):
            raise AgentSkillsError("gh api returned invalid pinned Git tree metadata")
        if not isinstance(object_id, str) or _EXACT_COMMIT.fullmatch(object_id) is None:
            raise AgentSkillsError("gh api returned an invalid pinned Git object ID")
        return _GitTreeEntry(path, kind, mode, object_id)

    def _execute(self, arguments: list[str], action: str) -> subprocess.CompletedProcess[str]:
        command = [self.executable, *arguments]
        try:
            result = self.run(
                command,
                capture_output=True,
                check=False,
                env=dict(self.environment),
                text=True,
            )
        except OSError as error:
            raise AgentSkillsError(f"could not {action}: {error}") from error
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
            raise AgentSkillsError(f"could not {action}: {detail}")
        return result


@dataclass(frozen=True)
class _AcceptedCatalog:
    destination: Path
    skills: tuple[InstalledSkill, ...]
    local_content_digest: str
    local_git_blobs: tuple[tuple[str, str], ...]
    skill_sources: Mapping[str, bytes] = field(default_factory=dict)


@dataclass(frozen=True)
class _LocalCatalogSnapshot:
    digest: str
    git_blobs: tuple[tuple[str, str], ...]
    skill_sources: Mapping[str, bytes] = field(default_factory=dict)


def load_agent_skills_lock(repo_root: Path) -> AgentSkillsLock:
    """Read and validate the immutable global skill installation contract."""

    path = repo_root.resolve() / "agent-skills.lock.toml"
    try:
        with path.open("rb") as file:
            payload = tomllib.load(file)
    except FileNotFoundError as error:
        raise AgentSkillsError(f"missing agent skill lock: {path}") from error
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise AgentSkillsError(f"cannot read agent skill lock {path}: {error}") from error

    if payload.get("version") != 2:
        raise AgentSkillsError(f"{path} must declare version = 2")
    repository = payload.get("repository")
    commit = payload.get("commit")
    agent = payload.get("agent")
    directory = payload.get("directory")
    if not isinstance(repository, str) or _REPOSITORY.fullmatch(repository) is None:
        raise AgentSkillsError(f"{path} must declare repository as OWNER/REPO")
    if not isinstance(commit, str) or _EXACT_COMMIT.fullmatch(commit) is None:
        raise AgentSkillsError(f"{path} must pin a full lowercase 40-character commit SHA")
    if agent != "codex":
        raise AgentSkillsError(f'{path} must declare agent = "codex"')
    if not isinstance(directory, str) or not directory:
        raise AgentSkillsError(f"{path} must declare a relative shared skill directory")
    directory_path = Path(directory)
    if directory_path.is_absolute() or any(
        part in {"", ".", ".."} for part in directory_path.parts
    ):
        raise AgentSkillsError(f"{path} must declare a normalized relative shared skill directory")
    return AgentSkillsLock(repository, commit, agent, directory)


def install_agent_skills(
    repo_root: Path,
    *,
    run: CommandRunner = subprocess.run,
    which: CommandLocator = shutil.which,
    environ: Mapping[str, str] | None = None,
) -> AgentSkillsResult:
    """Install every skill at the locked commit and verify the resulting user catalog."""

    lock = load_agent_skills_lock(repo_root)
    environment = dict(os.environ if environ is None else environ)
    registry = _registry(run, which, environment)
    expected = registry.discover(lock)
    destination = _target_directory(lock, environment)
    _reject_collisions(registry.list_shared(destination), expected, lock, destination)
    _reject_conflicting_legacy_skills(registry.list_legacy(lock), expected, lock)
    registry.install(lock, destination)
    catalog = _accept_catalog(registry, lock, expected, destination)
    _accept_pinned_content(registry, lock, expected, catalog)
    return _result(lock, catalog)


def verify_agent_skills(
    repo_root: Path,
    *,
    run: CommandRunner = subprocess.run,
    which: CommandLocator = shutil.which,
    environ: Mapping[str, str] | None = None,
) -> AgentSkillsResult:
    """Verify every skill from the locked remote catalog in the shared user directory."""

    lock = load_agent_skills_lock(repo_root)
    environment = dict(os.environ if environ is None else environ)
    registry = _registry(run, which, environment)
    expected = registry.discover(lock)
    destination = _target_directory(lock, environment)
    catalog = _accept_catalog(registry, lock, expected, destination)
    _accept_pinned_content(registry, lock, expected, catalog)
    return _result(lock, catalog)


def cleanup_legacy_agent_skills(
    repo_root: Path,
    *,
    run: CommandRunner = subprocess.run,
    which: CommandLocator = shutil.which,
    environ: Mapping[str, str] | None = None,
) -> AgentSkillsCleanupResult:
    """Quarantine only the exact, verified legacy Codex catalog after migration."""

    lock = load_agent_skills_lock(repo_root)
    environment = dict(os.environ if environ is None else environ)
    registry = _registry(run, which, environment)
    expected = registry.discover(lock)
    destination = _target_directory(lock, environment)
    catalog = _accept_catalog(registry, lock, expected, destination)
    _accept_pinned_content(registry, lock, expected, catalog)
    legacy = registry.list_legacy(lock)
    plan = _legacy_cleanup_candidates(legacy, expected, lock, environment)
    if plan is None:
        return AgentSkillsCleanupResult(0, None, ())
    try:
        quarantines = remove_verified_directories(
            plan.directories,
            parent_identity=plan.parent_identity,
            parent_parent_identity=plan.parent_parent_identity,
        )
    except MutationExecutionError as error:
        raise AgentSkillsError(f"refusing legacy skill cleanup: {error}") from error
    return AgentSkillsCleanupResult(len(quarantines), plan.parent, quarantines)


def _registry(
    run: CommandRunner,
    which: CommandLocator,
    environment: Mapping[str, str],
) -> GitHubSkillRegistry:
    return GitHubSkillRegistry(_require_gh(which), run=run, environment=environment)


def _require_gh(which: CommandLocator) -> str:
    gh = which("gh")
    if gh is None:
        raise AgentSkillsError("gh is not available in PATH; run ./bootstrap.sh profile first")
    return gh


def _reject_collisions(
    installed: Sequence[InstalledSkill],
    expected: tuple[str, ...],
    lock: AgentSkillsLock,
    destination: Path,
) -> None:
    expected_names = set(expected)
    existing_targets = _existing_expected_targets(destination, expected)
    for name in expected_names:
        matches = [item for item in installed if item.name == name]
        if len(matches) > 1:
            paths = ", ".join(str(item.path or "unknown") for item in matches)
            raise AgentSkillsError(f"refusing to update duplicate user skill {name!r} at: {paths}")
        if not matches:
            if name in existing_targets:
                raise AgentSkillsError(
                    f"refusing to overwrite user skill {name!r}: physical target "
                    "exists without matching inventory ownership"
                )
            continue
        item = matches[0]
        if not _source_matches(item.source, lock.repository):
            raise AgentSkillsError(
                f"refusing to overwrite user skill {name!r} from another source: "
                f"{item.source or 'unknown'}"
            )
        if item.path != destination / name:
            raise AgentSkillsError(
                f"refusing to overwrite user skill {name!r} from another location: "
                f"{item.path or 'unknown'}"
            )
        if item.scope != "custom":
            raise AgentSkillsError(
                f"refusing to overwrite user skill {name!r} from another scope: "
                f"{item.scope or 'unknown'}"
            )


def _reject_conflicting_legacy_skills(
    installed: Sequence[InstalledSkill],
    expected: tuple[str, ...],
    lock: AgentSkillsLock,
) -> None:
    """Refuse install when a legacy copy of a pinned name conflicts with the pin."""

    expected_names = set(expected)
    matching = [item for item in installed if item.name in expected_names]
    if not matching:
        return
    problems: list[str] = []
    for name, matches in _inventory_by_name(matching, expected).items():
        if len(matches) > 1:
            problems.append(f"{name}: legacy catalog is duplicated")
            continue
        if not matches:
            continue
        item = matches[0]
        _append_source_pin_version_problems(
            problems,
            name,
            item,
            lock,
            source_label="legacy source",
            version_label="legacy version",
        )
        if item.scope != "user":
            problems.append(f"{name}: legacy scope is not user")
    _raise_inventory_problems(problems, "refusing legacy skill install")


def _existing_expected_targets(
    destination: Path,
    expected: tuple[str, ...],
) -> frozenset[str]:
    """Inspect every force-install target through one stable directory descriptor."""

    try:
        visible_root = destination.lstat()
    except FileNotFoundError:
        return frozenset()
    except OSError as error:
        raise AgentSkillsError(
            f"refusing force install: cannot inspect shared directory {destination}: {error}"
        ) from error
    if stat.S_ISLNK(visible_root.st_mode) or not stat.S_ISDIR(visible_root.st_mode):
        raise AgentSkillsError(
            f"refusing force install: shared directory is not a physical directory: {destination}"
        )

    descriptor: int | None = None
    try:
        descriptor = os.open(destination, _directory_open_flags())
        opened_root = os.fstat(descriptor)
        root_identity = (visible_root.st_dev, visible_root.st_ino)
        if (
            not stat.S_ISDIR(opened_root.st_mode)
            or (opened_root.st_dev, opened_root.st_ino) != root_identity
        ):
            raise AgentSkillsError(
                f"refusing force install: shared directory changed during inspection: {destination}"
            )
        first = _target_identities(descriptor, expected, destination)
        second = _target_identities(descriptor, expected, destination)
        if first != second:
            raise AgentSkillsError(
                "refusing force install: a physical skill target changed during inspection"
            )
        final_root = destination.lstat()
        if (final_root.st_dev, final_root.st_ino) != root_identity:
            raise AgentSkillsError(
                f"refusing force install: shared directory changed during inspection: {destination}"
            )
        return frozenset(name for name, identity in first.items() if identity is not None)
    except AgentSkillsError:
        raise
    except OSError as error:
        raise AgentSkillsError(
            f"refusing force install: cannot inspect shared directory {destination}: {error}"
        ) from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _target_identities(
    descriptor: int,
    expected: tuple[str, ...],
    destination: Path,
) -> dict[str, tuple[int, int, int] | None]:
    identities: dict[str, tuple[int, int, int] | None] = {}
    for name in expected:
        try:
            metadata = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
        except FileNotFoundError:
            identities[name] = None
        except OSError as error:
            raise AgentSkillsError(
                f"refusing force install: cannot inspect {destination / name}: {error}"
            ) from error
        else:
            identities[name] = (
                metadata.st_dev,
                metadata.st_ino,
                stat.S_IFMT(metadata.st_mode),
            )
    return identities


def _inventory_by_name(
    installed: Sequence[InstalledSkill],
    names: tuple[str, ...],
) -> dict[str, list[InstalledSkill]]:
    return {name: [item for item in installed if item.name == name] for name in names}


def _append_source_pin_version_problems(
    problems: list[str],
    name: str,
    item: InstalledSkill,
    lock: AgentSkillsLock,
    *,
    source_label: str,
    version_label: str,
) -> None:
    if not _source_matches(item.source, lock.repository):
        problems.append(f"{name}: {source_label} does not match {lock.repository}")
    if item.pinned is not True:
        problems.append(f"{name}: installation is not pinned")
    if item.version != lock.commit:
        problems.append(f"{name}: {version_label} does not match {lock.commit}")


def _raise_inventory_problems(problems: list[str], prefix: str) -> None:
    if not problems:
        return
    detail = "; ".join(problems[:5])
    if len(problems) > 5:
        detail += f"; and {len(problems) - 5} more"
    raise AgentSkillsError(f"{prefix}: {detail}")


def _accept_catalog(
    registry: GitHubSkillRegistry,
    lock: AgentSkillsLock,
    expected: tuple[str, ...],
    destination: Path,
) -> _AcceptedCatalog:
    installed = registry.list_shared(destination)
    problems: list[str] = []
    accepted: list[InstalledSkill] = []
    matches_by_name = _inventory_by_name(installed, expected)
    for name in expected:
        matches = matches_by_name[name]
        if not matches:
            problems.append(f"{name}: missing from Codex user scope")
            continue
        if len(matches) > 1:
            problems.append(f"{name}: appears in more than one Codex user-scope location")
            continue
        item = matches[0]
        path = item.path
        if path is None:
            problems.append(f"{name}: installed path is missing")
            continue
        if path != destination / name:
            problems.append(f"{name}: installed path is outside the configured shared directory")
            continue
        _append_source_pin_version_problems(
            problems,
            name,
            item,
            lock,
            source_label="source",
            version_label="installed version",
        )
        if item.scope != "custom":
            problems.append(f"{name}: custom-directory inventory scope is missing")
        accepted.append(item)
    _raise_inventory_problems(problems, "agent skill verification failed")
    snapshot = _local_catalog_snapshot(destination, tuple(accepted))
    return _AcceptedCatalog(
        destination,
        tuple(accepted),
        snapshot.digest,
        snapshot.git_blobs,
        snapshot.skill_sources,
    )


def _result(lock: AgentSkillsLock, catalog: _AcceptedCatalog) -> AgentSkillsResult:
    return AgentSkillsResult(
        repository=lock.repository,
        commit=lock.commit,
        count=len(catalog.skills),
        destination=catalog.destination,
        local_content_digest=catalog.local_content_digest,
    )


def _local_catalog_snapshot(
    destination: Path, installed: tuple[InstalledSkill, ...]
) -> _LocalCatalogSnapshot:
    """Capture one stable, descriptor-bound snapshot of the installed catalog."""

    descriptor: int | None = None
    try:
        visible_root = destination.lstat()
        if stat.S_ISLNK(visible_root.st_mode):
            raise AgentSkillsError(
                "agent skill verification failed: shared skill directory is a "
                f"symbolic link: {destination}"
            )
        if not stat.S_ISDIR(visible_root.st_mode):
            raise AgentSkillsError(
                "agent skill verification failed: shared skill directory is not a "
                f"directory: {destination}"
            )
        descriptor = os.open(destination, _directory_open_flags())
        opened_root = os.fstat(descriptor)
        root_identity = (visible_root.st_dev, visible_root.st_ino)
        if (
            not stat.S_ISDIR(opened_root.st_mode)
            or (opened_root.st_dev, opened_root.st_ino) != root_identity
        ):
            raise AgentSkillsError(
                "agent skill verification failed: shared skill directory changed "
                f"during verification: {destination}"
            )
        files: list[tuple[str, bytes]] = []
        for item in installed:
            files.extend(_capture_skill_files(descriptor, destination, item.name))
        final_root = destination.lstat()
        if (final_root.st_dev, final_root.st_ino) != root_identity:
            raise AgentSkillsError(
                "agent skill verification failed: shared skill directory changed "
                f"during verification: {destination}"
            )
    except AgentSkillsError:
        raise
    except OSError as error:
        raise AgentSkillsError(
            "agent skill verification failed: cannot inspect shared skill directory "
            f"{destination}: {error}"
        ) from error
    finally:
        if descriptor is not None:
            os.close(descriptor)

    digest = hashlib.sha256()
    git_blobs: list[tuple[str, str]] = []
    skill_sources: dict[str, bytes] = {}
    for relative, content in sorted(files):
        skill_name = relative.split("/", 1)[0]
        if relative == f"{skill_name}/SKILL.md":
            # GitHub CLI rewrites SKILL.md frontmatter (sorted keys plus
            # injected github-* source metadata), so it cannot be compared
            # by content blob; the source attestation check covers it.
            skill_sources[skill_name] = content
            continue
        encoded_path = relative.encode()
        digest.update(len(encoded_path).to_bytes(8, "big"))
        digest.update(encoded_path)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
        git_blobs.append((relative, _git_blob_id(content)))
    return _LocalCatalogSnapshot(digest.hexdigest(), tuple(git_blobs), skill_sources)


def _capture_skill_files(
    catalog_descriptor: int,
    destination: Path,
    name: str,
) -> list[tuple[str, bytes]]:
    display_path = destination / name
    try:
        visible = os.stat(name, dir_fd=catalog_descriptor, follow_symlinks=False)
    except OSError as error:
        raise AgentSkillsError(
            f"agent skill verification failed: {name}: skill directory is missing "
            f"or unreadable: {error}"
        ) from error
    if stat.S_ISLNK(visible.st_mode):
        raise AgentSkillsError(
            f"agent skill verification failed: {name}: skill directory is a symbolic link"
        )
    if not stat.S_ISDIR(visible.st_mode):
        raise AgentSkillsError(
            f"agent skill verification failed: {name}: skill directory is not a directory"
        )

    descriptor: int | None = None
    try:
        descriptor = os.open(name, _directory_open_flags(), dir_fd=catalog_descriptor)
        opened = os.fstat(descriptor)
        identity = (visible.st_dev, visible.st_ino)
        if not stat.S_ISDIR(opened.st_mode) or (opened.st_dev, opened.st_ino) != identity:
            raise AgentSkillsError(
                f"agent skill verification failed: {name} changed during verification"
            )
        try:
            snapshot = capture_verified_directory(display_path, descriptor)
        except MutationExecutionError as error:
            raise AgentSkillsError(
                "agent skill verification failed: cannot inspect "
                f"{name}; it changed or contains a symbolic link or unsupported "
                f"file type: {error}"
            ) from error
        except OSError as error:
            raise AgentSkillsError(
                f"agent skill verification failed: cannot inspect {name}: {error}"
            ) from error
        skill_file = next(
            (entry for entry in snapshot.entries if entry.relative_path == Path("SKILL.md")),
            None,
        )
        if skill_file is None or skill_file.kind != "file":
            raise AgentSkillsError(
                f"agent skill verification failed: {name}: SKILL.md is not a readable regular file"
            )
        files = _read_verified_skill_files(descriptor, snapshot, name)
        final_visible = os.stat(
            name,
            dir_fd=catalog_descriptor,
            follow_symlinks=False,
        )
        if (final_visible.st_dev, final_visible.st_ino) != identity:
            raise AgentSkillsError(
                f"agent skill verification failed: {name} changed during verification"
            )
        return files
    except AgentSkillsError:
        raise
    except OSError as error:
        raise AgentSkillsError(
            f"agent skill verification failed: cannot inspect {name}: {error}"
        ) from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _read_verified_skill_files(
    descriptor: int,
    snapshot: VerifiedDirectory,
    skill_name: str,
) -> list[tuple[str, bytes]]:
    children: dict[Path, list[VerifiedDirectoryEntry]] = {}
    for entry in snapshot.entries:
        children.setdefault(entry.relative_path.parent, []).append(entry)
    ordered_children = {
        parent: tuple(sorted(entries, key=lambda entry: entry.relative_path.name))
        for parent, entries in children.items()
    }
    files: list[tuple[str, bytes]] = []
    _read_verified_directory_contents(
        descriptor,
        Path(),
        ordered_children,
        skill_name,
        files,
    )
    return files


def _read_verified_directory_contents(
    descriptor: int,
    relative_parent: Path,
    children: Mapping[Path, tuple[VerifiedDirectoryEntry, ...]],
    skill_name: str,
    files: list[tuple[str, bytes]],
) -> None:
    expected = children.get(relative_parent, ())
    expected_names = tuple(entry.relative_path.name for entry in expected)
    current_names = _scanned_names(descriptor, skill_name, relative_parent)
    if current_names != expected_names:
        raise AgentSkillsError(
            f"agent skill verification failed: {skill_name} changed during verification"
        )
    for entry in expected:
        name = entry.relative_path.name
        display = f"{skill_name}/{entry.relative_path.as_posix()}"
        try:
            visible = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
        except OSError as error:
            raise AgentSkillsError(
                f"agent skill verification failed: cannot inspect {display}: {error}"
            ) from error
        if (visible.st_dev, visible.st_ino) != (entry.device, entry.inode):
            raise AgentSkillsError(
                f"agent skill verification failed: {display} changed during verification"
            )
        if entry.kind == "file":
            content = _read_verified_catalog_file(descriptor, entry, display)
            files.append((display, content))
            continue
        if not stat.S_ISDIR(visible.st_mode):
            raise AgentSkillsError(f"agent skill verification failed: {display} is not a directory")
        child: int | None = None
        try:
            child = os.open(name, _directory_open_flags(), dir_fd=descriptor)
            opened = os.fstat(child)
            if not stat.S_ISDIR(opened.st_mode) or (opened.st_dev, opened.st_ino) != (
                entry.device,
                entry.inode,
            ):
                raise AgentSkillsError(
                    f"agent skill verification failed: {display} changed during verification"
                )
            _read_verified_directory_contents(
                child,
                entry.relative_path,
                children,
                skill_name,
                files,
            )
        except AgentSkillsError:
            raise
        except OSError as error:
            raise AgentSkillsError(
                f"agent skill verification failed: cannot inspect {display}: {error}"
            ) from error
        finally:
            if child is not None:
                os.close(child)
        final_visible = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
        if (final_visible.st_dev, final_visible.st_ino) != (entry.device, entry.inode):
            raise AgentSkillsError(
                f"agent skill verification failed: {display} changed during verification"
            )
    if _scanned_names(descriptor, skill_name, relative_parent) != expected_names:
        raise AgentSkillsError(
            f"agent skill verification failed: {skill_name} changed during verification"
        )


def _scanned_names(
    descriptor: int,
    skill_name: str,
    relative_parent: Path,
) -> tuple[str, ...]:
    try:
        with os.scandir(descriptor) as scanned:
            return tuple(sorted(entry.name for entry in scanned))
    except OSError as error:
        display = skill_name
        if relative_parent != Path():
            display = f"{skill_name}/{relative_parent.as_posix()}"
        raise AgentSkillsError(
            f"agent skill verification failed: cannot inspect {display}: {error}"
        ) from error


def _read_verified_catalog_file(
    parent_descriptor: int,
    entry: VerifiedDirectoryEntry,
    display: str,
) -> bytes:
    descriptor: int | None = None
    try:
        descriptor = os.open(
            entry.relative_path.name,
            _file_open_flags(),
            dir_fd=parent_descriptor,
        )
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or (before.st_dev, before.st_ino) != (
            entry.device,
            entry.inode,
        ):
            raise AgentSkillsError(
                f"agent skill verification failed: {display} changed during verification"
            )
        with os.fdopen(descriptor, "rb") as file:
            descriptor = None
            content = file.read()
            after = os.fstat(file.fileno())
        if (
            not stat.S_ISREG(after.st_mode)
            or (after.st_dev, after.st_ino) != (entry.device, entry.inode)
            or after.st_size != before.st_size
            or after.st_mtime_ns != before.st_mtime_ns
            or hashlib.sha256(content).hexdigest() != entry.content_hash
        ):
            raise AgentSkillsError(
                f"agent skill verification failed: {display} changed during verification"
            )
        visible = os.stat(
            entry.relative_path.name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        if not stat.S_ISREG(visible.st_mode) or (visible.st_dev, visible.st_ino) != (
            entry.device,
            entry.inode,
        ):
            raise AgentSkillsError(
                f"agent skill verification failed: {display} changed during verification"
            )
        return content
    except AgentSkillsError:
        raise
    except OSError as error:
        raise AgentSkillsError(
            f"agent skill verification failed: cannot read {display}: {error}"
        ) from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _directory_open_flags() -> int:
    return (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )


def _file_open_flags() -> int:
    return (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )


def _git_blob_id(content: bytes) -> str:
    digest = hashlib.sha1(usedforsecurity=False)
    digest.update(f"blob {len(content)}\0".encode())
    digest.update(content)
    return digest.hexdigest()


def _pinned_catalog_blobs(
    tree: tuple[_GitTreeEntry, ...],
    expected: tuple[str, ...],
) -> tuple[tuple[str, str], ...]:
    expected_names = set(expected)
    blobs: dict[str, str] = {}
    for entry in tree:
        parts = entry.path.parts
        if len(parts) < 2 or parts[0] != "skills" or parts[1] not in expected_names:
            continue
        skill_name = parts[1]
        if len(parts) == 2:
            if entry.kind != "tree":
                raise AgentSkillsError(
                    f"pinned agent skill source has an invalid root: {entry.path}"
                )
            continue
        relative = PurePosixPath(*parts[2:])
        if relative.as_posix() == "SKILL.md":
            # GitHub CLI rewrites SKILL.md frontmatter; verified via the
            # source attestation instead of a content blob.
            continue
        installed_path = f"{skill_name}/{relative.as_posix()}"
        if entry.kind == "tree":
            continue
        if entry.kind != "blob" or entry.mode not in {"100644", "100755"}:
            raise AgentSkillsError(
                "pinned agent skill source contains a symbolic link or unsupported "
                f"entry: {entry.path}"
            )
        if installed_path in blobs:
            raise AgentSkillsError(
                f"pinned agent skill source contains a duplicate path: {entry.path}"
            )
        blobs[installed_path] = entry.object_id
    for name in expected:
        if not any(
            entry.path.parts[:2] == ("skills", name) and entry.kind == "tree"
            for entry in tree
        ):
            raise AgentSkillsError(f"pinned agent skill source is missing {name}/SKILL.md")
    return tuple(sorted(blobs.items()))


def _pinned_skill_tree_shas(
    tree: tuple[_GitTreeEntry, ...],
    expected: tuple[str, ...],
) -> dict[str, str]:
    shas: dict[str, str] = {}
    for name in expected:
        children = sorted(
            (
                entry
                for entry in tree
                if len(entry.path.parts) == 3
                and entry.path.parts[0] == "skills"
                and entry.path.parts[1] == name
            ),
            key=lambda entry: entry.path.parts[-1]
            + ("/" if entry.kind == "tree" else ""),
        )
        body = b"".join(
            f"{'40000' if entry.kind == 'tree' else entry.mode} {entry.path.parts[-1]}\0".encode()
            + bytes.fromhex(entry.object_id)
            for entry in children
        )
        digest = hashlib.sha1(usedforsecurity=False)
        digest.update(f"tree {len(body)}\0".encode())
        digest.update(body)
        shas[name] = digest.hexdigest()
    return shas


def _accept_pinned_content(
    registry: GitHubSkillRegistry,
    lock: AgentSkillsLock,
    expected: tuple[str, ...],
    catalog: _AcceptedCatalog,
) -> None:
    tree = registry.pinned_tree(lock)
    pinned_blobs = _pinned_catalog_blobs(tree, expected)
    _require_pinned_content(catalog.local_git_blobs, pinned_blobs)
    _require_source_attestation(catalog.skill_sources, tree, expected, lock)


_GH_META_LINES = {
    name: re.compile(rf"^    {name}: (.+)$", re.MULTILINE)
    for name in ("github-path", "github-pinned", "github-ref", "github-tree-sha")
}


def _require_source_attestation(
    skill_sources: Mapping[str, bytes],
    tree: tuple[_GitTreeEntry, ...],
    expected: tuple[str, ...],
    lock: AgentSkillsLock,
) -> None:
    """Verify GitHub CLI's injected source metadata pins each SKILL.md to the lock.

    GitHub CLI rewrites SKILL.md frontmatter (alphabetized keys plus injected
    github-* source metadata), so SKILL.md content cannot be byte-compared
    against the pinned tree. GitHub CLI instead records which git tree each
    skill was installed from; that attestation must name the lock commit and
    the pinned skill directory's exact tree SHA.
    """
    expected_trees = _pinned_skill_tree_shas(tree, expected)
    missing = sorted(set(expected) - set(skill_sources))
    if missing:
        raise AgentSkillsError(
            "agent skill verification failed: installed SKILL.md is unreadable "
            f"for {', '.join(missing[:3])}"
        )
    problems: list[str] = []
    for name in sorted(expected):
        text = skill_sources[name].decode("utf-8", errors="replace")
        found = {
            meta: (match.group(1).strip() if (match := pattern.search(text)) else None)
            for meta, pattern in _GH_META_LINES.items()
        }
        if found["github-path"] != f"skills/{name}":
            problems.append(f"{name}: SKILL.md source path is not attested")
        if found["github-pinned"] != lock.commit or found["github-ref"] != lock.commit:
            problems.append(f"{name}: SKILL.md is not attested to the pinned commit")
        if found["github-tree-sha"] != expected_trees[name]:
            problems.append(f"{name}: SKILL.md tree does not match the pinned tree")
    if problems:
        raise AgentSkillsError(
            "agent skill verification failed: installed source attestation does not "
            f"match the pinned commit ({'; '.join(problems[:3])})"
        )


def _require_pinned_content(
    local: tuple[tuple[str, str], ...],
    pinned: tuple[tuple[str, str], ...],
) -> None:
    local_by_path = dict(local)
    pinned_by_path = dict(pinned)
    missing = sorted(pinned_by_path.keys() - local_by_path.keys())
    unexpected = sorted(local_by_path.keys() - pinned_by_path.keys())
    changed = sorted(
        path
        for path in local_by_path.keys() & pinned_by_path.keys()
        if local_by_path[path] != pinned_by_path[path]
    )
    if not missing and not unexpected and not changed:
        return
    details: list[str] = []
    if missing:
        details.append(f"missing {', '.join(missing[:3])}")
    if unexpected:
        details.append(f"unexpected {', '.join(unexpected[:3])}")
    if changed:
        details.append(f"changed {', '.join(changed[:3])}")
    raise AgentSkillsError(
        "agent skill verification failed: installed content does not match the "
        f"pinned commit ({'; '.join(details)})"
    )


def _target_directory(lock: AgentSkillsLock, environment: Mapping[str, str]) -> Path:
    context = UserPathContext.from_environment(environment)
    try:
        return context.agent_skills_target(lock.directory)
    except ValueError as error:
        raise AgentSkillsError(
            "configured shared skill directory escapes the current home directory"
        ) from error


def _legacy_cleanup_candidates(
    installed: Sequence[InstalledSkill],
    expected: tuple[str, ...],
    lock: AgentSkillsLock,
    environment: Mapping[str, str],
) -> _LegacyCleanupPlan | None:
    expected_names = set(expected)
    matching = [item for item in installed if item.name in expected_names]
    if not matching:
        return None
    home = UserPathContext.from_environment(environment).home
    resolved_home = home.resolve()
    shared_directory = _target_directory(lock, environment)
    candidates: list[VerifiedDirectory] = []
    problems: list[str] = []
    matches_by_name = _inventory_by_name(matching, expected)
    for name in expected:
        matches = matches_by_name[name]
        if len(matches) != 1:
            problems.append(f"{name}: legacy catalog is incomplete or duplicated")
            continue
        item = matches[0]
        path = item.path
        if (
            path is None
            or not path.is_absolute()
            or path.name != name
            or not path.is_relative_to(home)
        ):
            problems.append(f"{name}: legacy path is outside the current home directory")
            continue
        _append_source_pin_version_problems(
            problems,
            name,
            item,
            lock,
            source_label="legacy source",
            version_label="legacy version",
        )
        if item.scope != "user":
            problems.append(f"{name}: legacy scope is not user")
        try:
            resolved_path = path.resolve(strict=True)
        except OSError:
            problems.append(f"{name}: legacy path is missing or unreadable")
            continue
        if resolved_path != path or not resolved_path.is_relative_to(resolved_home):
            problems.append(f"{name}: legacy path has a symlinked ancestor or escapes HOME")
            continue
        if path.parent == shared_directory:
            problems.append(f"{name}: legacy path resolves to the shared directory")
            continue
        candidate = _inspect_legacy_skill_directory(problems, name, path)
        if candidate is not None:
            candidates.append(candidate)
    parents = {candidate.path.parent for candidate in candidates}
    if len(parents) > 1:
        problems.append("legacy catalog directories do not share one parent")
    _raise_inventory_problems(problems, "refusing legacy skill cleanup")
    if not candidates:
        return None
    parent = candidates[0].path.parent
    try:
        parent_metadata = parent.lstat()
        parent_parent_metadata = parent.parent.lstat()
    except OSError as error:
        raise AgentSkillsError(
            f"refusing legacy skill cleanup: parent is unavailable: {parent}"
        ) from error
    if (
        stat.S_ISLNK(parent_metadata.st_mode)
        or not stat.S_ISDIR(parent_metadata.st_mode)
        or stat.S_ISLNK(parent_parent_metadata.st_mode)
        or not stat.S_ISDIR(parent_parent_metadata.st_mode)
    ):
        raise AgentSkillsError(f"refusing legacy skill cleanup: parent is unsafe: {parent}")
    return _LegacyCleanupPlan(
        tuple(candidates),
        (parent_metadata.st_dev, parent_metadata.st_ino),
        (parent_parent_metadata.st_dev, parent_parent_metadata.st_ino),
    )


def _inspect_legacy_skill_directory(
    problems: list[str], name: str, path: Path
) -> VerifiedDirectory | None:
    """Validate one legacy skill through bound parent and directory descriptors."""

    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    parent_descriptor: int | None = None
    directory_descriptor: int | None = None
    skill_descriptor: int | None = None
    try:
        parent_metadata = path.parent.lstat()
        parent_descriptor = os.open(path.parent, flags)
        opened_parent = os.fstat(parent_descriptor)
        if (opened_parent.st_dev, opened_parent.st_ino) != (
            parent_metadata.st_dev,
            parent_metadata.st_ino,
        ):
            problems.append(f"{name}: legacy parent changed during validation")
            return None
        directory_descriptor = os.open(path.name, flags, dir_fd=parent_descriptor)
        metadata = os.fstat(directory_descriptor)
        visible_skill = os.stat(
            "SKILL.md",
            dir_fd=directory_descriptor,
            follow_symlinks=False,
        )
        if not stat.S_ISREG(visible_skill.st_mode):
            problems.append(f"{name}: SKILL.md is not a readable regular file")
            return None
        skill_descriptor = os.open(
            "SKILL.md",
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_NONBLOCK", 0),
            dir_fd=directory_descriptor,
        )
        skill_metadata = os.fstat(skill_descriptor)
        if (skill_metadata.st_dev, skill_metadata.st_ino) != (
            visible_skill.st_dev,
            visible_skill.st_ino,
        ) or not stat.S_ISREG(skill_metadata.st_mode):
            problems.append(f"{name}: SKILL.md is not a readable regular file")
            return None
        os.read(skill_descriptor, 1)
        candidate = capture_verified_directory(path, directory_descriptor)
        visible = os.stat(
            path.name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        if (visible.st_dev, visible.st_ino) != (metadata.st_dev, metadata.st_ino):
            problems.append(f"{name}: legacy path changed during validation")
            return None
        return candidate
    except (MutationExecutionError, OSError):
        problems.append(f"{name}: legacy path changed or SKILL.md is unreadable")
        return None
    finally:
        for descriptor in (
            skill_descriptor,
            directory_descriptor,
            parent_descriptor,
        ):
            if descriptor is not None:
                os.close(descriptor)


def _source_matches(value: object, repository: str) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.rstrip("/").removesuffix(".git")
    return normalized in {
        repository,
        f"https://github.com/{repository}",
        f"git@github.com:{repository}",
    }


def _optional_string(value: object, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise AgentSkillsError(f"gh skill list returned invalid {field_name} metadata")
    return value
