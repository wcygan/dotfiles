import io
import json
import zipfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "invalid",
    [None, "expired", "stale", "fork", "pr", "branch", "workflow", "failed", "sha", "key"],
)
def test_receipt_requires_a_matching_successful_main_push(monkeypatch, invalid):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    import ci_evidence

    repo = "owner/repo"
    monkeypatch.setenv("GITHUB_REPOSITORY", repo)
    monkeypatch.setenv("DEFAULT_BRANCH", "main")
    artifact = {
        "id": 21,
        "created_at": (
            datetime.now(UTC) - timedelta(days=8 if invalid == "stale" else 0)
        ).isoformat(),
        "workflow_run": {"id": 11},
        "name": "evidence-native-key",
        "expired": invalid == "expired",
    }
    run = {
        "head_repository": {"full_name": "other/repo" if invalid == "fork" else repo},
        "head_branch": "topic" if invalid == "branch" else "main",
        "event": "pull_request" if invalid == "pr" else "push",
        "path": "other.yml" if invalid == "workflow" else ".github/workflows/ci.yml",
        "conclusion": "failure" if invalid == "failed" else "success",
        "head_sha": "abc",
        "html_url": "trusted-run",
    }
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as out:
        out.writestr(
            "receipt.json",
            json.dumps(
                {
                    "job": "native",
                    "fingerprint": "old" if invalid == "key" else "key",
                    "sha": "old" if invalid == "sha" else "abc",
                }
            ),
        )

    def api(endpoint):
        if endpoint.endswith("/zip"):
            return archive.getvalue()
        if "/actions/runs/" in endpoint:
            return json.dumps(run)
        return json.dumps({"artifacts": [artifact]})

    monkeypatch.setattr(ci_evidence, "api", api)
    assert ci_evidence.receipt("native", "key") == (None if invalid else "trusted-run")


@pytest.mark.parametrize(
    ("changed", "receipt", "force", "skip"),
    [
        (False, "prior", "false", True),
        (False, "prior", "true", False),
        (False, None, "false", False),
        (True, "prior", "false", False),
    ],
)
def test_decision_requires_both_selection_and_verifiable_evidence(
    monkeypatch, tmp_path, changed, receipt, force, skip
):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    import ci_evidence

    monkeypatch.setenv("FORCE_FULL", force)
    monkeypatch.setenv("RUNNER_TEMP", str(tmp_path))
    monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path / "output"))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(tmp_path / "summary"))
    monkeypatch.setattr(ci_evidence, "fingerprint", lambda _: "key")
    monkeypatch.setattr(
        ci_evidence, "plan", lambda *_: {"checks": {"native": ["src/a"]} if changed else {}}
    )
    monkeypatch.setattr(ci_evidence, "receipt", lambda *_: receipt)
    monkeypatch.setattr(ci_evidence, "git", lambda *_: b"abc")
    ci_evidence.main("native")
    assert f"skip={str(skip).lower()}" in (tmp_path / "output").read_text().splitlines()


def test_fingerprint_intentionally_reuses_only_passive_config_contents(monkeypatch, tmp_path):
    import subprocess

    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    import check_changes
    import ci_evidence

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=tmp_path).decode().strip()

    def write(path, contents):
        file = tmp_path / path
        file.parent.mkdir(exist_ok=True, parents=True)
        file.write_text(contents)

    def commit():
        git("add", ".")
        git("-c", "user.name=test", "-c", "user.email=test@example.org", "commit", "-qm", "change")

    git("init", "-q")
    write(".github/workflows/ci.yml", "workflow")
    write("config/zed/settings.json", "{}")
    write("flake.lock", "locked")
    commit()
    monkeypatch.setattr(check_changes, "ROOT", tmp_path)
    monkeypatch.setenv("GITHUB_SHA", git("rev-parse", "HEAD"))
    for name in ("ImageOS", "ImageVersion", "RUNNER_ARCH"):
        monkeypatch.setenv(name, "identity")
    first = ci_evidence.fingerprint("native")
    assert first
    write("config/zed/settings.json", '{"disable_ai": true}')
    commit()
    assert ci_evidence.fingerprint("native") == first
    write("flake.lock", "changed")
    commit()
    second = ci_evidence.fingerprint("native")
    assert second and second != first
    monkeypatch.setenv("ImageVersion", "updated")
    assert ci_evidence.fingerprint("native") != second
    monkeypatch.delenv("ImageVersion")
    assert ci_evidence.fingerprint("native") is None


@pytest.mark.parametrize("exit_code", [0, 1])
def test_runner_reuses_only_a_responsive_daemon(tmp_path, exit_code):
    import os
    import subprocess
    import textwrap

    root = Path(__file__).resolve().parents[1]
    action = (root / ".github/actions/prepare-shadow/action.yml").read_text()
    probe = textwrap.dedent(action.split("run: |\n", 1)[1].split("    - shell:", 1)[0])
    nix = tmp_path / "nix"
    nix.write_text(
        f'#!/bin/sh\n[ "$*" = "--extra-experimental-features nix-command store info '
        f'--store daemon" ] || exit 2\nexit {exit_code}\n'
    )
    nix.chmod(0o755)
    output = tmp_path / "output"
    path = tmp_path / "path"
    output.touch()
    path.touch()
    subprocess.run(
        ["bash", "-ec", probe],
        check=True,
        env={
            **os.environ,
            "PATH": str(tmp_path) + os.pathsep + os.environ["PATH"],
            "GITHUB_OUTPUT": str(output),
            "GITHUB_PATH": str(path),
        },
    )
    assert output.read_text() == ("ready=true\n" if exit_code == 0 else "")
    assert path.read_text() == (str(tmp_path) + "\n" if exit_code == 0 else "")
