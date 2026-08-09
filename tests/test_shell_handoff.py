from __future__ import annotations

from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.shell_handoff import ShellHandoffResult, configure_shell_handoff


def test_configures_temp_home_with_legacy_markers_and_bash_login_blocks(tmp_path: Path) -> None:
    result = configure_shell_handoff(home=tmp_path, shell="/bin/bash", backup_timestamp=42)

    bashrc = (tmp_path / ".bashrc").read_text()
    assert 'source "$HOME/.config/shell-nix.sh" 2>/dev/null || true' in bashrc
    assert "if case $- in *i*) true;; *) false;; esac && [ -t 1 ]; then" in bashrc
    assert "DOTFILES:NIX_SHELL_HELPERS" in bashrc
    assert "DOTFILES:EXEC_FISH" in bashrc

    bash_profile = (tmp_path / ".bash_profile").read_text()
    assert "DOTFILES:BASH_PROFILE_SOURCE_BASHRC" in bash_profile
    assert "DOTFILES:BASH_PROFILE_SOURCE_PROFILE" in bash_profile
    assert (tmp_path / ".zshrc") in result.updated_files
    assert (tmp_path / ".zshenv").read_text().count("DOTFILES:NIX_PATH") == 1
    assert result.backups == ()


def test_zsh_shell_does_not_create_bash_profile(tmp_path: Path) -> None:
    configure_shell_handoff(home=tmp_path, shell="/bin/zsh", backup_timestamp=42)

    assert not (tmp_path / ".bash_profile").exists()
    assert "[[ -o interactive && -t 1 ]]" in (tmp_path / ".zshrc").read_text()


def test_rerunning_is_idempotent_and_does_not_create_new_backups(tmp_path: Path) -> None:
    first = configure_shell_handoff(home=tmp_path, shell="bash", backup_timestamp=42)
    second = configure_shell_handoff(home=tmp_path, shell="bash", backup_timestamp=99)

    assert first.updated_files
    assert second.updated_files == ()
    assert second.backups == ()
    assert (tmp_path / ".bashrc").read_text().count("DOTFILES:EXEC_FISH") == 1
    assert not list(tmp_path.glob(".*.backup.*"))


def test_existing_regular_files_are_backed_up_once_before_multiple_blocks(tmp_path: Path) -> None:
    bashrc = tmp_path / ".bashrc"
    bashrc.write_text("export PROJECT_VALUE=original\n")

    result = configure_shell_handoff(home=tmp_path, shell="/bin/zsh", backup_timestamp=42)

    backup = tmp_path / ".bashrc.backup.42"
    assert result.backups == (backup,)
    assert backup.read_text() == "export PROJECT_VALUE=original\n"
    assert "DOTFILES:NIX_SHELL_HELPERS" in bashrc.read_text()
    assert "DOTFILES:EXEC_FISH" in bashrc.read_text()


def test_existing_symlink_is_updated_without_a_backup(tmp_path: Path) -> None:
    target = tmp_path / "bashrc-target"
    target.write_text("export PROJECT_VALUE=original\n")
    (tmp_path / ".bashrc").symlink_to(target)

    result = configure_shell_handoff(home=tmp_path, shell="/bin/zsh", backup_timestamp=42)

    assert result.backups == ()
    assert "DOTFILES:EXEC_FISH" in target.read_text()


def test_shell_handoff_cli_reports_updated_files(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        cli,
        "configure_shell_handoff",
        lambda: ShellHandoffResult((Path(".bashrc"), Path(".zshrc")), ()),
    )

    assert cli.main(["shell-handoff"]) == 0
    assert "Updated 2" in capsys.readouterr().out
