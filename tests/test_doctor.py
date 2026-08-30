from pathlib import Path

from dotfiles_setup.doctor import (
    CheckResult,
    command_check,
    default_checks,
    evaluate_checks,
    run_doctor,
)


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


def test_default_checks_ignore_relative_config_override(tmp_path: Path) -> None:
    home = tmp_path / "home"

    checks = default_checks(
        home,
        environ={"HOME": str(home), "XDG_CONFIG_HOME": "relative-config"},
        system="Linux",
    )

    fish_result = checks[-1]()
    assert fish_result.message == f"{home / '.config' / 'fish'} does not exist"


def test_command_check_uses_only_the_selected_path(tmp_path: Path) -> None:
    selected = tmp_path / "selected"
    selected.mkdir()
    command = selected / "example"
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)

    present = command_check("example", {"PATH": str(selected)})()
    absent = command_check("example", {"PATH": ""})()

    assert present.passed
    assert str(command) in present.message
    assert not absent.passed
