import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_bootstrap_is_the_only_root_setup_shell_entrypoint() -> None:
    automation_scripts = sorted(
        [
            *REPO_ROOT.glob("*.sh"),
            *REPO_ROOT.glob("scripts/**/*.sh"),
            *REPO_ROOT.glob("tests/**/*.sh"),
        ]
    )

    assert automation_scripts == [REPO_ROOT / "bootstrap.sh"]


def test_shell_compatibility_config_remains_declarative() -> None:
    shell_config = REPO_ROOT / "config" / "shell-nix.sh"

    assert shell_config.is_file()
    assert "Shell configuration for Nix package manager" in shell_config.read_text()


def test_zed_install_task_uses_bootstrap_entrypoint() -> None:
    tasks = json.loads(REPO_ROOT.joinpath(".zed", "tasks.json").read_text())

    install_task = next(task for task in tasks if task["label"] == "Install Dotfiles")
    assert install_task["command"] == "./bootstrap.sh install"


def test_operational_python_is_exactly_3_13() -> None:
    assert sys.version_info[:2] == (3, 13)

    flake = REPO_ROOT.joinpath("flake.nix").read_text()
    assert "python313" in flake
    assert "\n                python3\n" not in flake


def test_nix_consumers_do_not_write_the_committed_lock() -> None:
    bootstrap = REPO_ROOT.joinpath("bootstrap.sh").read_text()
    makefile = REPO_ROOT.joinpath("Makefile").read_text()
    profile = REPO_ROOT.joinpath("src/dotfiles_setup/nix_profile.py").read_text()

    assert "develop --no-write-lock-file .#default" in bootstrap
    assert "develop --no-write-lock-file .\\#default" in makefile
    assert profile.count('"--no-write-lock-file"') == 2
    assert "flake update --refresh" in makefile
    update_recipe = makefile.split("update:", 1)[1].split("\n\n", 1)[0]
    assert "--no-write-lock-file" not in update_recipe
