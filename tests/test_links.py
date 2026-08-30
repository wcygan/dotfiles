from __future__ import annotations

from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup import links as links_module
from dotfiles_setup import mutations as mutations_module
from dotfiles_setup import scoped_file_input as scoped_file_input_module
from dotfiles_setup.errors import LinkError
from dotfiles_setup.links import link_config, managed_links


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
    authoritative_agents = repo / "config" / "agents" / "AGENTS.md"
    compatibility_agents = repo / "config" / "codex" / "AGENTS.md"
    home = tmp_path / "home"
    xdg = tmp_path / "xdg"
    codex = tmp_path / "codex"
    values = environment(home, xdg=xdg, codex=codex)

    link_config(repo, environ=values, system="Linux")
    link_config(repo, environ=values, system="Linux")

    assert (xdg / "git").readlink() == (repo / "config" / "git").resolve()
    assert (home / ".tmux.conf").readlink() == (repo / "config" / "tmux" / "tmux.conf").resolve()
    assert compatibility_agents.readlink() == Path("../agents/AGENTS.md")
    assert compatibility_agents.resolve() == authoritative_agents.resolve()
    assert (home / ".agents" / "AGENTS.md").readlink() == authoritative_agents.resolve()
    assert (codex / "AGENTS.md").readlink() == authoritative_agents.resolve()
    assert not (codex / "config.toml").is_symlink()
    template = repo / "config" / "codex" / "config.toml"
    assert (codex / "config.toml").read_text() == template.read_text()
    assert (xdg / "Code" / "User" / "settings.json").is_symlink()


def test_idempotent_link_run_does_not_report_transient_backups(tmp_path: Path) -> None:
    home = tmp_path / "home"
    values = environment(home)
    link_config(Path.cwd(), environ=values, system="Linux", output=lambda _: None)
    output: list[str] = []

    link_config(Path.cwd(), environ=values, system="Linux", output=output.append)

    assert not any("Backed up" in line for line in output)


def test_darwin_uses_application_support_for_vscode(tmp_path: Path) -> None:
    home = tmp_path / "home"

    link_config(Path.cwd(), environ=environment(home), system="Darwin")

    settings = home / "Library" / "Application Support" / "Code" / "User" / "settings.json"
    assert settings.is_symlink()
    assert not (home / ".config" / "Code" / "User" / "settings.json").exists()


def test_relative_config_overrides_fall_back_inside_home(tmp_path: Path) -> None:
    home = tmp_path / "home"
    values = environment(home)
    values.update({"XDG_CONFIG_HOME": "relative-config", "CODEX_HOME": "relative-codex"})

    link_config(Path.cwd(), environ=values, system="Linux")

    assert (home / ".config" / "git").is_symlink()
    assert (home / ".agents" / "AGENTS.md").is_symlink()
    assert (home / ".codex" / "AGENTS.md").is_symlink()
    assert not (Path.cwd() / "relative-config").exists()
    assert not (Path.cwd() / "relative-codex").exists()


def test_existing_files_are_backed_up_and_symlinks_are_replaced(tmp_path: Path) -> None:
    home = tmp_path / "home"
    xdg = tmp_path / "xdg"
    git_destination = xdg / "git"
    git_destination.parent.mkdir(parents=True)
    git_destination.write_text("local git config")
    starship_destination = xdg / "starship.toml"
    starship_destination.symlink_to(tmp_path / "old-starship")

    link_config(Path.cwd(), environ=environment(home, xdg=xdg), system="Linux", now=lambda: 123)

    backups = list(xdg.glob("git.backup.123.*"))
    assert len(backups) == 1
    assert backups[0].read_text() == "local git config"
    assert git_destination.is_symlink()
    assert starship_destination.readlink() == (Path.cwd() / "config" / "starship.toml").resolve()


def test_link_rejects_destination_created_after_planning(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    xdg = tmp_path / "xdg"
    destination = xdg / "git"
    original_symlink = mutations_module._create_symlink

    def competing_symlink(
        source: Path | str, planned_destination: Path | str, **kwargs: object
    ) -> None:
        if Path(planned_destination) == destination:
            destination.write_text("created by competing actor")
        original_symlink(source, planned_destination, **kwargs)

    monkeypatch.setattr(mutations_module, "_create_symlink", competing_symlink)

    with pytest.raises(LinkError, match="atomically update"):
        link_config(Path.cwd(), environ=environment(home, xdg=xdg), system="Linux")

    assert destination.read_text() == "created by competing actor"
    assert not destination.is_symlink()


def test_existing_shared_agents_file_is_backed_up(tmp_path: Path) -> None:
    home = tmp_path / "home"
    shared_agents = home / ".agents" / "AGENTS.md"
    shared_agents.parent.mkdir(parents=True)
    shared_agents.write_text("local agent instructions")

    link_config(Path.cwd(), environ=environment(home), system="Linux", now=lambda: 123)

    backups = list(shared_agents.parent.glob("AGENTS.md.backup.123.*"))
    assert len(backups) == 1
    assert backups[0].read_text() == "local agent instructions"
    assert shared_agents.readlink() == (Path.cwd() / "config" / "agents" / "AGENTS.md").resolve()


def test_codex_home_at_shared_agents_root_has_one_agents_link(tmp_path: Path) -> None:
    repo = Path.cwd()
    home = tmp_path / "home"
    agents_home = home / ".agents"
    values = environment(home, codex=agents_home)
    links = managed_links(
        repo,
        home=home,
        config_home=home / ".config",
        codex_home=agents_home,
        system="Linux",
    )

    agents_destination = agents_home / "AGENTS.md"
    assert [link.destination for link in links].count(agents_destination) == 1

    link_config(repo, environ=values, system="Linux")
    link_config(repo, environ=values, system="Linux")

    assert agents_destination.readlink() == (repo / "config" / "agents" / "AGENTS.md").resolve()


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


def test_codex_migration_preserves_preexisting_temporary_name(tmp_path: Path) -> None:
    home = tmp_path / "home"
    codex = tmp_path / "codex"
    old_config = tmp_path / "old-config.toml"
    old_config.write_text("machine local state")
    codex.mkdir(parents=True)
    (codex / "config.toml").symlink_to(old_config)
    preexisting_temporary = codex / ".config.toml.migration"
    preexisting_temporary.write_text("do not overwrite")

    link_config(Path.cwd(), environ=environment(home, codex=codex), system="Linux")

    assert (codex / "config.toml").read_text() == "machine local state"
    assert preexisting_temporary.read_text() == "do not overwrite"


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


def test_npmrc_symlink_is_preserved_and_target_is_updated_atomically(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir()
    target = home / "machine-npmrc"
    target.write_text("prefix=/wrong\n")
    npmrc = home / ".npmrc"
    npmrc.symlink_to(target)

    link_config(Path.cwd(), environ=environment(home), system="Linux", now=lambda: 456)

    assert npmrc.is_symlink()
    assert target.read_text() == "prefix=${HOME}/.local\nmin-release-age=1\n"
    assert (home / "machine-npmrc.backup.456").read_text() == "prefix=/wrong\n"


def test_npmrc_refuses_user_edit_after_preparation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    npmrc = home / ".npmrc"
    npmrc.write_text("prefix=/wrong\n")
    execute_mutations = links_module.execute_mutations

    def edit_before_execution(*args: object, **kwargs: object) -> object:
        npmrc.write_text("registry=https://user.example/\n")
        return execute_mutations(*args, **kwargs)

    monkeypatch.setattr(links_module, "execute_mutations", edit_before_execution)

    with pytest.raises(LinkError, match="atomically update"):
        link_config(Path.cwd(), environ=environment(home), system="Linux")

    assert npmrc.read_text() == "registry=https://user.example/\n"
    assert not (home / ".tmux.conf").exists()


def test_npmrc_refuses_user_creation_after_preparation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    npmrc = home / ".npmrc"
    execute_mutations = links_module.execute_mutations

    def create_before_execution(*args: object, **kwargs: object) -> object:
        npmrc.write_text("registry=https://user.example/\n")
        return execute_mutations(*args, **kwargs)

    monkeypatch.setattr(links_module, "execute_mutations", create_before_execution)

    with pytest.raises(LinkError, match="atomically update"):
        link_config(Path.cwd(), environ=environment(home), system="Linux")

    assert npmrc.read_text() == "registry=https://user.example/\n"
    assert not (home / ".tmux.conf").exists()


def test_npmrc_swap_to_external_symlink_is_not_read_or_planned(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    npmrc = home / ".npmrc"
    npmrc.write_text("prefix=/wrong\n")
    external = tmp_path / "external-npmrc"
    external.write_text("outside secret\n")
    original_read = scoped_file_input_module._read_regular_file_at
    reads: list[Path] = []
    executed = False

    def swap_before_read(path: Path, *args: object, **kwargs: object) -> tuple[bytes, int]:
        reads.append(path)
        if path == npmrc:
            npmrc.unlink()
            npmrc.symlink_to(external)
        return original_read(path, *args, **kwargs)

    def unexpected_execution(*args: object, **kwargs: object) -> tuple[object, ...]:
        nonlocal executed
        executed = True
        return ()

    monkeypatch.setattr(scoped_file_input_module, "_read_regular_file_at", swap_before_read)
    monkeypatch.setattr(links_module, "execute_mutations", unexpected_execution)

    with pytest.raises(LinkError, match="file input changed during inspection"):
        link_config(Path.cwd(), environ=environment(home), system="Linux")

    assert reads == [npmrc]
    assert external.read_text() == "outside secret\n"
    assert npmrc.is_symlink()
    assert not executed
    assert not (home / ".tmux.conf").exists()


def test_codex_migration_refuses_symlink_change_after_preparation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    codex = home / ".codex"
    codex.mkdir(parents=True)
    original = home / "original-codex.toml"
    replacement = home / "replacement-codex.toml"
    original.write_text("original machine state\n")
    replacement.write_text("new user state\n")
    destination = codex / "config.toml"
    destination.symlink_to(original)
    execute_mutations = links_module.execute_mutations

    def retarget_before_execution(*args: object, **kwargs: object) -> object:
        destination.unlink()
        destination.symlink_to(replacement)
        return execute_mutations(*args, **kwargs)

    monkeypatch.setattr(links_module, "execute_mutations", retarget_before_execution)

    with pytest.raises(LinkError, match="atomically update"):
        link_config(Path.cwd(), environ=environment(home), system="Linux")

    assert destination.is_symlink()
    assert destination.resolve() == replacement
    assert replacement.read_text() == "new user state\n"
    assert not (home / ".tmux.conf").exists()


def test_dry_run_does_not_mutate_filesystem(tmp_path: Path) -> None:
    home = tmp_path / "home"
    values = {"HOME": str(home)}

    link_config(
        Path.cwd(),
        environ=values,
        system="Linux",
        dry_run=True,
    )

    assert not home.exists()


def test_link_cli_forwards_dry_run(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[Path, bool]] = []
    monkeypatch.setattr(
        cli,
        "link_config",
        lambda repo_root, *, dry_run: calls.append((repo_root, dry_run)),
    )

    assert cli.main(["link", "--dry-run"]) == 0
    assert calls == [(cli.REPO_ROOT, True)]


def test_link_setup_does_not_mutate_fish_universal_variables() -> None:
    source = (Path.cwd() / "src" / "dotfiles_setup" / "links.py").read_text()

    assert "set -U fish_greeting" not in source
