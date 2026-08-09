import json
import re
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

    for path in REPO_ROOT.joinpath(".github/workflows").glob("*.yml"):
        for line in path.read_text().splitlines():
            if "nix develop" in line:
                assert "--no-write-lock-file" in line, f"mutable Nix consumer in {path}"


def test_github_actions_are_pinned_to_full_release_shas() -> None:
    action = re.compile(r"uses:\s+[^@\s]+@([0-9a-f]{40})\s+#\s+v\S+$")

    for path in REPO_ROOT.joinpath(".github/workflows").glob("*.yml"):
        uses = [line.strip() for line in path.read_text().splitlines() if "uses:" in line]
        assert uses, f"workflow has no actions: {path}"
        assert all(action.search(line) for line in uses), (
            f"mutable or undocumented action in {path}"
        )


def test_reproducible_dockerfiles_pin_manifest_digests() -> None:
    pinned = re.compile(r"^FROM\s+\S+:\S+@sha256:[0-9a-f]{64}(?:\s+AS\s+\S+)?$")

    for path in sorted(REPO_ROOT.glob("Dockerfile.*")):
        from_lines = [line for line in path.read_text().splitlines() if line.startswith("FROM ")]
        assert from_lines
        assert all(pinned.fullmatch(line) for line in from_lines), f"unpinned image in {path}"


def test_floating_images_are_confined_to_freshness_workflow() -> None:
    ci = REPO_ROOT.joinpath(".github/workflows/ci.yml").read_text()
    makefile = REPO_ROOT.joinpath("Makefile").read_text()
    driver = REPO_ROOT.joinpath("tests/docker_matrix.py").read_text()
    freshness = REPO_ROOT.joinpath(".github/workflows/freshness.yml").read_text()

    assert "--pull" not in ci
    assert "docker build --pull" not in makefile
    assert "--pull" not in driver
    assert "schedule:" in freshness
    assert "workflow_dispatch:" in freshness
    assert "docker build --pull" in freshness
    assert "s/@sha256:[0-9a-f]{64}//g" in freshness
    assert "docker run --rm" in freshness
    assert "git diff --exit-code" in freshness


def test_dependency_automation_requires_human_review() -> None:
    dependabot = REPO_ROOT.joinpath(".github/dependabot.yml").read_text()

    assert "package-ecosystem: github-actions" in dependabot
    assert "package-ecosystem: docker" in dependabot
    assert "interval: weekly" in dependabot
    workflows = "\n".join(
        path.read_text() for path in REPO_ROOT.joinpath(".github/workflows").glob("*.yml")
    )
    assert "auto-merge" not in workflows.lower()
    assert "automerge" not in workflows.lower()
