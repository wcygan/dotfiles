"""Own mutating setup workflows, journals, locks, and terminal states."""

from __future__ import annotations

import os
import re
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from dotfiles_setup.links import link_config
from dotfiles_setup.locking import mutation_lock
from dotfiles_setup.manifest import OperationJournal
from dotfiles_setup.nix_profile import ensure_profile
from dotfiles_setup.paths import UserPathContext
from dotfiles_setup.recovery import run_recovery
from dotfiles_setup.rustup import setup_rustup
from dotfiles_setup.shell_handoff import configure_shell_handoff
from dotfiles_setup.verify import run_verify

JournalOperation = Callable[[OperationJournal], object]
Operation = Callable[[], object]
Output = Callable[[str], None]

_TERMINAL_FAILURE_STATES = {"failed", "recovery-needed"}
_BOOTSTRAP_STARTED_AT = "DOTFILES_BOOTSTRAP_STARTED_AT"
_LONGEST_PLAUSIBLE_STARTUP_SECONDS = 24 * 60 * 60


@dataclass(frozen=True)
class OperationResult:
    """Describe one workflow operation result."""

    name: str
    succeeded: bool
    detail: str
    skipped: bool = False
    seconds: float | None = None


def _run_operation(name: str, operation: Operation) -> OperationResult:
    started = time.monotonic()
    try:
        result = operation()
    except Exception as error:  # noqa: BLE001 - workflow boundary records operation failures
        return OperationResult(name, False, str(error), seconds=time.monotonic() - started)
    detail = str(result) if result is not None else "complete"
    return OperationResult(name, True, detail, seconds=time.monotonic() - started)


def _report(result: OperationResult, output: Output) -> None:
    marker = "SKIP" if result.skipped else "PASS" if result.succeeded else "FAIL"
    output(f"[{marker}] {result.name}: {result.detail}")


def _record_result(journal: OperationJournal, result: OperationResult) -> None:
    status = "skipped" if result.skipped else "completed" if result.succeeded else "failed"
    duration_ms = None if result.seconds is None else _duration_ms(result.seconds)
    journal.record_operation(result.name, status, duration_ms=duration_ms)


def _duration_ms(seconds: float) -> int:
    return round(seconds * 1000)


def _startup_seconds(environ: Mapping[str, str]) -> float | None:
    """Return the time since bootstrap.sh started, when its clock was sub-second.

    A whole-second start time is up to a second early, which is longer than a
    normal startup, so it is not reported. A `date` without `%N` leaves a
    fraction that is not a number and lands here too.
    """

    raw = environ.get(_BOOTSTRAP_STARTED_AT, "")
    if not re.fullmatch(r"[0-9]+[.,][0-9]+", raw):
        return None
    elapsed = time.time() - float(raw.replace(",", "."))
    if not 0 <= elapsed < _LONGEST_PLAUSIBLE_STARTUP_SECONDS:
        return None
    return elapsed


def _timing_summary(
    results: list[OperationResult],
    startup: float | None,
    workflow_seconds: float,
) -> str:
    """Render where one install spent its time."""

    parts: list[str] = []
    total = workflow_seconds
    if startup is not None:
        total += startup
        parts.append(f"startup {startup:.1f}s")
    parts.extend(
        f"{result.name} {result.seconds:.1f}s"
        for result in results
        if result.seconds is not None
    )
    return f"Install took {total:.1f}s: {', '.join(parts)}"


def _checkpoint_failure(
    journal: OperationJournal,
    *,
    operation_name: str | None = None,
    duration_ms: int | None = None,
) -> tuple[str, ...]:
    """Persist one failure checkpoint and return each checkpoint error."""

    errors: list[str] = []
    if operation_name is not None:
        try:
            journal.record_operation(operation_name, "failed", duration_ms=duration_ms)
        except Exception as error:  # noqa: BLE001 - report every journal failure
            errors.append(f"could not record {operation_name} failure: {error}")

    try:
        current_state = journal.state
    except Exception as error:  # noqa: BLE001 - attempt a safe terminal checkpoint
        errors.append(f"could not read the journal state: {error}")
        current_state = "recovery-needed"
    terminal_state = (
        current_state if current_state in _TERMINAL_FAILURE_STATES else "recovery-needed"
    )
    try:
        journal.transition(terminal_state)
    except Exception as error:  # noqa: BLE001 - report every journal failure
        errors.append(f"could not write the {terminal_state} state: {error}")
    return tuple(errors)


def _failure_message(
    prefix: str,
    error: Exception,
    journal_errors: tuple[str, ...],
    *,
    lock_error: Exception | None = None,
) -> str:
    message = f"{prefix}: {error}"
    if journal_errors:
        message += "; journal checkpoint failed: " + "; ".join(journal_errors)
    if lock_error is not None:
        message += f"; mutation lock release failed: {lock_error}"
    return message


def _run_verification(
    repo_root: Path,
    *,
    environ: Mapping[str, str],
    output: Output,
) -> tuple[OperationResult, int]:
    started = time.monotonic()
    try:
        exit_code = run_verify(repo_root, environ=environ, output=output)
    except Exception as error:  # noqa: BLE001 - verification boundary records failures
        result = OperationResult("verify", False, str(error), seconds=time.monotonic() - started)
        _report(result, output)
        return result, 1
    detail = "complete" if exit_code == 0 else f"exit {exit_code}"
    seconds = time.monotonic() - started
    return OperationResult("verify", exit_code == 0, detail, seconds=seconds), exit_code


def run_mutation(
    command: str,
    repo_root: Path,
    operation: JournalOperation,
    *,
    environ: Mapping[str, str] | None = None,
    output: Output = print,
) -> int:
    """Run one direct mutation under one lock and durable journal.

    The journal's entry for the command records how long the operation took.
    """

    values = os.environ if environ is None else environ
    started = time.monotonic()
    journal: OperationJournal | None = None
    primary_error: Exception | None = None
    journal_errors: tuple[str, ...] = ()
    lock_error: Exception | None = None
    exit_code = 1
    try:
        with mutation_lock(command, environ=values):
            try:
                journal = OperationJournal(command, repo_root, environ=values)
                journal.transition("applying")
                operation(journal)
                if journal.state not in _TERMINAL_FAILURE_STATES:
                    journal.record_operation(
                        command,
                        "completed",
                        duration_ms=_duration_ms(time.monotonic() - started),
                    )
                    journal.transition("completed")
                exit_code = 1 if journal.state in _TERMINAL_FAILURE_STATES else 0
            except Exception as error:  # noqa: BLE001 - checkpoint before lock release
                primary_error = error
                if journal is not None:
                    journal_errors = _checkpoint_failure(
                        journal,
                        operation_name=command,
                        duration_ms=_duration_ms(time.monotonic() - started),
                    )
    except Exception as error:  # noqa: BLE001 - command boundary converts failures to exit codes
        if primary_error is None:
            primary_error = error
        else:
            lock_error = error

    if primary_error is not None:
        output(
            _failure_message(
                f"{command} failed",
                primary_error,
                journal_errors,
                lock_error=lock_error,
            )
        )
        return 1
    return exit_code


def _install_results(
    repo_root: Path,
    journal: OperationJournal,
    *,
    shell_handoff: bool,
    environ: Mapping[str, str],
    output: Output,
) -> tuple[list[OperationResult], int]:
    results: list[OperationResult] = []
    context = UserPathContext.from_environment(environ)
    from dotfiles_setup.nightly import directory, read_state

    schedule_state = read_state(directory(environ) / "schedule.json")
    schedule_requested = bool(
        schedule_state.get("requested_enabled", schedule_state.get("enabled"))
    )

    def add(result: OperationResult, *, report: bool = True) -> None:
        results.append(result)
        if report:
            _report(result, output)
        _record_result(journal, result)

    def install_links() -> None:
        link_config(
            repo_root,
            environ=environ,
            output=lambda line: output(f"[links] {line}"),
            journal=journal,
        )

    operations: list[tuple[str, Operation]] = [
        ("profile", lambda: ensure_profile(repo_root, environment=environ, skip_when_current=True)),
        ("links", install_links),
        ("rustup", lambda: setup_rustup(repo_root, environment=environ, skip_when_current=True)),
    ]
    if shell_handoff:
        operations.append(("shell-handoff", lambda: configure_shell_handoff(
            home=context.home, shell=environ.get("SHELL", ""), journal=journal
        )))
    if schedule_requested:
        from dotfiles_setup.nightly_schedule import configure

        operations.append(("nightly-schedule", lambda: configure(
            repo_root, journal, enabled=True, environ=environ
        )))

    failed = None
    for name, operation in operations:
        if failed is None:
            result = _run_operation(name, operation)
            if not result.succeeded:
                failed = name
        else:
            reason = "required setup failed"
            if failed == "profile" or (failed == "links" and name == "rustup"):
                reason = f"{failed} failed"
            elif name == "shell-handoff":
                reason = "required setup operation failed"
            result = OperationResult(name, False, reason, skipped=True)
        add(result)

    verification, verification_exit = _run_verification(repo_root, environ=environ, output=output)
    add(verification, report=False)
    if failed == "profile" and verification_exit:
        return results, verification_exit
    return results, int(failed is not None or not verification.succeeded)


def run_install(
    repo_root: Path,
    *,
    shell_handoff: bool = False,
    environ: Mapping[str, str] | None = None,
    output: Output = print,
) -> int:
    """Run the production install workflow under one lock and journal."""

    values = os.environ if environ is None else environ
    startup = _startup_seconds(values)
    started = time.monotonic()
    journal: OperationJournal | None = None
    primary_error: Exception | None = None
    journal_errors: tuple[str, ...] = ()
    lock_error: Exception | None = None
    exit_code = 1
    try:
        with mutation_lock("install", environ=values):
            try:
                journal = OperationJournal("install", repo_root, environ=values)
                journal.transition("applying")
                results, exit_code = _install_results(
                    repo_root,
                    journal,
                    shell_handoff=shell_handoff,
                    environ=values,
                    output=output,
                )
                output(_timing_summary(results, startup, time.monotonic() - started))
                if journal.state not in _TERMINAL_FAILURE_STATES:
                    mutation_failed = any(
                        not result.succeeded
                        and not result.skipped
                        and result.name != "verify"
                        for result in results
                    )
                    verify_failed = any(
                        result.name == "verify" and not result.succeeded for result in results
                    )
                    if mutation_failed:
                        journal.transition("recovery-needed")
                    elif verify_failed:
                        journal.transition("failed")
                    else:
                        journal.transition("completed")
                if journal.state in _TERMINAL_FAILURE_STATES:
                    exit_code = 1 if exit_code == 0 else exit_code
            except Exception as error:  # noqa: BLE001 - checkpoint before lock release
                primary_error = error
                if journal is not None:
                    journal_errors = _checkpoint_failure(journal)
    except Exception as error:  # noqa: BLE001 - install boundary owns terminal-state policy
        if primary_error is None:
            primary_error = error
        else:
            lock_error = error

    if primary_error is not None:
        output(
            _failure_message(
                "Install failed",
                primary_error,
                journal_errors,
                lock_error=lock_error,
            )
        )
        return 1
    return exit_code


def run_recovery_workflow(
    *,
    apply: bool = False,
    yes: bool = False,
    environ: Mapping[str, str] | None = None,
    output: Output = print,
) -> int:
    """Run recovery read-only, or lock an explicit recovery apply."""

    values = os.environ if environ is None else environ
    try:
        if not apply:
            return run_recovery(environ=values, output=output)
        with mutation_lock("recover", environ=values):
            return run_recovery(environ=values, apply=True, yes=yes, output=output)
    except Exception as error:  # noqa: BLE001 - recovery boundary converts failures to exit codes
        output(f"Recovery failed: {error}")
        return 1
