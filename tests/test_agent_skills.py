from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path

import pytest

from dotfiles_setup import agent_skills as agent_skills_module
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

COMMIT = "2ee4c6b85a7d7ca5c0a0c9f5cc0b4f4d7b1fc9a4"


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


def _write_catalog(
    destination: Path,
    names: tuple[str, ...] = ("animate", "hill-climbing"),
) -> None:
    for name in names:
        skill = destination / name
        skill.mkdir(parents=True)
        skill.joinpath("SKILL.md").write_bytes(_gh_installed_contents(name))


def _skill_contents(name: str) -> bytes:
    return f"---\nname: {name}\ndescription: test skill\n---\n".encode()


def _git_blob_id(contents: bytes) -> str:
    digest = hashlib.sha1(usedforsecurity=False)
    digest.update(f"blob {len(contents)}\0".encode())
    digest.update(contents)
    return digest.hexdigest()


def _tree_object_sha(entries: tuple[tuple[str, str, str], ...]) -> str:
    body = b"".join(
        f"{mode} {path_name}\0".encode() + bytes.fromhex(sha)
        for mode, path_name, sha in entries
    )
    digest = hashlib.sha1()
    digest.update(f"tree {len(body)}\0".encode())
    digest.update(body)
    return digest.hexdigest()


_GH_TREE_SHAS = {
    name: _tree_object_sha(
        (("100644", "SKILL.md", _git_blob_id(_skill_contents(name))),)
    )
    for name in ("animate", "hill-climbing")
}


def _gh_installed_contents(name: str) -> bytes:
    """Simulate GitHub CLI's installed SKILL.md rewrite: alphabetized
    frontmatter plus injected github-* source metadata."""
    return (
        "---\n"
        "description: test skill\n"
        "metadata:\n"
        f"    github-path: skills/{name}\n"
        f"    github-pinned: {COMMIT}\n"
        f"    github-ref: {COMMIT}\n"
        "    github-repo: https://github.com/wcygan/agent-skills\n"
        f"    github-tree-sha: {_GH_TREE_SHAS[name]}\n"
        f"name: {name}\n"
        "---\n"
    ).encode()




def _pinned_tree() -> str:
    tree: list[dict[str, object]] = []
    for index, name in enumerate(("animate", "hill-climbing"), start=1):
        tree.extend(
            (
                {
                    "path": f"skills/{name}",
                    "mode": "040000",
                    "type": "tree",
                    "sha": f"{index:040x}",
                },
                {
                    "path": f"skills/{name}/SKILL.md",
                    "mode": "100644",
                    "type": "blob",
                    "sha": _git_blob_id(_skill_contents(name)),
                },
            )
        )
    return json.dumps({"truncated": False, "tree": tree})


def _catalog_response(command: list[str]) -> subprocess.CompletedProcess[str]:
    if command[1] == "api":
        return _completed(command, stdout=_pinned_tree())
    return _completed(
        command,
        stdout="animate\tdescription\nhill-climbing\tdescription\n",
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
    architecture = Path(".agents/skills/dotfiles-operations/references/architecture.md").read_text()
    operations = Path(".agents/skills/dotfiles-operations/references/operations.md").read_text()

    assert skill.is_file()
    assert skill.read_text().startswith("---\nname: agent-skills-integration\ndescription:")
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
    path.write_text(path.read_text().replace('directory = ".agents/skills"', 'directory = "/tmp"'))

    with pytest.raises(AgentSkillsError, match="relative shared skill directory"):
        load_agent_skills_lock(tmp_path)


def test_install_discovers_installs_and_verifies_with_gh(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    gh = str(tmp_path / "bin" / "gh")
    list_count = 0
    installed = False

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        nonlocal installed, list_count
        if command[1] == "api":
            return _completed(command, stdout=_pinned_tree())
        if command[1:3] == ["skill", "list"]:
            list_count += 1
            return _completed(command, stdout=_installed(home) if installed else "[]")
        if "--all" in command:
            installed = True
            _write_catalog(home / ".agents" / "skills")
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
    assert result.local_content_digest
    assert list_count == 3


def test_install_rejects_content_that_does_not_match_the_pinned_tree(
    tmp_path: Path,
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    installed = False

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        nonlocal installed
        if command[1] == "api":
            return _completed(command, stdout=_pinned_tree())
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=_installed(home) if installed else "[]")
        if "--all" in command:
            installed = True
            _write_catalog(home / ".agents" / "skills")
            home.joinpath(".agents/skills/animate/SKILL.md").write_text("changed\n")
            return _completed(command, stdout="Installed 2 skills\n")
        return _completed(
            command,
            stdout="animate\tdescription\nhill-climbing\tdescription\n",
        )

    with pytest.raises(AgentSkillsError, match="does not match the pinned commit"):
        install_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert installed is True


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


@pytest.mark.parametrize("target_kind", ("file", "directory", "symlink"))
def test_install_refuses_an_existing_target_omitted_from_inventory(
    tmp_path: Path,
    target_kind: str,
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    destination = home / ".agents" / "skills"
    destination.mkdir(parents=True)
    target = destination / "animate"
    if target_kind == "file":
        target.write_text("keep this file\n")
    elif target_kind == "directory":
        target.mkdir()
        target.joinpath("keep.txt").write_text("keep this directory\n")
    else:
        external = tmp_path / "external"
        external.mkdir()
        target.symlink_to(external, target_is_directory=True)
    calls: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout="[]")
        return _completed(
            command,
            stdout="animate\tdescription\nhill-climbing\tdescription\n",
        )

    with pytest.raises(
        AgentSkillsError,
        match="physical target exists without matching inventory ownership",
    ):
        install_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert target.lstat()
    assert not any("--all" in command for command in calls)


def test_install_refuses_a_foreign_legacy_name_before_force(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    calls: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[1:3] != ["skill", "list"]:
            return _completed(
                command,
                stdout="animate\tdescription\nhill-climbing\tdescription\n",
            )
        if "--dir" in command:
            return _completed(command, stdout="[]")
        return _completed(
            command,
            stdout=json.dumps(
                [
                    {
                        "skillName": "animate",
                        "sourceURL": "https://github.com/example/other",
                        "scope": "user",
                        "version": "v1",
                        "pinned": False,
                        "path": str(home / ".codex" / "skills" / "animate"),
                    }
                ]
            ),
        )

    with pytest.raises(AgentSkillsError, match="legacy source does not match"):
        install_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert not any("--all" in command for command in calls)


def test_install_allows_a_verified_legacy_catalog_migration(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    calls: list[list[str]] = []
    installed = False
    _write_catalog(home / ".codex" / "skills")

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        nonlocal installed
        calls.append(command)
        if command[1] == "api":
            return _completed(command, stdout=_pinned_tree())
        if command[1:3] != ["skill", "list"]:
            if "--all" in command:
                installed = True
                _write_catalog(home / ".agents" / "skills")
                return _completed(command, stdout="Installed 2 skills\n")
            return _completed(
                command,
                stdout="animate\tdescription\nhill-climbing\tdescription\n",
            )
        if "--dir" in command:
            return _completed(command, stdout=_installed(home) if installed else "[]")
        return _completed(command, stdout=_legacy_installed(home))

    result = install_agent_skills(
        tmp_path,
        run=runner,
        which=lambda _: "/bin/gh",
        environ={"HOME": str(home)},
    )

    assert result.count == 2
    assert any("--all" in command for command in calls)
    assert (home / ".codex" / "skills" / "animate").is_dir()


def test_install_allows_a_partial_legacy_catalog(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    calls: list[list[str]] = []
    installed = False
    _write_catalog(home / ".codex" / "skills", ("animate",))
    legacy_inventory = [
        item
        for item in json.loads(_legacy_installed(home))
        if item["skillName"] == "animate"
    ]

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        nonlocal installed
        calls.append(command)
        if command[1] == "api":
            return _completed(command, stdout=_pinned_tree())
        if command[1:3] != ["skill", "list"]:
            if "--all" in command:
                installed = True
                _write_catalog(home / ".agents" / "skills")
                return _completed(command, stdout="Installed 2 skills\n")
            return _completed(
                command,
                stdout="animate\tdescription\nhill-climbing\tdescription\n",
            )
        if "--dir" in command:
            return _completed(command, stdout=_installed(home) if installed else "[]")
        return _completed(command, stdout=json.dumps(legacy_inventory))

    result = install_agent_skills(
        tmp_path,
        run=runner,
        which=lambda _: "/bin/gh",
        environ={"HOME": str(home)},
    )

    assert result.count == 2
    assert any("--all" in command for command in calls)


def test_install_skips_namespaced_builtin_entries_in_legacy_inventory(tmp_path: Path) -> None:
    """Codex built-in .system/* entries are agent-internal and never user catalog members."""
    _write_lock(tmp_path)
    home = tmp_path / "home"
    calls: list[list[str]] = []
    installed = False

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        nonlocal installed
        calls.append(command)
        if command[1] == "api":
            return _completed(command, stdout=_pinned_tree())
        if command[1:3] != ["skill", "list"]:
            if "--all" in command:
                installed = True
                _write_catalog(home / ".agents" / "skills")
                return _completed(command, stdout="Installed 2 skills\n")
            return _completed(
                command,
                stdout="animate\tdescription\nhill-climbing\tdescription\n",
            )
        if "--dir" in command:
            return _completed(command, stdout=_installed(home) if installed else "[]")
        return _completed(
            command,
            stdout=json.dumps(
                [
                    {
                        "skillName": ".system/imagegen",
                        "sourceURL": "",
                        "scope": "custom",
                        "version": "",
                        "pinned": False,
                        "path": str(home / ".codex" / "skills" / ".system" / "imagegen"),
                    }
                ]
            ),
        )

    result = install_agent_skills(
        tmp_path,
        run=runner,
        which=lambda _: "/bin/gh",
        environ={"HOME": str(home)},
    )

    assert result.count == 2
    assert any("--all" in command for command in calls)


def test_verify_requires_the_exact_pin_for_every_catalog_skill(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    inventory = json.loads(_installed(home))
    inventory[1]["version"] = "main"
    _write_catalog(home / ".agents" / "skills")

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


def test_cleanup_quarantines_only_the_verified_legacy_catalog(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    legacy_root = home / ".codex" / "skills"
    _write_catalog(home / ".agents" / "skills")
    for name in ("animate", "hill-climbing"):
        skill = legacy_root / name
        skill.mkdir(parents=True)
        skill.joinpath("SKILL.md").write_text("---\nname: test\ndescription: test\n---\n")

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            if "--dir" in command:
                return _completed(command, stdout=_installed(home))
            return _completed(command, stdout=_legacy_installed(home))
        return _catalog_response(command)

    result = cleanup_legacy_agent_skills(
        tmp_path,
        run=runner,
        which=lambda _: "/bin/gh",
        environ={"HOME": str(home)},
    )

    assert result.count == 2
    assert result.destination == legacy_root
    assert not legacy_root.joinpath("animate").exists()
    assert not legacy_root.joinpath("hill-climbing").exists()
    tombstones = tuple(legacy_root.iterdir())
    assert len(tombstones) == 2
    assert all(".dotfiles-cleanup." in path.name for path in tombstones)
    assert all(path.joinpath("SKILL.md").is_file() for path in tombstones)
    assert set(result.quarantines) == set(tombstones)
    assert "Quarantined 2 legacy Codex user skills" in str(result)
    assert all(str(path) in str(result) for path in result.quarantines)


def test_cleanup_refuses_when_shared_catalog_content_is_not_pinned(
    tmp_path: Path,
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    shared_root = home / ".agents" / "skills"
    legacy_root = home / ".codex" / "skills"
    _write_catalog(shared_root)
    _write_catalog(legacy_root)
    shared_root.joinpath("animate", "SKILL.md").write_text("tampered\n")

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            stdout = _installed(home) if "--dir" in command else _legacy_installed(home)
            return _completed(command, stdout=stdout)
        return _catalog_response(command)

    with pytest.raises(AgentSkillsError, match="does not match the pinned commit"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert legacy_root.joinpath("animate", "SKILL.md").is_file()
    assert legacy_root.joinpath("hill-climbing", "SKILL.md").is_file()
    assert not tuple(legacy_root.glob(".dotfiles-cleanup.*"))


def test_cleanup_refuses_a_legacy_skill_fifo_without_blocking(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    _write_catalog(home / ".agents" / "skills")
    legacy_root = home / ".codex" / "skills"
    _write_catalog(legacy_root)
    skill_file = legacy_root / "animate" / "SKILL.md"
    skill_file.unlink()
    os.mkfifo(skill_file)

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            stdout = _installed(home) if "--dir" in command else _legacy_installed(home)
            return _completed(command, stdout=stdout)
        return _catalog_response(command)

    with pytest.raises(AgentSkillsError, match="not a readable regular file"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert stat.S_ISFIFO(skill_file.lstat().st_mode)


def test_cleanup_refuses_a_legacy_catalog_from_another_source(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    inventory = json.loads(_legacy_installed(home))
    inventory[0]["sourceURL"] = "https://github.com/example/other"
    _write_catalog(home / ".agents" / "skills")

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            if "--dir" in command:
                return _completed(command, stdout=_installed(home))
            return _completed(command, stdout=json.dumps(inventory))
        return _catalog_response(command)

    with pytest.raises(AgentSkillsError, match="legacy source does not match"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_cleanup_refuses_to_quarantine_the_shared_catalog(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    inventory = json.loads(_legacy_installed(home))
    _write_catalog(home / ".agents" / "skills")
    for item in inventory:
        item["path"] = str(home / ".agents" / "skills" / item["skillName"])

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            if "--dir" in command:
                return _completed(command, stdout=_installed(home))
            return _completed(command, stdout=json.dumps(inventory))
        return _catalog_response(command)

    with pytest.raises(AgentSkillsError, match="resolves to the shared directory"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_verify_rejects_a_symlinked_skill_directory(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    external = tmp_path / "external" / "animate"
    _write_catalog(external.parent, ("animate",))
    destination = home / ".agents" / "skills"
    destination.mkdir(parents=True)
    destination.joinpath("animate").symlink_to(external, target_is_directory=True)
    _write_catalog(destination, ("hill-climbing",))

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=_installed(home))
        return _completed(command, stdout="animate\tdescription\nhill-climbing\tdescription\n")

    with pytest.raises(AgentSkillsError, match="skill directory is a symbolic link"):
        verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_verify_rejects_a_symlink_inside_a_skill_directory(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    destination = home / ".agents" / "skills"
    _write_catalog(destination)
    external = tmp_path / "external.md"
    external.write_text("external\n")
    destination.joinpath("animate", "external.md").symlink_to(external)

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=_installed(home))
        return _completed(command, stdout="animate\tdescription\nhill-climbing\tdescription\n")

    with pytest.raises(AgentSkillsError, match="symbolic link"):
        verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_verify_rejects_a_fifo_inside_a_skill_directory_without_blocking(
    tmp_path: Path,
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    destination = home / ".agents" / "skills"
    _write_catalog(destination)
    fifo = destination / "animate" / "input.pipe"
    os.mkfifo(fifo)

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=_installed(home))
        return _completed(command, stdout="animate\tdescription\nhill-climbing\tdescription\n")

    with pytest.raises(AgentSkillsError, match="unsupported file type"):
        verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert stat.S_ISFIFO(fifo.lstat().st_mode)


def test_verify_rejects_an_unreadable_nested_skill_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    destination = home / ".agents" / "skills"
    _write_catalog(destination)
    nested = destination / "animate" / "references"
    nested.mkdir()
    nested.joinpath("guide.md").write_text("guide\n")
    nested_metadata = nested.lstat()
    nested_identity = (nested_metadata.st_dev, nested_metadata.st_ino)
    real_scandir = os.scandir

    def unreadable_scandir(
        path: int | os.PathLike[str] | str,
    ) -> os.ScandirIterator[str]:
        if isinstance(path, int):
            metadata = os.fstat(path)
            is_nested = (metadata.st_dev, metadata.st_ino) == nested_identity
        else:
            is_nested = Path(path) == nested
        if is_nested:
            raise PermissionError("permission denied")
        return real_scandir(path)

    monkeypatch.setattr(agent_skills_module.os, "scandir", unreadable_scandir)

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=_installed(home))
        return _completed(command, stdout="animate\tdescription\nhill-climbing\tdescription\n")

    with pytest.raises(
        AgentSkillsError,
        match=r"cannot inspect animate: permission denied",
    ):
        verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_verify_requires_a_regular_readable_skill_file(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    _write_catalog(home / ".agents" / "skills")
    skill_file = home / ".agents" / "skills" / "animate" / "SKILL.md"
    skill_file.unlink()
    skill_file.mkdir()

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=_installed(home))
        return _completed(command, stdout="animate\tdescription\nhill-climbing\tdescription\n")

    with pytest.raises(AgentSkillsError, match="SKILL.md is not a readable regular file"):
        verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_verify_requires_each_exact_catalog_directory(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    _write_catalog(home / ".agents" / "skills")
    inventory = json.loads(_installed(home))
    inventory[0]["path"] = str(home / ".agents" / "skills" / "nested" / "animate")

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=json.dumps(inventory))
        return _completed(command, stdout="animate\tdescription\nhill-climbing\tdescription\n")

    with pytest.raises(AgentSkillsError, match="outside the configured shared directory"):
        verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )


def test_local_content_digest_is_stable_and_detects_content_changes(tmp_path: Path) -> None:
    _write_lock(tmp_path)
    homes = (tmp_path / "first", tmp_path / "second")
    _write_catalog(homes[0] / ".agents" / "skills")
    _write_catalog(homes[1] / ".agents" / "skills", ("hill-climbing", "animate"))

    def verify(home: Path) -> AgentSkillsResult:
        def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
            if command[1] == "api":
                return _completed(command, stdout=_pinned_tree())
            if command[1:3] == ["skill", "list"]:
                return _completed(command, stdout=_installed(home))
            return _completed(command, stdout="hill-climbing\tdescription\nanimate\tdescription\n")

        return verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    first = verify(homes[0])
    second = verify(homes[1])

    assert first.local_content_digest == second.local_content_digest
    # SKILL.md is attested rather than content-hashed, and these catalogs
    # contain no other files, so the non-attested content digest is empty.
    expected_digest = hashlib.sha256()
    assert first.local_content_digest == expected_digest.hexdigest()
    homes[1].joinpath(".agents/skills/animate/SKILL.md").write_text("changed\n")
    with pytest.raises(AgentSkillsError, match="does not match the pinned commit"):
        verify(homes[1])


def test_verify_rejects_content_added_between_catalog_capture_and_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    destination = home / ".agents" / "skills"
    _write_catalog(destination)
    later_file = destination / "animate" / "later.txt"
    real_capture = agent_skills_module.capture_verified_directory
    changed = False

    def capture_then_change(path: Path, descriptor: int):
        nonlocal changed
        captured = real_capture(path, descriptor)
        if path.name == "animate" and not changed:
            later_file.write_text("late content\n")
            changed = True
        return captured

    monkeypatch.setattr(
        agent_skills_module,
        "capture_verified_directory",
        capture_then_change,
    )

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=_installed(home))
        return _completed(command, stdout="animate\tdescription\nhill-climbing\tdescription\n")

    with pytest.raises(AgentSkillsError, match="changed during verification"):
        verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert later_file.read_text() == "late content\n"


def test_verify_rejects_a_file_replaced_between_snapshot_stat_and_open(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    destination = home / ".agents" / "skills"
    _write_catalog(destination)
    target = destination / "animate" / "SKILL.md"
    displaced = tmp_path / "original-SKILL.md"
    replacement = tmp_path / "replacement-SKILL.md"
    replacement.write_text("attacker content\n")
    real_open = agent_skills_module.os.open
    swapped = False

    def swap_before_open(
        path: Path | str,
        flags: int,
        mode: int = 0o777,
        *,
        dir_fd: int | None = None,
    ) -> int:
        nonlocal swapped
        if dir_fd is not None and str(path) == "SKILL.md" and not swapped:
            target.rename(displaced)
            replacement.rename(target)
            swapped = True
        return real_open(path, flags, mode, dir_fd=dir_fd)

    monkeypatch.setattr(agent_skills_module.os, "open", swap_before_open)

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            return _completed(command, stdout=_installed(home))
        return _completed(command, stdout="animate\tdescription\nhill-climbing\tdescription\n")

    with pytest.raises(AgentSkillsError, match="changed"):
        verify_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert displaced.read_bytes() == _gh_installed_contents("animate")
    assert target.read_text() == "attacker content\n"


def test_cleanup_stops_before_legacy_inspection_when_shared_acceptance_fails(
    tmp_path: Path,
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    _write_catalog(home / ".agents" / "skills")
    inventory = json.loads(_installed(home))
    inventory[0]["version"] = "main"
    inspected_legacy = False

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        nonlocal inspected_legacy
        if command[1:3] == ["skill", "list"]:
            if "--dir" in command:
                return _completed(command, stdout=json.dumps(inventory))
            inspected_legacy = True
            return _completed(command, stdout=_legacy_installed(home))
        return _completed(command, stdout="animate\tdescription\nhill-climbing\tdescription\n")

    with pytest.raises(AgentSkillsError, match="installed version does not match"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert inspected_legacy is False


def test_cleanup_rejects_a_legacy_path_through_a_symlinked_ancestor(
    tmp_path: Path,
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    _write_catalog(home / ".agents" / "skills")
    outside = tmp_path / "outside"
    _write_catalog(outside / "skills")
    home.mkdir(exist_ok=True)
    home.joinpath(".codex").symlink_to(outside, target_is_directory=True)

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            stdout = _installed(home) if "--dir" in command else _legacy_installed(home)
            return _completed(command, stdout=stdout)
        return _catalog_response(command)

    with pytest.raises(AgentSkillsError, match="symlinked ancestor"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert outside.joinpath("skills", "animate").is_dir()
    assert outside.joinpath("skills", "hill-climbing").is_dir()


def test_cleanup_refuses_an_ancestor_replaced_after_catalog_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    _write_catalog(home / ".agents" / "skills")
    legacy_root = home / ".codex" / "skills"
    _write_catalog(legacy_root)
    displaced = home / ".codex-displaced"
    real_remove = agent_skills_module.remove_verified_directories

    def remove_after_swap(*args: object, **kwargs: object) -> bool:
        legacy_root.parent.rename(displaced)
        _write_catalog(legacy_root)
        return real_remove(*args, **kwargs)

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            stdout = _installed(home) if "--dir" in command else _legacy_installed(home)
            return _completed(command, stdout=stdout)
        return _catalog_response(command)

    monkeypatch.setattr(
        agent_skills_module,
        "remove_verified_directories",
        remove_after_swap,
    )

    with pytest.raises(AgentSkillsError, match="destination parent changed"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert (legacy_root / "animate" / "SKILL.md").is_file()
    assert (legacy_root / "hill-climbing" / "SKILL.md").is_file()
    assert (displaced / "skills" / "animate" / "SKILL.md").is_file()
    assert (displaced / "skills" / "hill-climbing" / "SKILL.md").is_file()


def test_cleanup_preserves_nested_content_added_after_catalog_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    _write_catalog(home / ".agents" / "skills")
    legacy_root = home / ".codex" / "skills"
    _write_catalog(legacy_root)
    later_file = legacy_root / "animate" / "notes" / "keep.md"
    real_remove = agent_skills_module.remove_verified_directories

    def add_content_before_removal(*args: object, **kwargs: object) -> bool:
        later_file.parent.mkdir()
        later_file.write_text("keep this content\n")
        return real_remove(*args, **kwargs)

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            stdout = _installed(home) if "--dir" in command else _legacy_installed(home)
            return _completed(command, stdout=stdout)
        return _catalog_response(command)

    monkeypatch.setattr(
        agent_skills_module,
        "remove_verified_directories",
        add_content_before_removal,
    )

    with pytest.raises(AgentSkillsError, match="contents changed after acceptance"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    assert later_file.read_text() == "keep this content\n"
    assert (legacy_root / "animate" / "SKILL.md").is_file()
    assert (legacy_root / "hill-climbing" / "SKILL.md").is_file()


def test_cleanup_refuses_a_skill_replaced_during_content_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_lock(tmp_path)
    home = tmp_path / "home"
    _write_catalog(home / ".agents" / "skills")
    legacy_root = home / ".codex" / "skills"
    for name in ("animate", "hill-climbing"):
        skill = legacy_root / name
        skill.mkdir(parents=True)
        skill.joinpath("precious.txt").write_text("unvalidated\n")
    displaced = home / "validated-legacy"
    displaced.mkdir()
    decoys = home / "decoy-legacy"
    _write_catalog(decoys)
    active: set[str] = set()
    real_open = agent_skills_module.os.open
    real_stat = agent_skills_module.os.stat

    def swap_before_open(
        path: Path | str,
        flags: int,
        mode: int = 0o777,
        *,
        dir_fd: int | None = None,
    ) -> int:
        name = str(path)
        if dir_fd is not None and name in {"animate", "hill-climbing"}:
            legacy_root.joinpath(name).rename(displaced / name)
            decoys.joinpath(name).rename(legacy_root / name)
            active.add(name)
        return real_open(path, flags, mode, dir_fd=dir_fd)

    def restore_before_stat(
        path: Path | str,
        *,
        dir_fd: int | None = None,
        follow_symlinks: bool = True,
    ) -> os.stat_result:
        name = str(path)
        if dir_fd is not None and name in active:
            legacy_root.joinpath(name).rename(decoys / name)
            displaced.joinpath(name).rename(legacy_root / name)
            active.remove(name)
        return real_stat(path, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if command[1:3] == ["skill", "list"]:
            stdout = _installed(home) if "--dir" in command else _legacy_installed(home)
            return _completed(command, stdout=stdout)
        return _catalog_response(command)

    monkeypatch.setattr(agent_skills_module.os, "open", swap_before_open)
    monkeypatch.setattr(agent_skills_module.os, "stat", restore_before_stat)

    with pytest.raises(AgentSkillsError, match="changed during validation"):
        cleanup_legacy_agent_skills(
            tmp_path,
            run=runner,
            which=lambda _: "/bin/gh",
            environ={"HOME": str(home)},
        )

    for name in ("animate", "hill-climbing"):
        assert legacy_root.joinpath(name, "precious.txt").read_text() == "unvalidated\n"
        assert decoys.joinpath(name, "SKILL.md").is_file()


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
        lambda _: AgentSkillsResult("wcygan/agent-skills", COMMIT, 42, home / ".agents" / "skills"),
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
        lambda _: AgentSkillsResult("wcygan/agent-skills", COMMIT, 42, home / ".agents" / "skills"),
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
        lambda _: AgentSkillsCleanupResult(
            2,
            home / ".codex" / "skills",
            (
                home / ".codex" / "skills" / ".animate.dotfiles-cleanup.test",
                home / ".codex" / "skills" / ".hill-climbing.dotfiles-cleanup.test",
            ),
        ),
    )

    assert cli.main(["agent-skills", "--cleanup-legacy", "--yes"]) == 0
    output = capsys.readouterr().out
    assert "Quarantined 2 legacy Codex user skills" in output
    assert "retained at:" in output
    assert state_directory().joinpath("completed.json").is_file()
