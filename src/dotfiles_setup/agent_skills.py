"""Install the repository-pinned shared Codex skill catalog with GitHub CLI."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tomllib
from collections.abc import Callable, Mapping, Sequence
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotfiles_setup.errors import SetupError

Command = Sequence[str]
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
class AgentSkillsResult:
    repository: str
    commit: str
    count: int
    destination: Path

    def __str__(self) -> str:
        return (
            f"{self.count} pinned Codex shared-user skills from "
            f"{self.repository}@{self.commit} at {self.destination}"
        )


@dataclass(frozen=True)
class AgentSkillsCleanupResult:
    count: int
    destination: Path | None

    def __str__(self) -> str:
        if self.destination is None:
            return "No legacy Codex user skills required cleanup."
        return f"Removed {self.count} legacy Codex user skills from {self.destination}"


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
    gh = _require_gh(which)
    environment = dict(os.environ if environ is None else environ)
    expected = _discover_catalog(gh, lock, run=run, environment=environment)
    installed = _list_installed(gh, lock, run=run, environment=environment)
    _reject_collisions(installed, expected, lock)

    command = [
        gh,
        "skill",
        "install",
        lock.repository,
        "--all",
        "--pin",
        lock.commit,
        "--force",
        "--dir",
        str(_target_directory(lock, environment)),
    ]
    _run_gh(run, command, environment, "install pinned agent skills")
    return _verify(gh, lock, expected, run=run, environment=environment)


def verify_agent_skills(
    repo_root: Path,
    *,
    run: CommandRunner = subprocess.run,
    which: CommandLocator = shutil.which,
    environ: Mapping[str, str] | None = None,
) -> AgentSkillsResult:
    """Verify every skill from the locked remote catalog in the shared user directory."""

    lock = load_agent_skills_lock(repo_root)
    gh = _require_gh(which)
    environment = dict(os.environ if environ is None else environ)
    expected = _discover_catalog(gh, lock, run=run, environment=environment)
    return _verify(gh, lock, expected, run=run, environment=environment)


def cleanup_legacy_agent_skills(
    repo_root: Path,
    *,
    run: CommandRunner = subprocess.run,
    which: CommandLocator = shutil.which,
    environ: Mapping[str, str] | None = None,
) -> AgentSkillsCleanupResult:
    """Remove only the exact, verified legacy Codex catalog after migration."""

    lock = load_agent_skills_lock(repo_root)
    gh = _require_gh(which)
    environment = dict(os.environ if environ is None else environ)
    expected = _discover_catalog(gh, lock, run=run, environment=environment)
    legacy = _list_legacy_installed(gh, lock, run=run, environment=environment)
    candidates = _legacy_cleanup_candidates(legacy, expected, lock, environment)
    if not candidates:
        return AgentSkillsCleanupResult(0, None)

    parent = candidates[0].parent
    for candidate in candidates:
        if candidate.parent != parent or candidate.is_symlink() or not candidate.is_dir():
            raise AgentSkillsError(
                f"refusing to remove an unexpected legacy skill path: {candidate}"
            )
    for candidate in candidates:
        shutil.rmtree(candidate)
    with suppress(OSError):
        parent.rmdir()
    return AgentSkillsCleanupResult(len(candidates), parent)


def _require_gh(which: CommandLocator) -> str:
    gh = which("gh")
    if gh is None:
        raise AgentSkillsError("gh is not available in PATH; run ./bootstrap.sh profile first")
    return gh


def _discover_catalog(
    gh: str,
    lock: AgentSkillsLock,
    *,
    run: CommandRunner,
    environment: Mapping[str, str],
) -> tuple[str, ...]:
    command = [
        gh,
        "skill",
        "install",
        lock.repository,
        "--pin",
        lock.commit,
    ]
    result = _run_gh(run, command, environment, "list the pinned agent skill catalog")
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


def _list_installed(
    gh: str,
    lock: AgentSkillsLock,
    *,
    run: CommandRunner,
    environment: Mapping[str, str],
) -> list[dict[str, Any]]:
    command = [
        gh,
        "skill",
        "list",
        "--dir",
        str(_target_directory(lock, environment)),
        "--json",
        _LIST_FIELDS,
    ]
    return _parse_inventory(
        _run_gh(run, command, environment, "inspect installed agent skills")
    )


def _list_legacy_installed(
    gh: str,
    lock: AgentSkillsLock,
    *,
    run: CommandRunner,
    environment: Mapping[str, str],
) -> list[dict[str, Any]]:
    command = [
        gh,
        "skill",
        "list",
        "--agent",
        lock.agent,
        "--scope",
        "user",
        "--json",
        _LIST_FIELDS,
    ]
    return _parse_inventory(
        _run_gh(run, command, environment, "inspect legacy Codex skills")
    )


def _parse_inventory(result: subprocess.CompletedProcess[str]) -> list[dict[str, Any]]:
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise AgentSkillsError("gh skill list returned invalid JSON") from error
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise AgentSkillsError("gh skill list returned an invalid skill inventory")
    return payload


def _reject_collisions(
    installed: list[dict[str, Any]],
    expected: tuple[str, ...],
    lock: AgentSkillsLock,
) -> None:
    expected_names = set(expected)
    for name in expected_names:
        matches = [item for item in installed if item.get("skillName") == name]
        if len(matches) > 1:
            paths = ", ".join(str(item.get("path") or "unknown") for item in matches)
            raise AgentSkillsError(
                f"refusing to update duplicate user skill {name!r} at: {paths}"
            )
        if not matches:
            continue
        item = matches[0]
        source = item.get("sourceURL")
        if not _source_matches(source, lock.repository):
            raise AgentSkillsError(
                f"refusing to overwrite user skill {name!r} from another source: "
                f"{source or 'unknown'}"
            )


def _verify(
    gh: str,
    lock: AgentSkillsLock,
    expected: tuple[str, ...],
    *,
    run: CommandRunner,
    environment: Mapping[str, str],
) -> AgentSkillsResult:
    installed = _list_installed(gh, lock, run=run, environment=environment)
    problems: list[str] = []
    parents: set[Path] = set()
    destination = _target_directory(lock, environment)
    for name in expected:
        matches = [item for item in installed if item.get("skillName") == name]
        if not matches:
            problems.append(f"{name}: missing from Codex user scope")
            continue
        if len(matches) > 1:
            problems.append(f"{name}: appears in more than one Codex user-scope location")
            continue
        item = matches[0]
        path_value = item.get("path")
        if not isinstance(path_value, str):
            problems.append(f"{name}: installed path is missing")
            continue
        path = Path(path_value).resolve(strict=False)
        if path.name != name or path.parent != destination:
            problems.append(
                f"{name}: installed path is outside the configured shared directory"
            )
        parents.add(path.parent)
        if not _source_matches(item.get("sourceURL"), lock.repository):
            problems.append(f"{name}: source does not match {lock.repository}")
        if item.get("scope") != "custom":
            problems.append(f"{name}: custom-directory inventory scope is missing")
        if item.get("pinned") is not True:
            problems.append(f"{name}: installation is not pinned")
        if item.get("version") != lock.commit:
            problems.append(f"{name}: installed version does not match {lock.commit}")
    if problems:
        detail = "; ".join(problems[:5])
        if len(problems) > 5:
            detail += f"; and {len(problems) - 5} more"
        raise AgentSkillsError(f"agent skill verification failed: {detail}")
    if len(parents) != 1:
        rendered = ", ".join(str(path) for path in sorted(parents)) or "none"
        raise AgentSkillsError(
            f"agent skill verification failed: catalog spans unexpected locations: {rendered}"
        )
    return AgentSkillsResult(lock.repository, lock.commit, len(expected), parents.pop())


def _target_directory(lock: AgentSkillsLock, environment: Mapping[str, str]) -> Path:
    home = Path(environment.get("HOME", str(Path.home()))).expanduser().resolve()
    destination = (home / lock.directory).resolve(strict=False)
    if not destination.is_relative_to(home):
        raise AgentSkillsError(
            "configured shared skill directory escapes the current home directory"
        )
    return destination


def _legacy_cleanup_candidates(
    installed: list[dict[str, Any]],
    expected: tuple[str, ...],
    lock: AgentSkillsLock,
    environment: Mapping[str, str],
) -> list[Path]:
    expected_names = set(expected)
    matching = [item for item in installed if item.get("skillName") in expected_names]
    if not matching:
        return []
    home = Path(environment.get("HOME", str(Path.home()))).expanduser().resolve()
    shared_directory = _target_directory(lock, environment)
    candidates: list[Path] = []
    problems: list[str] = []
    for name in expected:
        matches = [item for item in matching if item.get("skillName") == name]
        if len(matches) != 1:
            problems.append(f"{name}: legacy catalog is incomplete or duplicated")
            continue
        item = matches[0]
        path_value = item.get("path")
        path = (
            Path(path_value).resolve(strict=False)
            if isinstance(path_value, str)
            else None
        )
        if path is None or path.name != name or not path.is_relative_to(home):
            problems.append(f"{name}: legacy path is outside the current home directory")
            continue
        if path.parent == shared_directory:
            problems.append(f"{name}: legacy path resolves to the shared directory")
            continue
        if not _source_matches(item.get("sourceURL"), lock.repository):
            problems.append(f"{name}: legacy source does not match {lock.repository}")
        if item.get("scope") != "user":
            problems.append(f"{name}: legacy scope is not user")
        if item.get("pinned") is not True:
            problems.append(f"{name}: legacy installation is not pinned")
        if item.get("version") != lock.commit:
            problems.append(f"{name}: legacy version does not match {lock.commit}")
        candidates.append(path)
    if problems:
        detail = "; ".join(problems[:5])
        if len(problems) > 5:
            detail += f"; and {len(problems) - 5} more"
        raise AgentSkillsError(f"refusing legacy skill cleanup: {detail}")
    return candidates


def _source_matches(value: object, repository: str) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.rstrip("/").removesuffix(".git")
    return normalized in {
        repository,
        f"https://github.com/{repository}",
        f"git@github.com:{repository}",
    }


def _run_gh(
    run: CommandRunner,
    command: Command,
    environment: Mapping[str, str],
    action: str,
) -> subprocess.CompletedProcess[str]:
    try:
        result = run(
            list(command),
            capture_output=True,
            check=False,
            env=dict(environment),
            text=True,
        )
    except OSError as error:
        raise AgentSkillsError(f"could not {action}: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise AgentSkillsError(f"could not {action}: {detail}")
    return result
