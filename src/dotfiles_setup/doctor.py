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


Check = Callable[[], CheckResult]


def command_check(command: str) -> Check:
    def check() -> CheckResult:
        path = shutil.which(command)
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


def default_checks(home: Path | None = None) -> list[Check]:
    resolved_home = home or Path.home()
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", resolved_home / ".config"))
    return [
        command_check("nix"),
        command_check("python3"),
        command_check("uv"),
        command_check("fish"),
        command_check("direnv"),
        command_check("starship"),
        path_check("nix-store", Path("/nix")),
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
        marker = "PASS" if result.passed else "WARN"
        output(f"[{marker}] {result.message}")

    return 0
