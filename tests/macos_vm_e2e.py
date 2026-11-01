"""Run the macOS acceptance flow in an ephemeral Tart VM.

The VM is cloned from a base image, the checkout is copied in, Nix is installed
if absent, and the setup runs twice before doctor and verify. The VM is deleted
afterward unless --keep is passed.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Sequence
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SHARE_NAME = "dotfiles"
SHARE_PATH = "/Volumes/My Shared Files/dotfiles"
DEFAULT_BASE = "tahoe-base"
EXCLUDES = (
    ".git",
    ".jj",
    ".venv",
    ".direnv",
    ".pytest_cache",
    ".ruff_cache",
    ".ropeproject",
    "docs/node_modules",
)
NIX_INSTALL = (
    'curl --proto "=https" --tlsv1.2 -sSf -L '
    "https://install.determinate.systems/nix | sh -s -- install --no-confirm"
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default=DEFAULT_BASE,
        help=f"Tart image to clone (default: {DEFAULT_BASE})",
    )
    parser.add_argument("--keep", action="store_true", help="keep the VM running")
    parser.add_argument(
        "--with-tests",
        action="store_true",
        help="also run make test-syntax and make test-pre in the VM",
    )
    return parser.parse_args(argv)


def run(
    command: Sequence[str],
    *,
    check: bool = True,
    timeout: int | None = None,
    capture: bool = False,
    quiet: bool = False,
) -> subprocess.CompletedProcess[str]:
    if not quiet:
        print("+", " ".join(command), flush=True)
    return subprocess.run(
        command,
        check=check,
        text=True,
        timeout=timeout,
        capture_output=capture,
    )


def guest(
    vm: str,
    script: str,
    *,
    check: bool = True,
    quiet: bool = False,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    return run(
        ["tart", "exec", vm, "/bin/bash", "-lc", script],
        check=check,
        quiet=quiet,
        timeout=timeout,
    )


def wait_for_ip(
    vm: str,
    runner: subprocess.Popen[str] | None = None,
    timeout: int = 240,
) -> str:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if runner is not None and runner.poll() is not None:
            raise RuntimeError(f"tart run exited with status {runner.returncode}")
        result = run(["tart", "ip", vm], check=False, capture=True, quiet=True)
        address = result.stdout.strip()
        if result.returncode == 0 and address:
            return address
        time.sleep(2)
    raise RuntimeError(f"{vm} did not report an IP address")


def wait_for_agent(vm: str, timeout: int = 240) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if guest(vm, "true", check=False, quiet=True).returncode == 0:
            return
        time.sleep(2)
    raise RuntimeError(f"{vm} guest agent did not become reachable")


def copy_checkout(vm: str) -> None:
    excludes = " ".join(f"--exclude={item}" for item in EXCLUDES)
    guest(
        vm,
        "rm -rf ~/dotfiles && mkdir -p ~/dotfiles && "
        f"COPYFILE_DISABLE=1 tar -C '{SHARE_PATH}' {excludes} -cf - . | "
        "tar -C ~/dotfiles -xf -",
    )


def ensure_nix(vm: str) -> None:
    guest(
        vm,
        "if [ ! -x /nix/var/nix/profiles/default/bin/nix ]; then "
        f"{NIX_INSTALL}; fi",
    )


def vm_exists(vm: str) -> bool:
    """Return whether Tart still lists the VM."""

    result = subprocess.run(
        ["tart", "list", "--format", "json"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return True
    try:
        entries = json.loads(result.stdout)
    except json.JSONDecodeError:
        return True
    return any(
        isinstance(entry, dict) and entry.get("Name") == vm for entry in entries
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        print("macOS VM acceptance requires Apple Silicon macOS.", file=sys.stderr)
        return 2
    if shutil.which("tart") is None:
        print("Tart is required: brew install cirruslabs/cli/tart", file=sys.stderr)
        return 2

    vm = f"dotfiles-e2e-{int(time.time())}"
    clone = run(["tart", "clone", args.base, vm], check=False)
    if clone.returncode != 0:
        print(
            f"cannot clone {args.base!r}; pass --base with a local or OCI image",
            file=sys.stderr,
        )
        return 2

    log_path = Path(tempfile.gettempdir()) / f"{vm}-tart.log"
    log = None
    runner = None
    success = False
    cleanup_failed = False
    try:
        log = log_path.open("w")
        runner = subprocess.Popen(  # noqa: S603 - tart is the intended executable
            [
                "tart",
                "run",
                "--no-graphics",
                f"--dir={SHARE_NAME}:{REPO_ROOT}",
                vm,
            ],
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        print(f"vm: {vm} (log: {log_path})", flush=True)
        wait_for_ip(vm, runner)
        wait_for_agent(vm)
        copy_checkout(vm)
        ensure_nix(vm)
        guest(vm, "cd ~/dotfiles && ./bootstrap.sh install", timeout=3600)
        guest(vm, "cd ~/dotfiles && ./bootstrap.sh install", timeout=3600)
        guest(vm, "cd ~/dotfiles && ./bootstrap.sh doctor", timeout=600)
        guest(vm, "cd ~/dotfiles && ./bootstrap.sh verify", timeout=600)
        if args.with_tests:
            guest(vm, "cd ~/dotfiles && make test-syntax && make test-pre", timeout=3600)
        success = True
    finally:
        if log is not None:
            log.close()
        if args.keep:
            print(f"kept VM: {vm}")
            print(f"stop with: tart stop {vm} && tart delete {vm}")
        else:
            if runner is not None:
                runner.terminate()
                try:
                    runner.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    runner.kill()
            run(["tart", "stop", vm], check=False, timeout=180, capture=True, quiet=True)
            run(["tart", "delete", vm], check=False, timeout=120, capture=True, quiet=True)
            if vm_exists(vm):
                print(
                    f"cleanup failed: {vm} still exists; run tart delete {vm}",
                    file=sys.stderr,
                )
                cleanup_failed = True
            elif success:
                log_path.unlink(missing_ok=True)
    if cleanup_failed:
        return 1
    print("macOS Tart acceptance passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
