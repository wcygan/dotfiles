from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_ephemeral_home_can_access_linked_configuration(tmp_path: Path) -> None:
    home = tmp_path / "home"
    config_home = home / ".config"
    config_home.mkdir(parents=True)
    (home / ".nix-profile/bin").mkdir(parents=True)

    fish_link = config_home / "fish"
    shell_nix_link = config_home / "shell-nix.sh"
    fish_link.symlink_to(REPO_ROOT / "config/fish")
    shell_nix_link.symlink_to(REPO_ROOT / "config/shell-nix.sh")

    assert (fish_link / "config.fish").is_file()
    assert (fish_link / "conf.d/10-nix.fish").is_file()
    assert (fish_link / "conf.d/20-direnv.fish").is_file()
    assert (fish_link / "conf.d/30-starship.fish").is_file()
    assert (fish_link / "functions/nix-try.fish").is_file()
    assert (fish_link / "functions/nix-install.fish").is_file()
    assert shell_nix_link.is_file()


def test_fish_loads_the_linked_configuration_in_an_ephemeral_home(tmp_path: Path) -> None:
    fish = shutil.which("fish")
    assert fish is not None, "fish is required by the canonical Nix test suite"

    home = tmp_path / "home"
    config_home = home / ".config"
    config_home.mkdir(parents=True)
    (home / ".nix-profile/bin").mkdir(parents=True)
    (config_home / "fish").symlink_to(REPO_ROOT / "config/fish")

    command = """
        functions -q fish_add_path; or exit 10
        functions -q nix-try; or exit 11
        functions -q nix-install; or exit 12
        set -q NIX_CONFIG; or exit 13
        string match -q '*nix-command flakes*' -- $NIX_CONFIG; or exit 14
        abbr --show | string match -q '*nix-update*'; or exit 15
        contains $HOME/.nix-profile/bin $PATH; or exit 16
    """
    environment = {
        **os.environ,
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(config_home),
        "TERM": "dumb",
    }
    result = subprocess.run(
        [fish, "--private", "--interactive", "--command", command],
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
