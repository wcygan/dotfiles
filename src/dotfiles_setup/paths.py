"""Resolve all managed user paths from one explicit environment context."""

from __future__ import annotations

import os
import platform
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class UserPathContext:
    """The normalized path and platform policy for one user operation."""

    home: Path
    config_home: Path
    state_home: Path
    cache_home: Path
    codex_home: Path
    platform: str

    @classmethod
    def from_environment(
        cls,
        environ: Mapping[str, str] | None = None,
        *,
        system: str | None = None,
        home: Path | None = None,
    ) -> UserPathContext:
        """Build a context from injected values and conventional fallbacks."""

        values = os.environ if environ is None else environ
        configured_home = home
        if configured_home is None:
            home_value = values.get("HOME")
            configured_home = Path(home_value) if home_value is not None else Path.home()
        resolved_home = configured_home.expanduser().resolve()
        return cls(
            home=resolved_home,
            config_home=_absolute_override(
                values.get("XDG_CONFIG_HOME", ""), resolved_home / ".config"
            ),
            state_home=_absolute_override(
                values.get("XDG_STATE_HOME", ""), resolved_home / ".local" / "state"
            ),
            cache_home=_absolute_override(
                values.get("XDG_CACHE_HOME", ""), resolved_home / ".cache"
            ),
            codex_home=_absolute_override(
                values.get("CODEX_HOME", ""), resolved_home / ".codex"
            ),
            platform=system or platform.system(),
        )

    @property
    def state_directory(self) -> Path:
        """Return the private setup state directory."""

        return self.state_home / "dotfiles"

    @property
    def mutation_lock_path(self) -> Path:
        """Return the user-scoped setup mutation lock."""

        return self.cache_home / "dotfiles" / "setup.lock"

    @property
    def vscode_config_home(self) -> Path:
        """Return the platform-specific VS Code user directory."""

        if self.platform.lower() == "darwin":
            return self.home / "Library" / "Application Support" / "Code" / "User"
        return self.config_home / "Code" / "User"

    def agent_skills_target(self, directory: str | Path = ".agents/skills") -> Path:
        """Resolve a configured shared skill directory inside HOME."""

        relative = Path(directory)
        if relative.is_absolute() or any(part == ".." for part in relative.parts):
            raise ValueError("agent skill target must be a relative path inside HOME")
        destination = (self.home / relative).resolve(strict=False)
        if not destination.is_relative_to(self.home):
            raise ValueError("agent skill target must be a relative path inside HOME")
        return destination


def _absolute_override(value: str, fallback: Path) -> Path:
    configured = Path(value)
    if configured.is_absolute():
        return configured.resolve(strict=False)
    return fallback
