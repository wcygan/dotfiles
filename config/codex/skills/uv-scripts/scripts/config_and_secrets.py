#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "keyring>=25,<26",
#   "platformdirs>=4,<5",
#   "pydantic>=2,<3",
#   "pydantic-settings>=2,<3",
#   "rich>=13,<15",
# ]
# ///
"""Gold-standard config and local secret handling example.

Run:
    uv run --script config_and_secrets.py --demo
    MY_TOOL_API_BASE=https://api.example.com uv run --script config_and_secrets.py paths
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import keyring
import keyring.backend
import keyring.errors
import platformdirs
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from rich.table import Table

console = Console()
error_console = Console(stderr=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MY_TOOL_", env_file=".env", extra="ignore"
    )

    app_name: str = "uv-script-demo"
    api_base: AnyHttpUrl = "https://api.example.com"
    account: str = "default"


@dataclass(frozen=True)
class AppPaths:
    config_dir: Path
    cache_dir: Path
    data_dir: Path


class MemoryKeyring(keyring.backend.KeyringBackend):
    priority = 1

    def __init__(self) -> None:
        self.values: dict[tuple[str, str], str] = {}

    def get_password(self, service: str, username: str) -> str | None:
        return self.values.get((service, username))

    def set_password(self, service: str, username: str, password: str) -> None:
        self.values[(service, username)] = password

    def delete_password(self, service: str, username: str) -> None:
        self.values.pop((service, username), None)


def resolve_paths(settings: Settings) -> AppPaths:
    return AppPaths(
        config_dir=Path(platformdirs.user_config_dir(settings.app_name)),
        cache_dir=Path(platformdirs.user_cache_dir(settings.app_name)),
        data_dir=Path(platformdirs.user_data_dir(settings.app_name)),
    )


def render_settings(settings: Settings, paths: AppPaths) -> None:
    table = Table(title="Config")
    table.add_column("Name")
    table.add_column("Value")
    table.add_row("app_name", settings.app_name)
    table.add_row("api_base", str(settings.api_base))
    table.add_row("account", settings.account)
    table.add_row("config_dir", str(paths.config_dir))
    table.add_row("cache_dir", str(paths.cache_dir))
    table.add_row("data_dir", str(paths.data_dir))
    console.print(table)


def token_service(settings: Settings) -> str:
    return f"{settings.app_name}:api-token"


def get_token(settings: Settings) -> str | None:
    return keyring.get_password(token_service(settings), settings.account)


def set_token(settings: Settings, token: str) -> None:
    keyring.set_password(token_service(settings), settings.account, token)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Demonstrate pydantic-settings, platformdirs, and keyring."
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["paths", "get-token", "set-token"],
        default="paths",
    )
    parser.add_argument("--token", help="Token to store when command is set-token.")
    parser.add_argument(
        "--demo", action="store_true", help="Use an in-memory keyring and demo token."
    )
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> int:
    if args.demo:
        keyring.set_keyring(MemoryKeyring())

    settings = Settings()
    paths = resolve_paths(settings)

    if args.command == "paths":
        render_settings(settings, paths)
        return 0

    if args.command == "set-token":
        token = args.token or ("demo-token" if args.demo else None)
        if token is None:
            error_console.print("[red]missing --token[/red]")
            return 2
        set_token(settings, token)
        console.print(
            f"[green]stored token[/green] service={token_service(settings)} account={settings.account}"
        )
        return 0

    if args.demo:
        set_token(settings, "demo-token")

    token = get_token(settings)
    if token is None:
        error_console.print("[red]no token found[/red]")
        return 1
    console.print(f"[green]token available[/green] length={len(token)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except keyring.errors.KeyringError as exc:
        error_console.print(f"[red]keyring failed[/red] {exc}")
        return 1
    except KeyboardInterrupt:
        error_console.print("[red]interrupted[/red]")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
