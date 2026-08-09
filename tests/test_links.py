from __future__ import annotations

from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.links import link_config


def environment(
    home: Path, *, xdg: Path | None = None, codex: Path | None = None
) -> dict[str, str]:
    values = {"HOME": str(home), "DOTFILES_SKIP_FISH_GREETING": "1"}
    if xdg is not None:
        values["XDG_CONFIG_HOME"] = str(xdg)
    if codex is not None:
        values["CODEX_HOME"] = str(codex)
    return values


def test_links_use_absolute_sources_and_are_idempotent(tmp_path: Path) -> None:
    repo = Path.cwd()
    home = tmp_path / "home"
    xdg = tmp_path / "xdg"
    codex = tmp_path / "codex"
    values = environment(home, xdg=xdg, codex=codex)

    link_config(repo, environ=values, system="Linux")
    link_config(repo, environ=values, system="Linux")

    assert (xdg / "git").readlink() == (repo / "config" / "git").resolve()
    assert (home / ".tmux.conf").readlink() == (repo / "config" / "tmux" / "tmux.conf").resolve()
    assert (codex / "AGENTS.md").readlink() == (repo / "config" / "codex" / "AGENTS.md").resolve()
    assert not (codex / "config.toml").is_symlink()
    template = repo / "config" / "codex" / "config.toml"
    assert (codex / "config.toml").read_text() == template.read_text()
    assert (xdg / "Code" / "User" / "settings.json").is_symlink()


def test_darwin_uses_application_support_for_vscode(tmp_path: Path) -> None:
    home = tmp_path / "home"

    link_config(Path.cwd(), environ=environment(home), system="Darwin")

    settings = home / "Library" / "Application Support" / "Code" / "User" / "settings.json"
    assert settings.is_symlink()
    assert not (home / ".config" / "Code" / "User" / "settings.json").exists()


def test_existing_files_are_backed_up_and_symlinks_are_replaced(tmp_path: Path) -> None:
    home = tmp_path / "home"
    xdg = tmp_path / "xdg"
    git_destination = xdg / "git"
    git_destination.parent.mkdir(parents=True)
    git_destination.write_text("local git config")
    starship_destination = xdg / "starship.toml"
    starship_destination.symlink_to(tmp_path / "old-starship")

    link_config(Path.cwd(), environ=environment(home, xdg=xdg), system="Linux", now=lambda: 123)

    assert (xdg / "git.backup.123").read_text() == "local git config"
    assert git_destination.is_symlink()
    assert starship_destination.readlink() == (Path.cwd() / "config" / "starship.toml").resolve()


def test_migrates_symlinked_codex_config_but_preserves_local_state(tmp_path: Path) -> None:
    home = tmp_path / "home"
    codex = tmp_path / "codex"
    old_config = tmp_path / "old-config.toml"
    old_config.write_text("[projects.important]\ntrust_level = 'trusted'\n")
    codex.mkdir(parents=True)
    (codex / "config.toml").symlink_to(old_config)

    link_config(Path.cwd(), environ=environment(home, codex=codex), system="Linux")
    assert not (codex / "config.toml").is_symlink()
    assert (codex / "config.toml").read_text() == old_config.read_text()

    (codex / "config.toml").write_text("machine local state")
    link_config(Path.cwd(), environ=environment(home, codex=codex), system="Linux")
    assert (codex / "config.toml").read_text() == "machine local state"


def test_npmrc_is_normalized_with_backup(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir()
    npmrc = home / ".npmrc"
    npmrc.write_text(
        "registry=https://registry.npmjs.org/\nprefix=/wrong\nmin-release-age=3\nprefix=/again\n"
    )

    link_config(Path.cwd(), environ=environment(home), system="Linux", now=lambda: 456)

    assert npmrc.read_text() == (
        "registry=https://registry.npmjs.org/\nprefix=${HOME}/.local\nmin-release-age=1\n"
    )
    assert (home / ".npmrc.backup.456").read_text().startswith("registry=")
    link_config(Path.cwd(), environ=environment(home), system="Linux", now=lambda: 456)
    assert not (home / ".npmrc.backup.456.1").exists()


def test_dry_run_does_not_mutate_filesystem_or_run_fish(tmp_path: Path) -> None:
    home = tmp_path / "home"
    runs: list[object] = []
    values = {"HOME": str(home)}

    link_config(
        Path.cwd(),
        environ=values,
        system="Linux",
        dry_run=True,
        find_command=lambda _: "/usr/bin/fish",
        run_command=lambda *args, **kwargs: runs.append((args, kwargs)),  # type: ignore[arg-type]
    )

    assert not home.exists()
    assert runs == []


def test_link_cli_forwards_dry_run(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[Path, bool]] = []
    monkeypatch.setattr(
        cli,
        "link_config",
        lambda repo_root, *, dry_run: calls.append((repo_root, dry_run)),
    )

    assert cli.main(["link", "--dry-run"]) == 0
    assert calls == [(cli.REPO_ROOT, True)]
