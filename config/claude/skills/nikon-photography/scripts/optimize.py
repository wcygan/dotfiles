# /// script
# requires-python = ">=3.11"
# ///
"""Optimize JPEGs using the djpeg | cjpeg (mozjpeg) pipeline."""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def optimize_jpeg(src: Path, dst: Path, quality: int) -> None:
    """Decompress JPEG then re-encode with mozjpeg at target quality."""
    with tempfile.NamedTemporaryFile(suffix=".ppm", delete=True) as tmp:
        # djpeg decodes JPEG to PPM
        subprocess.run(
            ["djpeg", "-outfile", tmp.name, str(src)],
            check=True, capture_output=True,
        )
        # cjpeg re-encodes with mozjpeg optimizations
        subprocess.run(
            ["cjpeg", "-quality", str(quality), "-optimize", "-outfile", str(dst), tmp.name],
            check=True, capture_output=True,
        )


def copy_metadata(src: Path, dst: Path) -> None:
    """Copy EXIF metadata from source to destination (if exiftool available)."""
    try:
        subprocess.run(
            ["exiftool", "-TagsFromFile", str(src), "-all:all", "-overwrite_original", str(dst)],
            check=True, capture_output=True,
        )
    except FileNotFoundError:
        pass  # exiftool not installed, skip metadata copy


def main() -> None:
    parser = argparse.ArgumentParser(description="Optimize JPEGs with mozjpeg")
    parser.add_argument("input_dir", type=Path, help="Directory containing photos")
    parser.add_argument("--quality", type=int, default=85, help="JPEG quality 0-100 (default: 85)")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory (default: <input>/optimized)")
    parser.add_argument("--glob", type=str, default="*.JPG", help="File glob pattern (default: *.JPG)")
    parser.add_argument("--copy-metadata", action="store_true", default=True, help="Copy EXIF metadata (default: true)")
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir / "optimized").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    photos = sorted(input_dir.glob(args.glob))
    if not photos:
        photos = sorted(input_dir.glob(args.glob.lower()))
    if not photos:
        print(f"No files matching {args.glob} in {input_dir}")
        sys.exit(1)

    total_in = 0
    total_out = 0
    count = 0

    for photo in photos:
        if photo.is_dir():
            continue
        in_size = photo.stat().st_size
        dst = output_dir / photo.name

        try:
            optimize_jpeg(photo, dst, args.quality)
            if args.copy_metadata:
                copy_metadata(photo, dst)
            out_size = dst.stat().st_size
            total_in += in_size
            total_out += out_size
            count += 1
            ratio = out_size * 100 // in_size if in_size > 0 else 0
            print(f"[{count}/{len(photos)}] {photo.name}: {in_size // 1024}KB -> {out_size // 1024}KB ({ratio}%)")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {photo.name}: {e}", file=sys.stderr)

    print()
    print(f"Processed: {count} files")
    print(f"Input:     {total_in / 1_048_576:.1f} MB")
    print(f"Output:    {total_out / 1_048_576:.1f} MB")
    if total_in > 0:
        print(f"Ratio:     {total_out * 100 / total_in:.1f}%")
    print(f"Saved:     {(total_in - total_out) / 1_048_576:.1f} MB")
    print(f"Output in: {output_dir}")


if __name__ == "__main__":
    main()
