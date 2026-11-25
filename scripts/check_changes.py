"""Select validation commands for an exact Git comparison."""

import argparse
import json
import os
import platform
import subprocess
from pathlib import Path

from config_checks import check_kind, selected_paths

ROOT = Path.cwd()
FULL = {"quality", "evaluation", "native", "ubuntu", "fedora", "docs", "config"}
SETUP = {"quality", "native", "ubuntu", "fedora"}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def classify(path, status):
    if Path(path).name == "CLAUDE.md":
        return FULL
    if path == "README.md" or path.startswith("docs/"):
        return {"docs"}
    if path in {"flake.nix", "flake.lock"}:
        return SETUP | {"evaluation", "config"}
    if path.startswith("src/dotfiles_setup/") or path in {
        "bootstrap.sh",
        "rust-toolchain.toml",
        "pyproject.toml",
        "uv.lock",
    }:
        return SETUP
    if path.startswith(".agents/skills/starship-config/scripts/"):
        return {"quality", "config"}
    if path == "agent-skills.lock.toml" or path.startswith(".agents/skills/"):
        return {"quality"}
    if path == "AGENTS.md":
        return {"quality", "docs"}
    if path == "tests/test_jsonc_config.py":
        return {"config", "quality"}
    if path.startswith("tests/test_") and path.endswith(".py"):
        return {"quality"}
    if path.startswith("config/") and status == "M":
        if path.startswith("config/fish/") or path == "config/shell-nix.sh":
            return {"shell", "ubuntu", "fedora"}
        if path == "config/git/config":
            return SETUP | {"config"}
        if check_kind(path):
            return {"config"}
    if path in {"Dockerfile.ubuntu", "Dockerfile.fedora"}:
        return {"quality", path.split(".")[1]}
    return FULL


def plan(base, head=None):
    selected = {}
    try:
        if not base:
            return {"base": None, "checks": {check: ["comparison unavailable"] for check in FULL}}
        if head:
            head = (
                git("rev-parse", "--verify", "--end-of-options", head + "^{commit}")
                .decode()
                .strip()
            )
        base = git("rev-parse", "--verify", "--end-of-options", base + "^{commit}").decode().strip()
        args = ["diff", "--no-renames", "--name-status", "-z", base]
        if head:
            args.append(head)
        fields = git(*args, "--").split(b"\0")[:-1]
        changes = [
            (os.fsdecode(fields[i + 1]), os.fsdecode(fields[i])) for i in range(0, len(fields), 2)
        ]
        if not head:
            # Include staged edits even when an unstaged edit cancels their net diff.
            staged = git("diff", "--cached", "--no-renames", "--name-status", "-z", base, "--")
            fields = staged.split(b"\0")[:-1]
            changes.extend(
                (os.fsdecode(fields[i + 1]), os.fsdecode(fields[i]))
                for i in range(0, len(fields), 2)
            )
            changes.extend(
                (os.fsdecode(p), "A")
                for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
                if p
            )
        for path, status in sorted(set(changes)):
            for check in classify(path, status):
                selected.setdefault(check, []).append(path)
    except subprocess.CalledProcessError:
        selected = {check: ["comparison unavailable"] for check in FULL}
    return {"base": base, "checks": selected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if args.run and args.head is not None:
        parser.error("--run validates the working tree; use --head only to print a plan")
    base = args.base
    if base is None:
        try:
            base = git("merge-base", "HEAD", "origin/main").decode().strip()
        except subprocess.CalledProcessError:
            base = ""
    result = plan(base, args.head)
    print(json.dumps(result, sort_keys=True, indent=2), flush=True)
    if args.run:
        commands = {
            "quality": ["make", "test-syntax", "test-pre"],
            "shell": ["make", "test-syntax", "test-shell"],
            "config": ["./bootstrap.sh", "--run", "python3", "scripts/config_checks.py"],
            "evaluation": ["make", "test-eval"],
            "docs": ["make", "docs-build"],
            "native": ["make", "test-macos"]
            if platform.system() == "Darwin"
            else ["make", "test-linux", "DOCKER_CASE=ubuntu"],
            "ubuntu": ["make", "test-docker", "DOCKER_CASE=ubuntu"],
            "fedora": ["make", "test-docker", "DOCKER_CASE=fedora"],
        }
        if platform.system() == "Darwin" and "quality" in result["checks"]:
            commands["native"] = ["python3", "tests/macos_e2e.py", "--skip-tests"]
        elif platform.system() == "Linux" and "native" in result["checks"]:
            # test-linux builds Ubuntu's tests stage on top of its acceptance stage.
            commands.pop("ubuntu")
        if "quality" in result["checks"]:
            # Locked pytest includes both shell-specific test modules.
            commands.pop("shell")
        for check, command in commands.items():
            if check in result["checks"]:
                env = dict(os.environ)
                if check == "config":
                    env["DOTFILES_DEV_SHELL"] = "config-checks"
                    subprocess.run(
                        [
                            "./bootstrap.sh",
                            "--run",
                            "python3",
                            "-m",
                            "unittest",
                            "tests.test_jsonc_config",
                        ],
                        cwd=ROOT,
                        env=env,
                        check=True,
                    )
                    reasons = result["checks"][check]
                    command.extend(selected_paths(reasons))
                subprocess.run(command, cwd=ROOT, env=env, check=True)


if __name__ == "__main__":
    main()
