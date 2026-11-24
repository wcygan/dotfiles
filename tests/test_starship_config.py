import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[1] / ".agents/skills/starship-config/scripts/test-config.sh"
)


@pytest.mark.parametrize("valid", [True, False], ids=["valid-prompt", "invalid-toml"])
def test_starship_config_check_runs_without_editor(tmp_path: Path, valid: bool) -> None:
    config = tmp_path / "example prompt.toml"
    config.write_text(
        'format = "$character"\n[character]\nsuccess_symbol = "[ok](green)"\n'
        if valid
        else "[character\n"
    )
    calls = tmp_path / "calls"
    starship = tmp_path / "starship"
    starship.write_text(
        '#!/bin/sh\n'
        'echo "$1" >> "$CALLS"\n'
        '[ "$STARSHIP_CONFIG" = "$EXPECTED_CONFIG" ] || exit 1\n'
        'case "$1" in\n'
        '  prompt) echo "Rendered example prompt" ;;\n'
        '  explain|print-config|timings) exit 0 ;;\n'
        '  *) exit 1 ;;\n'
        'esac\n'
    )
    starship.chmod(0o755)
    result = subprocess.run(
        ["bash", str(SCRIPT), str(config)],
        cwd=tmp_path,
        env={
            **os.environ,
            "PATH": os.pathsep.join((str(tmp_path), os.environ["PATH"])),
            "EXPECTED_CONFIG": str(config),
            "CALLS": str(calls),
        },
        capture_output=True,
        text=True,
    )

    if valid:
        assert result.returncode == 0, result.stderr
        assert "Rendered example prompt" in result.stdout
        assert "config" not in calls.read_text().splitlines()
    else:
        assert result.returncode != 0
        assert "TOML syntax invalid" in result.stdout
        assert not calls.exists()
