from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.nix_profile import NixProfileError, ensure_profile, find_profile_element


class RecordingRunner:
    def __init__(self, profile_payload: dict[str, object]) -> None:
        self.profile_payload = profile_payload
        self.calls: list[list[str]] = []

    def __call__(self, args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        self.calls.append(args)
        stdout = json.dumps(self.profile_payload) if args[-2:] == ["list", "--json"] else ""
        return subprocess.CompletedProcess(args, 0, stdout=stdout, stderr="")


def test_find_profile_prefers_current_checkout_over_element_name(tmp_path: Path) -> None:
    elements = {
        "another-name": {"originalUrl": f"git+{tmp_path.as_uri()}"},
        "dotfiles": {"originalUrl": "github:someone/else"},
    }

    assert find_profile_element(elements, tmp_path) == "another-name"


def test_find_profile_ignores_unrelated_dotfiles_element(tmp_path: Path) -> None:
    elements = {"dotfiles": {"originalUrl": "github:someone/else"}}

    assert find_profile_element(elements, tmp_path) is None


def test_find_profile_matches_repository_file_url(tmp_path: Path) -> None:
    elements = {"local-checkout": {"originalUrl": f"git+{tmp_path.as_uri()}"}}

    assert find_profile_element(elements, tmp_path) == "local-checkout"


def test_existing_profile_is_upgraded(tmp_path: Path) -> None:
    runner = RecordingRunner(
        {
            "version": 3,
            "elements": {"dotfiles": {"originalUrl": f"git+{tmp_path.as_uri()}"}},
        }
    )

    message = ensure_profile(tmp_path, runner=runner)

    assert message == "Upgraded Nix profile element: dotfiles"
    assert runner.calls[-1][-3:] == ["profile", "upgrade", "dotfiles"]


def test_repository_profile_with_different_name_is_upgraded(tmp_path: Path) -> None:
    runner = RecordingRunner(
        {
            "version": 3,
            "elements": {"checkout": {"originalUrl": f"git+{tmp_path.as_uri()}"}},
        }
    )

    ensure_profile(tmp_path, runner=runner)

    assert runner.calls[-1][-3:] == ["profile", "upgrade", "checkout"]


def test_missing_profile_is_added_with_priority_five(tmp_path: Path) -> None:
    runner = RecordingRunner({"version": 3, "elements": {}})

    message = ensure_profile(tmp_path, runner=runner)

    assert message == f"Added Nix profile from: {tmp_path.resolve()}#default"
    assert runner.calls[-1][-5:] == [
        "profile",
        "add",
        f"{tmp_path.resolve()}#default",
        "--priority",
        "5",
    ]


def test_invalid_profile_json_is_reported(tmp_path: Path) -> None:
    def invalid_runner(args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args, 0, stdout="not-json", stderr="")

    with pytest.raises(NixProfileError, match="invalid JSON"):
        ensure_profile(tmp_path, runner=invalid_runner)


def test_command_failures_are_reported(tmp_path: Path) -> None:
    def failing_runner(args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.CalledProcessError(1, args, stderr="profile is locked")

    with pytest.raises(NixProfileError, match="profile is locked"):
        ensure_profile(tmp_path, runner=failing_runner)


def test_profile_cli_reports_success(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cli, "ensure_profile", lambda _: "profile ready")

    assert cli.main(["profile"]) == 0
    assert capsys.readouterr().out.strip() == "profile ready"


def test_profile_cli_reports_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail(_: Path) -> str:
        raise NixProfileError("profile is locked")

    monkeypatch.setattr(cli, "ensure_profile", fail)

    assert cli.main(["profile"]) == 1
    assert "profile is locked" in capsys.readouterr().out
