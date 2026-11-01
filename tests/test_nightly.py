from __future__ import annotations

import json
import plistlib
import subprocess
import sys
import time
from datetime import UTC
from pathlib import Path

import pytest

from dotfiles_setup import nightly
from dotfiles_setup.manifest import OperationJournal
from dotfiles_setup.mutations import FileMutation, execute_mutations
from dotfiles_setup.nightly_schedule import schedule_contents
from dotfiles_setup.paths import UserPathContext
from dotfiles_setup.recovery import run_recovery

REPO = Path(__file__).resolve().parents[1]


def revision(number: int) -> dict:
    return {
        "type": "github",
        "owner": "NixOS",
        "repo": "nixpkgs",
        "rev": f"{number:040x}",
        "narHash": "sha256-example",
        "lastModified": number,
    }


def test_quarantine_needs_full_seven_days_and_keeps_first_observation() -> None:
    now = 2_000_000
    first = nightly.observe([], revision(2), now)
    repeated = nightly.observe(first, revision(2), now + 100)
    assert repeated == first
    assert nightly.mature_revision(repeated, now + nightly.AGE_SECONDS - 1, revision(1)) is None
    assert nightly.mature_revision(repeated, now + nightly.AGE_SECONDS, revision(1)) == revision(2)
    assert nightly.mature_revision(repeated, now + nightly.AGE_SECONDS, revision(3)) is None


def test_backdated_commit_still_needs_observation_quarantine() -> None:
    records = nightly.observe([], revision(2), 10_000_000)
    assert nightly.mature_revision(records, 10_000_001, revision(1)) is None


def test_revision_cannot_change_under_same_sha() -> None:
    records = nightly.observe([], revision(2), 100)
    changed = {**revision(2), "narHash": "sha256-different"}
    with pytest.raises(nightly.NightlyError, match="immutable"):
        nightly.observe(records, changed, 101)


def test_commands_separate_json_stdout_from_nix_diagnostics(tmp_path: Path) -> None:
    commands = nightly.Commands(time.time() + 120, tmp_path / "log")
    result = commands.run(
        [
            sys.executable,
            "-c",
            'import sys; print("warning", file=sys.stderr); print("{\\"ok\\":true}")',
        ],
        tmp_path,
    )
    assert json.loads(result) == {"ok": True}
    assert "warning" in (tmp_path / "log").read_text()


def test_deadline_kills_child_before_apply(tmp_path: Path) -> None:
    marker = tmp_path / "applied"
    commands = nightly.Commands(time.time() + 60.3, tmp_path / "log")
    with pytest.raises(nightly.NightlyError, match="window"):
        commands.run(
            [
                sys.executable,
                "-c",
                "import time; from pathlib import Path; time.sleep(2); "
                f"Path({str(marker)!r}).write_text('bad')",
            ],
            tmp_path,
        )
    time.sleep(0.1)
    assert not marker.exists()


def test_checkout_ownership_preserves_human_edits(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "flake.lock").write_text("{}")
    source = tmp_path / "source.txt"
    source.write_text("baseline")
    state = {
        "repository": str(tmp_path),
        "source_hash": nightly.fingerprint(tmp_path),
        "lock_hash": nightly.lock_hash(tmp_path),
    }
    assert nightly.checkout_allowed(tmp_path, state)
    source.write_text("human change")
    assert not nightly.checkout_allowed(tmp_path, state)
    source.write_text("baseline")
    (tmp_path / "flake.lock").write_text('{"human":"change"}')
    assert not nightly.checkout_allowed(tmp_path, state)


@pytest.mark.parametrize("system", ["Darwin", "Linux"])
def test_scheduler_uses_nightly_gate_and_no_catch_up_policy(tmp_path: Path, system: str) -> None:
    context = UserPathContext.from_environment({"HOME": str(tmp_path)}, system=system)
    contents = schedule_contents(tmp_path / "repo with spaces", context, enabled=True)
    if system == "Darwin":
        job = plistlib.loads(next(iter(contents.values())))
        assert job["StartCalendarInterval"] == {"Hour": 3, "Minute": 0}
        assert job["ProgramArguments"][-1] == "nightly-run"
        assert "RunAtLoad" not in job and "KeepAlive" not in job
        assert job["Disabled"] is False
    else:
        service, timer = [data.decode() for data in contents.values()]
        assert '"nightly-run"' in service
        assert "03:00:00" in timer
        assert "Persistent=false" in timer and "WakeSystem=false" in timer


@pytest.mark.parametrize(
    "source, command",
    [
        ("nightly-schedule", "nightly-schedule"),
        ("nightly-lock", "nightly-update"),
    ],
)
def test_nightly_file_recovery_restores_prior_contents(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    source: str,
    command: str,
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    values = {"HOME": str(home)}
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    repo = home / "repo"
    repo.mkdir()
    destination = (
        home / "Library/LaunchAgents/com.wcygan.dotfiles.nightly.plist"
        if source == "nightly-schedule"
        else repo / "flake.lock"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("before")
    journal = OperationJournal(command, repo, environ=values)
    journal.transition("applying")
    execute_mutations(
        (
            FileMutation(
                destination=destination,
                visible_destination=destination,
                source=source,
                contents=b"after",
            ),
        ),
        journal=journal,
        authority_roots=(home,),
    )
    assert destination.read_text() == "after"
    assert (
        run_recovery(apply=True, yes=True, environ=values, system="Darwin", output=lambda _: None)
        == 0
    )
    assert destination.read_text() == "before"


@pytest.mark.parametrize("hour", [0, 2, 4, 11, 23])
def test_outside_window_does_not_start_nix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    hour: int,
) -> None:
    from datetime import datetime

    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 10, 31, hour, tzinfo=UTC)

    monkeypatch.setattr(nightly, "datetime", Clock)
    monkeypatch.setattr(nightly, "directory", lambda: tmp_path)

    def unexpected(*args, **kwargs):
        raise AssertionError("daytime must not start a mutating workflow")

    monkeypatch.setattr(nightly, "run_mutation", unexpected)
    assert nightly.run_nightly(REPO) == 0
    assert capsys.readouterr().out == ("Skipped: outside the 03:00–04:00 local update window.\n")


@pytest.mark.parametrize("fail_verify", [False, True])
def test_candidate_application_and_verification_rollback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fail_verify: bool,
) -> None:
    from dotfiles_setup.nix_profile import ProfileElement

    home = tmp_path / "home"
    repo = home / "repo"
    repo.mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    state_dir = home / ".local/state/dotfiles/nightly"
    state_dir.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "flake.nix").write_text("fixture")
    original = {
        "version": 7,
        "root": "root",
        "nodes": {
            "root": {"inputs": {"nixpkgs": "nixpkgs"}},
            "nixpkgs": {
                "original": {
                    "type": "github",
                    "owner": "NixOS",
                    "repo": "nixpkgs",
                    "ref": "stable",
                },
                "locked": revision(1),
            },
        },
    }
    lock = repo / "flake.lock"
    lock.write_text(json.dumps(original))
    reference = "github:NixOS/nixpkgs/stable"
    (state_dir / "observations.json").write_text(
        json.dumps(
            {
                reference: [
                    {"first_seen": time.time() - nightly.AGE_SECONDS - 10, "locked": revision(2)}
                ],
            }
        )
    )
    baseline = nightly.fingerprint(repo)
    state = {
        "repository": str(repo),
        "enabled": True,
        "source_hash": baseline,
        "lock_hash": nightly.lock_hash(repo),
    }
    before = ProfileElement("fixture", repo.as_uri(), (Path("/nix/store/before"),), True)
    after = ProfileElement("fixture", repo.as_uri(), (Path("/nix/store/after"),), True)
    installed = [before]
    monkeypatch.setattr(nightly, "list_profile_elements", lambda: tuple(installed))
    calls = []

    class CandidateCommands:
        end = time.time() + 3600

        def remaining(self):
            return 1800

        def run(self, args, cwd, *, cleanup=False):
            calls.append(args)
            if "metadata" in args:
                return json.dumps({"locked": revision(2)})
            if args[0] == "git":
                subprocess.run(args, cwd=cwd, check=True, capture_output=True)
            elif args[0] == "make":
                candidate = json.loads((cwd / "flake.lock").read_text())
                assert candidate["nodes"]["nixpkgs"]["locked"] == revision(2)
                assert (
                    candidate["nodes"]["nixpkgs"]["original"]
                    == original["nodes"]["nixpkgs"]["original"]
                )
            elif "upgrade" in args:
                installed[:] = [after]
            elif args[0] == "./bootstrap.sh" and fail_verify:
                raise nightly.NightlyError("verification failed")
            elif "rollback" in args:
                assert cleanup
                installed[:] = [before]
            return ""

    journal = OperationJournal("nightly-update", repo)
    journal.transition("applying")
    if fail_verify:
        with pytest.raises(nightly.NightlyError, match="verification"):
            nightly.update(repo, journal, CandidateCommands(), state)
        assert json.loads(lock.read_text()) == original
        assert installed == [before]
        assert not journal.pending_entries
        assert nightly.checkout_allowed(repo, state)
    else:
        nightly.update(repo, journal, CandidateCommands(), state)
        assert json.loads(lock.read_text())["nodes"]["nixpkgs"]["locked"] == revision(2)
        assert installed == [after]
        assert nightly.checkout_allowed(repo, state)
        assert state["backups"]
    assert any(args[0] == "make" for args in calls)


def test_verify_detects_incomplete_requested_schedule(tmp_path: Path) -> None:
    from dotfiles_setup.nightly_health import check_scheduler

    context = UserPathContext.from_environment({"HOME": str(tmp_path)}, system="Darwin")
    root = context.state_directory / "nightly"
    root.mkdir(parents=True)
    (root / "schedule.json").write_text(
        json.dumps(
            {
                "enabled": False,
                "requested_enabled": True,
                "repository": str(tmp_path),
            }
        )
    )
    with pytest.raises(ValueError, match="incomplete"):
        check_scheduler(tmp_path, context)


def test_health_acknowledgement_is_bound_to_checkout_and_valid_token(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from dotfiles_setup import nightly_health

    monkeypatch.setattr(nightly_health, "directory", lambda: tmp_path)
    nightly_health.acknowledge(REPO, "a" * 32)
    acknowledgement = json.loads((tmp_path / "last-health.json").read_text())
    assert acknowledgement["repository"] == str(REPO)
    assert acknowledgement["token"] == "a" * 32
    with pytest.raises(ValueError):
        nightly_health.acknowledge(REPO, "../unsafe")


def test_install_repairs_remembered_scheduler_with_selected_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from dotfiles_setup import installer, nightly_schedule

    home = tmp_path / "home"
    values = {"HOME": str(home)}
    root = home / ".local/state/dotfiles/nightly"
    root.mkdir(parents=True)
    (root / "schedule.json").write_text(
        json.dumps(
            {
                "repository": str(tmp_path),
                "requested_enabled": True,
                "enabled": False,
            }
        )
    )
    monkeypatch.setattr(installer, "ensure_profile", lambda *a, **kw: "profile")
    monkeypatch.setattr(installer, "link_config", lambda *a, **kw: None)
    monkeypatch.setattr(installer, "setup_rustup", lambda *a, **kw: "rustup")
    monkeypatch.setattr(installer, "run_verify", lambda *a, **kw: 0)
    repaired = []

    def configure(repo, journal, *, enabled, environ):
        repaired.append((repo, enabled, environ))
        assert journal.state == "applying"

    monkeypatch.setattr(nightly_schedule, "configure", configure)
    assert installer.run_install(tmp_path, environ=values, output=lambda _: None) == 0
    assert repaired == [(tmp_path, True, values)]


@pytest.mark.parametrize(
    "status, base, expected",
    [
        ("ahead", "1" * 40, True),
        ("behind", "1" * 40, False),
        ("diverged", "1" * 40, False),
        ("ahead", "3" * 40, False),
    ],
)
def test_quarantined_revision_must_remain_in_current_branch_history(
    monkeypatch: pytest.MonkeyPatch,
    status: str,
    base: str,
    expected: bool,
) -> None:
    import io

    def response(request, *, timeout):
        assert "/compare/" + "1" * 40 + "..." + "2" * 40 in request.full_url
        return io.BytesIO(
            json.dumps(
                {
                    "status": status,
                    "merge_base_commit": {"sha": base},
                }
            ).encode()
        )

    monkeypatch.setattr(nightly.urllib.request, "urlopen", response)
    assert nightly.still_on_branch("NixOS", "nixpkgs", "1" * 40, "2" * 40) is expected


def test_verify_detects_orphaned_scheduler_files(tmp_path: Path) -> None:
    from dotfiles_setup.nightly_health import check_scheduler

    context = UserPathContext.from_environment({"HOME": str(tmp_path)}, system="Darwin")
    plist = tmp_path / "Library/LaunchAgents/com.wcygan.dotfiles.nightly.plist"
    plist.parent.mkdir(parents=True)
    plist.write_text("orphaned")
    with pytest.raises(ValueError, match="without setup state"):
        check_scheduler(tmp_path, context)


def _clock_at(hour: int):
    from datetime import datetime

    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            local = datetime(2026, 10, 31, hour).astimezone()
            return local if tz is None else local.astimezone(tz)

    return Clock


def test_disabled_scheduler_with_registered_timer_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Replay DisabledNotRegistered: a disabled configuration cannot hide a live timer."""
    from dotfiles_setup import nightly_health

    context = UserPathContext.from_environment({"HOME": str(tmp_path)}, system="Darwin")
    root = context.state_directory / "nightly"
    root.mkdir(parents=True)
    (root / "schedule.json").write_text(
        json.dumps(
            {
                "repository": str(tmp_path),
                "requested_enabled": False,
                "enabled": False,
            }
        )
    )
    monkeypatch.setattr(nightly_health, "service_registered", lambda _: True)
    with pytest.raises(ValueError, match="still registered"):
        nightly_health.check_scheduler(tmp_path, context)

    monkeypatch.setattr(nightly_health, "service_registered", lambda _: False)
    assert nightly_health.check_scheduler(tmp_path, context) is None


def test_skipped_run_is_recorded_in_last_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Replay EveryRunRecorded: a skip must leave a durable last-run record."""
    monkeypatch.setattr(nightly, "datetime", _clock_at(0))
    monkeypatch.setattr(nightly, "directory", lambda: tmp_path)

    def unexpected(*args, **kwargs):
        raise AssertionError("a daytime run must not start a mutating workflow")

    monkeypatch.setattr(nightly, "run_mutation", unexpected)
    assert nightly.run_nightly(REPO) == 0
    payload = json.loads((tmp_path / "last-run.json").read_text())
    assert payload["result"] == "skipped-window"
    assert payload["exit_code"] == 0


def test_run_does_not_apply_after_disable_lands_before_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Replay NoApplyAfterDisable: a run must re-read state under the setup lock."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    for key in ("XDG_CACHE_HOME", "XDG_STATE_HOME", "XDG_CONFIG_HOME"):
        monkeypatch.delenv(key, raising=False)
    repo = (home / "repo").resolve()
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "flake.lock").write_text('{"lock": 1}\n')
    (repo / "source.txt").write_text("baseline\n")
    state_dir = home / ".local/state/dotfiles/nightly"
    state_dir.mkdir(parents=True)
    schedule_path = state_dir / "schedule.json"
    schedule_path.write_text(
        json.dumps(
            {
                "repository": str(repo),
                "requested_enabled": True,
                "enabled": True,
                "health_token": "a" * 32,
                "source_hash": nightly.fingerprint(repo),
                "lock_hash": nightly.lock_hash(repo),
            }
        )
    )
    original = (repo / "flake.lock").read_text()
    monkeypatch.setattr(nightly, "datetime", _clock_at(3))
    monkeypatch.setattr(
        nightly,
        "update",
        lambda *args, **kwargs: pytest.fail("update ran after the configuration was disabled"),
    )
    real_run_mutation = nightly.run_mutation

    def racing(command, repo_root, operation, **kwargs):
        # A separate disable completed just before this run acquired the lock.
        state = json.loads(schedule_path.read_text())
        state.update(requested_enabled=False, enabled=False, health_token=None)
        schedule_path.write_text(json.dumps(state))
        return real_run_mutation(command, repo_root, operation, **kwargs)

    monkeypatch.setattr(nightly, "run_mutation", racing)
    assert nightly.run_nightly(repo) == 0
    assert (repo / "flake.lock").read_text() == original
    assert json.loads(schedule_path.read_text())["requested_enabled"] is False
    payload = json.loads((state_dir / "last-run.json").read_text())
    assert payload["result"] == "skipped-state-changed"
    assert payload["exit_code"] == 0


def test_run_skips_and_records_while_setup_is_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Replay EveryRunRecorded: a timer that fires before setup completes still leaves a record."""
    monkeypatch.setattr(nightly, "datetime", _clock_at(3))
    state_dir = tmp_path / "nightly"
    state_dir.mkdir()
    (state_dir / "schedule.json").write_text(
        json.dumps(
            {
                "repository": str(REPO.resolve()),
                "requested_enabled": True,
                "enabled": False,
            }
        )
    )
    monkeypatch.setattr(nightly, "directory", lambda: state_dir)

    def unexpected(*args, **kwargs):
        raise AssertionError("an incomplete setup must not start a mutating workflow")

    monkeypatch.setattr(nightly, "run_mutation", unexpected)
    assert nightly.run_nightly(REPO) == 0
    payload = json.loads((state_dir / "last-run.json").read_text())
    assert payload["result"] == "skipped-disabled"
    assert payload["exit_code"] == 0


def test_disable_fails_when_timer_stays_registered(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Replay DisabledNotRegistered: configure must not call a disable complete."""
    from dotfiles_setup import nightly_health, nightly_schedule

    home = tmp_path / "home"
    binary = home / ".nix-profile/bin/python3"
    binary.parent.mkdir(parents=True)
    binary.write_text("#!/bin/sh\nexit 0\n")
    repo = home / "repo"
    repo.mkdir()
    values = {"HOME": str(home)}
    journal = OperationJournal("nightly-schedule", repo, environ=values)
    journal.transition("applying")
    monkeypatch.setattr(nightly_schedule, "execute_mutations", lambda *a, **kw: None)
    monkeypatch.setattr(
        nightly_schedule.subprocess,
        "run",
        lambda *a, **kw: subprocess.CompletedProcess(a[0], 0),
    )
    monkeypatch.setattr(nightly_health, "service_registered", lambda _: True)
    with pytest.raises(nightly.NightlyError, match="still registered"):
        nightly_schedule.configure(repo, journal, enabled=False, environ=values)
    state = json.loads((home / ".local/state/dotfiles/nightly/schedule.json").read_text())
    assert state["requested_enabled"] is False


def test_dirty_skip_records_checkout_status(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "flake.lock").write_text("{}")
    state_dir = tmp_path / "nightly"
    state_dir.mkdir()
    (state_dir / "schedule.json").write_text(
        json.dumps(
            {
                "repository": str(repo.resolve()),
                "requested_enabled": True,
                "enabled": True,
                "health_token": "a" * 32,
                "source_hash": nightly.fingerprint(repo),
                "lock_hash": nightly.lock_hash(repo),
            }
        )
    )
    (repo / "unreviewed.txt").write_text("private contents")
    monkeypatch.setattr(nightly, "datetime", _clock_at(3))
    monkeypatch.setattr(nightly, "directory", lambda: state_dir)

    assert nightly.run_nightly(repo) == 0
    payload = json.loads((state_dir / "last-run.json").read_text())
    assert payload["result"] == "skipped-dirty"
    assert "checkout contains changes" in payload["reason"]
    assert "?? unreviewed.txt" in payload["checkout_status"]
    assert "private contents" not in (state_dir / "last-run.json").read_text()


def test_failed_run_records_reason(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    for key in ("XDG_CACHE_HOME", "XDG_STATE_HOME", "XDG_CONFIG_HOME"):
        monkeypatch.delenv(key, raising=False)
    repo = home / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "flake.lock").write_text("{}")
    state_dir = home / ".local/state/dotfiles/nightly"
    state_dir.mkdir(parents=True)
    (state_dir / "schedule.json").write_text(
        json.dumps(
            {
                "repository": str(repo.resolve()),
                "requested_enabled": True,
                "enabled": True,
                "health_token": "a" * 32,
                "source_hash": nightly.fingerprint(repo),
                "lock_hash": nightly.lock_hash(repo),
            }
        )
    )
    monkeypatch.setattr(nightly, "datetime", _clock_at(3))

    def fail(*args, **kwargs):
        raise nightly.NightlyError("verification failed")

    monkeypatch.setattr(nightly, "update", fail)

    assert nightly.run_nightly(repo) == 1
    payload = json.loads((state_dir / "last-run.json").read_text())
    assert payload["result"] == "failed"
    assert payload["reason"] == "verification failed"
