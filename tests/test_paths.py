from __future__ import annotations

from pathlib import Path

import pytest

from dotfiles_setup.links import resolve_codex_home, resolve_config_home
from dotfiles_setup.paths import UserPathContext


def test_user_path_context_uses_absolute_overrides(tmp_path: Path) -> None:
    home = tmp_path / "home"
    config = tmp_path / "config"
    state = tmp_path / "state"
    cache = tmp_path / "cache"
    codex = tmp_path / "codex"

    context = UserPathContext.from_environment(
        {
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(config),
            "XDG_STATE_HOME": str(state),
            "XDG_CACHE_HOME": str(cache),
            "CODEX_HOME": str(codex),
        },
        system="Darwin",
    )

    assert context.home == home
    assert context.config_home == config
    assert context.state_home == state
    assert context.cache_home == cache
    assert context.codex_home == codex
    assert context.platform == "Darwin"
    assert context.state_directory == state / "dotfiles"
    assert context.mutation_lock_path == cache / "dotfiles" / "setup.lock"
    assert context.agent_skills_target() == home / ".agents" / "skills"


def test_supplied_home_does_not_read_the_ambient_home(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    selected_home = tmp_path / "selected-home"

    def fail_home_lookup() -> Path:
        raise RuntimeError("ambient home is unavailable")

    monkeypatch.setattr(Path, "home", fail_home_lookup)

    context = UserPathContext.from_environment(
        {"HOME": str(selected_home)},
        system="Linux",
    )

    assert context.home == selected_home


def test_relative_overrides_use_home_fallbacks(tmp_path: Path) -> None:
    home = tmp_path / "home"

    context = UserPathContext.from_environment(
        {
            "HOME": str(home),
            "XDG_CONFIG_HOME": "relative-config",
            "XDG_STATE_HOME": "relative-state",
            "XDG_CACHE_HOME": "relative-cache",
            "CODEX_HOME": "relative-codex",
        },
        system="Linux",
    )

    assert context.config_home == home / ".config"
    assert context.state_home == home / ".local" / "state"
    assert context.cache_home == home / ".cache"
    assert context.codex_home == home / ".codex"


def test_tilde_overrides_use_selected_home_fallbacks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ambient_home = tmp_path / "ambient-home"
    selected_home = tmp_path / "selected-home"
    monkeypatch.setenv("HOME", str(ambient_home))

    context = UserPathContext.from_environment(
        {
            "HOME": str(selected_home),
            "XDG_CONFIG_HOME": "~/.config",
            "XDG_STATE_HOME": "~/.local/state",
            "XDG_CACHE_HOME": "~/.cache",
        },
        system="Linux",
    )

    assert context.config_home == selected_home / ".config"
    assert context.state_home == selected_home / ".local" / "state"
    assert context.cache_home == selected_home / ".cache"


def test_compatibility_wrappers_preserve_a_relative_explicit_home() -> None:
    home = Path("relative-home")

    assert resolve_config_home(home, {}) == home / ".config"
    assert resolve_codex_home(home, {}) == home / ".codex"


def test_agent_skill_target_stays_inside_home(tmp_path: Path) -> None:
    context = UserPathContext.from_environment(
        {"HOME": str(tmp_path / "home")},
        system="Linux",
    )

    assert context.agent_skills_target("custom/skills") == tmp_path / "home" / "custom" / "skills"
    with pytest.raises(ValueError, match="relative path inside HOME"):
        context.agent_skills_target(tmp_path / "outside")
    with pytest.raises(ValueError, match="relative path inside HOME"):
        context.agent_skills_target("../outside")


def test_vscode_config_home_uses_context_platform(tmp_path: Path) -> None:
    home = tmp_path / "home"
    context = UserPathContext.from_environment(
        {"HOME": str(home)},
        system="Darwin",
    )

    vscode_home = home / "Library" / "Application Support" / "Code" / "User"
    assert context.vscode_config_home == vscode_home
