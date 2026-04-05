#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Loop state tool — canonical JSON state for /loop-plan and /loop-work.

State path is deterministic: sha256(repo_root + goal)[:12] → /tmp/.loop-state-<hash>.json

Subcommands:
  init <goal> [items...]        Create state (fails if goal already initialized for repo)
  reset                         Delete state for this repo's current goal (disambiguates if many)
  path [--goal GOAL]            Print state file path
  read                          Print human summary of current state for this repo
  next-item                     Start a new tick: reclaim stale, return next pending "<id>\t<text>" or DONE
  append-item <text>            Add a new pending item (dedup by text)
  mark-progress <id>            Mark item in_progress
  mark-done <id>                Mark item done
  stats                         One-line stats
  list                          List active states for this repo
  cleanup [--days N]            Delete state files older than N days (default 7)
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, glob, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

STATE_GLOB = "/tmp/.loop-state-*.json"
MAX_TICKS_DEFAULT = 100
STALE_IN_PROGRESS_SECS = 30 * 60  # 30 min — reclaim as pending on next tick


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def repo_root() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return r or os.getcwd()
    except Exception:
        return os.getcwd()


def state_hash(repo: str, goal: str) -> str:
    return hashlib.sha256(f"{repo}\x00{goal}".encode()).hexdigest()[:12]


def state_path(h: str) -> Path:
    return Path(f"/tmp/.loop-state-{h}.json")


def item_id(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8]


def load(p: Path) -> dict:
    return json.loads(p.read_text())


def save(p: Path, s: dict) -> None:
    s["updated"] = now()
    p.write_text(json.dumps(s, indent=2))


def find_for_repo(repo: str) -> list[Path]:
    out = []
    for f in glob.glob(STATE_GLOB):
        try:
            s = json.loads(Path(f).read_text())
            if s.get("repo") == repo:
                out.append(Path(f))
        except Exception:
            pass
    return out


def current(repo: str) -> Path:
    matches = find_for_repo(repo)
    if not matches:
        die("No loop state for this repo. Run /loop-plan first.")
    if len(matches) > 1:
        die(f"Multiple loop states for this repo; disambiguate:\n" +
            "\n".join(f"  {m}" for m in matches))
    return matches[0]


def die(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


# ——— commands ———

def cmd_init(args: list[str]):
    if not args:
        die("usage: init <goal> [item ...]")
    goal = args[0]
    items = args[1:]
    repo = repo_root()
    h = state_hash(repo, goal)
    p = state_path(h)
    if p.exists():
        die(f"State already exists: {p}")
    state = {
        "hash": h,
        "repo": repo,
        "goal": goal,
        "created": now(),
        "updated": now(),
        "tick": 0,
        "max_ticks": MAX_TICKS_DEFAULT,
        "items": [
            {
                "id": item_id(t),
                "text": t,
                "status": "pending",
                "added_tick": 0,
                "completed_tick": None,
                "claimed_at": None,
            }
            for t in items
        ],
    }
    save(p, state)
    print(str(p))


def cmd_path(args: list[str]):
    repo = repo_root()
    if args and args[0] == "--goal" and len(args) > 1:
        print(state_path(state_hash(repo, args[1])))
        return
    print(current(repo))


def reclaim_stale(s: dict) -> int:
    """Demote stale in_progress items back to pending. Returns count reclaimed."""
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=STALE_IN_PROGRESS_SECS)
    n = 0
    for i in s["items"]:
        if i["status"] != "in_progress":
            continue
        claimed = i.get("claimed_at")
        if not claimed:
            i["status"] = "pending"
            n += 1
            continue
        try:
            if datetime.fromisoformat(claimed) < cutoff:
                i["status"] = "pending"
                i["claimed_at"] = None
                n += 1
        except Exception:
            i["status"] = "pending"
            n += 1
    return n


def cmd_read(_):
    p = current(repo_root())
    s = load(p)
    pending = [i for i in s["items"] if i["status"] == "pending"]
    progress = [i for i in s["items"] if i["status"] == "in_progress"]
    done = [i for i in s["items"] if i["status"] == "done"]
    print(f"# Loop: {s['goal']}")
    print(f"State: {p}")
    print(f"Tick: {s['tick']}/{s['max_ticks']}  "
          f"Items: {len(done)} done, {len(progress)} in-progress, {len(pending)} pending")
    print()
    if progress:
        print("## In progress")
        for i in progress:
            print(f"  [{i['id']}] ~ {i['text']}")
    if pending:
        print("## Pending")
        for i in pending[:20]:
            print(f"  [{i['id']}]   {i['text']}")
        if len(pending) > 20:
            print(f"  ... and {len(pending) - 20} more")
    if done:
        print(f"## Done ({len(done)})")
        for i in done[-5:]:
            print(f"  [{i['id']}] x {i['text']}")


def cmd_next_item(_):
    """Start a tick: reclaim stale, bump tick counter, return next pending or DONE."""
    p = current(repo_root())
    s = load(p)
    reclaimed = reclaim_stale(s)
    if s["tick"] >= s["max_ticks"]:
        save(p, s)
        print("DONE max_ticks_reached")
        return
    s["tick"] += 1
    pending = [i for i in s["items"] if i["status"] == "pending"]
    if not pending:
        save(p, s)
        print("DONE all_items_complete")
        return
    item = pending[0]
    item["status"] = "in_progress"
    item["claimed_at"] = now()
    save(p, s)
    suffix = f"\treclaimed={reclaimed}" if reclaimed else ""
    print(f"{item['id']}\t{item['text']}{suffix}")


def cmd_append_item(args: list[str]):
    if not args:
        die("usage: append-item <text>")
    text = " ".join(args).strip()
    if not text:
        die("empty item text")
    p = current(repo_root())
    s = load(p)
    iid = item_id(text)
    if any(i["id"] == iid for i in s["items"]):
        print(f"DUPLICATE {iid}")
        return
    s["items"].append({
        "id": iid,
        "text": text,
        "status": "pending",
        "added_tick": s["tick"],
        "completed_tick": None,
        "claimed_at": None,
    })
    save(p, s)
    print(f"ADDED {iid}")


def _set_status(iid: str, status: str):
    p = current(repo_root())
    s = load(p)
    for i in s["items"]:
        if i["id"] == iid:
            i["status"] = status
            if status == "done":
                i["completed_tick"] = s["tick"]
                i["claimed_at"] = None
            elif status == "in_progress":
                i["claimed_at"] = now()
            save(p, s)
            print(f"OK {iid} -> {status}")
            return
    die(f"no such item id: {iid}")


def cmd_mark_progress(args: list[str]):
    if not args: die("usage: mark-progress <id>")
    _set_status(args[0], "in_progress")


def cmd_mark_done(args: list[str]):
    if not args: die("usage: mark-done <id>")
    _set_status(args[0], "done")


def cmd_stats(_):
    p = current(repo_root())
    s = load(p)
    done = sum(1 for i in s["items"] if i["status"] == "done")
    total = len(s["items"])
    print(f"tick={s['tick']}/{s['max_ticks']} done={done}/{total} "
          f"goal={s['goal']!r} path={p}")


def cmd_reset(_):
    p = current(repo_root())
    p.unlink()
    print(f"DELETED {p}")


def cmd_cleanup(args: list[str]):
    days = 7
    if args and args[0] == "--days" and len(args) > 1:
        days = int(args[1])
    cutoff = time.time() - days * 86400
    removed = 0
    for f in glob.glob(STATE_GLOB):
        try:
            if os.path.getmtime(f) < cutoff:
                os.unlink(f)
                removed += 1
        except Exception:
            pass
    print(f"CLEANED {removed} file(s) older than {days}d")


def cmd_list(_):
    repo = repo_root()
    for p in find_for_repo(repo):
        s = load(p)
        done = sum(1 for i in s["items"] if i["status"] == "done")
        print(f"{p}\t{done}/{len(s['items'])}\t{s['goal']}")


COMMANDS = {
    "init": cmd_init,
    "reset": cmd_reset,
    "path": cmd_path,
    "read": cmd_read,
    "next-item": cmd_next_item,
    "append-item": cmd_append_item,
    "mark-progress": cmd_mark_progress,
    "mark-done": cmd_mark_done,
    "stats": cmd_stats,
    "list": cmd_list,
    "cleanup": cmd_cleanup,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) >= 2 else 1)
    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        die(f"unknown command: {cmd}\n{__doc__}")
    COMMANDS[cmd](sys.argv[2:])


if __name__ == "__main__":
    main()
