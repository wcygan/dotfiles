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
    if job in ("ubuntu", "fedora"):
        paths += ["Dockerfile." + job, ".dockerignore", "tests/docker_matrix.py", "README.md"]
    image = [os.environ.get(key) for key in ("ImageOS", "ImageVersion", "RUNNER_ARCH")]
    if not all(image):
        return None
    # Workflow revision covers the actual command even when replaying an older checkout.
    workflow = git("rev-parse", os.environ["GITHUB_SHA"] + ":.github/workflows/ci.yml").strip()
    files = git("ls-tree", "-rz", "HEAD", "--", *paths)
    return hashlib.sha256(
        b"\0".join([workflow, files, job.encode(), json.dumps(image).encode()])
    ).hexdigest()


def api(endpoint):
    return subprocess.check_output(["gh", "api", endpoint], timeout=12)


def receipt(job, key):
    repo = os.environ["GITHUB_REPOSITORY"]
    branch = os.environ["DEFAULT_BRANCH"]
    runs = json.loads(
        api(
            f"repos/{repo}/actions/workflows/ci.yml/runs?branch={branch}&event=push&status=success&per_page=10"
        )
    )
    for run in runs["workflow_runs"]:
        if run["head_repository"]["full_name"] != repo or run["head_branch"] != branch:
            continue
        name = f"evidence-{job}-{key}"
        endpoint = f"repos/{repo}/actions/runs/{run['id']}/artifacts?name={name}"
        for artifact in json.loads(api(endpoint))["artifacts"]:
            if artifact["name"] != name or artifact["expired"]:
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
