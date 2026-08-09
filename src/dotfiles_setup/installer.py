from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

Operation = Callable[[], object]
Verifier = Callable[[], int]
Output = Callable[[str], None]


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
) -> int:
    """Run setup mutations in dependency order and aggregate independent results."""

    profile_result = _run_operation("profile", profile)
    _report(profile_result, output)
    if not profile_result.succeeded:
        _report(OperationResult("links", False, "profile failed", skipped=True), output)
        _report(OperationResult("rustup", False, "profile failed", skipped=True), output)
        if shell_handoff is not None:
            _report(OperationResult("shell-handoff", False, "profile failed", skipped=True), output)
        verification_exit = verify()
        return 1 if verification_exit == 0 else verification_exit

    operations = (("links", links), ("rustup", rustup))
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(_run_operation, name, operation) for name, operation in operations
        ]
        setup_results = [future.result() for future in futures]

    for result in setup_results:
        _report(result, output)

    setup_succeeded = all(result.succeeded for result in setup_results)
    handoff_result: OperationResult | None = None
    if setup_succeeded and shell_handoff is not None:
        handoff_result = _run_operation("shell-handoff", shell_handoff)
        _report(handoff_result, output)
    elif not setup_succeeded and shell_handoff is not None:
        handoff_result = OperationResult(
            "shell-handoff", False, "required setup operation failed", skipped=True
        )
        _report(handoff_result, output)

    verification_exit = verify()
    mutation_failed = not setup_succeeded or (
        handoff_result is not None and not handoff_result.succeeded
    )
    return 1 if mutation_failed or verification_exit != 0 else 0


def _report(result: OperationResult, output: Output) -> None:
    marker = "SKIP" if result.skipped else "PASS" if result.succeeded else "FAIL"
    output(f"[{marker}] {result.name}: {result.detail}")
