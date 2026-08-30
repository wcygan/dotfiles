from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup import installer as installer_module
from dotfiles_setup import locking as locking_module
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


@pytest.mark.parametrize("replacement_kind", ["directory", "symlink"])
def test_parent_swap_cannot_bypass_an_acquired_lock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    replacement_kind: str,
) -> None:
    values = _subprocess_environment(tmp_path / "home")
    path = lock_path(values)
    retained_parent = path.parent.with_name("dotfiles.retained")
    alternate_parent = path.parent.with_name("dotfiles.alternate")

    with mutation_lock("holder", environ=values):
        real_open = locking_module.os.open
        swapped = False

        def swap_parent_before_leaf_open(
            file: str | bytes | int,
            flags: int,
            mode: int = 0o777,
            *,
            dir_fd: int | None = None,
        ) -> int:
            nonlocal swapped
            if file == path.name and dir_fd is not None and not swapped:
                swapped = True
                path.parent.rename(retained_parent)
                if replacement_kind == "directory":
                    path.parent.mkdir()
                else:
                    alternate_parent.mkdir()
                    path.parent.symlink_to(alternate_parent, target_is_directory=True)
            return real_open(file, flags, mode, dir_fd=dir_fd)

        monkeypatch.setattr(locking_module.os, "open", swap_parent_before_leaf_open)
        with (
            pytest.raises(LockError, match="parent changed during acquisition"),
            mutation_lock("contender", environ=values),
        ):
            pytest.fail("the contender acquired a separate lock")

        assert swapped
        assert not (path.parent / path.name).exists()
        if path.parent.is_symlink():
            path.parent.unlink()
        else:
            path.parent.rename(alternate_parent)
        retained_parent.rename(path.parent)


def test_doctor_and_verify_do_not_take_mutation_lock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        installer_module,
        "mutation_lock",
        lambda *_args, **_kwargs: pytest.fail("locked"),
    )
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
