import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_changes.py"
FULL = {"quality", "evaluation", "native", "ubuntu", "fedora", "docs"}


def classify(repo, *args):
    output = subprocess.check_output([sys.executable, SCRIPT, *args], cwd=repo)
    return json.loads(output)["checks"]


def test_local_comparison_covers_index_worktree_untracked_and_rename(tmp_path):
    def git(*args):
        subprocess.run(["git", *args], cwd=tmp_path, check=True)

    git("init", "-q")
    (tmp_path / "README.md").touch()
    (tmp_path / "flake.nix").touch()
    git("add", ".")
    git("-c", "user.name=test", "-c", "user.email=test@example.org", "commit", "-qm", "base")
    git("mv", "README.md", "agent-skills.lock.toml")
    (tmp_path / "flake.nix").unlink()
    (tmp_path / "unknown").touch()
    checks = classify(tmp_path, "--base", "HEAD")
    assert set(checks) == FULL
    assert set(checks["docs"]) == {"README.md", "unknown"}
    assert set(checks["native"]) == {"flake.nix", "unknown"}
    assert "agent-skills.lock.toml" in checks["quality"]
    assert classify(tmp_path, "--base", "HEAD", "--head", "HEAD") == {}


def test_empty_or_unknown_base_selects_every_check(tmp_path):
    for base in ("", "unavailable"):
        assert set(classify(tmp_path, "--base", base)) == FULL


def test_classifier_changes_select_every_check(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=test",
            "-c",
            "user.email=test@example.org",
            "commit",
            "--allow-empty",
            "-qm",
            "base",
        ],
        cwd=tmp_path,
        check=True,
    )
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/check_changes.py").touch()
    assert set(classify(tmp_path, "--base", "HEAD")) == FULL
