"""Check a hosted install job against receipts published by successful main pushes."""

import hashlib
import io
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

from check_changes import git, plan
from config_checks import check_kind

# Config contents are exercised by acceptance (including Linux login-shell startup).
COMMON = (
    "bootstrap.sh",
    "src",
    "config",
    "flake.nix",
    "flake.lock",
    "rust-toolchain.toml",
    "pyproject.toml",
    "uv.lock",
    "Makefile",
    ".github",
    "scripts",
)


def fingerprint(job):
    paths = list(COMMON)
    if job == "evaluation":
        paths = ["flake.nix", "flake.lock", "Makefile", ".github", "scripts"]
    if job in ("ubuntu", "fedora"):
        paths += ["Dockerfile." + job, ".dockerignore", "tests/docker_matrix.py", "README.md"]
    image = [os.environ.get(key) for key in ("ImageOS", "ImageVersion", "RUNNER_ARCH")]
    if not all(image):
        return None
    # Workflow revision covers the actual command even when replaying an older checkout.
    workflow = git("rev-parse", os.environ["GITHUB_SHA"] + ":.github/workflows/ci.yml").strip()
    entries = []
    for record in git("ls-tree", "-rz", "HEAD", "--", *paths).split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, _, _ = metadata.split()
        # Acceptance verifies these links and their inventory. Application syntax
        # is checked separately. Keep modes, names and symlink targets in the key.
        if mode in (b"100644", b"100755") and check_kind(os.fsdecode(path)) in {
            "lua",
            "json",
            "jsonc",
            "toml",
        }:
            record = mode + b"\t" + path
        entries.append(record)
    files = b"\0".join(entries)
    return hashlib.sha256(
        b"\0".join([workflow, files, job.encode(), json.dumps(image).encode()])
    ).hexdigest()


def api(endpoint):
    return subprocess.check_output(["gh", "api", endpoint], timeout=12)


def receipt(job, key):
    repo = os.environ["GITHUB_REPOSITORY"]
    branch = os.environ["DEFAULT_BRANCH"]
    name = f"evidence-{job}-{key}"
    artifacts = json.loads(api(f"repos/{repo}/actions/artifacts?name={name}&per_page=30"))
    for artifact in artifacts["artifacts"]:
        if artifact["name"] != name or artifact["expired"]:
            continue
        run_id = artifact["workflow_run"]["id"]
        run = json.loads(api(f"repos/{repo}/actions/runs/{run_id}"))
        if (
            run["head_repository"]["full_name"] != repo
            or run["head_branch"] != branch
            or run["event"] != "push"
            or run["conclusion"] != "success"
            or run["path"] != ".github/workflows/ci.yml"
        ):
            continue
        payload = api(f"repos/{repo}/actions/artifacts/{artifact['id']}/zip")
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            data = json.loads(archive.read("receipt.json"))
        if data == {"job": job, "fingerprint": key, "sha": run["head_sha"]}:
            return run["html_url"]
    return None


def main(job):
    base = os.environ.get("COMPARE_BASE", "")
    if os.environ.get("SHADOW_HEAD"):
        base = "HEAD^"
    key = fingerprint(job)
    selection = plan(base, "HEAD")
    reason = selection["checks"].get(job)
    prior = None
    if not reason and key:
        try:
            prior = receipt(job, key)
        except (
            OSError,
            ValueError,
            KeyError,
            subprocess.SubprocessError,
            zipfile.BadZipFile,
        ) as error:
            print(f"Prior evidence unavailable ({type(error).__name__})")
    path = Path(os.environ["RUNNER_TEMP"]) / "receipt.json"
    path.write_text(
        json.dumps(
            {"job": job, "fingerprint": key, "sha": git("rev-parse", "HEAD").decode().strip()}
        )
    )
    with open(os.environ["GITHUB_OUTPUT"], "a") as out:
        for check in ("quality", "docs", "config", "shell"):
            print(f"{check}={str(check in selection['checks']).lower()}", file=out)
        print(f"key={key or ''}", file=out)
        print(f"reuse={'true' if prior else 'false'}", file=out)
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
        decision = f"Matching evidence: {prior}" if prior else "Run current acceptance"
        print(f"### {job}\n{decision}\n\nComparison and routing reasons\n", file=summary)
        # Indented JSON prevents paths from introducing markup.
        for line in json.dumps(selection, indent=2, sort_keys=True).splitlines():
            print("    " + line, file=summary)


if __name__ == "__main__":
    main(sys.argv[1])
