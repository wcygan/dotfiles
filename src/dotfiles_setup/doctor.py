from __future__ import annotations

import os
import platform
import shutil
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from dotfiles_setup.paths import UserPathContext


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    message: str


Check = Callable[[], CheckResult]


def command_check(command: str, environment: Mapping[str, str]) -> Check:
    def check() -> CheckResult:
        path = shutil.which(command, path=environment.get("PATH", ""))
        if path is None:
            return CheckResult(command, False, f"{command} is not available")
        return CheckResult(command, True, f"{command} is available at {path}")

    return check


def path_check(name: str, path: Path) -> Check:
    def check() -> CheckResult:
        if path.exists():
            return CheckResult(name, True, f"{path} exists")
        return CheckResult(name, False, f"{path} does not exist")

    return check


def default_checks(
    home: Path | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
) -> list[Check]:
    context = UserPathContext.from_environment(environ, home=home, system=system)
    values = os.environ if environ is None else environ
    return [
        command_check("nix", values),
        command_check("python3", values),
        command_check("uv", values),
        command_check("fish", values),
        command_check("direnv", values),
        command_check("starship", values),
        path_check("nix-store", Path("/nix")),
        path_check("fish-config", context.config_home / "fish"),
    ]


def evaluate_checks(checks: Iterable[Check]) -> list[CheckResult]:
    check_list = list(checks)
    with ThreadPoolExecutor(max_workers=max(1, len(check_list))) as executor:
        return list(executor.map(lambda check: check(), check_list))


def run_doctor(
    *,
    checks: Iterable[Check] | None = None,
    output: Callable[[str], None] = print,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
) -> int:
    values = os.environ if environ is None else environ
    context = UserPathContext.from_environment(values, system=system)
    output(f"System: {context.platform} {platform.machine()}")
    output(f"Shell: {values.get('SHELL', '(unknown)')}")

    results = evaluate_checks(
        checks or default_checks(environ=values, system=context.platform)
    )
    for result in results:
        marker = "PASS" if result.passed else "WARN"
        output(f"[{marker}] {result.message}")

    return 0
