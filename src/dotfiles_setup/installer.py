from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

Operation = Callable[[], object]
Verifier = Callable[[], int]
Output = Callable[[str], None]
Observer = Callable[["OperationResult"], None]


@dataclass(frozen=True)
class OperationResult:
    name: str
    succeeded: bool
    detail: str
    skipped: bool = False


def _run_operation(name: str, operation: Operation) -> OperationResult:
    try:
        result = operation()
    except Exception as error:  # noqa: BLE001 - operation boundary must aggregate failures
        return OperationResult(name, False, str(error))
    detail = str(result) if result is not None else "complete"
    return OperationResult(name, True, detail)


def run_install(
    *,
    profile: Operation,
    links: Operation,
    rustup: Operation,
    verify: Verifier,
    shell_handoff: Operation | None = None,
    output: Output = print,
    observer: Observer | None = None,
) -> int:
    """Run setup mutations serially so one journal can describe their exact order."""

    profile_result = _run_operation("profile", profile)
    _report(profile_result, output, observer)
    if not profile_result.succeeded:
        _report(OperationResult("links", False, "profile failed", skipped=True), output, observer)
        _report(OperationResult("rustup", False, "profile failed", skipped=True), output, observer)
        if shell_handoff is not None:
            _report(
                OperationResult("shell-handoff", False, "profile failed", skipped=True),
                output,
                observer,
            )
        verification_exit = verify()
        return 1 if verification_exit == 0 else verification_exit

    links_result = _run_operation("links", links)
    setup_results = [links_result]
    if links_result.succeeded:
        setup_results.append(_run_operation("rustup", rustup))
    else:
        setup_results.append(OperationResult("rustup", False, "links failed", skipped=True))

    for result in setup_results:
        _report(result, output, observer)

    setup_succeeded = all(result.succeeded for result in setup_results)
    handoff_result: OperationResult | None = None
    if setup_succeeded and shell_handoff is not None:
        handoff_result = _run_operation("shell-handoff", shell_handoff)
        _report(handoff_result, output, observer)
    elif not setup_succeeded and shell_handoff is not None:
        handoff_result = OperationResult(
            "shell-handoff", False, "required setup operation failed", skipped=True
        )
        _report(handoff_result, output, observer)

    verification_exit = verify()
    mutation_failed = not setup_succeeded or (
        handoff_result is not None and not handoff_result.succeeded
    )
    return 1 if mutation_failed or verification_exit != 0 else 0


def _report(result: OperationResult, output: Output, observer: Observer | None = None) -> None:
    marker = "SKIP" if result.skipped else "PASS" if result.succeeded else "FAIL"
    output(f"[{marker}] {result.name}: {result.detail}")
    if observer is not None:
        observer(result)
