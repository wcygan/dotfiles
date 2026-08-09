from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DockerCase:
    name: str
    dockerfile: str

    @property
    def image_tag(self) -> str:
        return f"nixdotfiles:test-{self.name}"


CASES = (
    DockerCase("ubuntu", "Dockerfile.ubuntu"),
    DockerCase("fedora", "Dockerfile.fedora"),
)


def build_command(case: DockerCase) -> list[str]:
    return [
        "docker",
        "build",
        "-f",
        str(REPO_ROOT / case.dockerfile),
        "-t",
        case.image_tag,
        str(REPO_ROOT),
    ]


def smoke_command(case: DockerCase) -> list[str]:
    check = " && ".join(
        (
            "set -eu",
            'test "$(id -un)" = tester',
            "test -d /home/tester/app",
            "test -f config/fish/config.fish",
            "test -f config/fish/conf.d/10-nix.fish",
            "test -x bootstrap.sh",
            "bash -n bootstrap.sh",
            "command -v curl",
            "command -v git",
            "command -v make",
        )
    )
    return [
        "docker",
        "run",
        "--rm",
        "-e",
        f"TERM={os.environ.get('TERM', 'xterm-256color')}",
        case.image_tag,
        "/bin/bash",
        "-lc",
        check,
    ]


def docker_environment(
    *,
    environ: dict[str, str] | None = None,
    system: str | None = None,
) -> dict[str, str]:
    environment = dict(os.environ if environ is None else environ)
    if (system or platform.system()) == "Darwin":
        host_helper_paths = ("/usr/local/bin", "/opt/homebrew/bin")
        existing_paths = [path for path in host_helper_paths if Path(path).is_dir()]
        environment["PATH"] = os.pathsep.join([*existing_paths, environment.get("PATH", "")])
    return environment


def run(command: Sequence[str]) -> None:
    subprocess.run(command, cwd=REPO_ROOT, env=docker_environment(), check=True)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and smoke-test Ubuntu and Fedora test images."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="print commands without invoking Docker"
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.dry_run and shutil.which("docker") is None:
        print(
            "Docker is required for the container matrix. "
            "Re-run with --dry-run to inspect commands."
        )
        return 2

    for case in CASES:
        commands = (build_command(case), smoke_command(case))
        for command in commands:
            print("+", " ".join(command))
            if not args.dry_run:
                run(command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
