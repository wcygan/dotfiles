from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
FISH_ROOT = REPO_ROOT / "config" / "fish"


@pytest.mark.parametrize("shell", ["fish", "bash"])
@pytest.mark.parametrize("custom_ca", [False, True])
def test_shell_ca_defaults_preserve_explicit_overrides(
    tmp_path: Path, shell: str, custom_ca: bool
) -> None:
    certificates = tmp_path / ".nix-profile/etc/ssl/certs"
    certificates.mkdir(parents=True)
    bundle = certificates / "ca-bundle.crt"
    bundle.touch()
    environment = os.environ.copy()
    environment["HOME"] = str(tmp_path)
    for key in ("SSL_CERT_FILE", "SSL_CERT_DIR", "NIX_SSL_CERT_FILE"):
        environment.pop(key, None)
    expected = [str(bundle), str(certificates), str(bundle)]
    if custom_ca:
        expected = [
            str(tmp_path / "custom.pem"),
            str(tmp_path / "custom-certs"),
            str(tmp_path / "nix-custom.pem"),
        ]
        environment.update(
            zip(("SSL_CERT_FILE", "SSL_CERT_DIR", "NIX_SSL_CERT_FILE"), expected, strict=True)
        )
    if shell == "fish":
        command = [
            shell,
            "--no-config",
            "-c",
            'source $argv[1]; printf "%s\\n" "$SSL_CERT_FILE" "$SSL_CERT_DIR" "$NIX_SSL_CERT_FILE"',
            str(FISH_ROOT / "conf.d/10-nix.fish"),
        ]
    else:
        command = [
            shell,
            "--noprofile",
            "--norc",
            "-c",
            '. "$1"; printf "%s\\n" "$SSL_CERT_FILE" "$SSL_CERT_DIR" "$NIX_SSL_CERT_FILE"',
            "test",
            str(REPO_ROOT / "config/shell-nix.sh"),
        ]
    result = subprocess.run(command, env=environment, text=True, capture_output=True, check=True)
    assert result.stdout.splitlines()[-3:] == expected


def read_repo_file(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text()


def test_flake_declares_fish_node_and_default_package_shell() -> None:
    flake = read_repo_file("flake.nix")

    for package in ("fish", "nodejs"):
        assert re.search(rf"^\s+{package}\s*$", flake, re.MULTILINE)

    assert "self.packages.${pkgs.stdenv.hostPlatform.system}.default" in flake


def test_required_fish_config_files_exist() -> None:
    required_files = (
        "config.fish",
        "conf.d/10-nix.fish",
        "conf.d/20-direnv.fish",
        "conf.d/30-starship.fish",
        "functions/nix-try.fish",
        "functions/nix-install.fish",
        "functions/qmd.fish",
    )

    missing = [
        relative_path
        for relative_path in required_files
        if not (FISH_ROOT / relative_path).is_file()
    ]
    assert not missing, f"missing Fish configuration files: {', '.join(missing)}"


def test_all_tracked_fish_files_parse_when_fish_is_available() -> None:
    fish = shutil.which("fish")
    assert fish is not None, "fish is required by the canonical Nix test suite"

    fish_files = sorted(
        path for path in FISH_ROOT.rglob("*.fish") if not path.is_symlink() or path.exists()
    )
    assert fish_files

    for fish_file in fish_files:
        result = subprocess.run(
            [fish, "--no-execute", str(fish_file)],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, f"{fish_file.relative_to(REPO_ROOT)}:\n{result.stderr}"


def test_linker_and_codex_templates_are_wired() -> None:
    linker = read_repo_file("src/dotfiles_setup/links.py")
    qmd = read_repo_file("config/fish/functions/qmd.fish")

    assert 'Link(config / "fish", config_home / "fish")' in linker
    assert "_prepare_codex_template" in linker
    assert "Preserved existing local Codex config" in linker
    assert 'agents_source = config / "agents" / "AGENTS.md"' in linker
    assert "Link(agents_source, shared_agents)" in linker
    assert "Link(agents_source, codex_agents)" in linker
    assert (REPO_ROOT / "config/codex/config.toml").is_file()
    assert (REPO_ROOT / "config/agents/AGENTS.md").is_file()
    compatibility_agents = REPO_ROOT / "config/codex/AGENTS.md"
    assert compatibility_agents.is_symlink()
    assert compatibility_agents.readlink() == Path("../agents/AGENTS.md")
    assert "GGML_METAL_NO_RESIDENCY=1" in qmd
    assert "GGML_METAL_TENSOR_DISABLE=1" in qmd
    assert "command qmd" in qmd


def test_fish_path_priorities_and_nix_defaults_are_preserved() -> None:
    nix_config = read_repo_file("config/fish/conf.d/10-nix.fish")
    repair_function = read_repo_file("config/fish/functions/fix-paths.fish")

    for path in (
        "$HOME/.nix-profile/bin",
        "/nix/var/nix/profiles/default/bin",
        "$HOME/.tiup/bin",
    ):
        assert f"fish_add_path --path --move --prepend {path}" in nix_config

    assert "test -d $HOME/.tiup/bin; and set new_path $HOME/.tiup/bin $new_path" in repair_function
    assert "experimental-features = nix-command flakes" in nix_config

    assert nix_config.index("$HOME/.bun/bin") < nix_config.index("$HOME/.local/bin")
    assert repair_function.index("$HOME/.bun/bin") < repair_function.index("$HOME/.local/bin")


def test_direnv_uses_the_repository_flake() -> None:
    envrc = read_repo_file(".envrc")
    assert "use flake" in envrc


def test_retired_deno_integration_is_absent() -> None:
    from dotfiles_setup.links import managed_links

    home = Path("/tmp/dotfiles-test-home")
    links = managed_links(
        REPO_ROOT,
        home=home,
        config_home=home / ".config",
        codex_home=home / ".codex",
        system="Darwin",
    )
    assert all(link.source != REPO_ROOT / "config/deno" for link in links)
    assert not (FISH_ROOT / "conf.d/15-deno.fish").exists()
    assert not (FISH_ROOT / "completions/deno.fish").exists()


@pytest.mark.parametrize("custom_java", [False, True])
@pytest.mark.parametrize("installed", [False, True])
def test_java_home_uses_available_homebrew_jdk_without_overriding_user(
    tmp_path: Path, custom_java: bool, installed: bool
) -> None:
    bin_home = tmp_path / "bin"
    bin_home.mkdir()
    jdk = tmp_path / "homebrew" / "openjdk"
    if installed:
        (jdk / "bin").mkdir(parents=True)
    brew = bin_home / "brew"
    brew.write_text(f"#!/bin/sh\nprintf '%s\\n' '{jdk}'\n")
    brew.chmod(0o755)
    environment = os.environ.copy()
    environment["PATH"] = f"{bin_home}:{environment['PATH']}"
    environment.pop("JAVA_HOME", None)
    if custom_java:
        environment["JAVA_HOME"] = "/custom/jdk"
    result = subprocess.run(
        [
            "fish",
            "--no-config",
            "-c",
            'source $argv[1]; printf "%s" "$JAVA_HOME"',
            str(FISH_ROOT / "conf.d/java.fish"),
        ],
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    expected = "/custom/jdk" if custom_java else str(jdk) if installed else ""
    assert result.stdout == expected


def test_java_home_uses_known_homebrew_prefix_without_running_brew(tmp_path: Path) -> None:
    prefix = tmp_path / "homebrew"
    (prefix / "bin").mkdir(parents=True)
    (prefix / "opt/openjdk/bin").mkdir(parents=True)
    brew = prefix / "bin/brew"
    brew.write_text("#!/bin/sh\nexit 1\n")
    brew.chmod(0o755)
    environment = os.environ.copy()
    environment.update(PATH=f"{prefix / 'bin'}:{environment['PATH']}", HOMEBREW_PREFIX=str(prefix))
    environment.pop("JAVA_HOME", None)
    result = subprocess.run(
        [
            "fish",
            "--no-config",
            "-c",
            'source $argv[1]; printf "%s\\n" "$JAVA_HOME"; contains -- "$JAVA_HOME/bin" $PATH',
            str(FISH_ROOT / "conf.d/java.fish"),
        ],
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == str(prefix / "opt/openjdk")


def test_nix_daemon_import_handles_newlines_empty_values_and_shell_state(tmp_path: Path) -> None:
    daemon = tmp_path / "nix-daemon.sh"
    daemon.write_text(
        "export NIX_TEST_VALUE='a=b\nc'\n"
        "export NIX_TEST_EMPTY=''\n"
        "export NIX_PROFILES='system user'\n"
        'export PATH="/daemon/path:$PATH"\n'
    )
    config = tmp_path / "nix.fish"
    config.write_text(
        (FISH_ROOT / "conf.d/10-nix.fish")
        .read_text()
        .replace("/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh", str(daemon))
    )
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    env.pop("NIX_TEST_EMPTY", None)
    env.pop("NIX_TEST_VALUE", None)
    result = subprocess.run(
        [
            "fish",
            "--no-config",
            "-c",
            'source $argv[1]; test "$NIX_TEST_VALUE" = "a=b\nc"; or exit 1; '
            'set -q NIX_TEST_EMPTY; or exit 2; test -z "$NIX_TEST_EMPTY"; or exit 3; '
            'test "$NIX_PROFILES" = "system user"; or exit 4; '
            "contains -- /daemon/path $PATH; and exit 5; "
            'printf "%s" "$NIX_TEST_VALUE"',
            str(config),
        ],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == "a=b\nc"


@pytest.mark.parametrize("standard_brew", [False, True])
def test_homebrew_initialization_preserves_standard_and_custom_installs(
    tmp_path: Path, standard_brew: bool
) -> None:
    prefix = tmp_path / "homebrew"
    (prefix / "bin").mkdir(parents=True)
    other_bin = tmp_path / "other-bin"
    other_bin.mkdir()
    uname = other_bin / "uname"
    uname.write_text("#!/bin/sh\nprintf 'Darwin\\n'\n")
    uname.chmod(0o755)
    log = tmp_path / "brew.log"
    brew = (prefix / "bin" if standard_brew else other_bin) / "brew"
    brew.write_text(f"#!/bin/sh\nprintf called > '{log}'\nprintf 'export BREW_EXTRA=custom\\n'\n")
    brew.chmod(0o755)
    config = tmp_path / "homebrew.fish"
    config.write_text(
        (FISH_ROOT / "conf.d/05-homebrew.fish").read_text().replace("/opt/homebrew", str(prefix))
    )
    env = os.environ.copy()
    env["PATH"] = f"{other_bin}:{env['PATH']}"
    env.pop("HOMEBREW_PREFIX", None)
    env.pop("BREW_EXTRA", None)
    result = subprocess.run(
        [
            "fish",
            "--no-config",
            "-c",
            'source $argv[1]; printf "%s\\n" "$HOMEBREW_PREFIX" "$BREW_EXTRA"',
            str(config),
        ],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.splitlines() == [str(prefix), "" if standard_brew else "custom"]
    assert log.exists() is not standard_brew


@pytest.mark.parametrize("installed", [False, True])
def test_project_envrc_uses_cache_when_available_and_falls_back(
    tmp_path: Path, installed: bool
) -> None:
    if installed:
        script = tmp_path / ".nix-profile/share/nix-direnv/direnvrc"
        script.parent.mkdir(parents=True)
        script.write_text(
            "use_flake() { printf 'cached\\n'; }\n"
            "nix_direnv_disallow_fallback() { printf 'no stale fallback\\n'; }\n"
        )
    env = os.environ.copy()
    env.update(HOME=str(tmp_path), XDG_STATE_HOME=str(tmp_path / "state"))
    command = (
        "use() { if declare -F use_flake >/dev/null; then use_flake; "
        "else printf 'builtin\\n'; fi; }; source \"$1\""
    )
    result = subprocess.run(
        ["bash", "--noprofile", "--norc", "-c", command, "test", str(REPO_ROOT / ".envrc")],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.splitlines() == (
        ["no stale fallback", "cached"] if installed else ["builtin"]
    )


def test_project_envrc_keeps_existing_nix_direnv_configuration(tmp_path: Path) -> None:
    script = tmp_path / ".nix-profile/share/nix-direnv/direnvrc"
    script.parent.mkdir(parents=True)
    script.write_text("printf 'unexpected override\\n'\n")
    env = os.environ.copy()
    env.update(HOME=str(tmp_path), XDG_STATE_HOME=str(tmp_path / "state"))
    command = (
        "nix_direnv_version() { :; }; "
        "nix_direnv_disallow_fallback() { printf 'unexpected override\\n'; }; "
        "use() { printf 'existing cache\\n'; }; source \"$1\""
    )
    result = subprocess.run(
        ["bash", "--noprofile", "--norc", "-c", command, "test", str(REPO_ROOT / ".envrc")],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == "existing cache\n"


def test_project_envrc_keeps_custom_direnvrc(tmp_path: Path) -> None:
    script = tmp_path / ".nix-profile/share/nix-direnv/direnvrc"
    script.parent.mkdir(parents=True)
    script.write_text("printf 'unexpected override\\n'\n")
    config = tmp_path / "custom-direnv"
    config.mkdir()
    (config / "direnvrc").write_text("# Existing configuration\n")
    env = os.environ.copy()
    env.update(HOME=str(tmp_path), DIRENV_CONFIG=str(config))
    command = "use() { printf 'existing implementation\\n'; }; source \"$1\""
    result = subprocess.run(
        ["bash", "--noprofile", "--norc", "-c", command, "test", str(REPO_ROOT / ".envrc")],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == "existing implementation\n"
