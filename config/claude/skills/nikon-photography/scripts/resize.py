# /// script
# requires-python = ">=3.11"
# ///
"""Resize photos to a target long-edge dimension for sharing."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def get_file_size(path: Path) -> int:
    return path.stat().st_size


def resize_photo(src: Path, dst: Path, max_dim: int, quality: int) -> None:
    subprocess.run(
        [
            "ffmpeg", "-i", str(src),
            "-vf", f"scale='min({max_dim},iw)':'min({max_dim},ih)':force_original_aspect_ratio=decrease",
            "-q:v", str(quality),
            str(dst), "-y", "-loglevel", "error",
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Resize photos for sharing")
    parser.add_argument("input_dir", type=Path, help="Directory containing photos")
    parser.add_argument("--max-dim", type=int, default=2048, help="Max long-edge pixels (default: 2048)")
    parser.add_argument("--quality", type=int, default=2, help="ffmpeg JPEG quality 1-31, lower=better (default: 2)")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory (default: <input>/share)")
    parser.add_argument("--glob", type=str, default="*.JPG", help="File glob pattern (default: *.JPG)")
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir / "share").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    photos = sorted(input_dir.glob(args.glob))
    if not photos:
        # Try lowercase
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
        in_size = get_file_size(photo)
        dst = output_dir / photo.name

        try:
            resize_photo(photo, dst, args.max_dim, args.quality)
            out_size = get_file_size(dst)
            total_in += in_size
            total_out += out_size
            count += 1
            print(f"[{count}/{len(photos)}] {photo.name}: {in_size // 1024}KB -> {out_size // 1024}KB")
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
