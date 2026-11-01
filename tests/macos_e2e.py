"""Run the macOS acceptance flow locally in an isolated HOME tree.

This mirrors .github/workflows/macos.yml: the installer writes only under a
temporary HOME/XDG/CODEX/RUSTUP/CARGO tree, so the host's real configuration
and Nix profile are untouched.
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep", action="store_true", help="keep the isolated tree")
    parser.add_argument(
        "--reuse-rustup",
        action="store_true",
        help="reuse the host RUSTUP_HOME/CARGO_HOME instead of downloading",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="skip make test-syntax and make test-pre",
    )
    return parser.parse_args(argv)


def isolated_environment(root: Path, *, reuse_rustup: bool) -> dict[str, str]:
    environment = dict(os.environ)
    if reuse_rustup:
        environment.setdefault(
            "RUSTUP_HOME", str(Path(environment.get("HOME", "~")).expanduser() / ".rustup")
        )
        environment.setdefault(
            "CARGO_HOME", str(Path(environment.get("HOME", "~")).expanduser() / ".cargo")
        )
    home = root / "home"
    environment.update(
        HOME=str(home),
        XDG_CONFIG_HOME=str(home / ".config"),
        XDG_CACHE_HOME=str(home / ".cache"),
        XDG_STATE_HOME=str(home / ".local/state"),
        CODEX_HOME=str(home / ".codex"),
        DOTFILES_SKIP_FISH_GREETING="1",
    )
    if not reuse_rustup:
        environment["RUSTUP_HOME"] = str(home / ".rustup")
        environment["CARGO_HOME"] = str(home / ".cargo")
    home.mkdir(parents=True, exist_ok=True)
    return environment


def run(command: Sequence[str], *, environment: dict[str, str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=REPO_ROOT, env=environment, check=True)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if platform.system() != "Darwin":
        print("macOS acceptance only runs on macOS.", file=sys.stderr)
        return 2
    root = Path(tempfile.mkdtemp(prefix="dotfiles-macos-e2e-"))
    environment = isolated_environment(root, reuse_rustup=args.reuse_rustup)
    print(f"isolated home: {environment['HOME']}", flush=True)
    try:
        if not args.skip_tests:
            run(["make", "test-syntax"], environment=environment)
            run(["make", "test-pre"], environment=environment)
        run(["./bootstrap.sh", "install"], environment=environment)
        run(["./bootstrap.sh", "install"], environment=environment)
        run(["./bootstrap.sh", "doctor"], environment=environment)
        run(["./bootstrap.sh", "verify"], environment=environment)
        run(
            ["git", "diff", "--exit-code", "--", "flake.lock", "uv.lock", "agent-skills.lock.toml"],
            environment=environment,
        )
    finally:
        if args.keep:
            print(f"kept isolated tree: {root}")
        else:
            shutil.rmtree(root)
    print("macOS isolated acceptance passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
