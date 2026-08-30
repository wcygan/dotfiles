from __future__ import annotations

import json
import subprocess
from pathlib import Path, PurePosixPath

import pytest

from dotfiles_setup.agent_skills import (
    AgentSkillsError,
    AgentSkillsLock,
    GitHubSkillRegistry,
    InstalledSkill,
)

COMMIT = "1fd1be4aff30a4f4741e1f9cc3ae9faf1a876398"


def _completed(
    command: list[str], *, stdout: str = "", stderr: str = "", returncode: int = 0
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(command, returncode, stdout, stderr)


def _lock() -> AgentSkillsLock:
    return AgentSkillsLock(
        repository="wcygan/agent-skills",
        commit=COMMIT,
        agent="codex",
        directory=".agents/skills",
    )


def test_registry_owns_catalog_discovery_command_and_parsing() -> None:
    calls: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return _completed(
            command,
            stdout=f"Using ref {COMMIT}\nanimate\tdescription\n"
            "hill-climbing\tdescription\n",
        )

    registry = GitHubSkillRegistry("/opt/bin/gh", run=runner, environment={})

    assert registry.discover(_lock()) == ("animate", "hill-climbing")
    assert calls == [
        [
            "/opt/bin/gh",
            "skill",
            "install",
            "wcygan/agent-skills",
            "--pin",
            COMMIT,
        ]
    ]


def test_registry_owns_shared_inventory_command_and_typed_parsing(tmp_path: Path) -> None:
    destination = tmp_path / ".agents" / "skills"
    payload = [
        {
            "skillName": "animate",
            "sourceURL": "https://github.com/wcygan/agent-skills",
            "scope": "custom",
            "version": COMMIT,
            "pinned": True,
            "path": str(destination / "animate"),
        }
    ]
    calls: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return _completed(command, stdout=json.dumps(payload))

    registry = GitHubSkillRegistry("/opt/bin/gh", run=runner, environment={})

    assert registry.list_shared(destination) == (
        InstalledSkill(
            name="animate",
            source="https://github.com/wcygan/agent-skills",
            scope="custom",
            version=COMMIT,
            pinned=True,
            path=destination / "animate",
        ),
    )
    assert calls == [
        [
            "/opt/bin/gh",
            "skill",
            "list",
            "--dir",
            str(destination),
            "--json",
            "skillName,sourceURL,scope,version,pinned,path",
        ]
    ]


def test_registry_owns_install_command(tmp_path: Path) -> None:
    destination = tmp_path / ".agents" / "skills"
    calls: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return _completed(command)

    registry = GitHubSkillRegistry("/opt/bin/gh", run=runner, environment={})

    registry.install(_lock(), destination)

    assert calls == [
        [
            "/opt/bin/gh",
            "skill",
            "install",
            "wcygan/agent-skills",
            "--all",
            "--pin",
            COMMIT,
            "--force",
            "--dir",
            str(destination),
        ]
    ]


def test_registry_owns_legacy_inventory_command() -> None:
    calls: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return _completed(command, stdout="[]")

    registry = GitHubSkillRegistry("/opt/bin/gh", run=runner, environment={})

    assert registry.list_legacy(_lock()) == ()
    assert calls == [
        [
            "/opt/bin/gh",
            "skill",
            "list",
            "--agent",
            "codex",
            "--scope",
            "user",
            "--json",
            "skillName,sourceURL,scope,version,pinned,path",
        ]
    ]


def test_registry_owns_pinned_tree_command_and_typed_parsing() -> None:
    calls: list[list[str]] = []
    payload = {
        "truncated": False,
        "tree": [
            {
                "path": "skills/animate/SKILL.md",
                "mode": "100644",
                "type": "blob",
                "sha": "1" * 40,
            }
        ],
    }

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return _completed(command, stdout=json.dumps(payload))

    registry = GitHubSkillRegistry("/opt/bin/gh", run=runner, environment={})

    entries = registry.pinned_tree(_lock())

    assert len(entries) == 1
    assert entries[0].path == PurePosixPath("skills/animate/SKILL.md")
    assert entries[0].kind == "blob"
    assert entries[0].mode == "100644"
    assert entries[0].object_id == "1" * 40
    assert calls == [
        [
            "/opt/bin/gh",
            "api",
            f"repos/wcygan/agent-skills/git/trees/{COMMIT}?recursive=1",
        ]
    ]


def test_registry_translates_command_failures() -> None:
    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        return _completed(command, stderr="authentication failed", returncode=1)

    registry = GitHubSkillRegistry("/opt/bin/gh", run=runner, environment={})

    with pytest.raises(AgentSkillsError, match="authentication failed"):
        registry.discover(_lock())
