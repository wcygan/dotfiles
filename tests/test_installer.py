from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any

import pytest

from dotfiles_setup import cli
from dotfiles_setup import installer as installer_module
from dotfiles_setup.installer import run_install, run_mutation, run_recovery_workflow
from dotfiles_setup.manifest import OperationJournal, read_manifest, state_directory


def _environment(home: Path) -> dict[str, str]:
    return {"HOME": str(home), "DOTFILES_SKIP_FISH_GREETING": "1"}


def _install_stubs(
    monkeypatch: pytest.MonkeyPatch,
    events: list[str],
    *,
    profile_error: Exception | None = None,
    link_error: Exception | None = None,
    verify_exit: int = 0,
    verify_error: Exception | None = None,
) -> None:
    def profile(_repo_root: Path, **_kwargs: object) -> str:
        events.append("profile")
        if profile_error is not None:
            raise profile_error
        return "ready"

    def links(_repo_root: Path, **_kwargs: Any) -> None:
        events.append("links")
        if link_error is not None:
            raise link_error

    monkeypatch.setattr(installer_module, "ensure_profile", profile)
    monkeypatch.setattr(installer_module, "link_config", links)
    monkeypatch.setattr(
        installer_module,
        "setup_rustup",
        lambda _repo_root, **_kwargs: events.append("rustup"),
    )
    monkeypatch.setattr(
        installer_module,
        "configure_shell_handoff",
        lambda **_kwargs: events.append("handoff"),
    )

    def verify(_repo_root: Path, **_kwargs: Any) -> int:
        events.append("verify")
        if verify_error is not None:
            raise verify_error
        return verify_exit

    monkeypatch.setattr(installer_module, "run_verify", verify)


def test_direct_mutation_success_records_one_operation(tmp_path: Path) -> None:
    values = _environment(tmp_path / "home")

    assert run_mutation("example", tmp_path, lambda _journal: None, environ=values) == 0

    manifest = read_manifest(state_directory(values) / "completed.json")
    assert manifest["state"] == "completed"
    assert manifest["operations"] == [{"name": "example", "status": "completed"}]


def test_direct_mutation_failure_creates_recovery_needed_state(tmp_path: Path) -> None:
    values = _environment(tmp_path / "home")

    def fail(_journal: OperationJournal) -> None:
        raise RuntimeError("injected failure")

    assert run_mutation("example", tmp_path, fail, environ=values, output=lambda _: None) == 1

    manifest = read_manifest(state_directory(values) / "recovery-needed.json")
    assert manifest["state"] == "recovery-needed"
    assert manifest["operations"] == [{"name": "example", "status": "failed"}]


def test_direct_mutation_checkpoints_failure_before_releasing_lock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []

    @contextmanager
    def lock(_command: str, **_kwargs: object):
        events.append("lock-enter")
        yield
        events.append("lock-exit")

    class Journal:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.state = "planned"

        def transition(self, state: str) -> None:
            events.append(f"journal-{state}")
            self.state = state

        def record_operation(self, name: str, status: str) -> None:
            events.append(f"journal-{name}-{status}")

    def fail(_journal: object) -> None:
        events.append("operation")
        raise RuntimeError("mutation failed")

    monkeypatch.setattr(installer_module, "mutation_lock", lock)
    monkeypatch.setattr(installer_module, "OperationJournal", Journal)

    output: list[str] = []
    assert run_mutation("example", tmp_path, fail, output=output.append) == 1
    assert events == [
        "lock-enter",
        "journal-applying",
        "operation",
        "journal-example-failed",
        "journal-recovery-needed",
        "lock-exit",
    ]
    assert output == ["example failed: mutation failed"]


def test_direct_mutation_reports_primary_and_journal_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []

    @contextmanager
    def lock(_command: str, **_kwargs: object):
        events.append("lock-enter")
        yield
        events.append("lock-exit")

    class Journal:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.state = "planned"

        def transition(self, state: str) -> None:
            events.append(f"journal-{state}")
            self.state = state

        def record_operation(self, _name: str, _status: str) -> None:
            events.append("journal-record-failed")
            raise RuntimeError("journal storage failed")

    monkeypatch.setattr(installer_module, "mutation_lock", lock)
    monkeypatch.setattr(installer_module, "OperationJournal", Journal)

    def fail(_journal: object) -> None:
        raise RuntimeError("mutation failed")

    output: list[str] = []
    assert run_mutation("example", tmp_path, fail, output=output.append) == 1
    assert events[-2:] == ["journal-recovery-needed", "lock-exit"]
    assert output == [
        "example failed: mutation failed; journal checkpoint failed: "
        "could not record example failure: journal storage failed"
    ]


def test_direct_mutation_preserves_a_terminal_mutator_state(tmp_path: Path) -> None:
    values = _environment(tmp_path / "home")

    def stop(journal: OperationJournal) -> None:
        journal.transition("failed")

    assert run_mutation("example", tmp_path, stop, environ=values) == 1
    assert read_manifest(state_directory(values) / "current.json")["state"] == "failed"


def test_profile_completes_before_serial_setup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    _install_stubs(monkeypatch, events)

    exit_code = run_install(
        tmp_path,
        environ=_environment(tmp_path / "home"),
        output=lambda _: None,
    )

    assert exit_code == 0
    assert events == ["profile", "links", "rustup", "verify"]


def test_link_failure_stops_later_mutations_and_handoff_is_skipped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    output: list[str] = []
    _install_stubs(monkeypatch, events, link_error=RuntimeError("link failure"))

    exit_code = run_install(
        tmp_path,
        shell_handoff=True,
        environ=_environment(tmp_path / "home"),
        output=output.append,
    )

    assert exit_code == 1
    assert events == ["profile", "links", "verify"]
    assert "[FAIL] links: link failure" in output
    assert "[SKIP] rustup: links failed" in output
    assert "[SKIP] shell-handoff: required setup operation failed" in output


def test_profile_failure_skips_setup_but_still_verifies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    output: list[str] = []
    _install_stubs(monkeypatch, events, profile_error=RuntimeError("profile locked"))

    exit_code = run_install(
        tmp_path,
        shell_handoff=True,
        environ=_environment(tmp_path / "home"),
        output=output.append,
    )

    assert exit_code == 1
    assert events == ["profile", "verify"]
    assert "[SKIP] links: profile failed" in output
    assert "[SKIP] rustup: profile failed" in output
    assert "[SKIP] shell-handoff: profile failed" in output


def test_profile_failure_preserves_a_verification_exit_code(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    _install_stubs(
        monkeypatch,
        events,
        profile_error=RuntimeError("profile locked"),
        verify_exit=7,
    )

    assert (
        run_install(
            tmp_path,
            environ=_environment(tmp_path / "home"),
            output=lambda _: None,
        )
        == 7
    )
    assert events == ["profile", "verify"]


def test_successful_setup_runs_opt_in_handoff_before_verify(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    _install_stubs(monkeypatch, events)

    exit_code = run_install(
        tmp_path,
        shell_handoff=True,
        environ=_environment(tmp_path / "home"),
        output=lambda _: None,
    )

    assert exit_code == 0
    assert events == ["profile", "links", "rustup", "handoff", "verify"]


def test_verification_only_failure_records_failed_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    values = _environment(tmp_path / "home")
    _install_stubs(monkeypatch, events, verify_exit=1)

    assert run_install(tmp_path, environ=values, output=lambda _: None) == 1

    manifest = read_manifest(state_directory(values) / "current.json")
    assert manifest["state"] == "failed"
    assert not (state_directory(values) / "recovery-needed.json").exists()


def test_verification_exception_records_failed_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    values = _environment(tmp_path / "home")
    _install_stubs(
        monkeypatch,
        events,
        verify_error=RuntimeError("verification unavailable"),
    )

    output: list[str] = []
    assert run_install(tmp_path, environ=values, output=output.append) == 1

    manifest = read_manifest(state_directory(values) / "current.json")
    assert manifest["state"] == "failed"
    assert manifest["operations"][-1] == {"name": "verify", "status": "failed"}
    assert not (state_directory(values) / "recovery-needed.json").exists()
    assert "[FAIL] verify: verification unavailable" in output


def test_install_forwards_one_user_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    values = _environment(tmp_path / "selected-home")
    values["SHELL"] = "/bin/zsh"
    captured: dict[str, object] = {}

    def profile(_root: Path, **kwargs: object) -> str:
        captured["profile_environment"] = kwargs["environment"]
        return "ready"

    monkeypatch.setattr(installer_module, "ensure_profile", profile)
    monkeypatch.setattr(installer_module, "link_config", lambda *_args, **_kwargs: None)

    def rustup(_root: Path, **kwargs: object) -> None:
        captured["rustup_environment"] = kwargs["environment"]

    def handoff(**kwargs: object) -> None:
        captured["handoff_home"] = kwargs["home"]
        captured["handoff_shell"] = kwargs["shell"]

    def verify(_root: Path, **kwargs: object) -> int:
        captured["verify_environment"] = kwargs["environ"]
        return 0

    monkeypatch.setattr(installer_module, "setup_rustup", rustup)
    monkeypatch.setattr(installer_module, "configure_shell_handoff", handoff)
    monkeypatch.setattr(installer_module, "run_verify", verify)

    assert run_install(
        tmp_path,
        shell_handoff=True,
        environ=values,
        output=lambda _: None,
    ) == 0
    assert captured == {
        "profile_environment": values,
        "rustup_environment": values,
        "handoff_home": (tmp_path / "selected-home").resolve(),
        "handoff_shell": "/bin/zsh",
        "verify_environment": values,
    }


def test_install_does_not_use_ambient_shell_for_selected_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []
    captured: dict[str, object] = {}
    values = _environment(tmp_path / "selected-home")
    monkeypatch.setenv("SHELL", "/bin/bash")
    _install_stubs(monkeypatch, events)

    def handoff(**kwargs: object) -> None:
        events.append("handoff")
        captured["shell"] = kwargs["shell"]

    monkeypatch.setattr(installer_module, "configure_shell_handoff", handoff)

    assert run_install(
        tmp_path,
        shell_handoff=True,
        environ=values,
        output=lambda _: None,
    ) == 0
    assert events == ["profile", "links", "rustup", "handoff", "verify"]
    assert captured == {"shell": ""}


def test_install_preserves_verification_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    output: list[str] = []
    _install_stubs(monkeypatch, events)

    def verify(_root: Path, **kwargs: object) -> int:
        callback = kwargs["output"]
        assert callable(callback)
        callback("[PASS] exact verification line")
        return 0

    monkeypatch.setattr(installer_module, "run_verify", verify)

    assert run_install(tmp_path, environ=_environment(tmp_path / "home"), output=output.append) == 0
    assert "[PASS] exact verification line" in output
    assert not any(line.startswith("[verify]") for line in output)
    assert "[PASS] verify: complete" not in output


def test_install_preserves_a_terminal_state_from_a_mutator(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    values = _environment(tmp_path / "home")
    _install_stubs(monkeypatch, events)

    def terminal_links(_repo_root: Path, **kwargs: Any) -> None:
        events.append("links")
        journal = kwargs["journal"]
        assert isinstance(journal, OperationJournal)
        journal.transition("failed")

    monkeypatch.setattr(installer_module, "link_config", terminal_links)

    assert run_install(tmp_path, environ=values, output=lambda _: None) == 1
    assert read_manifest(state_directory(values) / "current.json")["state"] == "failed"


def test_install_checkpoints_unexpected_failure_before_releasing_lock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []

    @contextmanager
    def lock(_command: str, **_kwargs: object):
        events.append("lock-enter")
        yield
        events.append("lock-exit")

    class Journal:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.state = "planned"

        def transition(self, state: str) -> None:
            events.append(f"journal-{state}")
            self.state = state

    def fail_results(*_args: object, **_kwargs: object) -> tuple[list[object], int]:
        events.append("install-workflow")
        raise RuntimeError("workflow failed")

    monkeypatch.setattr(installer_module, "mutation_lock", lock)
    monkeypatch.setattr(installer_module, "OperationJournal", Journal)
    monkeypatch.setattr(installer_module, "_install_results", fail_results)

    output: list[str] = []
    assert run_install(tmp_path, output=output.append) == 1
    assert events == [
        "lock-enter",
        "journal-applying",
        "install-workflow",
        "journal-recovery-needed",
        "lock-exit",
    ]
    assert output == ["Install failed: workflow failed"]


def test_install_reports_primary_and_terminal_checkpoint_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @contextmanager
    def lock(_command: str, **_kwargs: object):
        yield

    class Journal:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.state = "planned"

        def transition(self, state: str) -> None:
            self.state = state
            if state == "recovery-needed":
                raise RuntimeError("checkpoint storage failed")

    def fail_results(*_args: object, **_kwargs: object) -> tuple[list[object], int]:
        raise RuntimeError("workflow failed")

    monkeypatch.setattr(installer_module, "mutation_lock", lock)
    monkeypatch.setattr(installer_module, "OperationJournal", Journal)
    monkeypatch.setattr(installer_module, "_install_results", fail_results)

    output: list[str] = []
    assert run_install(tmp_path, output=output.append) == 1
    assert output == [
        "Install failed: workflow failed; journal checkpoint failed: "
        "could not write the recovery-needed state: checkpoint storage failed"
    ]


def test_recovery_dry_run_does_not_lock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        installer_module,
        "mutation_lock",
        lambda *_args, **_kwargs: pytest.fail("recovery dry run took a lock"),
    )
    monkeypatch.setattr(installer_module, "run_recovery", lambda **_kwargs: 0)

    assert run_recovery_workflow() == 0


def test_recovery_apply_locks_without_replacing_the_pending_journal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    values = _environment(tmp_path / "home")
    pending = OperationJournal("link", tmp_path, environ=values)
    pending.transition("applying")
    operation_id = pending.data["operation_id"]
    events: list[str] = []

    @contextmanager
    def lock(command: str, **_kwargs: Any):
        events.append(command)
        yield

    monkeypatch.setattr(installer_module, "mutation_lock", lock)
    monkeypatch.setattr(installer_module, "run_recovery", lambda **_kwargs: 0)

    assert run_recovery_workflow(apply=True, yes=True, environ=values) == 0
    assert events == ["recover"]
    current = read_manifest(state_directory(values) / "current.json")
    assert current["operation_id"] == operation_id


def test_install_cli_forwards_optional_shell_handoff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def install(repo_root: Path, **kwargs: object) -> int:
        captured["repo_root"] = repo_root
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(cli, "run_install", install)

    assert cli.main(["install", "--shell-handoff"]) == 0
    assert captured == {"repo_root": cli.REPO_ROOT, "shell_handoff": True}
