from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_FISH = REPO_ROOT / "config" / "fish" / "config.fish"


def _fish_path_after_config(tmp_path: Path, rex_bin_dir: Path | None) -> list[str]:
    fish = shutil.which("fish")
    if fish is None:
        pytest.skip("fish is not installed")
    environment = os.environ.copy()
    environment["HOME"] = str(tmp_path)
    environment["XDG_CONFIG_HOME"] = str(tmp_path / ".config")
    environment["PATH"] = os.pathsep.join(["/usr/bin", "/bin"])
    environment.pop("REX_BIN_DIR", None)
    if rex_bin_dir is not None:
        environment["PATH"] = os.pathsep.join(["/usr/bin", str(rex_bin_dir), "/bin"])
        environment["REX_BIN_DIR"] = str(rex_bin_dir)
    result = subprocess.run(
        [fish, "--no-config", "-c", 'source $argv[1]; printf "%s\\n" $PATH', str(CONFIG_FISH)],
        env=environment,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.splitlines()


def test_rex_bin_dir_ends_first_on_path(tmp_path: Path) -> None:
    rex_bin_dir = tmp_path / "Rex Server.app" / "Contents" / "MacOS"
    rex_bin_dir.mkdir(parents=True)

    path = _fish_path_after_config(tmp_path, rex_bin_dir)

    assert path[0] == str(rex_bin_dir)
    assert path.count(str(rex_bin_dir)) == 1


def test_path_has_no_rex_entry_outside_rex(tmp_path: Path) -> None:
    path = _fish_path_after_config(tmp_path, None)

    assert "" not in path
    assert path[:2] == ["/usr/bin", "/bin"]
