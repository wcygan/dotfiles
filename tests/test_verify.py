from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup import verify as verify_module
from dotfiles_setup.nix_profile import ProfileElement
from dotfiles_setup.verify import (
    VerificationResult,
    _codex_config_result,
    _link_result,
    run_verify,
    verify_installation,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def profile_element(
    tmp_path: Path,
    source: Path,
    *,
    name: str = "checkout",
    binaries: tuple[str, ...] = ("python3", "rustup"),
) -> ProfileElement:
    store_path = tmp_path / f"store-{name}"
    binary_home = store_path / "bin"
    binary_home.mkdir(parents=True)
    analyzer = store_path / "toolchains" / "1.97.1" / "bin" / "rust-analyzer"
    analyzer.parent.mkdir(parents=True)
    analyzer.write_text("#!/bin/sh\nexit 0\n")
    analyzer.chmod(0o755)
    for binary in binaries:
        path = binary_home / binary
        if binary == "python3":
            output = "echo 'Python 3.13.0'"
        elif binary == "rustup":
            output = f"echo '{analyzer}'"
        else:
            output = "exit 0"
        path.write_text(f"#!/bin/sh\n{output}\n")
        path.chmod(0o755)
    return ProfileElement(
        name=name,
        original_url=f"git+{source.resolve().as_uri()}",
        store_paths=(store_path,),
        active=True,
    )


def link_inventory(home: Path, system: str) -> None:
    config_home = home / ".config"
    codex_home = home / ".codex"
    from dotfiles_setup.links import managed_links

    for link in managed_links(
        REPO_ROOT,
        home=home,
        config_home=config_home,
        codex_home=codex_home,
        system=system,
    ):
        link.destination.parent.mkdir(parents=True, exist_ok=True)
        link.destination.symlink_to(link.source, target_is_directory=link.source.is_dir())
    codex_home.mkdir(parents=True, exist_ok=True)
    (codex_home / "config.toml").write_text("model = 'local'\n")


def test_dev_shell_path_does_not_replace_missing_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dev_shell = tmp_path / "dev-shell"
    dev_shell.mkdir()
    (dev_shell / "python3").write_text("")
    monkeypatch.setenv("PATH", f"{dev_shell}:{os.environ['PATH']}")

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(tmp_path / "home")},
        system="Linux",
        profile_loader=lambda: (),
        required_binaries=("python3",),
    )

    assert not next(result for result in results if result.name == "nix-profile").passed
    assert not next(result for result in results if result.name == "profile-binaries").passed


def test_profile_from_current_checkout_reports_name_and_source(tmp_path: Path) -> None:
    element = profile_element(tmp_path, REPO_ROOT, name="renamed-profile")

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(tmp_path / "home")},
        system="Linux",
        profile_loader=lambda: (element,),
        required_binaries=("python3",),
    )

    profile = next(result for result in results if result.name == "nix-profile")
    assert profile.passed
    assert "renamed-profile" in profile.message
    assert element.original_url in profile.message


@pytest.mark.parametrize("name", ["other-checkout", "dotfiles"])
def test_profile_from_elsewhere_is_rejected_even_if_named_dotfiles(
    tmp_path: Path, name: str
) -> None:
    other_checkout = tmp_path / "other"
    other_checkout.mkdir()
    element = profile_element(tmp_path, other_checkout, name=name)

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(tmp_path / "home")},
        system="Linux",
        profile_loader=lambda: (element,),
        required_binaries=("python3",),
    )

    profile = next(result for result in results if result.name == "nix-profile")
    assert not profile.passed
    assert name in profile.message
    assert element.original_url in profile.message


def test_profile_binaries_must_come_from_reported_store_paths(tmp_path: Path) -> None:
    element = profile_element(tmp_path, REPO_ROOT, binaries=("python3",))

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(tmp_path / "home")},
        system="Linux",
        profile_loader=lambda: (element,),
        required_binaries=("python3", "fish"),
    )

    binaries = next(result for result in results if result.name == "profile-binaries")
    assert not binaries.passed
    assert "fish" in binaries.message


def test_non_executable_profile_binary_is_rejected(tmp_path: Path) -> None:
    element = profile_element(tmp_path, REPO_ROOT)
    rustup = element.store_paths[0] / "bin" / "rustup"
    rustup.chmod(0o644)

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(tmp_path / "home")},
        system="Linux",
        profile_loader=lambda: (element,),
        required_binaries=("python3", "rustup"),
    )

    binaries = next(result for result in results if result.name == "profile-binaries")
    rust = next(result for result in results if result.name == "rust-analyzer")
    assert not binaries.passed
    assert "rustup" in binaries.message
    assert not rust.passed
    assert "does not provide rustup" in rust.message


def test_inactive_current_checkout_profile_is_rejected(tmp_path: Path) -> None:
    active = profile_element(tmp_path, REPO_ROOT)
    inactive = ProfileElement(
        name=active.name,
        original_url=active.original_url,
        store_paths=active.store_paths,
        active=False,
    )

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(tmp_path / "home")},
        system="Linux",
        profile_loader=lambda: (inactive,),
        required_binaries=("python3",),
    )

    assert not next(result for result in results if result.name == "nix-profile").passed


def test_profile_python_must_be_version_3_13(tmp_path: Path) -> None:
    element = profile_element(tmp_path, REPO_ROOT)
    python = element.store_paths[0] / "bin" / "python3"
    python.write_text("#!/bin/sh\necho 'Python 3.14.0'\n")

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(tmp_path / "home")},
        system="Linux",
        profile_loader=lambda: (element,),
        required_binaries=("python3",),
    )

    runtime = next(result for result in results if result.name == "python-runtime")
    assert not runtime.passed
    assert "Python 3.14.0" in runtime.message


def test_rust_analyzer_uses_profile_rustup_and_exact_pinned_toolchain(tmp_path: Path) -> None:
    element = profile_element(tmp_path, REPO_ROOT)
    analyzer = element.store_paths[0] / "toolchains" / "1.97.1" / "bin" / "rust-analyzer"
    calls: list[list[str]] = []
    environments: list[object] = []

    def runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        environments.append(kwargs.get("env"))
        if command[0].endswith("python3"):
            return subprocess.CompletedProcess(command, 0, stdout="Python 3.13.0\n", stderr="")
        return subprocess.CompletedProcess(command, 0, stdout=f"{analyzer}\n", stderr="")

    environment = {"HOME": str(tmp_path / "home"), "PATH": "/selected/bin"}
    results = verify_installation(
        REPO_ROOT,
        environ=environment,
        system="Linux",
        profile_loader=lambda: (element,),
        required_binaries=("python3", "rustup"),
        command_runner=runner,
    )

    rust = next(result for result in results if result.name == "rust-analyzer")
    assert rust.passed
    assert calls[-1] == [
        str(element.store_paths[0] / "bin" / "rustup"),
        "which",
        "--toolchain",
        "1.97.1",
        "rust-analyzer",
    ]
    assert environments == [environment, environment]


def test_missing_pinned_rust_analyzer_fails_strict_verification(tmp_path: Path) -> None:
    element = profile_element(tmp_path, REPO_ROOT)
    analyzer = element.store_paths[0] / "toolchains" / "1.97.1" / "bin" / "rust-analyzer"
    analyzer.unlink()

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(tmp_path / "home")},
        system="Linux",
        profile_loader=lambda: (element,),
        required_binaries=("python3", "rustup"),
    )

    rust = next(result for result in results if result.name == "rust-analyzer")
    assert not rust.passed
    assert "unusable path" in rust.message


def test_link_states_are_distinguished(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_text("managed")

    absent = _link_result(source, tmp_path / "absent")

    unmanaged_path = tmp_path / "unmanaged"
    unmanaged_path.write_text("local")
    unmanaged = _link_result(source, unmanaged_path)

    broken_path = tmp_path / "broken"
    broken_path.symlink_to(tmp_path / "missing-target")
    broken = _link_result(source, broken_path)

    stale_target = tmp_path / "stale-target"
    stale_target.write_text("old")
    stale_path = tmp_path / "stale"
    stale_path.symlink_to(stale_target)
    stale = _link_result(source, stale_path)

    correct_path = tmp_path / "correct"
    correct_path.symlink_to(source)
    correct = _link_result(source, correct_path)

    assert "absent" in absent.message
    assert "unmanaged" in unmanaged.message
    assert "broken" in broken.message
    assert "stale" in stale.message
    assert correct.passed


def test_symlink_loop_is_reported_as_broken(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.symlink_to(second)
    second.symlink_to(first)

    result = _link_result(tmp_path / "source", first)

    assert not result.passed
    assert "broken" in result.message


@pytest.mark.parametrize("system", ["Linux", "Darwin"])
def test_correct_platform_inventory_and_local_codex_config_pass(
    tmp_path: Path, system: str
) -> None:
    home = tmp_path / "home"
    link_inventory(home, system)
    element = profile_element(tmp_path, REPO_ROOT)

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(home)},
        system=system,
        profile_loader=lambda: (element,),
        required_binaries=("python3",),
    )

    assert all(result.passed for result in results)
    vscode_fragment = (
        "Library/Application Support/Code/User" if system == "Darwin" else ".config/Code/User"
    )
    assert any(vscode_fragment in result.message for result in results)


def test_default_profile_loader_uses_the_selected_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    environment = {"HOME": str(tmp_path / "selected-home")}
    captured: dict[str, object] = {}

    def load(**kwargs: object) -> tuple[ProfileElement, ...]:
        captured.update(kwargs)
        return ()

    monkeypatch.setattr(verify_module, "list_profile_elements", load)

    verify_installation(REPO_ROOT, environ=environment, system="Linux")

    assert captured == {"environment": environment}


def test_shared_and_codex_agents_links_are_verified(tmp_path: Path) -> None:
    home = tmp_path / "home"
    link_inventory(home, "Linux")
    element = profile_element(tmp_path, REPO_ROOT)

    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(home)},
        system="Linux",
        profile_loader=lambda: (element,),
        required_binaries=("python3",),
    )

    agents_destinations = (
        home / ".agents" / "AGENTS.md",
        home / ".codex" / "AGENTS.md",
    )
    for destination in agents_destinations:
        result = next(item for item in results if item.name == f"link:{destination}")
        assert result.passed

    agents_destinations[0].unlink()
    results = verify_installation(
        REPO_ROOT,
        environ={"HOME": str(home)},
        system="Linux",
        profile_loader=lambda: (element,),
        required_binaries=("python3",),
    )
    shared_result = next(
        item for item in results if item.name == f"link:{agents_destinations[0]}"
    )
    assert not shared_result.passed


def test_codex_config_must_be_a_regular_local_file(tmp_path: Path) -> None:
    codex_home = tmp_path / "codex"
    codex_home.mkdir()

    missing = _codex_config_result(codex_home)
    assert not missing.passed
    assert "missing" in missing.message

    local_target = tmp_path / "tracked-config.toml"
    local_target.write_text("tracked")
    (codex_home / "config.toml").symlink_to(local_target)
    symlinked = _codex_config_result(codex_home)
    assert not symlinked.passed
    assert "symlink" in symlinked.message

    (codex_home / "config.toml").unlink()
    (codex_home / "config.toml").write_text("machine-local")
    assert _codex_config_result(codex_home).passed


@pytest.mark.parametrize(
    "result",
    [
        VerificationResult("profile", False, "profile missing"),
        VerificationResult("links", False, "link stale"),
        VerificationResult("codex", False, "config missing"),
        VerificationResult("rust", False, "pinned analyzer missing"),
    ],
)
def test_strict_verify_fails_for_each_missing_postcondition(
    result: VerificationResult,
) -> None:
    output: list[str] = []

    assert run_verify(REPO_ROOT, results=[result], output=output.append) == 1
    assert output == [f"[FAIL] {result.message}"]


def test_strict_verify_passes_only_when_all_postconditions_pass() -> None:
    result = VerificationResult("complete", True, "installation complete")

    assert run_verify(REPO_ROOT, results=[result], output=lambda _: None) == 0


def test_verify_cli_uses_strict_verifier(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[Path] = []
    monkeypatch.setattr(cli, "run_verify", lambda root: calls.append(root) or 7)

    assert cli.main(["verify"]) == 7
    assert calls == [cli.REPO_ROOT]
