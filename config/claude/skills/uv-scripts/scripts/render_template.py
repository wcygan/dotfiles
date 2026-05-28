#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "jinja2>=3.1,<4",
#   "pydantic>=2,<3",
#   "pyyaml>=6,<7",
#   "rich>=13,<15",
# ]
# ///
"""Gold-standard template rendering with validation and atomic writes.

Run:
    uv run --script render_template.py --demo --output report.md
    uv run --script render_template.py data.yaml template.j2 --output report.md
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import yaml
from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel, Field
from rich.console import Console

console = Console()
error_console = Console(stderr=True)


class Metric(BaseModel):
    name: str
    value: str


class ReportData(BaseModel):
    title: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    metrics: list[Metric]


DEFAULT_TEMPLATE = """# {{ title }}

Owner: {{ owner }}

{% for metric in metrics -%}
- {{ metric.name }}: {{ metric.value }}
{% endfor -%}
"""


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def load_data(path: Path | None, demo: bool) -> ReportData:
    if demo:
        return ReportData(
            title="Demo Report",
            owner="uv-scripts",
            metrics=[
                Metric(name="rows", value="42"),
                Metric(name="status", value="green"),
            ],
        )
    if path is None:
        raise ValueError("missing data path")
    return ReportData.model_validate(yaml.safe_load(path.read_text()))


def load_template(path: Path | None, demo: bool) -> str:
    if demo:
        return DEFAULT_TEMPLATE
    if path is None:
        raise ValueError("missing template path")
    return path.read_text()


def render_report(data: ReportData, template_source: str) -> str:
    environment = Environment(undefined=StrictUndefined, autoescape=False)
    template = environment.from_string(template_source)
    return template.render(**data.model_dump())


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a validated Jinja template.")
    parser.add_argument("data", nargs="?", type=Path, help="YAML data file.")
    parser.add_argument("template", nargs="?", type=Path, help="Jinja template file.")
    parser.add_argument(
        "--output", type=Path, help="Output path. Prints to stdout when omitted."
    )
    parser.add_argument(
        "--demo", action="store_true", help="Render embedded demo data and template."
    )
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> int:
    data = load_data(args.data, args.demo)
    template = load_template(args.template, args.demo)
    rendered = render_report(data, template)

    if args.output is None:
        console.print(rendered)
    else:
        atomic_write_text(args.output, rendered)
        console.print(f"[green]rendered[/green] {args.output}")

    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        error_console.print(f"[red]render failed[/red] {exc}")
        return 1
    except KeyboardInterrupt:
        error_console.print("[red]interrupted[/red]")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
