from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.agent_skills import (
    AgentSkillsCleanupResult,
    AgentSkillsError,
    AgentSkillsResult,
    cleanup_legacy_agent_skills,
    install_agent_skills,
    load_agent_skills_lock,
    verify_agent_skills,
)
from dotfiles_setup.manifest import state_directory

COMMIT = "897d6df567d6d7ed50aa62f4d5c3733c60d1adc7"


def _write_lock(repo_root: Path, *, commit: str = COMMIT) -> None:
    repo_root.joinpath("agent-skills.lock.toml").write_text(
        "\n".join(
            (
                "version = 2",
                'repository = "wcygan/agent-skills"',
                f'commit = "{commit}"',
                'agent = "codex"',
                'directory = ".agents/skills"',
                "",
            )
        )
    )


def _completed(
    command: list[str], *, stdout: str = "", stderr: str = "", returncode: int = 0
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(command, returncode, stdout, stderr)


def _installed(home: Path) -> str:
    return json.dumps(
        [
            {
                "skillName": name,
                "sourceURL": "https://github.com/wcygan/agent-skills",
                "scope": "custom",
                "version": COMMIT,
                "pinned": True,
                "path": str(home / ".agents" / "skills" / name),
            }
            for name in ("animate", "hill-climbing")
        ]
    )


def _legacy_installed(home: Path) -> str:
    return json.dumps(
        [
            {
                "skillName": name,
                "sourceURL": "https://github.com/wcygan/agent-skills",
                "scope": "user",
                "version": COMMIT,
                "pinned": True,
                "path": str(home / ".codex" / "skills" / name),
            }
            for name in ("animate", "hill-climbing")
        ]
    )


def test_lock_requires_an_exact_commit_and_shared_codex_directory(tmp_path: Path) -> None:
    _write_lock(tmp_path)

    lock = load_agent_skills_lock(tmp_path)

    assert lock.repository == "wcygan/agent-skills"
    assert lock.commit == COMMIT
    assert lock.agent == "codex"
    assert lock.directory == ".agents/skills"


def test_repository_lock_pins_the_authoritative_catalog() -> None:
    lock = load_agent_skills_lock(Path.cwd())

    assert lock.repository == "wcygan/agent-skills"
    assert lock.commit == COMMIT
    assert lock.agent == "codex"
    assert lock.directory == ".agents/skills"


def test_make_targets_route_through_the_supported_bootstrap_entrypoint() -> None:
    makefile = Path("Makefile").read_text()

    assert "agent-skills:\n\t@$(BOOTSTRAP) agent-skills" in makefile
    assert "agent-skills-check:\n\t@$(BOOTSTRAP) agent-skills --check" in makefile


def test_repository_mandates_the_agent_skills_integration_skill() -> None:
    skill = Path(".agents/skills/agent-skills-integration/SKILL.md")
    agents = Path("AGENTS.md").read_text()
    operations_skill = Path(".agents/skills/dotfiles-operations/SKILL.md").read_text()
    architecture = Path(
        ".agents/skills/dotfiles-operations/references/architecture.md"
    ).read_text()
    operations = Path(
        ".agents/skills/dotfiles-operations/references/operations.md"
    ).read_text()

    assert skill.is_file()
    assert skill.read_text().startswith(
        "---\nname: agent-skills-integration\ndescription:"
    )
    assert "**must** also use `$agent-skills-integration`" in agents
    assert "$agent-skills-integration" in operations_skill
    assert "Agent Skills Provider/Consumer Boundary" in architecture
    assert "Use `$agent-skills-integration` for every" in operations
    assert "GitHub CLI refreshes `updatedAt`" in skill.read_text()
    assert "catalog-state idempotent" in operations


def test_lock_rejects_a_mutable_ref(tmp_path: Path) -> None:
    _write_lock(tmp_path, commit="main")

    with pytest.raises(AgentSkillsError, match="40-character commit SHA"):
        load_agent_skills_lock(tmp_path)


def test_lock_rejects_a_directory_outside_home(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    path = tmp_path / "agent-skills.lock.toml"
    path.write_text(
        path.read_text().replace('directory = ".agents/skills"', 'directory = "/tmp"')
    )

    with pytest.raises(AgentSkillsError, match="relative shared skill directory"):
        load_agent_skills_lock(tmp_path)


def test_install_discovers_installs_and_verifies_with_gh(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    gh = str(tmp_path / "bin" / "gh")
    calls: list[list[str]] = []
    list_count = 0

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        nonlocal list_count
        calls.append(command)
        if command[1:3] == ["skill", "list"]:
            list_count += 1
            return _completed(command, stdout="[]" if list_count == 1 else _installed(home))
        if "--all" in command:
            return _completed(command, stdout="Installed 2 skills\n")
        return _completed(
            command,
            stdout=f"Using ref {COMMIT} ({COMMIT[:8]})\nanimate\tdescription\n"
            "hill-climbing\tdescription\n",
        )

    result = install_agent_skills(
        tmp_path,
        run=runner,
        which=lambda _: gh,
        environ={"HOME": str(home)},
    )

    assert result == AgentSkillsResult(
        "wcygan/agent-skills", COMMIT, 2, home / ".agents" / "skills"
    )
    install = next(command for command in calls if "--all" in command)
    assert install == [
        gh,
        "skill",
        "install",
        "wcygan/agent-skills",
        "--all",
        "--pin",
        COMMIT,
        "--force",
        "--dir",
        str(home / ".agents" / "skills"),
    ]


def test_install_refuses_to_overwrite_another_source(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    calls: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[1:3] == ["skill", "list"]:
            return _completed(
                command,
                stdout=json.dumps(
                    [
                        {
                            "skillName": "animate",
                            "sourceURL": "https://github.com/example/other",
                            "scope": "custom",
                            "version": "v1",
                            "pinned": False,
                            "path": str(home / ".agents" / "skills" / "animate"),
                        }
                    ]
                ),
            )
        return _completed(command, stdout="animate\tdescription\n")

    with pytest.raises(AgentSkillsError, match="refusing to overwrite"):
        install_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert not any("--all" in command for command in calls)


def test_verify_requires_the_exact_pin_for_every_catalog_skill(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    inventory = json.loads(_installed(home))
    inventory[1]["version"] = "main"

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=json.dumps(inventory))
        return _completed(
            command,
            stdout="animate\tdescription\nhill-climbing\tdescription\n",
        )

    with pytest.raises(AgentSkillsError, match="installed version does not match"):
        verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_cleanup_removes_only_the_verified_legacy_catalog(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    legacy_root = home / ".codex" / "skills"
    for name in ("animate", "hill-climbing"):
        skill = legacy_root / name
        skill.mkdir(parents=True)
        skill.joinpath("SKILL.md").write_text("---\nname: test\ndescription: test\n---\n")

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=_legacy_installed(home))
        return _completed(
            command, stdout="animate\tdescription\nhill-climbing\tdescription\n"
        )

    result = cleanup_legacy_agent_skills(
        tmp_path,
        run=runner,
        which=lambda _: "/bin/gh",
        environ={"HOME": str(home)},
    )

    assert result.count == 2
    assert result.destination == legacy_root
    assert not legacy_root.exists()


def test_cleanup_refuses_a_legacy_catalog_from_another_source(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    inventory = json.loads(_legacy_installed(home))
    inventory[0]["sourceURL"] = "https://github.com/example/other"

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=json.dumps(inventory))
        return _completed(
            command, stdout="animate\tdescription\nhill-climbing\tdescription\n"
        )

    with pytest.raises(AgentSkillsError, match="legacy source does not match"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_cleanup_refuses_to_remove_the_shared_catalog(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    inventory = json.loads(_legacy_installed(home))
    for item in inventory:
        item["path"] = str(home / ".agents" / "skills" / item["skillName"])

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=json.dumps(inventory))
        return _completed(
            command, stdout="animate\tdescription\nhill-climbing\tdescription\n"
        )

    with pytest.raises(AgentSkillsError, match="resolves to the shared directory"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_agent_skills_cli_uses_a_mutation_journal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setattr(
        cli,
        "install_agent_skills",
        lambda _: AgentSkillsResult(
            "wcygan/agent-skills", COMMIT, 42, home / ".agents" / "skills"
        ),
    )

    assert cli.main(["agent-skills"]) == 0
    assert "42 pinned Codex shared-user skills" in capsys.readouterr().out
    assert state_directory().joinpath("completed.json").is_file()


def test_agent_skills_check_is_read_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setattr(
        cli,
        "verify_agent_skills",
        lambda _: AgentSkillsResult(
            "wcygan/agent-skills", COMMIT, 42, home / ".agents" / "skills"
        ),
    )

    assert cli.main(["agent-skills", "--check"]) == 0
    assert "42 pinned Codex shared-user skills" in capsys.readouterr().out
    assert not state_directory().exists()


def test_agent_skills_legacy_cleanup_requires_explicit_authorization(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert cli.main(["agent-skills", "--cleanup-legacy"]) == 2
    assert "Legacy cleanup requires --yes." in capsys.readouterr().out


def test_agent_skills_legacy_cleanup_uses_a_mutation_journal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setattr(
        cli,
        "cleanup_legacy_agent_skills",
        lambda _: AgentSkillsCleanupResult(2, home / ".codex" / "skills"),
    )

    assert cli.main(["agent-skills", "--cleanup-legacy", "--yes"]) == 0
    assert "Removed 2 legacy Codex user skills" in capsys.readouterr().out
    assert state_directory().joinpath("completed.json").is_file()
