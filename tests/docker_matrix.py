from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import time
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


TARGETS = ("acceptance", "tests")


def build_command(
    case: DockerCase,
    *,
    target: str = "acceptance",
    keep: bool = False,
    cache_from: Path | None = None,
    cache_to: Path | None = None,
) -> list[str]:
    """Build one Dockerfile stage; the checks are the stage's RUN steps.

    Nothing is exported unless ``keep`` asks for the image: exporting the
    multi-gigabyte result took longer than the checks themselves.
    """

    command = [
        "docker",
        "buildx",
        "build",
        "--progress=plain",
        "-f",
        str(REPO_ROOT / case.dockerfile),
        "--target",
        target,
    ]
    if cache_from is not None:
        command += ["--cache-from", f"type=local,src={cache_from}"]
    if cache_to is not None:
        command += ["--cache-to", f"type=local,dest={cache_to},mode=max,compression=zstd"]
    command += ["--load", "-t", case.image_tag] if keep else ["--output", "type=cacheonly"]
    command.append(str(REPO_ROOT))
    return command


def build_commands(
    case: DockerCase,
    *,
    target: str = "acceptance",
    keep: bool = False,
    layer_cache: Path | None = None,
) -> list[list[str]]:
    """Return the builds for one case, seeding an empty layer cache first.

    The layer cache holds only the stages that depend on the locked inputs, so
    CI can key it on those files and reuse it when anything else changes.
    """

    if layer_cache is None:
        return [build_command(case, target=target, keep=keep)]
    commands = []
    if not layer_cache.joinpath("index.json").is_file():
        commands.append(build_command(case, target="prewarm", cache_to=layer_cache))
    commands.append(build_command(case, target=target, keep=keep, cache_from=layer_cache))
    return commands


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


def prune_cache(*, dry_run: bool) -> None:
    command = ["docker", "builder", "prune", "-f"]
    print("+", " ".join(command))
    if not dry_run:
        subprocess.run(command, cwd=REPO_ROOT, env=docker_environment(), check=True)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Ubuntu and Fedora install checks as Docker builds."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="print commands without invoking Docker"
    )
    parser.add_argument(
        "--case",
        choices=[case.name for case in CASES],
        help="run only one distro case (used by the CI matrix)",
    )
    parser.add_argument(
        "--target",
        choices=TARGETS,
        default="acceptance",
        help="acceptance: install twice, doctor, verify, smoke. tests: also the test suite",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="also load the built image as nixdotfiles:test-<distro> for debugging",
    )
    parser.add_argument(
        "--layer-cache",
        type=Path,
        default=os.environ.get("DOCKER_LAYER_CACHE") or None,
        help="directory for the locked-input layers (CI restores and saves it)",
    )
    parser.add_argument(
        "--prune-cache",
        action="store_true",
        help="also prune the global Docker build cache (affects other projects)",
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

    selected = tuple(case for case in CASES if args.case in {None, case.name})
    for case in selected:
        started = time.monotonic()
        for command in build_commands(
            case, target=args.target, keep=args.keep, layer_cache=args.layer_cache
        ):
            print("+", " ".join(command), flush=True)
            if not args.dry_run:
                run(command)
        if not args.dry_run:
            print(f"{case.name} {args.target}: passed in {time.monotonic() - started:.0f}s")
    if args.prune_cache:
        prune_cache(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
