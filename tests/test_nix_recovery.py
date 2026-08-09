from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def bootstrap_script() -> str:
    return (REPO_ROOT / "bootstrap.sh").read_text()


def test_existing_daemon_profile_is_sourced_before_nix_lookup() -> None:
    script = bootstrap_script()
    daemon_profile = "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh"

    assert daemon_profile in script
    assert "source_nix_profile" in script
    assert script.index(daemon_profile) < script.index("command -v nix")


def test_profile_recovery_tries_all_supported_locations_before_download() -> None:
    script = bootstrap_script()
    profiles = (
        "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh",
        "/etc/profile.d/nix.sh",
        '"$HOME/.nix-profile/etc/profile.d/nix.sh"',
    )
    recovery_section = script[: script.index("if ! command -v nix")]

    for profile in profiles:
        assert profile in recovery_section
    assert "source_nix_profile" in recovery_section


def test_remote_install_is_linux_only_and_requires_explicit_consent() -> None:
    script = bootstrap_script()

    assert "Darwin)" in script
    assert "Linux)" in script
    assert '"$install_nix" != true || "$assume_yes" != true' in script
    assert "curl --proto '=https' --tlsv1.2 -sSf -L \"$DETERMINATE_INSTALL_URL\"" in script
    assert "| sh -s -- install" in script
