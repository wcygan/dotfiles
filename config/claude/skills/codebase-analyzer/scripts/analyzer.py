#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""
Codebase improvement analyzer — accumulator state manager.

Manages structured state in /tmp/{repo-name}/improvement-analysis.json
for use with dynamic context injection in the codebase-analyzer skill.

Commands:
    init [--force]                         Bootstrap state from cwd
    read                                   Compact state summary for context injection
    next-targets [--count N]               Return N unexplored directories (default: 3)
    record-finding --file F --category C
                   --severity S --desc D
                   [--line N]              Append a finding (deduplicates)
    mark-explored DIRECTORY                Mark directory as scanned
    report                                 Generate full findings report
    stats                                  One-line progress summary
"""

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = frozenset({
    ".git", "node_modules", "__pycache__", ".direnv", ".nix-profile",
    "target", "dist", "build", ".mypy_cache", ".pytest_cache",
    "vendor", ".venv", "venv", ".tox", ".eggs", ".claude",
    ".next", "coverage", "_build", "pkg", "bin", "obj",
})

SKIP_PREFIXES = (".", "_")

CODE_EXTENSIONS = frozenset({
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java",
    ".rb", ".sh", ".fish", ".nix", ".ex", ".exs", ".kt", ".swift",
    ".c", ".cpp", ".h", ".hpp", ".cs", ".lua", ".zig",
})

MAX_DEPTH = 2
STATE_VERSION = 1


# ── Helpers ───────────────────────────────────────────────────────────


def repo_root() -> Path:
    """Find git repo root, or fall back to cwd."""
    cwd = Path.cwd()
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, cwd=cwd,
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except FileNotFoundError:
        pass
    return cwd


def repo_name() -> str:
    return repo_root().name


def state_dir() -> Path:
    p = Path(f"/tmp/{repo_name()}")
    p.mkdir(parents=True, exist_ok=True)
    return p


def state_path() -> Path:
    return state_dir() / "improvement-analysis.json"


def load_state() -> dict:
    sp = state_path()
    if sp.exists():
        try:
            with open(sp) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"status": "corrupted"}
    return {"status": "uninitialized"}


def save_state(state: dict):
    """Atomic write: write to temp file, then rename into place."""
    sp = state_path()
    sp.parent.mkdir(parents=True, exist_ok=True)
    state["updated"] = now_iso()
    fd, tmp = tempfile.mkstemp(dir=sp.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(state, f, indent=2)
        os.replace(tmp, sp)
    except Exception:
        os.unlink(tmp)
        raise


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def finding_key(file: str, line: int, desc: str) -> str:
    raw = f"{file}:{line}:{desc[:80]}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def compute_priority(rel_path: str, file_count: int, code_count: int) -> float:
    """Score 0.0-1.0. Higher = analyze sooner."""
    score = 0.0
    total = max(file_count, 1)
    code_ratio = code_count / total
    score += code_ratio * 0.4

    if file_count > 20:
        score += 0.2
    elif file_count > 5:
        score += 0.1

    important = {"src", "lib", "app", "pkg", "internal", "cmd",
                 "services", "handlers", "controllers", "models",
                 "components", "pages", "api", "core", "utils"}
    parts = set(rel_path.split("/"))
    if parts & important:
        score += 0.2

    tests = {"test", "tests", "__tests__", "spec", "specs"}
    if parts & tests:
        score += 0.1

    config = {"config", "configs", ".github", "scripts", "docs"}
    if parts & config:
        score += 0.05

    depth = rel_path.count("/")
    score -= depth * 0.05

    return max(0.0, min(1.0, round(score, 3)))


def scan_directories() -> dict[str, dict]:
    """Walk repo up to MAX_DEPTH, returning directory metadata."""
    root = repo_root()
    result = {}
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        depth = len(rel.parts)
        if depth > MAX_DEPTH:
            dirnames.clear()
            continue
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS and not d.startswith(".")
        ]
        if depth == 0:
            continue
        rel_str = str(rel)
        code_count = sum(1 for f in filenames if Path(f).suffix in CODE_EXTENSIONS)
        if not filenames:
            continue
        result[rel_str] = {
            "status": "pending",
            "file_count": len(filenames),
            "code_files": code_count,
            "priority": compute_priority(rel_str, len(filenames), code_count),
        }
    return result


# ── Commands ──────────────────────────────────────────────────────────


def cmd_init(args):
    sp = state_path()
    if sp.exists() and not args.force:
        existing = load_state()
        if existing.get("status") not in ("uninitialized", "corrupted"):
            print(f"State exists ({existing['status']}). Use --force to reset.", file=sys.stderr)
            # Still print current stats for context injection
            cmd_stats(args)
            return
    dirs = scan_directories()
    state = {
        "version": STATE_VERSION,
        "repo": repo_name(),
        "root": str(repo_root()),
        "status": "in_progress",
        "created": now_iso(),
        "updated": now_iso(),
        "iteration": 0,
        "directories": dirs,
        "findings": [],
    }
    save_state(state)
    print(f"Initialized: {len(dirs)} directories to explore in '{repo_name()}'")
    for d, info in sorted(dirs.items(), key=lambda x: -x[1]["priority"])[:5]:
        print(f"  {info['priority']:.2f}  {d} ({info['code_files']} code files)")


def cmd_read(_args):
    state = load_state()
    if state.get("status") in ("uninitialized", "corrupted"):
        print(f"Status: {state['status']}. Run `init` first.")
        return

    dirs = state.get("directories", {})
    explored = [d for d, info in dirs.items() if info["status"] == "explored"]
    pending = [d for d, info in dirs.items() if info["status"] == "pending"]
    findings = state.get("findings", [])

    print(f"## Analyzer State: {state['repo']}")
    print(f"Status: {state['status']} | Iteration: {state.get('iteration', 0)}")
    print(f"Coverage: {len(explored)}/{len(dirs)} dirs | {len(findings)} findings")
    print()

    if findings:
        by_sev = {}
        for f in findings:
            by_sev.setdefault(f["severity"], []).append(f)
        print("### Findings by Severity")
        for sev in ("critical", "high", "medium", "low"):
            if sev in by_sev:
                print(f"  {sev}: {len(by_sev[sev])}")
        print()

        by_cat = {}
        for f in findings:
            by_cat.setdefault(f["category"], []).append(f)
        print("### Findings by Category")
        for cat, items in sorted(by_cat.items(), key=lambda x: -len(x[1])):
            print(f"  {cat}: {len(items)}")
        print()

        print("### All Findings (do not re-discover these)")
        for f in findings:
            line_info = f":L{f['line']}" if f.get("line") else ""
            print(f"- [{f['severity']}] {f['file']}{line_info} — {f['description']}")
        print()

    if explored:
        print("### Explored Directories (skip these)")
        for d in sorted(explored):
            print(f"- {d}")
        print()


def cmd_next_targets(args):
    state = load_state()
    if state.get("status") != "in_progress":
        print("DONE")
        return

    dirs = state.get("directories", {})
    pending = [(d, info) for d, info in dirs.items() if info["status"] == "pending"]
    if not pending:
        state["status"] = "complete"
        save_state(state)
        print("DONE")
        return

    count = getattr(args, "count", 3) or 3
    pending.sort(key=lambda x: -x[1]["priority"])

    # Spread across different top-level directories
    selected = []
    seen_top = set()
    for d, info in pending:
        top = d.split("/")[0]
        if top not in seen_top:
            selected.append(d)
            seen_top.add(top)
        if len(selected) >= count:
            break
    # Fill remaining from highest priority
    if len(selected) < count:
        for d, info in pending:
            if d not in selected:
                selected.append(d)
            if len(selected) >= count:
                break

    for d in selected:
        info = dirs[d]
        print(f"{d} ({info['code_files']} code files, priority: {info['priority']})")


def cmd_record_finding(args):
    state = load_state()
    if state.get("status") in ("uninitialized", "corrupted"):
        print("No state. Run init first.", file=sys.stderr)
        sys.exit(1)

    key = finding_key(args.file, args.line or 0, args.desc)

    # Deduplicate
    existing_keys = {f.get("key") for f in state.get("findings", [])}
    if key in existing_keys:
        print(f"Duplicate skipped: {args.file}:{args.line or '?'}")
        return

    finding = {
        "key": key,
        "file": args.file,
        "line": args.line or 0,
        "category": args.category,
        "severity": args.severity,
        "description": args.desc,
        "iteration": state.get("iteration", 0),
        "recorded": now_iso(),
    }
    state.setdefault("findings", []).append(finding)
    save_state(state)
    print(f"Recorded [{args.severity}] {args.file}:{args.line or '?'} — {args.desc[:80]}")


def cmd_mark_explored(args):
    state = load_state()
    d = args.directory
    dirs = state.get("directories", {})
    if d in dirs:
        dirs[d]["status"] = "explored"
        state["iteration"] = state.get("iteration", 0) + 1
        save_state(state)
        remaining = sum(1 for info in dirs.values() if info["status"] == "pending")
        print(f"Explored: {d} | {remaining} directories remaining")
    else:
        print(f"Unknown directory: {d}", file=sys.stderr)


def cmd_report(_args):
    state = load_state()
    findings = state.get("findings", [])
    dirs = state.get("directories", {})
    explored = sum(1 for info in dirs.values() if info["status"] == "explored")

    print(f"# Codebase Improvement Report: {state.get('repo', '?')}")
    print(f"Generated: {now_iso()}")
    print(f"Coverage: {explored}/{len(dirs)} directories")
    print(f"Findings: {len(findings)}")
    print()

    if not findings:
        print("No findings recorded.")
        return

    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    findings_sorted = sorted(findings, key=lambda f: (
        severity_order.get(f.get("severity", "low"), 9),
        f.get("category", ""),
    ))

    current_sev = None
    for f in findings_sorted:
        sev = f["severity"].upper()
        if sev != current_sev:
            current_sev = sev
            print(f"\n## {sev}\n")
        line_info = f":{f['line']}" if f.get("line") else ""
        print(f"- **[{f['category']}]** `{f['file']}{line_info}`")
        print(f"  {f['description']}")

    print("\n## Summary by Category\n")
    cats = {}
    for f in findings:
        cats[f["category"]] = cats.get(f["category"], 0) + 1
    for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"- {cat}: {n}")

    remaining = [d for d, info in dirs.items() if info["status"] == "pending"]
    if remaining:
        print(f"\n## Unexplored ({len(remaining)} dirs remaining)\n")
        for d in sorted(remaining, key=lambda x: -dirs[x]["priority"])[:10]:
            info = dirs[d]
            print(f"- {d} ({info['code_files']} code files)")


def cmd_stats(_args):
    state = load_state()
    if state.get("status") in ("uninitialized", "corrupted"):
        print(f"Status: {state['status']}")
        return
    dirs = state.get("directories", {})
    explored = sum(1 for info in dirs.values() if info["status"] == "explored")
    n_findings = len(state.get("findings", []))
    iters = state.get("iteration", 0)
    status = state.get("status", "?")
    print(f"[{status}] {explored}/{len(dirs)} dirs | {n_findings} findings | iter {iters}")


# ── CLI ───────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Codebase analyzer state manager")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="Bootstrap state from current repo")
    p_init.add_argument("--force", action="store_true", help="Reset existing state")

    sub.add_parser("read", help="State summary for context injection")

    p_next = sub.add_parser("next-targets", help="List unexplored directories")
    p_next.add_argument("--count", type=int, default=3, help="Number of targets")

    p_rec = sub.add_parser("record-finding", help="Append a finding")
    p_rec.add_argument("--file", required=True)
    p_rec.add_argument("--line", type=int, default=0)
    p_rec.add_argument("--category", required=True)
    p_rec.add_argument("--severity", required=True, choices=["low", "medium", "high", "critical"])
    p_rec.add_argument("--desc", required=True)

    p_mark = sub.add_parser("mark-explored", help="Mark directory as scanned")
    p_mark.add_argument("directory")

    sub.add_parser("report", help="Full findings report")
    sub.add_parser("stats", help="One-line progress")

    args = parser.parse_args()
    cmds = {
        "init": cmd_init, "read": cmd_read, "next-targets": cmd_next_targets,
        "record-finding": cmd_record_finding, "mark-explored": cmd_mark_explored,
        "report": cmd_report, "stats": cmd_stats,
    }
    fn = cmds.get(args.command)
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
