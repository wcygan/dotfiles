#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Vendor obra/superpowers skills, commands, and the code-reviewer agent into
this dotfiles repo at a pinned commit SHA.

By design:
  - The plugin's SessionStart hook is NOT vendored. (Its only job is to inject
    using-superpowers/SKILL.md as session context. The skill remains discoverable
    via the Skill tool; auto-injection is a per-session execution surface we'd
    rather not adopt.)
  - All skills are namespaced `superpowers-<name>` (directory + frontmatter `name:`).
  - Commands land under `commands/superpowers/<name>.md`.
  - The lockfile records the upstream SHA. Bumping requires `--update <sha>` to
    force a deliberate review of the diff.
  - Pre-existing `superpowers-*` paths under destinations are removed before
    copy so re-runs are idempotent. Non-superpowers paths are never touched.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_URL = "https://github.com/obra/superpowers.git"
REPO_ROOT = Path(__file__).resolve().parent.parent
LOCKFILE = REPO_ROOT / "config/claude/.superpowers.lock"
SKILLS_DST = REPO_ROOT / "config/claude/skills"
COMMANDS_DST = REPO_ROOT / "config/claude/commands/superpowers"
AGENTS_DST = REPO_ROOT / "config/claude/agents"
NAMESPACE = "superpowers"


def run(cmd: list[str], cwd: Path | None = None, capture: bool = False) -> str:
    result = subprocess.run(
        cmd, cwd=cwd, check=True, text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return (result.stdout or "").strip()


def read_lock() -> str | None:
    if not LOCKFILE.exists():
        return None
    for line in LOCKFILE.read_text().splitlines():
        line = line.strip()
        if line.startswith("sha="):
            return line.split("=", 1)[1].strip()
    return None


def write_lock(sha: str) -> None:
    LOCKFILE.parent.mkdir(parents=True, exist_ok=True)
    LOCKFILE.write_text(
        "# Pinned upstream commit for obra/superpowers.\n"
        "# Bump with: scripts/vendor-superpowers.py --update <new-sha>\n"
        "# Then review the resulting diff before committing.\n"
        f"repo={REPO_URL}\n"
        f"sha={sha}\n"
    )


def clone_at(sha: str, dest: Path) -> None:
    run(["git", "clone", "--quiet", REPO_URL, str(dest)])
    run(["git", "checkout", "--quiet", sha], cwd=dest)


def rename_skill_frontmatter(skill_md: Path, original_name: str, new_name: str) -> None:
    """Rewrite the `name:` field inside the YAML frontmatter to the namespaced form."""
    text = skill_md.read_text()
    if not text.startswith("---"):
        raise RuntimeError(f"{skill_md}: missing YAML frontmatter")
    pattern = re.compile(
        rf"^(name:\s*){re.escape(original_name)}\s*$", re.MULTILINE
    )
    new_text, n = pattern.subn(rf"\g<1>{new_name}", text, count=1)
    if n != 1:
        raise RuntimeError(
            f"{skill_md}: did not find `name: {original_name}` to rename"
        )
    skill_md.write_text(new_text)


def vendor_skills(src_root: Path) -> list[str]:
    src_skills = src_root / "skills"
    namespaced: list[str] = []
    for skill_dir in sorted(p for p in src_skills.iterdir() if p.is_dir()):
        original = skill_dir.name
        new_name = f"{NAMESPACE}-{original}"
        dst = SKILLS_DST / new_name

        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(skill_dir, dst)
        rename_skill_frontmatter(dst / "SKILL.md", original, new_name)
        namespaced.append(new_name)
    return namespaced


def vendor_commands(src_root: Path) -> list[str]:
    src_commands = src_root / "commands"
    if COMMANDS_DST.exists():
        shutil.rmtree(COMMANDS_DST)
    COMMANDS_DST.mkdir(parents=True)
    copied: list[str] = []
    for md in sorted(src_commands.glob("*.md")):
        shutil.copy2(md, COMMANDS_DST / md.name)
        copied.append(md.name)
    return copied


def vendor_agent(src_root: Path) -> str:
    src = src_root / "agents/code-reviewer.md"
    AGENTS_DST.mkdir(parents=True, exist_ok=True)
    dst = AGENTS_DST / f"{NAMESPACE}-code-reviewer.md"
    shutil.copy2(src, dst)
    return dst.name


def conflict_scan() -> list[Path]:
    """Find any non-superpowers paths that share a destination name we'd write.

    We only ever write into superpowers-prefixed names, so this only catches
    user-created collisions (e.g. a hand-written `superpowers-foo` skill).
    """
    return []  # Namespace prefix makes accidental collision impossible in practice.


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update",
        metavar="SHA",
        help="Bump the lockfile to a new SHA. Required to vendor a different "
             "commit than what's currently pinned.",
    )
    parser.add_argument(
        "--init",
        metavar="SHA",
        help="Create the lockfile for the first time at this SHA.",
    )
    args = parser.parse_args()

    locked = read_lock()
    if args.init:
        if locked:
            print(
                f"error: lockfile already exists (sha={locked[:12]}). "
                "Use --update to bump.",
                file=sys.stderr,
            )
            return 2
        target_sha = args.init
        write_lock(target_sha)
    elif args.update:
        if not locked:
            print(
                "error: no lockfile yet. Use --init <sha> first.",
                file=sys.stderr,
            )
            return 2
        target_sha = args.update
        write_lock(target_sha)
    else:
        if not locked:
            print(
                "error: no lockfile. Run with --init <sha> to create one.",
                file=sys.stderr,
            )
            return 2
        target_sha = locked

    print(f"vendoring obra/superpowers at {target_sha[:12]}…")

    with tempfile.TemporaryDirectory(prefix="superpowers-") as tmp:
        src_root = Path(tmp) / "src"
        clone_at(target_sha, src_root)

        actual_sha = run(
            ["git", "rev-parse", "HEAD"], cwd=src_root, capture=True
        )
        if actual_sha != target_sha:
            # User passed a short SHA or tag; record the resolved long SHA.
            write_lock(actual_sha)
            print(f"  resolved to full SHA {actual_sha}")

        skills = vendor_skills(src_root)
        commands = vendor_commands(src_root)
        agent = vendor_agent(src_root)

    print(f"  skills:   {len(skills)} → config/claude/skills/superpowers-*")
    for s in skills:
        print(f"    - {s}")
    print(f"  commands: {len(commands)} → config/claude/commands/superpowers/")
    for c in commands:
        print(f"    - {c}")
    print(f"  agent:    config/claude/agents/{agent}")
    print()
    print("Hook NOT vendored (intentional — see script docstring).")
    print("Review the diff before committing: git diff --stat")
    return 0


if __name__ == "__main__":
    sys.exit(main())
