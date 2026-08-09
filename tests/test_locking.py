from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.errors import LockError
from dotfiles_setup.locking import lock_path, mutation_lock
from dotfiles_setup.manifest import state_directory


def _subprocess_environment(home: Path) -> dict[str, str]:
    values = dict(os.environ)
    values["HOME"] = str(home)
    values.pop("XDG_CACHE_HOME", None)
    values.pop("XDG_STATE_HOME", None)
    values["PYTHONPATH"] = str(Path.cwd() / "src")
    return values


def test_second_process_fails_fast_and_lock_file_persists(tmp_path: Path) -> None:
    home = tmp_path / "home"
    ready = tmp_path / "ready"
    release = tmp_path / "release"
    script = (
        "from pathlib import Path\n"
        "import os, time\n"
        "from dotfiles_setup.locking import mutation_lock\n"
        "with mutation_lock('holder'):\n"
        " Path(os.environ['READY']).write_text('ready')\n"
        " while not Path(os.environ['RELEASE']).exists(): time.sleep(0.01)\n"
    )
    values = _subprocess_environment(home)
    values.update({"READY": str(ready), "RELEASE": str(release)})
    holder = subprocess.Popen([sys.executable, "-c", script], env=values)
    try:
        deadline = time.monotonic() + 5
        while not ready.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert ready.exists()
        started = time.monotonic()
        with (
            pytest.raises(LockError, match="another dotfiles setup operation is running"),
            mutation_lock("contender", environ=values),
        ):
            pass
        assert time.monotonic() - started < 1
    finally:
        release.write_text("release")
        holder.wait(timeout=5)
    assert holder.returncode == 0
    assert lock_path(values).is_file()


def test_doctor_and_verify_do_not_take_mutation_lock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "mutation_lock", lambda *_args, **_kwargs: pytest.fail("locked"))
    monkeypatch.setattr(cli, "run_doctor", lambda: 0)
    monkeypatch.setattr(cli, "run_verify", lambda _repo: 0)

    assert cli.main(["doctor"]) == 0
    assert cli.main(["verify"]) == 0


def test_shell_handoff_cli_reports_contention_without_traceback(tmp_path: Path) -> None:
    values = _subprocess_environment(tmp_path / "home")
    with mutation_lock("holder", environ=values):
        result = subprocess.run(
            [sys.executable, "-m", "dotfiles_setup", "shell-handoff"],
            env=values,
            check=False,
            capture_output=True,
            text=True,
        )
    assert result.returncode == 1
    assert "another dotfiles setup operation is running" in result.stdout
    assert "Traceback" not in result.stdout + result.stderr


def test_relative_xdg_lock_and_state_paths_fall_back_to_home(tmp_path: Path) -> None:
    values = {
        "HOME": str(tmp_path / "home"),
        "XDG_CACHE_HOME": "relative-cache",
        "XDG_STATE_HOME": "relative-state",
    }

    assert lock_path(values) == (tmp_path / "home" / ".cache" / "dotfiles" / "setup.lock")
    assert state_directory(values) == (tmp_path / "home" / ".local" / "state" / "dotfiles")
