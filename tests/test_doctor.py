from dotfiles_setup.doctor import CheckResult, evaluate_checks, run_doctor


def passing_check() -> CheckResult:
    return CheckResult("passing", True, "diagnostic passed")


def warning_check() -> CheckResult:
    return CheckResult("warning", False, "optional check failed")


def failing_check() -> CheckResult:
    return CheckResult("failing", False, "diagnostic failed")


def test_evaluate_checks_preserves_declared_order() -> None:
    results = evaluate_checks([warning_check, passing_check])

    assert [result.name for result in results] == ["warning", "passing"]


def test_doctor_allows_advisory_warnings() -> None:
    output: list[str] = []

    exit_code = run_doctor(checks=[passing_check, warning_check], output=output.append)

    assert exit_code == 0
    assert any(line == "[WARN] optional check failed" for line in output)


def test_doctor_reports_every_failure_as_advisory() -> None:
    output: list[str] = []

    exit_code = run_doctor(checks=[failing_check], output=output.append)

    assert exit_code == 0
    assert any(line == "[WARN] diagnostic failed" for line in output)
