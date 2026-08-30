from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FISH_ROOT = REPO_ROOT / "config" / "fish"


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
