from __future__ import annotations

from pathlib import Path

from tests.docker_matrix import (
    CASES,
    build_command,
    build_commands,
    docker_environment,
    main,
)


def test_matrix_covers_ubuntu_and_fedora() -> None:
    assert [(case.name, case.dockerfile) for case in CASES] == [
        ("ubuntu", "Dockerfile.ubuntu"),
        ("fedora", "Dockerfile.fedora"),
    ]


def test_build_runs_the_acceptance_stage_without_exporting_an_image() -> None:
    command = build_command(CASES[0])

    assert command[:3] == ["docker", "buildx", "build"]
    assert "--progress=plain" in command
    assert "--pull" not in command
    assert command[command.index("--target") + 1] == "acceptance"
    assert command[command.index("--output") + 1] == "type=cacheonly"
    assert "--load" not in command
    assert "-t" not in command
    assert command[command.index("-f") + 1].endswith("Dockerfile.ubuntu")


def test_keep_loads_a_tagged_image_for_debugging() -> None:
    command = build_command(CASES[1], keep=True)

    assert command[-4:-1] == ["--load", "-t", "nixdotfiles:test-fedora"]
    assert "--output" not in command


def test_empty_layer_cache_is_seeded_with_only_the_locked_input_stages(
    tmp_path: Path,
) -> None:
    seed, build = build_commands(CASES[0], layer_cache=tmp_path)

    assert seed[seed.index("--target") + 1] == "prewarm"
    assert f"type=local,dest={tmp_path},mode=max,compression=zstd" in seed
    assert "--cache-to" not in build
    assert f"type=local,src={tmp_path}" in build
    assert build[build.index("--target") + 1] == "acceptance"


def test_restored_layer_cache_is_read_and_never_rewritten(tmp_path: Path) -> None:
    tmp_path.joinpath("index.json").write_text("{}")

    (build,) = build_commands(CASES[0], layer_cache=tmp_path)

    assert f"type=local,src={tmp_path}" in build
    assert "--cache-to" not in build


def test_local_runs_use_only_the_builder_cache() -> None:
    (build,) = build_commands(CASES[0], target="tests")

    assert build[build.index("--target") + 1] == "tests"
    assert "--cache-from" not in build
    assert "--cache-to" not in build


def test_dry_run_does_not_require_docker(capsys, monkeypatch) -> None:
    monkeypatch.delenv("DOCKER_LAYER_CACHE", raising=False)
    assert main(["--dry-run"]) == 0
    output = capsys.readouterr().out
    assert "Dockerfile.ubuntu" in output
    assert "Dockerfile.fedora" in output
    assert "passed" not in output


def test_dry_run_can_select_one_ci_case(capsys, monkeypatch) -> None:
    monkeypatch.delenv("DOCKER_LAYER_CACHE", raising=False)
    assert main(["--dry-run", "--case", "fedora"]) == 0
    output = capsys.readouterr().out
    assert "Dockerfile.fedora" in output
    assert "Dockerfile.ubuntu" not in output


def test_layer_cache_directory_comes_from_the_ci_environment(
    capsys, monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("DOCKER_LAYER_CACHE", str(tmp_path))
    assert main(["--dry-run", "--case", "ubuntu"]) == 0
    output = capsys.readouterr().out
    assert f"--cache-to type=local,dest={tmp_path}" in output
    assert f"--cache-from type=local,src={tmp_path}" in output


def test_darwin_docker_environment_restores_host_helper_paths() -> None:
    environment = docker_environment(environ={"PATH": "/nix/bin"}, system="Darwin")

    assert environment["PATH"].endswith("/nix/bin")
    assert "/usr/local/bin" in environment["PATH"]
