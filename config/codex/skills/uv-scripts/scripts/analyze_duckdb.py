#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "duckdb>=1.0,<2",
#   "rich>=13,<15",
# ]
# ///
"""Gold-standard local data analysis with DuckDB.

Run:
    uv run --script analyze_duckdb.py --demo
    uv run --script analyze_duckdb.py data.csv --query "select * from input limit 5"
"""

from __future__ import annotations

import argparse
import csv
import tempfile
from pathlib import Path

import duckdb
from rich.console import Console
from rich.table import Table

console = Console()
error_console = Console(stderr=True)


def create_demo_csv(directory: Path) -> Path:
    path = directory / "sales.csv"
    rows = [
        {"region": "North", "product": "A", "revenue": "1200", "units": "12"},
        {"region": "North", "product": "B", "revenue": "900", "units": "9"},
        {"region": "South", "product": "A", "revenue": "1700", "units": "17"},
        {"region": "West", "product": "C", "revenue": "800", "units": "4"},
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["region", "product", "revenue", "units"]
        )
        writer.writeheader()
        writer.writerows(rows)
    return path


def relation_for_path(
    connection: duckdb.DuckDBPyConnection, path: Path
) -> duckdb.DuckDBPyRelation:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return connection.read_csv(str(path), header=True)
    if suffix in {".json", ".jsonl", ".ndjson"}:
        return connection.read_json(str(path))
    if suffix == ".parquet":
        return connection.read_parquet(str(path))
    raise ValueError(f"unsupported data file: {path}")


def render_rows(title: str, columns: list[str], rows: list[tuple[object, ...]]) -> None:
    table = Table(title=title)
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*(str(value) for value in row))
    console.print(table)


def analyze(path: Path, query: str | None, export: Path | None) -> None:
    with duckdb.connect(":memory:") as connection:
        relation = relation_for_path(connection, path)
        relation.create_view("input")

        schema_rows = connection.sql("describe input").fetchall()
        render_rows(
            "Schema", ["column", "type", "null", "key", "default", "extra"], schema_rows
        )

        sample = connection.sql("select * from input limit 5")
        render_rows(
            "Sample", [column[0] for column in sample.description], sample.fetchall()
        )

        sql = query or "select count(*) as rows from input"
        result = connection.sql(sql)
        render_rows(
            "Query Result",
            [column[0] for column in result.description],
            result.fetchall(),
        )

        if export is not None:
            export.parent.mkdir(parents=True, exist_ok=True)
            if export.suffix.lower() == ".parquet":
                connection.sql(sql).write_parquet(str(export))
            else:
                connection.sql(sql).write_csv(str(export))
            console.print(f"[green]exported[/green] {export}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze CSV, JSON, or Parquet data with DuckDB."
    )
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument(
        "--query", help="SQL query. The input relation is named 'input'."
    )
    parser.add_argument(
        "--export", type=Path, help="Export query result to .csv or .parquet."
    )
    parser.add_argument(
        "--demo", action="store_true", help="Run against generated sample data."
    )
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> int:
    if args.demo:
        with tempfile.TemporaryDirectory() as tmp:
            analyze(
                create_demo_csv(Path(tmp)),
                args.query
                or "select region, sum(cast(revenue as int)) as revenue from input group by region order by revenue desc",
                args.export,
            )
        return 0

    if args.input is None:
        error_console.print("[red]missing input[/red] (or use --demo)")
        return 2
    if not args.input.exists():
        error_console.print(f"[red]missing file[/red] {args.input}")
        return 2

    analyze(args.input, args.query, args.export)
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except (duckdb.Error, ValueError) as exc:
        error_console.print(f"[red]analysis failed[/red] {exc}")
        return 1
    except KeyboardInterrupt:
        error_console.print("[red]interrupted[/red]")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
