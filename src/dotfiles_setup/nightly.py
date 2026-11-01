"""Quarantine Nix input revisions and apply verified updates during a local night window."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from dotfiles_setup.errors import SetupError
from dotfiles_setup.installer import run_mutation
from dotfiles_setup.manifest import ManifestRepository, OperationJournal, _atomic_json
from dotfiles_setup.mutations import (
    FileMutation,
    capture_file_input,
    execute_mutations,
    recover_mutation,
)
from dotfiles_setup.nightly_state import (
    RunDecision,
    SchedulerPhase,
    phase_of,
    run_result,
    select_mature_revision,
)
from dotfiles_setup.nix_profile import (
    list_profile_elements,
    select_current_checkout_profile,
)
from dotfiles_setup.paths import UserPathContext

AGE_SECONDS = 7 * 24 * 60 * 60
NIX = ["nix", "--extra-experimental-features", "nix-command flakes"]


class NightlyError(SetupError):
    """An unattended update cannot proceed safely."""


def directory(environ=None) -> Path:
    return UserPathContext.from_environment(environ).state_directory / "nightly"


def read_state(path: Path) -> dict:
    if not path.exists():
        return {}
    if path.is_symlink():
        raise NightlyError(f"state must be a regular local file: {path}")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise NightlyError(f"invalid state: {path}")
    return value


def source_files(repo: Path) -> list[Path]:
    result = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=repo
    )
    return sorted({Path(os.fsdecode(name)) for name in result.split(b"\0") if name})


def owned_backups(state: dict) -> set[Path]:
    return {
        Path(name)
        for name in state.get("backups", [])
        if Path(name).parent == Path(".")
        and Path(name).name.startswith(("flake.lock.backup.", ".flake.lock.dotfiles-result."))
    }


def fingerprint(repo: Path, ignored: set[Path] | None = None) -> str:
    digest = hashlib.sha256()
    for relative in source_files(repo):
        if relative == Path("flake.lock") or relative in (ignored or set()):
            continue
        path = repo / relative
        digest.update(os.fsencode(relative) + b"\0")
        if path.is_symlink():
            digest.update(b"link:" + os.fsencode(os.readlink(path)))
        elif path.is_file():
            digest.update(path.read_bytes())
        else:
            digest.update(b"absent")
        digest.update(b"\0")
    return digest.hexdigest()


def lock_hash(repo: Path) -> str:
    return hashlib.sha256((repo / "flake.lock").read_bytes()).hexdigest()


def checkout_allowed(repo: Path, state: dict) -> bool:
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, text=True
    )
    if not status:
        return True
    return (
        state.get("repository") == str(repo)
        and state.get("source_hash") == fingerprint(repo, owned_backups(state))
        and state.get("lock_hash") == lock_hash(repo)
    )


def observe(records: list[dict], locked: dict, now: float) -> list[dict]:
    if (
        locked.get("type") != "github"
        or not re.fullmatch(r"[0-9a-f]{40}", locked.get("rev", ""))
        or not str(locked.get("narHash", "")).startswith("sha256-")
        or not isinstance(locked.get("lastModified"), int)
    ):
        raise NightlyError("Nix returned invalid GitHub revision metadata")
    for record in records:
        if not isinstance(record.get("first_seen"), (int, float)):
            raise NightlyError("invalid quarantine timestamp")
        if record["locked"]["rev"] == locked["rev"]:
            if record["locked"] != locked:
                raise NightlyError("immutable revision metadata changed")
            return records
    return [*records, {"first_seen": now, "locked": locked}][-60:]


def mature_revision(records: list[dict], now: float, current: dict) -> dict | None:
    return select_mature_revision(
        records,
        now=now,
        age_seconds=AGE_SECONDS,
        current_last_modified=current["lastModified"],
    )


def still_on_branch(owner: str, project: str, candidate: str, head: str) -> bool:
    """Reject candidates withdrawn from the currently observed branch history."""
    if candidate == head:
        return True
    url = f"https://api.github.com/repos/{owner}/{project}/compare/{candidate}...{head}"
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=20) as response:
        comparison = json.load(response)
    return (
        comparison.get("status") == "ahead"
        and comparison.get("merge_base_commit", {}).get("sha") == candidate
    )


class Commands:
    """Bound subprocess groups by wall-clock time, including across sleep/resume."""

    def __init__(self, end: float, log: Path):
        self.end = end
        self.log = log

    def remaining(self) -> float:
        remaining = self.end - time.time() - 60
        if remaining <= 0:
            raise NightlyError("night window is ending; no further work")
        return remaining

    def run(self, args: list[str], cwd: Path, *, cleanup: bool = False) -> str:
        if not cleanup:
            self.remaining()
        elif time.time() >= self.end:
            raise NightlyError("cleanup deadline reached; manual recovery is required")
        with self.log.open("a") as log:
            log.write("START " + json.dumps(args) + "\n")
        with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
            process = subprocess.Popen(
                args,
                cwd=cwd,
                stdout=output,
                stderr=errors,
                start_new_session=True,
            )
            try:
                while process.poll() is None:
                    if not cleanup:
                        self.remaining()
                    elif time.time() >= self.end:
                        raise NightlyError("cleanup deadline reached")
                    time.sleep(0.1)
            except BaseException:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                raise
            output.seek(0)
            contents = output.read().decode(errors="replace")
            errors.seek(0)
            diagnostics = errors.read().decode(errors="replace")
            with self.log.open("a") as log:
                log.write(f"COMMAND {args[0]}: exit {process.returncode}\n")
                log.write(contents + diagnostics)
            if process.returncode:
                raise NightlyError(f"{args[0]} failed; see {self.log}")
            return contents


def _copy_checkout(repo: Path, target: Path) -> None:
    for relative in source_files(repo):
        source = repo / relative
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            destination.symlink_to(os.readlink(source))
        elif source.is_file():
            shutil.copy2(source, destination)


def update(repo: Path, journal: OperationJournal, commands: Commands, state: dict) -> None:
    repo = repo.resolve()
    baseline = fingerprint(repo, owned_backups(state))
    original_hash = lock_hash(repo)
    current_input = capture_file_input(repo / "flake.lock")
    lock = json.loads((repo / "flake.lock").read_bytes())
    inputs = lock["nodes"][lock["root"]]["inputs"]
    observations = read_state(directory() / "observations.json")
    now = time.time()
    changed = False
    for node_name in inputs.values():
        if not isinstance(node_name, str):
            raise NightlyError("nightly updates require direct GitHub inputs")
        node = lock["nodes"][node_name]
        original = node["original"]
        if node.get("inputs") or original.get("type") != "github" or not original.get("ref"):
            raise NightlyError("nightly updates require GitHub branch inputs without dependencies")
        owner, project, ref = original["owner"], original["repo"], original["ref"]
        if not all(re.fullmatch(r"[A-Za-z0-9_.\-/]+", part) for part in (owner, project, ref)):
            raise NightlyError("invalid GitHub input reference")
        reference = f"github:{owner}/{project}/{ref}"
        metadata = json.loads(
            commands.run(
                [
                    *NIX,
                    "flake",
                    "metadata",
                    "--json",
                    "--refresh",
                    "--no-write-lock-file",
                    reference,
                ],
                repo,
            )
        )
        locked = metadata["locked"]
        now = time.time()
        if locked.get("owner") != owner or locked.get("repo") != project:
            raise NightlyError("Nix resolved an unexpected input repository")
        records = observations.get(reference, [])
        for record in records:
            observe([], record["locked"], record["first_seen"])
        records = observe(records, locked, now)
        observations[reference] = records
        candidate = mature_revision(records, now, node["locked"])
        if candidate is not None and still_on_branch(
            owner, project, candidate["rev"], locked["rev"]
        ):
            node["locked"] = candidate
            changed = True
    commands.remaining()
    _atomic_json(directory() / "observations.json", observations)
    if not changed:
        print("No newer input revision has completed its seven-day quarantine.")
        return

    profile = select_current_checkout_profile(list_profile_elements(), repo, active_only=True)
    if profile is None:
        raise NightlyError("install this checkout's profile before enabling nightly updates")
    with tempfile.TemporaryDirectory(prefix="dotfiles-nightly-") as temporary:
        candidate_repo = Path(temporary)
        _copy_checkout(repo, candidate_repo)
        (candidate_repo / "flake.lock").write_text(json.dumps(lock, indent=2) + "\n")
        commands.run(["git", "init", "-q"], candidate_repo)
        commands.run(["git", "add", "-A"], candidate_repo)
        commands.run(["make", "test-pre", "test-eval"], candidate_repo)
        if fingerprint(repo, owned_backups(state)) != baseline or lock_hash(repo) != original_hash:
            raise NightlyError("checkout changed while the candidate was being tested")
        commands.remaining()
        if time.time() > commands.end - 180:
            raise NightlyError("not enough night window remains to apply and verify")
        execute_mutations(
            (
                FileMutation(
                    destination=repo / "flake.lock",
                    visible_destination=repo / "flake.lock",
                    source="nightly-lock",
                    contents=(candidate_repo / "flake.lock").read_bytes(),
                    mode=0o644,
                    precondition=current_input.state,
                ),
            ),
            journal=journal,
            authority_roots=(UserPathContext.from_environment().home,),
        )
        backups = owned_backups(state)
        for raw in journal.data["entries"]:
            backup = raw.get("backup")
            if backup and Path(backup).is_relative_to(repo):
                backups.add(Path(backup).relative_to(repo))
        attempted_profile = False
        try:
            commands.remaining()
            attempted_profile = True
            commands.run(
                [*NIX, "profile", "upgrade", profile.name, "--no-write-lock-file"],
                repo,
            )
            commands.run(["./bootstrap.sh", "verify"], repo)
            if fingerprint(repo, backups) != baseline:
                raise NightlyError("checkout changed during installation; restoring prior profile")
        except BaseException:
            if attempted_profile:
                current = select_current_checkout_profile(
                    list_profile_elements(),
                    repo,
                    active_only=True,
                )
                if current is None or current.store_paths != profile.store_paths:
                    commands.run([*NIX, "profile", "rollback"], repo, cleanup=True)
            for index in reversed(range(len(journal.data["entries"]))):
                result = recover_mutation(journal.entry(index))
                if not result.recovered:
                    raise NightlyError("lock restoration needs ./bootstrap.sh recover") from None
                if result.record is not None:
                    quarantine = getattr(result.record, "result_backup", None)
                    if quarantine and quarantine.is_relative_to(repo):
                        backups.add(quarantine.relative_to(repo))
                    journal.replace_entry(index, result.record)
                journal.mark_restored(index)
            state.update(
                source_hash=baseline,
                lock_hash=lock_hash(repo),
                backups=sorted(str(path) for path in backups),
            )
            _atomic_json(directory() / "schedule.json", state)
            raise
        state.update(
            source_hash=baseline,
            lock_hash=lock_hash(repo),
            backups=sorted(str(path) for path in backups),
        )
        _atomic_json(directory() / "schedule.json", state)
        print("Installed verified updates; flake.lock is ready for review.")


_SKIP_MESSAGES = {
    RunDecision.SKIP_WINDOW: "Skipped: outside the 03:00–04:00 local update window.",
    RunDecision.SKIP_DISABLED: "Skipped: this checkout is not enabled for nightly updates.",
    RunDecision.SKIP_DIRTY: "Skipped: checkout contains changes not owned by the nightly updater.",
    RunDecision.SKIP_RECOVERY: "Skipped: interrupted setup needs recovery.",
    RunDecision.SKIP_STATE_CHANGED: (
        "Skipped: nightly configuration changed while waiting for the setup lock."
    ),
}


def _decision(repo: Path, now: datetime) -> RunDecision:
    """Return the one durable decision for this invocation.

    The order is the contract: a daytime or disabled invocation must not read
    recovery manifests or run git, so those checks come first.
    """

    if now.hour != 3:
        return RunDecision.SKIP_WINDOW
    state = read_state(directory() / "schedule.json")
    if (
        phase_of(state) is not SchedulerPhase.ENABLED
        or state.get("repository") != str(repo.resolve())
    ):
        return RunDecision.SKIP_DISABLED
    if not checkout_allowed(repo, state):
        return RunDecision.SKIP_DIRTY
    if ManifestRepository.from_environment().pending() is not None:
        return RunDecision.SKIP_RECOVERY
    return RunDecision.PROCEED


def _write_last_run(
    decision: RunDecision,
    *,
    now: datetime,
    exit_code: int,
    lock_changed: bool,
) -> None:
    _atomic_json(
        directory() / "last-run.json",
        {
            "started_at": now.isoformat(),
            "finished_at": datetime.now().astimezone().isoformat(),
            "result": run_result(decision, exit_code=exit_code, lock_changed=lock_changed),
            "exit_code": exit_code,
        },
    )


def run_nightly(repo: Path) -> int:
    now = datetime.now().astimezone()
    decision = _decision(repo, now)
    if decision is not RunDecision.PROCEED:
        _write_last_run(decision, now=now, exit_code=0, lock_changed=False)
        print(_SKIP_MESSAGES[decision])
        return 0
    end = now.replace(hour=4, minute=0, second=0, microsecond=0).timestamp()
    log = directory() / "last-run.log"
    log.write_text(f"Nightly run at {now.isoformat()}\n")
    commands = Commands(end, log)
    outcome: RunDecision | None = None

    def operation(journal: OperationJournal) -> None:
        nonlocal outcome
        fresh = read_state(directory() / "schedule.json")
        if (
            phase_of(fresh) is not SchedulerPhase.ENABLED
            or fresh.get("repository") != str(repo.resolve())
        ):
            outcome = RunDecision.SKIP_STATE_CHANGED
            print(_SKIP_MESSAGES[outcome])
            return
        if not checkout_allowed(repo, fresh):
            outcome = RunDecision.SKIP_DIRTY
            print(_SKIP_MESSAGES[outcome])
            return
        try:
            update(repo, journal, commands, fresh)
        except (NightlyError, OSError, ValueError) as error:
            if journal.pending_entries:
                raise
            journal.record_operation("nightly-update", "failed")
            journal.transition("failed")
            print(f"Nightly update did not apply: {error}")

    before = lock_hash(repo)
    code = run_mutation("nightly-update", repo, operation)
    _write_last_run(
        outcome or RunDecision.PROCEED,
        now=now,
        exit_code=code,
        lock_changed=outcome is None and lock_hash(repo) != before,
    )
    return code
