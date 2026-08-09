from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.errors import LinkError, ManifestError, RecoveryError
from dotfiles_setup.links import Link, link_config
from dotfiles_setup.manifest import OperationJournal, read_manifest, state_directory
from dotfiles_setup.nix_profile import NixProfileError
from dotfiles_setup.recovery import run_recovery


def _environment(home: Path) -> dict[str, str]:
    return {"HOME": str(home), "DOTFILES_SKIP_FISH_GREETING": "1"}


def test_missing_source_is_detected_before_any_destination_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    destination = home / ".config" / "example"
    destination.parent.mkdir(parents=True)
    destination.write_text("preserve me")
    good_source = tmp_path / "good"
    good_source.write_text("good")
    missing_source = tmp_path / "missing"
    monkeypatch.setattr(
        "dotfiles_setup.links.managed_links",
        lambda *_args, **_kwargs: (
            Link(good_source, destination),
            Link(missing_source, home / ".config" / "missing"),
        ),
    )

    with pytest.raises(LinkError, match="managed source is missing"):
        link_config(tmp_path, environ=_environment(home), system="Linux")

    assert destination.read_text() == "preserve me"
    assert not state_directory(_environment(home)).exists()


def test_failed_replacement_restores_destination_from_backup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    source = tmp_path / "source"
    source.write_text("source")
    destination = home / ".config" / "example"
    destination.parent.mkdir(parents=True)
    destination.write_text("original")
    monkeypatch.setattr(
        "dotfiles_setup.links.managed_links",
        lambda *_args, **_kwargs: (Link(source, destination),),
    )
    calls = 0

    def replace(source_path: Path, destination_path: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected replacement failure")
        os.replace(source_path, destination_path)

    with pytest.raises(LinkError, match="prior destination restored"):
        link_config(
            tmp_path,
            environ=_environment(home),
            system="Linux",
            now=lambda: 123,
            replace=replace,
        )

    assert destination.read_text() == "original"
    assert not list(destination.parent.glob("example.backup.123.*"))
    manifest = read_manifest(state_directory(_environment(home)) / "current.json")
    assert manifest["state"] == "failed"


def test_failed_automatic_restore_creates_recoverable_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    source = tmp_path / "source"
    source.write_text("source")
    destination = home / ".config" / "example"
    destination.parent.mkdir(parents=True)
    destination.write_text("original")
    monkeypatch.setattr(
        "dotfiles_setup.links.managed_links",
        lambda *_args, **_kwargs: (Link(source, destination),),
    )
    calls = 0

    def replace(source_path: Path, destination_path: Path) -> None:
        nonlocal calls
        calls += 1
        if calls in {2, 3}:
            raise OSError("injected replacement and restore failure")
        os.replace(source_path, destination_path)

    with pytest.raises(LinkError, match="recovery manifest preserved"):
        link_config(
            tmp_path,
            environ=_environment(home),
            system="Linux",
            now=lambda: 123,
            replace=replace,
        )

    manifest = read_manifest(state_directory(_environment(home)) / "current.json")
    assert manifest["state"] == "recovery-needed"
    assert not (destination.exists() or destination.is_symlink())
    assert Path(manifest["entries"][0]["backup"]).read_text() == "original"
    assert (
        run_recovery(environ=_environment(home), apply=True, yes=True, output=lambda _: None) == 0
    )
    assert destination.read_text() == "original"


def test_manifest_failure_after_link_replace_restores_prior_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    values = _environment(home)
    source = tmp_path / "source"
    source.write_text("source")
    destination = home / ".config" / "example"
    destination.parent.mkdir(parents=True)
    destination.write_text("original")
    monkeypatch.setattr(
        "dotfiles_setup.links.managed_links",
        lambda *_args, **_kwargs: (Link(source, destination),),
    )
    journal = OperationJournal("link", tmp_path, environ=values)
    journal.transition("applying")
    original_update = journal.update_link_entry

    def fail_applied(index: int, **changes: object) -> None:
        if changes.get("applied"):
            raise ManifestError("injected manifest failure")
        original_update(index, **changes)

    monkeypatch.setattr(journal, "update_link_entry", fail_applied)

    with pytest.raises(LinkError, match="prior destination restored"):
        link_config(
            tmp_path,
            environ=values,
            system="Linux",
            journal=journal,
            now=lambda: 9,
        )

    assert destination.read_text() == "original"


def test_atomic_npmrc_failure_preserves_original_and_rolls_back_links(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    npmrc = home / ".npmrc"
    npmrc.write_text("registry=https://example.invalid\n")
    source = tmp_path / "source"
    source.write_text("source")
    destination = home / ".config" / "example"
    monkeypatch.setattr(
        "dotfiles_setup.links.managed_links",
        lambda *_args, **_kwargs: (Link(source, destination),),
    )
    original_replace = os.replace

    def fail_npmrc(source_path: Path, destination_path: Path) -> None:
        if destination_path == npmrc:
            raise OSError("injected npmrc failure")
        original_replace(source_path, destination_path)

    monkeypatch.setattr("dotfiles_setup.links.os.replace", fail_npmrc)

    with pytest.raises(LinkError, match="atomically update"):
        link_config(tmp_path, environ=_environment(home), system="Linux", now=lambda: 5)

    assert npmrc.read_text() == "registry=https://example.invalid\n"
    assert not (destination.exists() or destination.is_symlink())


def test_interrupted_link_command_recovers_links_npm_and_codex(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir()
    values = _environment(home)
    npmrc = home / ".npmrc"
    npmrc.write_text("registry=https://example.invalid\n")
    journal = OperationJournal("link", Path.cwd(), environ=values)
    journal.transition("applying")

    link_config(Path.cwd(), environ=values, system=os.uname().sysname, journal=journal)
    assert (home / ".config" / "git").is_symlink()
    assert (home / ".npmrc").is_file()
    assert (home / ".codex" / "config.toml").is_file()

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0
    assert not (home / ".config" / "git").exists()
    assert npmrc.read_text() == "registry=https://example.invalid\n"
    assert not (home / ".codex" / "config.toml").exists()


def test_recovery_restores_prior_codex_config_symlink(tmp_path: Path) -> None:
    home = tmp_path / "home"
    codex_home = home / ".codex"
    codex_home.mkdir(parents=True)
    old_config = home / "old-codex-config.toml"
    old_config.write_text("[projects.example]\ntrust_level = 'trusted'\n")
    config = codex_home / "config.toml"
    config.symlink_to(old_config)
    values = _environment(home)
    journal = OperationJournal("link", Path.cwd(), environ=values)
    journal.transition("applying")

    link_config(Path.cwd(), environ=values, system=os.uname().sysname, journal=journal)
    assert config.is_file() and not config.is_symlink()
    assert "trust_level" not in (state_directory(values) / "current.json").read_text()

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0
    assert config.is_symlink()
    assert config.resolve() == old_config


def _interrupted_manifest(
    tmp_path: Path,
    *,
    changed: bool = False,
) -> tuple[dict[str, str], Path, Path]:
    home = tmp_path / "home"
    values = _environment(home)
    source = tmp_path / "config" / "git"
    source.mkdir(parents=True)
    destination = home / ".config" / "git"
    destination.parent.mkdir(parents=True)
    destination.symlink_to(tmp_path / "unrelated" if changed else source)
    backup = destination.with_name("git.backup.1")
    backup.write_text("original")
    prior = backup.lstat()
    journal = OperationJournal("link", tmp_path, environ=values)
    journal.add_link_entry(
        {
            "destination": str(destination),
            "source": str(source),
            "prior_kind": "file",
            "prior_target": None,
            "prior_device": prior.st_dev,
            "prior_inode": prior.st_ino,
            "backup": str(backup),
            "result_kind": "symlink",
            "result_target": str(source),
            "mutation_started": True,
            "applied": True,
            "recovered": False,
        }
    )
    journal.transition("applying")
    return values, destination, backup


def test_recovery_dry_run_is_read_only(tmp_path: Path) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path)
    output: list[str] = []

    assert run_recovery(environ=values, output=output.append) == 0

    assert destination.is_symlink()
    assert backup.read_text() == "original"
    assert any("Dry run only" in line for line in output)


def test_successful_recovery_is_idempotent(tmp_path: Path) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path)

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0
    assert destination.read_text() == "original"
    assert not backup.exists()
    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0


def test_recovery_recognizes_restore_completed_before_checkpoint(tmp_path: Path) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path)
    destination.unlink()
    os.replace(backup, destination)

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0
    assert destination.read_text() == "original"
    assert not backup.exists()


def test_recovery_restores_link_removed_by_interrupted_uninstall(tmp_path: Path) -> None:
    home = tmp_path / "home"
    values = _environment(home)
    source = tmp_path / "config" / "git"
    source.mkdir(parents=True)
    destination = home / ".config" / "git"
    destination.parent.mkdir(parents=True)
    journal = OperationJournal("uninstall", tmp_path, environ=values)
    journal.add_link_entry(
        {
            "destination": str(destination),
            "source": str(source),
            "prior_kind": "symlink",
            "prior_target": str(source),
            "prior_device": None,
            "prior_inode": None,
            "backup": None,
            "result_kind": "absent",
            "result_target": None,
            "mutation_started": True,
            "applied": True,
            "recovered": False,
        }
    )
    journal.transition("applying")

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0
    assert destination.is_symlink()
    assert destination.resolve() == source


def test_recovery_refuses_changed_destination(tmp_path: Path) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path, changed=True)

    with pytest.raises(RecoveryError, match="recovery remains incomplete"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert destination.is_symlink()
    assert backup.read_text() == "original"


def test_recovery_rejects_destination_outside_managed_inventory(tmp_path: Path) -> None:
    values, _destination, _backup = _interrupted_manifest(tmp_path)
    manifest_path = state_directory(values) / "current.json"
    manifest = read_manifest(manifest_path)
    unrelated = tmp_path / "unrelated"
    unrelated.write_text("preserve")
    manifest["entries"][0]["destination"] = str(unrelated)
    manifest_path.write_text(json.dumps(manifest))
    manifest_path.chmod(0o600)

    with pytest.raises(RecoveryError, match="outside the managed inventory"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert unrelated.read_text() == "preserve"


def test_recovery_rejects_lexical_parent_traversal(tmp_path: Path) -> None:
    values, _destination, _backup = _interrupted_manifest(tmp_path)
    manifest_path = state_directory(values) / "current.json"
    manifest = read_manifest(manifest_path)
    home = Path(values["HOME"])
    manifest["entries"][0]["destination"] = str(home / ".." / "unrelated")
    manifest_path.write_text(json.dumps(manifest))
    manifest_path.chmod(0o600)

    with pytest.raises(RecoveryError, match="non-normalized destination"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)


def test_manifest_transitions_and_contains_no_user_contents(tmp_path: Path) -> None:
    values = _environment(tmp_path / "home")
    journal = OperationJournal("git-user", tmp_path, environ=values)
    journal.transition("applying")
    journal.record_operation("git-user", "completed")
    journal.transition("completed")

    contents = (state_directory(values) / "completed.json").read_text()
    manifest = json.loads(contents)
    assert manifest["state"] == "completed"
    assert "william@example.com" not in contents
    assert "trust_level" not in contents
    assert "file_contents" not in contents


def test_new_mutation_refuses_to_overwrite_interrupted_manifest(tmp_path: Path) -> None:
    values = _environment(tmp_path / "home")
    journal = OperationJournal("link", tmp_path, environ=values)
    journal.transition("applying")

    with pytest.raises(ManifestError, match="run ./bootstrap.sh recover"):
        OperationJournal("install", tmp_path, environ=values)


def test_new_journal_promotes_completed_current_manifest(tmp_path: Path) -> None:
    values = _environment(tmp_path / "home")
    first = OperationJournal("link", tmp_path, environ=values)
    first.transition("completed")
    first.completed_path.write_text("stale completed snapshot\n")

    second = OperationJournal("profile", tmp_path, environ=values)

    promoted = read_manifest(second.completed_path)
    assert promoted["operation_id"] == first.data["operation_id"]


def test_failed_direct_mutation_is_reported_as_recovery_needed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setattr(
        cli,
        "ensure_profile",
        lambda _repo: (_ for _ in ()).throw(NixProfileError("injected profile failure")),
    )

    assert cli.main(["profile"]) == 1

    manifest = read_manifest(state_directory() / "recovery-needed.json")
    assert manifest["state"] == "recovery-needed"
    assert "injected profile failure" in capsys.readouterr().out
