# /// script
# requires-python = ">=3.11"
# ///
"""Generate a contact sheet (grid montage) of all photos for quick visual review."""

import argparse
import subprocess
import sys
from pathlib import Path


def make_contact_sheet(
    input_dir: Path,
    output: Path,
    columns: int,
    thumb_width: int,
    glob_pattern: str,
) -> None:
    # Build file list to ensure we process only matching files
    photos = sorted(input_dir.glob(glob_pattern))
    if not photos:
        photos = sorted(input_dir.glob(glob_pattern.lower()))
    if not photos:
        print(f"No files matching {glob_pattern} in {input_dir}")
        sys.exit(1)

    import math
    rows = math.ceil(len(photos) / columns)

    print(f"Creating contact sheet from {len(photos)} photos...")
    print(f"  Grid: {columns} columns x {rows} rows, {thumb_width}px thumbnails")

    # Use ffmpeg concat demuxer with a file list for reliable ordering
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=True) as filelist:
        for photo in photos:
            filelist.write(f"file '{photo}'\n")
        filelist.flush()

        subprocess.run(
            [
                "ffmpeg",
                "-f", "concat", "-safe", "0", "-i", filelist.name,
                "-vf", f"scale={thumb_width}:-1,tile={columns}x{rows}",
                str(output), "-y", "-loglevel", "error",
            ],
            check=True,
        )

    out_size = output.stat().st_size
    print(f"Contact sheet: {output} ({out_size // 1024}KB)")
    print(f"  {len(photos)} photos in {columns}-column grid")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create photo contact sheet")
    parser.add_argument("input_dir", type=Path, help="Directory containing photos")
    parser.add_argument("--columns", type=int, default=8, help="Grid columns (default: 8)")
    parser.add_argument("--thumb-width", type=int, default=320, help="Thumbnail width in px (default: 320)")
    parser.add_argument("--output", type=Path, default=None, help="Output file (default: <input>/contact-sheet.jpg)")
    parser.add_argument("--glob", type=str, default="*.JPG", help="File glob pattern (default: *.JPG)")
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    output = (args.output or input_dir / "contact-sheet.jpg").resolve()

    make_contact_sheet(input_dir, output, args.columns, args.thumb_width, args.glob)


if __name__ == "__main__":
    main()
