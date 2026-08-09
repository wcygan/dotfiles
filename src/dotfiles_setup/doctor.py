from __future__ import annotations

import os
import platform
import shutil
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    message: str
    required: bool = False


Check = Callable[[], CheckResult]


def command_check(command: str, *, required: bool) -> Check:
    def check() -> CheckResult:
        path = shutil.which(command)
        if path is None:
            return CheckResult(command, False, f"{command} is not available", required)
        return CheckResult(command, True, f"{command} is available at {path}", required)

    return check


def path_check(name: str, path: Path, *, required: bool = False) -> Check:
    def check() -> CheckResult:
        if path.exists():
            return CheckResult(name, True, f"{path} exists", required)
        return CheckResult(name, False, f"{path} does not exist", required)

    return check


def default_checks(home: Path | None = None) -> list[Check]:
    resolved_home = home or Path.home()
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", resolved_home / ".config"))
    return [
        command_check("nix", required=True),
        command_check("python3", required=True),
        command_check("uv", required=True),
        command_check("fish", required=False),
        command_check("direnv", required=False),
        command_check("starship", required=False),
        path_check("nix-store", Path("/nix"), required=True),
        path_check("fish-config", config_home / "fish"),
    ]


def evaluate_checks(checks: Iterable[Check]) -> list[CheckResult]:
    check_list = list(checks)
    with ThreadPoolExecutor(max_workers=max(1, len(check_list))) as executor:
        return list(executor.map(lambda check: check(), check_list))


def run_doctor(
    *,
    checks: Iterable[Check] | None = None,
    output: Callable[[str], None] = print,
) -> int:
    output(f"System: {platform.system()} {platform.machine()}")
    output(f"Shell: {os.environ.get('SHELL', '(unknown)')}")

    results = evaluate_checks(checks or default_checks())
    for result in results:
        if result.passed:
            marker = "PASS"
        elif result.required:
            marker = "FAIL"
        else:
            marker = "WARN"
        output(f"[{marker}] {result.message}")

    return 1 if any(not result.passed and result.required for result in results) else 0
