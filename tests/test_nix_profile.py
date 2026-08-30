from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.nix_profile import (
    NixProfileError,
    ProfileElement,
    ensure_profile,
    find_profile_element,
    list_profile_elements,
    select_current_checkout_profile,
)


class RecordingRunner:
    def __init__(self, profile_payload: dict[str, object]) -> None:
        self.profile_payload = profile_payload
        self.calls: list[list[str]] = []
        self.kwargs: list[dict[str, object]] = []

    def __call__(self, args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        self.calls.append(args)
        self.kwargs.append(kwargs)
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


def test_find_profile_matches_nix_path_url(tmp_path: Path) -> None:
    elements = {"local-checkout": {"originalUrl": f"path:{tmp_path.resolve()}"}}

    assert find_profile_element(elements, tmp_path) == "local-checkout"


def test_current_checkout_selector_applies_active_policy(tmp_path: Path) -> None:
    unrelated = ProfileElement(
        name="unrelated",
        original_url=f"git+{(tmp_path / 'other').as_uri()}",
        store_paths=(),
        active=True,
    )
    inactive = ProfileElement(
        name="inactive-checkout",
        original_url=f"git+{tmp_path.as_uri()}",
        store_paths=(),
        active=False,
    )

    assert (
        select_current_checkout_profile(
            (unrelated, inactive), tmp_path, active_only=True
        )
        is None
    )
    assert (
        select_current_checkout_profile(
            (unrelated, inactive), tmp_path, active_only=False
        )
        == inactive
    )


def test_profile_element_resolves_only_executable_outputs(tmp_path: Path) -> None:
    first_store = tmp_path / "first-store"
    second_store = tmp_path / "second-store"
    unusable = first_store / "bin" / "rustup"
    usable = second_store / "bin" / "rustup"
    unusable.parent.mkdir(parents=True)
    usable.parent.mkdir(parents=True)
    unusable.write_text("not executable")
    usable.write_text("#!/bin/sh\nexit 0\n")
    usable.chmod(0o755)
    element = ProfileElement(
        name="checkout",
        original_url=f"git+{tmp_path.as_uri()}",
        store_paths=(first_store, second_store),
        active=True,
    )

    assert element.executable("rustup") == usable
    assert element.executable("missing") is None


def test_existing_profile_is_upgraded(tmp_path: Path) -> None:
    runner = RecordingRunner(
        {
            "version": 3,
            "elements": {
                "dotfiles": {
                    "originalUrl": f"git+{tmp_path.as_uri()}",
                    "active": True,
                    "storePaths": [],
                }
            },
        }
    )

    message = ensure_profile(tmp_path, runner=runner)

    assert message == "Upgraded Nix profile element: dotfiles"
    assert runner.calls[-1][-4:] == [
        "profile",
        "upgrade",
        "dotfiles",
        "--no-write-lock-file",
    ]


def test_inactive_repository_profile_is_rejected_with_recovery_guidance(
    tmp_path: Path,
) -> None:
    runner = RecordingRunner(
        {
            "version": 3,
            "elements": {
                "checkout": {
                    "originalUrl": f"git+{tmp_path.as_uri()}",
                    "active": False,
                    "storePaths": [],
                }
            },
        }
    )

    with pytest.raises(NixProfileError, match="nix profile remove checkout"):
        ensure_profile(tmp_path, runner=runner)

    assert len(runner.calls) == 1


def test_active_repository_profile_is_preferred_over_inactive_duplicate(
    tmp_path: Path,
) -> None:
    runner = RecordingRunner(
        {
            "version": 3,
            "elements": {
                "inactive-checkout": {
                    "originalUrl": f"git+{tmp_path.as_uri()}",
                    "active": False,
                    "storePaths": [],
                },
                "active-checkout": {
                    "originalUrl": f"git+{tmp_path.as_uri()}",
                    "active": True,
                    "storePaths": [],
                },
            },
        }
    )

    ensure_profile(tmp_path, runner=runner)

    assert runner.calls[-1][-4:] == [
        "profile",
        "upgrade",
        "active-checkout",
        "--no-write-lock-file",
    ]


def test_missing_profile_is_added_with_priority_five(tmp_path: Path) -> None:
    runner = RecordingRunner({"version": 3, "elements": {}})

    message = ensure_profile(tmp_path, runner=runner)

    assert message == f"Added Nix profile from: {tmp_path.resolve()}#default"
    assert runner.calls[-1][-6:] == [
        "profile",
        "add",
        f"{tmp_path.resolve()}#default",
        "--priority",
        "5",
        "--no-write-lock-file",
    ]


def test_profile_commands_use_the_selected_user_environment(tmp_path: Path) -> None:
    runner = RecordingRunner({"version": 3, "elements": {}})
    environment = {"HOME": str(tmp_path / "selected-home"), "PATH": "/nix/bin"}

    ensure_profile(tmp_path, runner=runner, environment=environment)

    assert len(runner.kwargs) == 2
    assert all(call["env"] is environment for call in runner.kwargs)


def test_invalid_profile_json_is_reported(tmp_path: Path) -> None:
    def invalid_runner(args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args, 0, stdout="not-json", stderr="")

    with pytest.raises(NixProfileError, match="invalid JSON"):
        ensure_profile(tmp_path, runner=invalid_runner)


def test_invalid_profile_element_is_reported() -> None:
    def invalid_runner(args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args, 0, stdout=json.dumps({"elements": {"dotfiles": "invalid"}}), stderr=""
        )

    with pytest.raises(NixProfileError, match="invalid element"):
        list_profile_elements(runner=invalid_runner)


@pytest.mark.parametrize(
    "details,error",
    [
        ({"storePaths": ["/nix/store/profile"]}, "active state"),
        ({"active": "true", "storePaths": ["/nix/store/profile"]}, "active state"),
        ({"active": True}, "store paths"),
        ({"active": True, "storePaths": None}, "store paths"),
        ({"active": True, "storePaths": ["relative-store"]}, "store paths"),
        ({"active": True, "storePaths": ["/nix/store/profile", 7]}, "store paths"),
    ],
)
def test_profile_inventory_rejects_malformed_contract(
    details: dict[str, object], error: str
) -> None:
    def invalid_runner(args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args, 0, stdout=json.dumps({"elements": {"dotfiles": details}}), stderr=""
        )

    with pytest.raises(NixProfileError, match=error):
        list_profile_elements(runner=invalid_runner)


def test_command_failures_are_reported(tmp_path: Path) -> None:
    def failing_runner(args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.CalledProcessError(1, args, stderr="profile is locked")

    with pytest.raises(NixProfileError, match="profile is locked"):
        ensure_profile(tmp_path, runner=failing_runner)


def test_profile_cli_reports_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setattr(cli, "ensure_profile", lambda _: "profile ready")

    assert cli.main(["profile"]) == 0
    assert capsys.readouterr().out.strip() == "profile ready"


def test_profile_cli_reports_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)

    def fail(_: Path) -> str:
        raise NixProfileError("profile is locked")

    monkeypatch.setattr(cli, "ensure_profile", fail)

    assert cli.main(["profile"]) == 1
    assert "profile is locked" in capsys.readouterr().out
