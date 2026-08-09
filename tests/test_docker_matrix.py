from __future__ import annotations

from tests.docker_matrix import (
    CASES,
    build_command,
    docker_environment,
    main,
    smoke_command,
)


def test_matrix_covers_ubuntu_and_fedora() -> None:
    assert [(case.name, case.dockerfile) for case in CASES] == [
        ("ubuntu", "Dockerfile.ubuntu"),
        ("fedora", "Dockerfile.fedora"),
    ]


def test_build_commands_use_the_expected_images_and_context() -> None:
    command = build_command(CASES[0])

    assert command[:3] == ["docker", "buildx", "build"]
    assert "--load" in command
    assert "--progress=plain" in command
    assert "--pull" not in command
    assert command[-3:] == ["-t", "nixdotfiles:test-ubuntu", str(command[-1])]


def test_ci_build_commands_use_separate_gha_cache_scopes() -> None:
    ubuntu = build_command(CASES[0], environ={"GITHUB_ACTIONS": "true"})
    fedora = build_command(CASES[1], environ={"GITHUB_ACTIONS": "true"})

    assert "type=gha,scope=dotfiles-ubuntu" in ubuntu
    assert "type=gha,mode=max,scope=dotfiles-ubuntu" in ubuntu
    assert "type=gha,scope=dotfiles-fedora" in fedora
    assert "type=gha,mode=max,scope=dotfiles-fedora" in fedora


def test_smoke_command_checks_the_non_root_repo_and_never_installs_nix() -> None:
    command = smoke_command(CASES[1])
    shell_command = command[-1]

    assert command[:3] == ["docker", "run", "--rm"]
    assert '$(id -un)" = tester' in shell_command
    assert "bash -n bootstrap.sh" in shell_command
    assert "./bootstrap.sh verify" in shell_command
    assert "__direnv_export_eval" in shell_command
    assert "install.determinate.systems" not in shell_command
    assert "curl --proto" not in shell_command
    assert "| sh" not in shell_command


def test_dry_run_does_not_require_docker(capsys) -> None:
    assert main(["--dry-run"]) == 0
    output = capsys.readouterr().out
    assert "nixdotfiles:test-ubuntu" in output
    assert "nixdotfiles:test-fedora" in output


def test_dry_run_can_select_one_ci_case(capsys) -> None:
    assert main(["--dry-run", "--case", "fedora"]) == 0
    output = capsys.readouterr().out
    assert "nixdotfiles:test-fedora" in output
    assert "nixdotfiles:test-ubuntu" not in output


def test_darwin_docker_environment_restores_host_helper_paths() -> None:
    environment = docker_environment(environ={"PATH": "/nix/bin"}, system="Darwin")

    assert environment["PATH"].endswith("/nix/bin")
    assert "/usr/local/bin" in environment["PATH"]
