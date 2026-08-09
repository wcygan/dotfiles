from __future__ import annotations

from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.cleanup import cleanup_links
from dotfiles_setup.links import link_config


def environment(home: Path, codex: Path) -> dict[str, str]:
    return {"HOME": str(home), "CODEX_HOME": str(codex), "DOTFILES_SKIP_FISH_GREETING": "1"}


def test_cleanup_removes_only_managed_links_and_preserves_local_state(tmp_path: Path) -> None:
    repo = Path.cwd()
    home = tmp_path / "home"
    codex = tmp_path / "codex"
    values = environment(home, codex)
    link_config(repo, environ=values, system="Linux")
    backup = home / ".tmux.conf.backup.1"
    backup.write_text("keep me")
    (codex / "config.toml").write_text("local Codex state")
    (home / ".npmrc").write_text("local npm state")
    unmanaged = home / ".config" / "zed"
    unmanaged.unlink()
    unrelated_source = tmp_path / "unrelated-zed"
    unrelated_source.mkdir()
    unmanaged.symlink_to(unrelated_source)

    cleanup_links(repo, environ=values, system="Linux")

    assert not (home / ".config" / "git").exists()
    assert not (codex / "AGENTS.md").exists()
    assert unmanaged.is_symlink()
    assert backup.read_text() == "keep me"
    assert (codex / "config.toml").read_text() == "local Codex state"
    assert (home / ".npmrc").read_text() == "local npm state"


def test_cleanup_dry_run_preserves_managed_link(tmp_path: Path) -> None:
    home = tmp_path / "home"
    codex = tmp_path / "codex"
    values = environment(home, codex)
    link_config(Path.cwd(), environ=values, system="Darwin")
    settings = home / "Library" / "Application Support" / "Code" / "User" / "settings.json"

    cleanup_links(Path.cwd(), environ=values, system="Darwin", dry_run=True)

    assert settings.is_symlink()


def test_uninstall_requires_confirmation(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def record_cleanup(_: Path, *, dry_run: bool) -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(cli, "cleanup_links", record_cleanup)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    assert cli.main(["uninstall"]) == 0
    assert called is False


def test_uninstall_yes_skips_confirmation(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[Path, bool]] = []
    monkeypatch.setattr(
        cli,
        "cleanup_links",
        lambda repo_root, *, dry_run: calls.append((repo_root, dry_run)),
    )

    assert cli.main(["uninstall", "--yes"]) == 0
    assert calls == [(cli.REPO_ROOT, False)]
