#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Gold-standard quality gate for uv standalone scripts.

Run:
    uv run --script script_quality_gate.py config/claude/skills/uv-scripts/scripts
    uv run --script script_quality_gate.py config/claude/skills/uv-scripts/scripts --run-help --ruff
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*=\s*['\"][^'\"]+['\"]"),
    re.compile(r"(?i)bearer\s+[a-z0-9._~+/=-]{16,}"),
]
MACHINE_PATH_SENTINELS = ["/" + "Users/"]


@dataclass(frozen=True)
class Finding:
    path: Path
    severity: str
    message: str


def iter_scripts(paths: list[Path]) -> list[Path]:
    scripts: list[Path] = []
    for path in paths:
        if path.is_dir():
            scripts.extend(
                sorted(child for child in path.glob("*.py") if child.is_file())
            )
        elif path.suffix == ".py":
            scripts.append(path)
    return sorted(set(scripts))


def has_inline_metadata(text: str) -> bool:
    return "# /// script" in text and "# ///" in text


def check_script(path: Path) -> list[Finding]:
    text = path.read_text()
    findings: list[Finding] = []

    if not text.startswith("#!/usr/bin/env -S uv run --script"):
        findings.append(Finding(path, "error", "missing uv shebang"))
    if not has_inline_metadata(text):
        findings.append(
            Finding(path, "error", "missing PEP 723 inline script metadata")
        )
    if "requires-python" not in text:
        findings.append(Finding(path, "error", "missing requires-python"))
    if "dependencies = [" not in text and "dependencies = []" not in text:
        findings.append(Finding(path, "error", "missing dependencies field"))
    if "def main(" not in text:
        findings.append(Finding(path, "error", "missing main(argv) function"))
    if "raise SystemExit(main())" not in text:
        findings.append(Finding(path, "error", "missing raise SystemExit(main())"))
    for sentinel in MACHINE_PATH_SENTINELS:
        if sentinel in text:
            findings.append(
                Finding(
                    path,
                    "error",
                    f"contains machine-specific path sentinel: {sentinel}",
                )
            )

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(Finding(path, "error", "possible hard-coded secret"))

    return findings


def run_help(path: Path) -> Finding | None:
    command = ["uv", "run", "--script", str(path), "--help"]
    result = subprocess.run(
        command, text=True, capture_output=True, timeout=30, check=False
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        message = detail[-1] if detail else "help command failed"
        return Finding(path, "error", f"--help failed: {message}")
    return None


def run_ruff(paths: list[Path]) -> list[Finding]:
    if not paths:
        return []
    command = [
        "uv",
        "run",
        "--with",
        "ruff",
        "--no-project",
        "ruff",
        "check",
        *[str(path) for path in paths],
    ]
    result = subprocess.run(
        command, text=True, capture_output=True, timeout=60, check=False
    )
    if result.returncode == 0:
        return []
    message = (result.stdout or result.stderr).strip().splitlines()
    return [
        Finding(
            Path("."),
            "error",
            f"ruff failed: {message[-1] if message else 'no output'}",
        )
    ]


def print_findings(findings: list[Finding]) -> None:
    for finding in findings:
        print(f"{finding.severity.upper()}: {finding.path}: {finding.message}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check uv standalone scripts against the minimum bar."
    )
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--run-help", action="store_true", help="Run each script with --help."
    )
    parser.add_argument("--ruff", action="store_true", help="Run ruff check via uv.")
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> int:
    scripts = iter_scripts(args.paths)
    if not scripts:
        print("ERROR: no Python scripts found", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    for script in scripts:
        findings.extend(check_script(script))
        if args.run_help:
            help_finding = run_help(script)
            if help_finding is not None:
                findings.append(help_finding)

    if args.ruff:
        findings.extend(run_ruff(scripts))

    if findings:
        print_findings(findings)
        return 1

    print(f"OK: {len(scripts)} script(s) passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except subprocess.TimeoutExpired as exc:
        print(f"ERROR: command timed out: {exc.cmd}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("ERROR: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
