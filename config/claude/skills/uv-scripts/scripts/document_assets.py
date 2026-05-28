#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pillow>=10,<13",
#   "pypdf>=5,<7",
#   "rich>=13,<15",
# ]
# ///
"""Gold-standard PDF and image asset utility.

Run:
    uv run --script document_assets.py --demo
    uv run --script document_assets.py image-info image.png
    uv run --script document_assets.py pdf-info report.pdf
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter
from rich.console import Console
from rich.table import Table

console = Console()
error_console = Console(stderr=True)


def render_mapping(title: str, values: dict[str, object]) -> None:
    table = Table(title=title)
    table.add_column("Name")
    table.add_column("Value")
    for key, value in values.items():
        table.add_row(key, str(value))
    console.print(table)


def image_info(path: Path) -> None:
    with Image.open(path) as image:
        render_mapping(
            "Image",
            {
                "path": path,
                "format": image.format,
                "size": f"{image.width}x{image.height}",
                "mode": image.mode,
            },
        )


def resize_image(input_path: Path, output_path: Path, width: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(input_path) as image:
        ratio = width / image.width
        height = max(1, round(image.height * ratio))
        resized = image.resize((width, height))
        resized.save(output_path)
    console.print(f"[green]wrote[/green] {output_path}")


def pdf_info(path: Path) -> None:
    reader = PdfReader(path)
    first_page = reader.pages[0] if reader.pages else None
    render_mapping(
        "PDF",
        {
            "path": path,
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
            "first_page_width": first_page.mediabox.width if first_page else "n/a",
            "first_page_height": first_page.mediabox.height if first_page else "n/a",
        },
    )


def split_pdf(input_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(input_path)
    for index, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        output = output_dir / f"page-{index:03d}.pdf"
        with output.open("wb") as handle:
            writer.write(handle)
        console.print(f"[green]wrote[/green] {output}")


def create_demo_files(directory: Path) -> tuple[Path, Path]:
    image_path = directory / "demo.png"
    Image.new("RGB", (64, 32), "steelblue").save(image_path)

    pdf_path = directory / "demo.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=144, height=72)
    with pdf_path.open("wb") as handle:
        writer.write(handle)

    return image_path, pdf_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect and transform simple PDF/image assets."
    )
    subcommands = parser.add_subparsers(dest="command")

    image_info_parser = subcommands.add_parser(
        "image-info", help="Inspect an image file."
    )
    image_info_parser.add_argument("input", type=Path)

    resize_parser = subcommands.add_parser(
        "resize-image", help="Resize an image by width."
    )
    resize_parser.add_argument("input", type=Path)
    resize_parser.add_argument("output", type=Path)
    resize_parser.add_argument("--width", type=int, required=True)

    pdf_info_parser = subcommands.add_parser("pdf-info", help="Inspect a PDF file.")
    pdf_info_parser.add_argument("input", type=Path)

    split_parser = subcommands.add_parser(
        "split-pdf", help="Split a PDF into one-page PDFs."
    )
    split_parser.add_argument("input", type=Path)
    split_parser.add_argument("output_dir", type=Path)

    parser.add_argument(
        "--demo", action="store_true", help="Run a no-input asset demo."
    )
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> int:
    if args.demo:
        with tempfile.TemporaryDirectory() as tmp:
            image_path, pdf_path = create_demo_files(Path(tmp))
            image_info(image_path)
            resize_image(image_path, Path(tmp) / "demo-small.png", width=16)
            pdf_info(pdf_path)
            split_pdf(pdf_path, Path(tmp) / "pages")
        return 0

    if args.command is None:
        error_console.print("[red]missing command[/red] (or use --demo)")
        return 2

    input_path = args.input
    if not input_path.exists():
        error_console.print(f"[red]missing file[/red] {input_path}")
        return 2

    if args.command == "image-info":
        image_info(input_path)
    elif args.command == "resize-image":
        resize_image(input_path, args.output, args.width)
    elif args.command == "pdf-info":
        pdf_info(input_path)
    elif args.command == "split-pdf":
        split_pdf(input_path, args.output_dir)
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except (OSError, ValueError) as exc:
        error_console.print(f"[red]asset operation failed[/red] {exc}")
        return 1
    except KeyboardInterrupt:
        error_console.print("[red]interrupted[/red]")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
