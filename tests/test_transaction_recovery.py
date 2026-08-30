from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import replace
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup import mutations as mutations_module
from dotfiles_setup import recovery as recovery_module
from dotfiles_setup.errors import LinkError, ManifestError, RecoveryError
from dotfiles_setup.links import Link, link_config
from dotfiles_setup.manifest import (
    ManifestRepository,
    OperationJournal,
    read_manifest,
    state_directory,
)
from dotfiles_setup.mutations import (
    DirectoryRecoveryRecord,
    FileMutation,
    FileRecoveryRecord,
    LinkRecoveryRecord,
    decode_recovery_record,
    execute_mutations,
)
from dotfiles_setup.nix_profile import NixProfileError
from dotfiles_setup.recovery import run_recovery


def _environment(home: Path) -> dict[str, str]:
    return {"HOME": str(home), "DOTFILES_SKIP_FISH_GREETING": "1"}


def _write_codex_template(repo_root: Path) -> None:
    template = repo_root / "config" / "codex" / "config.toml"
    template.parent.mkdir(parents=True)
    template.write_text("model = 'test'\n")


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
    _write_codex_template(tmp_path)
    original_symlink = mutations_module._create_symlink

    def fail_destination_symlink(
        source_path: Path | str, destination_path: Path | str, **kwargs: object
    ) -> None:
        if Path(destination_path) == destination:
            raise OSError("injected replacement failure")
        original_symlink(source_path, destination_path, **kwargs)

    monkeypatch.setattr(mutations_module, "_create_symlink", fail_destination_symlink)

    with pytest.raises(LinkError, match="recovery manifest preserved"):
        link_config(
            tmp_path,
            environ=_environment(home),
            system="Linux",
            now=lambda: 123,
        )

    assert destination.read_text() == "original"
    assert not list(destination.parent.glob("example.backup.123.*"))
    manifest = read_manifest(state_directory(_environment(home)) / "current.json")
    assert manifest["state"] == "recovery-needed"


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
    _write_codex_template(tmp_path)
    original_symlink = mutations_module._create_symlink
    original_move = mutations_module._move_no_replace

    def fail_destination_symlink(
        source_path: Path | str, destination_path: Path | str, **kwargs: object
    ) -> None:
        if Path(destination_path) == destination:
            raise OSError("injected replacement failure")
        original_symlink(source_path, destination_path, **kwargs)

    def fail_restore(
        source_path: Path,
        destination_path: Path,
        **kwargs: object,
    ) -> None:
        if Path(source_path).name.startswith("example.backup"):
            raise OSError("injected restore failure")
        original_move(source_path, destination_path, **kwargs)

    monkeypatch.setattr(mutations_module, "_create_symlink", fail_destination_symlink)
    monkeypatch.setattr(mutations_module, "_move_no_replace", fail_restore)

    with pytest.raises(LinkError, match="recovery manifest preserved"):
        link_config(
            tmp_path,
            environ=_environment(home),
            system="Linux",
            now=lambda: 123,
        )

    manifest = read_manifest(state_directory(_environment(home)) / "current.json")
    assert manifest["state"] == "recovery-needed"
    assert not (destination.exists() or destination.is_symlink())
    entry = next(
        item for item in manifest["entries"] if item["destination"] == str(destination)
    )
    assert Path(entry["backup"]).read_text() == "original"
    monkeypatch.setattr(mutations_module, "_move_no_replace", original_move)
    monkeypatch.setattr(mutations_module, "_create_symlink", original_symlink)
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
    _write_codex_template(tmp_path)
    journal = OperationJournal("link", tmp_path, environ=values)
    journal.transition("applying")
    def fail_applied(index: int) -> None:
        raise ManifestError("injected manifest failure")

    monkeypatch.setattr(journal, "mark_applied", fail_applied)

    with pytest.raises(LinkError, match="recovery manifest preserved"):
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
    _write_codex_template(tmp_path)
    original_move = mutations_module._move_no_replace

    def fail_npmrc(
        source_path: Path, destination_path: Path, **kwargs: object
    ) -> None:
        if (
            destination_path == npmrc
            and "npmrc.dotfiles." in source_path.name
        ):
            raise OSError("injected npmrc failure")
        original_move(source_path, destination_path, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", fail_npmrc)

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


def test_interrupted_link_command_recovers_a_missing_external_config_root(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    external_parent = tmp_path / "external"
    external_parent.mkdir()
    config_home = external_parent / "config"
    values = {
        **_environment(home),
        "XDG_CONFIG_HOME": str(config_home),
    }
    journal = OperationJournal("link", Path.cwd(), environ=values)
    journal.transition("applying")

    link_config(Path.cwd(), environ=values, system=os.uname().sysname, journal=journal)
    assert config_home.is_dir()
    assert (config_home / "git").is_symlink()

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0
    assert not config_home.exists()


def test_recovery_accepts_a_missing_parent_planned_by_directory_records(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path.resolve()
    home = root / "home"
    values = {
        **_environment(home),
        "XDG_STATE_HOME": str(root / "state"),
    }
    journal = OperationJournal("link", Path.cwd(), environ=values)
    journal.transition("applying")
    real_replace = journal.replace_entry

    def interrupt_file_stage(index: int, entry: object) -> None:
        if isinstance(entry, FileRecoveryRecord):
            raise SystemExit("injected interruption")
        assert isinstance(entry, DirectoryRecoveryRecord)
        real_replace(index, entry)

    monkeypatch.setattr(journal, "replace_entry", interrupt_file_stage)

    with pytest.raises(SystemExit, match="injected interruption"):
        execute_mutations(
            (
                FileMutation(
                    destination=home / ".npmrc",
                    visible_destination=home / ".npmrc",
                    source="npmrc",
                    contents=b"managed\n",
                ),
            ),
            journal=journal,
            authority_roots=(home,),
        )

    assert not home.exists()
    file_entry = next(
        entry
        for entry in journal.data["entries"]
        if entry.get("entry_type") == "file"
    )
    assert file_entry["mutation_started"] is True
    assert Path(file_entry["stage_path"]).is_file()

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0
    assert not home.exists()
    assert Path(file_entry["stage_path"]).is_file()


def test_recovery_restores_a_file_when_applied_checkpoint_is_interrupted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    destination = home / ".npmrc"
    destination.write_text("original\n")
    values = {
        **_environment(home),
        "XDG_STATE_HOME": str(tmp_path / "state"),
    }
    journal = OperationJournal("link", Path.cwd(), environ=values)
    journal.transition("applying")

    def interrupt_applied(_index: int) -> None:
        raise SystemExit("injected applied checkpoint interruption")

    monkeypatch.setattr(journal, "mark_applied", interrupt_applied)

    with pytest.raises(SystemExit, match="applied checkpoint interruption"):
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="npmrc",
                    contents=b"managed\n",
                ),
            ),
            journal=journal,
            authority_roots=(home,),
        )

    entry = journal.entry(0)
    assert isinstance(entry, FileRecoveryRecord)
    assert entry.mutation_started
    assert not entry.applied
    assert entry.result_mode == 0o600
    assert entry.result_device == destination.stat().st_dev
    assert entry.result_inode == destination.stat().st_ino
    assert destination.read_bytes() == b"managed\n"

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0
    assert destination.read_bytes() == b"original\n"


@pytest.mark.parametrize("change", ("chmod", "same-content-replacement"))
def test_recovery_preserves_a_changed_file_result_identity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    change: str,
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    destination = home / ".npmrc"
    destination.write_text("original\n")
    values = {
        **_environment(home),
        "XDG_STATE_HOME": str(tmp_path / "state"),
    }
    journal = OperationJournal("link", Path.cwd(), environ=values)
    journal.transition("applying")

    def interrupt_applied(_index: int) -> None:
        raise SystemExit("injected applied checkpoint interruption")

    monkeypatch.setattr(journal, "mark_applied", interrupt_applied)
    with pytest.raises(SystemExit, match="applied checkpoint interruption"):
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="npmrc",
                    contents=b"managed\n",
                ),
            ),
            journal=journal,
            authority_roots=(home,),
        )

    record = journal.entry(0)
    assert isinstance(record, FileRecoveryRecord)
    if change == "chmod":
        destination.chmod(0o644)
    else:
        replacement = home / "replacement"
        replacement.write_bytes(b"managed\n")
        replacement.chmod(record.result_mode or 0o600)
        os.replace(replacement, destination)

    output: list[str] = []
    with pytest.raises(RecoveryError, match="recovery remains incomplete"):
        run_recovery(
            environ=values,
            apply=True,
            yes=True,
            output=output.append,
        )

    assert destination.read_bytes() == b"managed\n"
    if change == "chmod":
        assert stat.S_IMODE(destination.stat().st_mode) == 0o644
    else:
        assert destination.stat().st_ino != record.result_inode
    assert record.backup is not None
    assert record.backup.read_text() == "original\n"
    assert any("current state changed" in line for line in output)


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


def test_recovery_keeps_the_live_result_when_a_required_backup_is_missing(
    tmp_path: Path,
) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path)
    identity = destination.lstat()
    backup.unlink()
    output: list[str] = []

    with pytest.raises(RecoveryError, match="recovery remains incomplete"):
        run_recovery(
            environ=values,
            apply=True,
            yes=True,
            output=output.append,
        )

    current = destination.lstat()
    assert destination.is_symlink()
    assert (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino)
    assert any("required prior backup" in line for line in output)


def test_unresolved_recovery_reports_every_retained_file_quarantine(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    destination = home / ".npmrc"
    destination.write_bytes(b"managed\n")
    stage = destination.with_name(f".{destination.name}.dotfiles.stage")
    stage.write_bytes(b"staged\n")
    result_backup = destination.with_name(
        f".{destination.name}.dotfiles-result.test"
    )
    result_backup.write_bytes(b"managed\n")
    missing_backup = destination.with_name(".npmrc.backup.missing")
    values = {
        **_environment(home),
        "XDG_STATE_HOME": str(tmp_path / "state"),
    }
    journal = OperationJournal("link", Path.cwd(), environ=values)
    journal.add_entry(
        FileRecoveryRecord(
            destination=destination,
            visible_destination=destination,
            source="npmrc",
            prior_kind="file",
            prior_target=None,
            prior_hash=hashlib.sha256(b"original\n").hexdigest(),
            backup=missing_backup,
            result_hash=hashlib.sha256(b"managed\n").hexdigest(),
            result_backup=result_backup,
            stage_path=stage,
            mutation_started=True,
            applied=True,
        )
    )
    journal.transition("applying")
    output: list[str] = []

    with pytest.raises(RecoveryError, match="recovery remains incomplete"):
        run_recovery(
            environ=values,
            apply=True,
            yes=True,
            output=output.append,
        )

    failure = next(line for line in output if line.startswith("[FAIL]"))
    assert str(stage) in failure
    assert str(result_backup) in failure
    assert destination.read_bytes() == b"managed\n"
    assert stage.read_bytes() == b"staged\n"
    assert result_backup.read_bytes() == b"managed\n"


def test_recovery_preserves_legacy_and_future_entry_fields(tmp_path: Path) -> None:
    values, destination, _backup = _interrupted_manifest(tmp_path)
    current_path = state_directory(values) / "current.json"
    manifest = read_manifest(current_path)
    manifest["entries"][0]["future_safe_field"] = "preserve-me"
    current_path.write_text(json.dumps(manifest))
    current_path.chmod(0o600)

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0

    completed = read_manifest(state_directory(values) / "completed.json")
    assert completed["entries"][0]["future_safe_field"] == "preserve-me"
    assert "entry_type" not in completed["entries"][0]
    assert destination.read_text() == "original"


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


def test_recovery_preserves_a_destination_changed_at_the_move_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path)
    real_move = mutations_module._move_no_replace

    def move_with_swap(source: Path, target: Path, **kwargs: object) -> None:
        if Path(source) == destination and ".dotfiles-result." in Path(target).name:
            destination.unlink()
            destination.write_text("user change")
        real_move(source, target, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", move_with_swap)

    with pytest.raises(RecoveryError, match="recovery remains incomplete"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert destination.read_text() == "user change"
    assert backup.read_text() == "original"


def test_recovery_refuses_a_parent_replaced_after_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    values, destination, _backup = _interrupted_manifest(tmp_path)
    original_parent = destination.parent
    displaced_parent = original_parent.with_name("displaced-config")
    expected_source = destination.resolve()
    real_persist = recovery_module._persist_progress
    swapped = False

    def persist_then_swap(*args: object, **kwargs: object) -> None:
        nonlocal swapped
        real_persist(*args, **kwargs)
        if swapped:
            return
        swapped = True
        original_parent.rename(displaced_parent)
        original_parent.mkdir()
        destination.symlink_to(expected_source)

    monkeypatch.setattr(recovery_module, "_persist_progress", persist_then_swap)

    with pytest.raises(RecoveryError, match="recovery remains incomplete"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert destination.is_symlink()
    assert destination.resolve() == expected_source
    assert (displaced_parent / "git.backup.1").read_text() == "original"


def test_recovery_refuses_a_parent_removed_after_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    values, destination, _backup = _interrupted_manifest(tmp_path)
    original_parent = destination.parent
    displaced_parent = original_parent.with_name("displaced-config")
    expected_source = destination.resolve()
    real_persist = recovery_module._persist_progress
    removed = False

    def persist_then_remove(*args: object, **kwargs: object) -> None:
        nonlocal removed
        real_persist(*args, **kwargs)
        if removed:
            return
        removed = True
        original_parent.rename(displaced_parent)

    monkeypatch.setattr(recovery_module, "_persist_progress", persist_then_remove)
    output: list[str] = []

    with pytest.raises(RecoveryError, match="recovery remains incomplete"):
        run_recovery(environ=values, apply=True, yes=True, output=output.append)

    assert not original_parent.exists()
    displaced_destination = displaced_parent / destination.name
    assert displaced_destination.is_symlink()
    assert displaced_destination.resolve() == expected_source
    assert (displaced_parent / "git.backup.1").read_text() == "original"
    assert any("recovery path is unavailable" in line for line in output)
    assert (state_directory(values) / "recovery-needed.json").exists()


def test_recovery_restores_a_legacy_link_symlink_without_a_backup(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    values = _environment(home)
    source = tmp_path / "config" / "git"
    source.mkdir(parents=True)
    prior_source = tmp_path / "prior-git"
    prior_source.mkdir()
    destination = home / ".config" / "git"
    destination.parent.mkdir(parents=True)
    destination.symlink_to(prior_source)
    prior_identity = destination.lstat()
    destination.unlink()
    destination.symlink_to(source)
    journal = OperationJournal("link", tmp_path, environ=values)
    journal.add_link_entry(
        {
            "destination": str(destination),
            "source": str(source),
            "prior_kind": "symlink",
            "prior_target": str(prior_source),
            "prior_device": prior_identity.st_dev,
            "prior_inode": prior_identity.st_ino,
            "backup": None,
            "result_kind": "symlink",
            "result_target": str(source),
            "mutation_started": True,
            "applied": True,
            "recovered": False,
        }
    )
    journal.transition("applying")

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0

    assert destination.is_symlink()
    assert destination.resolve() == prior_source


def test_recovery_restores_a_legacy_file_symlink_without_a_backup(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    values = _environment(home)
    codex_home = home / ".codex"
    codex_home.mkdir(parents=True)
    prior_config = home / "prior-codex.toml"
    prior_config.write_text("model = 'prior'\n")
    destination = codex_home / "config.toml"
    destination.write_bytes(b"model = 'managed'\n")
    raw = {
        "entry_type": "file",
        "destination": str(destination),
        "visible_destination": str(destination),
        "source": "codex-template",
        "prior_kind": "symlink",
        "prior_target": str(prior_config),
        "prior_hash": None,
        "backup": None,
        "result_kind": "file",
        "result_target": None,
        "result_hash": hashlib.sha256(b"model = 'managed'\n").hexdigest(),
        "mutation_started": True,
        "applied": True,
        "recovered": False,
    }
    journal = OperationJournal("link", tmp_path, environ=values)
    journal.add_entry(decode_recovery_record(raw))
    journal.transition("applying")

    assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0

    assert destination.is_symlink()
    assert destination.resolve() == prior_config


def test_file_recovery_refuses_a_visible_link_replaced_after_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    values = _environment(home)
    destination = home / "shell-target"
    destination.write_text("managed")
    visible = home / ".zshrc"
    visible.symlink_to(destination)
    visible_identity = visible.lstat()
    replacement = home / "replacement"
    replacement.write_text("user content")
    backup = destination.with_name("shell-target.backup.1")
    backup.write_text("original")
    journal = OperationJournal("shell-handoff", tmp_path, environ=values)
    index = journal.add_entry(
        FileRecoveryRecord(
            destination=destination,
            visible_destination=visible,
            source="shell-handoff",
            prior_kind="file",
            prior_target=None,
            prior_hash=hashlib.sha256(b"original").hexdigest(),
            backup=backup,
            result_hash=hashlib.sha256(b"managed").hexdigest(),
            visible_kind="symlink",
            visible_target=str(destination),
            visible_device=visible_identity.st_dev,
            visible_inode=visible_identity.st_ino,
            result_backup=destination.with_name(".shell-target.dotfiles-result.test"),
        )
    )
    journal.mark_started(index)
    journal.mark_applied(index)
    journal.transition("applying")
    real_persist = recovery_module._persist_progress
    swapped = False

    def persist_then_swap(*args: object, **kwargs: object) -> None:
        nonlocal swapped
        real_persist(*args, **kwargs)
        if swapped:
            return
        swapped = True
        visible.unlink()
        visible.symlink_to(replacement)

    monkeypatch.setattr(recovery_module, "_persist_progress", persist_then_swap)

    with pytest.raises(RecoveryError, match="recovery remains incomplete"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert visible.resolve() == replacement
    assert destination.read_text() == "managed"
    assert backup.read_text() == "original"


def test_recovery_refuses_an_applied_result_that_disappeared(tmp_path: Path) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path)
    destination.unlink()

    with pytest.raises(RecoveryError, match="recovery remains incomplete"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert not destination.exists()
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


def test_recovery_rejects_an_unknown_entry_type(tmp_path: Path) -> None:
    values, _destination, _backup = _interrupted_manifest(tmp_path)
    manifest_path = state_directory(values) / "current.json"
    manifest = read_manifest(manifest_path)
    manifest["entries"][0]["entry_type"] = "command"
    manifest_path.write_text(json.dumps(manifest))
    manifest_path.chmod(0o600)

    with pytest.raises(RecoveryError, match="unsupported recovery entry type"):
        run_recovery(environ=values)


def test_recovery_retains_an_invalid_progress_manifest(tmp_path: Path) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path)
    manifest_path = state_directory(values) / "current.json"
    manifest = read_manifest(manifest_path)
    manifest["entries"][0]["mutation_started"] = False
    manifest_path.write_text(json.dumps(manifest))
    manifest_path.chmod(0o600)

    with pytest.raises(RecoveryError, match="applied without a started mutation"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert manifest_path.is_file()
    assert destination.is_symlink()
    assert backup.read_text() == "original"


def test_recovery_rejects_a_restored_entry_with_active_progress(tmp_path: Path) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path)
    manifest_path = state_directory(values) / "current.json"
    manifest = read_manifest(manifest_path)
    manifest["entries"][0].update(recovered=True, restored=True)
    manifest_path.write_text(json.dumps(manifest))
    manifest_path.chmod(0o600)

    with pytest.raises(RecoveryError, match="progress remains active"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert manifest_path.is_file()
    assert destination.is_symlink()
    assert backup.read_text() == "original"


def test_recovery_rejects_an_absent_prior_with_an_injected_backup(
    tmp_path: Path,
) -> None:
    values, destination, backup = _interrupted_manifest(tmp_path)
    manifest_path = state_directory(values) / "current.json"
    manifest = read_manifest(manifest_path)
    manifest["entries"][0].update(
        prior_kind="absent",
        prior_target=None,
        prior_device=None,
        prior_inode=None,
    )
    manifest_path.write_text(json.dumps(manifest))
    manifest_path.chmod(0o600)

    with pytest.raises(RecoveryError, match="invalid prior state"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert manifest_path.is_file()
    assert destination.is_symlink()
    assert backup.read_text() == "original"


def test_recovery_refuses_a_file_backup_with_changed_mode(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir()
    destination = home / ".npmrc"
    destination.write_text("managed\n")
    backup = home / ".npmrc.backup.1"
    backup.write_text("original\n")
    backup.chmod(0o600)
    identity = backup.lstat()
    values = {
        **_environment(home),
        "XDG_STATE_HOME": str(tmp_path / "state"),
    }
    journal = OperationJournal("link", Path.cwd(), environ=values)
    journal.add_entry(
        FileRecoveryRecord(
            destination=destination,
            visible_destination=destination,
            source="npmrc",
            prior_kind="file",
            prior_target=None,
            prior_hash=hashlib.sha256(b"original\n").hexdigest(),
            prior_mode=0o600,
            prior_device=identity.st_dev,
            prior_inode=identity.st_ino,
            backup=backup,
            result_hash=hashlib.sha256(b"managed\n").hexdigest(),
            mutation_started=True,
            applied=True,
        )
    )
    journal.transition("applying")
    backup.chmod(0o644)

    with pytest.raises(RecoveryError, match="backup mode changed"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert destination.read_text() == "managed\n"
    assert backup.read_text() == "original\n"
    assert stat.S_IMODE(backup.stat().st_mode) == 0o644


def test_recovery_rejects_a_directory_through_a_symlinked_parent(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    outside = tmp_path / "outside"
    home.mkdir()
    outside.mkdir()
    created = outside / "bin"
    created.mkdir()
    (home / ".local").symlink_to(outside, target_is_directory=True)
    identity = created.lstat()
    values = {
        **_environment(home),
        "XDG_STATE_HOME": str(tmp_path / "state"),
    }
    journal = OperationJournal("link", Path.cwd(), environ=values)
    journal.transition("applying")
    index = journal.add_entry(
        DirectoryRecoveryRecord(
            destination=home / ".local" / "bin",
            result_device=identity.st_dev,
            result_inode=identity.st_ino,
            result_backup=home / ".local" / ".bin.dotfiles-result.test",
        )
    )
    journal.mark_started(index)
    journal.mark_applied(index)

    with pytest.raises(RecoveryError, match="parent path is unsafe"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert created.is_dir()


def test_recovery_rejects_a_result_quarantine_outside_the_destination_directory(
    tmp_path: Path,
) -> None:
    values, destination, _backup = _interrupted_manifest(tmp_path)
    manifest_path = state_directory(values) / "current.json"
    manifest = read_manifest(manifest_path)
    outside = tmp_path / "outside-result"
    outside.symlink_to(destination.resolve())
    manifest["entries"][0]["result_backup"] = str(outside)
    manifest_path.write_text(json.dumps(manifest))
    manifest_path.chmod(0o600)

    with pytest.raises(RecoveryError, match="outside the managed destination path"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)

    assert outside.is_symlink()


def test_recovery_rejects_a_root_parent_quarantine_without_missing_root_proof(
    tmp_path: Path,
) -> None:
    values, destination, _backup = _interrupted_manifest(tmp_path)
    manifest_path = state_directory(values) / "current.json"
    manifest = read_manifest(manifest_path)
    home = Path(values["HOME"])
    manifest["entries"][0]["result_backup"] = str(
        home.parent / f".{destination.name}.dotfiles-result.test"
    )
    manifest_path.write_text(json.dumps(manifest))
    manifest_path.chmod(0o600)

    with pytest.raises(RecoveryError, match="outside the managed destination path"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)


def test_recovery_rejects_a_result_target_outside_the_inventory(tmp_path: Path) -> None:
    values, _destination, _backup = _interrupted_manifest(tmp_path)
    manifest_path = state_directory(values) / "current.json"
    manifest = read_manifest(manifest_path)
    manifest["entries"][0]["result_target"] = str(tmp_path / "unmanaged")
    manifest_path.write_text(json.dumps(manifest))
    manifest_path.chmod(0o600)

    with pytest.raises(RecoveryError, match="invalid result target"):
        run_recovery(environ=values, apply=True, yes=True, output=lambda _: None)


def test_recovery_uses_the_injected_platform_for_inventory_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "home"
    values = _environment(home)
    source = tmp_path / "config" / "vscode" / "settings.json"
    source.parent.mkdir(parents=True)
    source.write_text("{}\n")
    destination = home / "Library" / "Application Support" / "Code" / "User" / "settings.json"
    destination.parent.mkdir(parents=True)
    destination.symlink_to(source)
    journal = OperationJournal("link", tmp_path, environ=values)
    index = journal.add_entry(
        LinkRecoveryRecord(
            destination=destination,
            source=source,
            prior_kind="absent",
            prior_target=None,
            prior_device=None,
            prior_inode=None,
            backup=None,
            result_kind="symlink",
            result_target=str(source),
            mutation_started=True,
            applied=True,
        )
    )
    assert index == 0
    journal.transition("applying")
    monkeypatch.setattr("dotfiles_setup.paths.platform.system", lambda: "Linux")

    assert run_recovery(environ=values, system="Darwin", output=lambda _: None) == 0


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


def test_typed_journal_methods_report_pending_and_failed_work(tmp_path: Path) -> None:
    values = _environment(tmp_path / "home")
    journal = OperationJournal("link", tmp_path, environ=values)
    index = journal.add_entry(
        LinkRecoveryRecord(
            destination=tmp_path / "destination",
            source=tmp_path / "source",
            prior_kind="absent",
            prior_target=None,
            prior_device=None,
            prior_inode=None,
            backup=None,
            result_kind="symlink",
            result_target=str(tmp_path / "source"),
        )
    )

    journal.mark_started(index)
    journal.mark_applied(index)
    journal.record_operation("links", "failed")

    assert journal.state == "planned"
    assert journal.failed_operations == ("links",)
    assert journal.pending_entries == (journal.entry(index),)

    journal.mark_restored(index)

    assert journal.pending_entries == ()


def test_journal_replacement_preserves_monotonic_progress(tmp_path: Path) -> None:
    values = _environment(tmp_path / "home")
    journal = OperationJournal("link", tmp_path, environ=values)
    record = FileRecoveryRecord(
        destination=tmp_path / "destination",
        visible_destination=tmp_path / "destination",
        source="npmrc",
        prior_kind="absent",
        prior_target=None,
        prior_hash=None,
        backup=None,
        result_hash="result-hash",
        stage_path=tmp_path / ".destination.dotfiles.stage",
    )
    index = journal.add_entry(record)
    journal.mark_started(index)
    journal.mark_applied(index)

    journal.replace_entry(index, record)

    replaced = journal.entry(index)
    assert replaced.mutation_started
    assert replaced.applied


def test_manifest_repository_owns_recovery_progress_and_completion(tmp_path: Path) -> None:
    values = _environment(tmp_path / "home")
    journal = OperationJournal("link", tmp_path, environ=values)
    index = journal.add_entry(
        LinkRecoveryRecord(
            destination=tmp_path / "destination",
            source=tmp_path / "source",
            prior_kind="absent",
            prior_target=None,
            prior_device=None,
            prior_inode=None,
            backup=None,
            result_kind="symlink",
            result_target=str(tmp_path / "source"),
        )
    )
    journal.mark_started(index)
    journal.data["future_safe_field"] = "preserve-me"
    journal.data["entries"][index]["future_entry_field"] = "preserve-me-too"
    repository = ManifestRepository(state_directory(values))

    repository.checkpoint_recovery(journal.active_path, journal.data)
    pending = repository.pending()

    assert pending is not None
    assert pending.data["future_safe_field"] == "preserve-me"
    assert pending.data["entries"][index]["future_entry_field"] == "preserve-me-too"

    repository.checkpoint_entry_recovery(
        pending.path,
        pending.data,
        index,
        replace(journal.entry(index), recovered=True),
    )
    pending = repository.pending()
    assert pending is not None
    repository.complete_recovery(pending.data)

    assert repository.pending() is None
    assert read_manifest(repository.completed_path)["state"] == "completed"


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
