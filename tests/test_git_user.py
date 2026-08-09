from __future__ import annotations

import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.git_user import GitUserConfig, GitUserError, configure_git_user


def completed(
    command: Sequence[str], *, stdout: str = "", stderr: str = "", returncode: int = 0
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(command, returncode, stdout, stderr)


class FakeRunner:
    def __init__(
        self, responses: Mapping[tuple[str, ...], subprocess.CompletedProcess[str]]
    ) -> None:
        self.responses = responses
        self.calls: list[list[str]] = []

    def __call__(
        self, command: Sequence[str], **kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        assert kwargs == {"capture_output": True, "check": False, "text": True}
        self.calls.append(list(command))
        return self.responses.get(tuple(command), completed(command, returncode=1))


def test_noninteractive_writes_local_identity_and_removes_global(tmp_path: Path) -> None:
    path = tmp_path / ".config" / "git" / "config.local"
    runner = FakeRunner(
        {
            ("git", "config", "--global", "--get", "user.name"): completed(
                ("git", "config"), stdout="Old Name\n"
            ),
            ("git", "config", "--global", "--get", "user.email"): completed(
                ("git", "config"), stdout="old@example.com\n"
            ),
            ("git", "config", "--file", str(path), "user.name", "New Name"): completed(
                ("git", "config")
            ),
            ("git", "config", "--file", str(path), "user.email", "new@example.com"): completed(
                ("git", "config")
            ),
            ("git", "config", "--global", "--unset", "user.name"): completed(("git", "config")),
            ("git", "config", "--global", "--unset", "user.email"): completed(("git", "config")),
        }
    )

    result = configure_git_user(
        home=tmp_path,
        name="New Name",
        email="new@example.com",
        remove_global=True,
        run=runner,
    )

    assert result.path == path
    assert result.updated is True
    assert result.removed_global is True
    assert runner.calls[-2:] == [
        ["git", "config", "--global", "--unset", "user.name"],
        ["git", "config", "--global", "--unset", "user.email"],
    ]


def test_noninteractive_existing_config_can_decline_update_without_prompt(tmp_path: Path) -> None:
    path = tmp_path / ".config" / "git" / "config.local"
    path.parent.mkdir(parents=True)
    path.write_text("[user]\n")
    runner = FakeRunner(
        {
            ("git", "config", "--file", str(path), "--get", "user.name"): completed(
                ("git", "config"), stdout="Existing\n"
            ),
            ("git", "config", "--file", str(path), "--get", "user.email"): completed(
                ("git", "config"), stdout="existing@example.com\n"
            ),
        }
    )

    result = configure_git_user(home=tmp_path, update=False, run=runner)

    assert result.name == "Existing"
    assert result.email == "existing@example.com"
    assert result.updated is False
    assert len(runner.calls) == 2


def test_interactive_preserves_global_defaults_and_default_global_removal(tmp_path: Path) -> None:
    path = tmp_path / ".config" / "git" / "config.local"
    runner = FakeRunner(
        {
            ("git", "config", "--global", "--get", "user.name"): completed(
                ("git", "config"), stdout="Global Name\n"
            ),
            ("git", "config", "--global", "--get", "user.email"): completed(
                ("git", "config"), stdout="global@example.com\n"
            ),
            ("git", "config", "--file", str(path), "user.name", "Global Name"): completed(
                ("git", "config")
            ),
            ("git", "config", "--file", str(path), "user.email", "global@example.com"): completed(
                ("git", "config")
            ),
            ("git", "config", "--global", "--unset", "user.name"): completed(("git", "config")),
            ("git", "config", "--global", "--unset", "user.email"): completed(("git", "config")),
        }
    )
    answers = iter(["", "", ""])

    result = configure_git_user(home=tmp_path, input_func=lambda _: next(answers), run=runner)

    assert result.name == "Global Name"
    assert result.email == "global@example.com"
    assert result.removed_global is True


def test_interactive_existing_config_keeps_it_when_update_prompt_declines(tmp_path: Path) -> None:
    path = tmp_path / ".config" / "git" / "config.local"
    path.parent.mkdir(parents=True)
    path.write_text("[user]\n")
    runner = FakeRunner(
        {
            ("git", "config", "--file", str(path), "--get", "user.name"): completed(
                ("git", "config"), stdout="Existing\n"
            ),
            ("git", "config", "--file", str(path), "--get", "user.email"): completed(
                ("git", "config"), stdout="existing@example.com\n"
            ),
        }
    )

    result = configure_git_user(home=tmp_path, input_func=lambda _: "n", run=runner)

    assert result.updated is False
    assert result.name == "Existing"


def test_noninteractive_write_requires_complete_identity(tmp_path: Path) -> None:
    with pytest.raises(GitUserError, match="requires both name and email"):
        configure_git_user(home=tmp_path, name="Only Name", run=FakeRunner({}))


def test_interactive_eof_is_a_clear_failure(tmp_path: Path) -> None:
    with pytest.raises(GitUserError, match="reached EOF"):
        configure_git_user(
            home=tmp_path,
            input_func=lambda _: (_ for _ in ()).throw(EOFError()),
            run=FakeRunner({}),
        )


def test_git_write_failure_includes_diagnostic(tmp_path: Path) -> None:
    path = tmp_path / ".config" / "git" / "config.local"
    runner = FakeRunner(
        {
            ("git", "config", "--global", "--get", "user.name"): completed(("git", "config")),
            ("git", "config", "--global", "--get", "user.email"): completed(("git", "config")),
            ("git", "config", "--file", str(path), "user.name", "Name"): completed(
                ("git", "config"), returncode=1, stderr="permission denied"
            ),
        }
    )

    with pytest.raises(GitUserError, match="permission denied"):
        configure_git_user(home=tmp_path, name="Name", email="email@example.com", run=runner)


def test_git_user_cli_forwards_noninteractive_identity(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    captured: dict[str, object] = {}

    def configure(**kwargs: object) -> GitUserConfig:
        captured.update(kwargs)
        return GitUserConfig(Path("config.local"), "Name", "email@example.com", True, True)

    monkeypatch.setattr(cli, "configure_git_user", configure)

    assert (
        cli.main(
            [
                "git-user",
                "--name",
                "Name",
                "--email",
                "email@example.com",
                "--remove-global",
            ]
        )
        == 0
    )
    assert captured == {
        "name": "Name",
        "email": "email@example.com",
        "remove_global": True,
    }
    assert "Updated Git identity" in capsys.readouterr().out
