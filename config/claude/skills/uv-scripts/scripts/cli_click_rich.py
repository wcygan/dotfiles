#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.1,<9",
#   "rich>=13,<15",
# ]
# ///
"""Gold-standard Click + Rich CLI example.

Run:
    uv run --script cli_click_rich.py demo
    uv run --script cli_click_rich.py summarize alpha beta gamma --json
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import click
from rich.console import Console
from rich.table import Table

console = Console()
error_console = Console(stderr=True)


@dataclass(frozen=True)
class ItemSummary:
    name: str
    characters: int
    words: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "characters": self.characters,
            "words": self.words,
        }


def summarize_item(value: str) -> ItemSummary:
    return ItemSummary(
        name=value,
        characters=len(value),
        words=len(value.split()),
    )


def render_summaries(summaries: list[ItemSummary]) -> None:
    table = Table(title="Item Summary")
    table.add_column("Item", style="cyan")
    table.add_column("Characters", justify="right")
    table.add_column("Words", justify="right")

    for summary in summaries:
        table.add_row(summary.name, str(summary.characters), str(summary.words))

    console.print(table)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--verbose", is_flag=True, help="Show extra status messages.")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Small reference CLI using Click for UX and Rich for output."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@cli.command()
def demo() -> None:
    """Run a no-input demo."""
    summaries = [summarize_item(value) for value in ["alpha", "beta value", "gamma"]]
    render_summaries(summaries)
    console.print("[green]demo complete[/green]")


@cli.command()
@click.argument("items", nargs=-1, required=True)
@click.option("--json", "json_output", is_flag=True, help="Emit machine-readable JSON.")
@click.pass_context
def summarize(ctx: click.Context, items: tuple[str, ...], json_output: bool) -> None:
    """Summarize one or more ITEM values."""
    if ctx.obj.get("verbose"):
        console.print(f"[dim]summarizing {len(items)} item(s)[/dim]")

    summaries = [summarize_item(item) for item in items]

    if json_output:
        console.print(
            json.dumps([summary.as_dict() for summary in summaries], indent=2)
        )
        return

    render_summaries(summaries)


def main(argv: list[str] | None = None) -> int:
    try:
        cli.main(args=argv, prog_name="cli_click_rich", standalone_mode=False)
    except click.ClickException as exc:
        exc.show(file=error_console.file)
        return exc.exit_code
    except KeyboardInterrupt:
        error_console.print("[red]interrupted[/red]")
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
