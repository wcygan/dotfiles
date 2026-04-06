# /// script
# requires-python = ">=3.11"
# ///
"""Full sharing pipeline: resize + optimize with mozjpeg + strip GPS metadata."""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def resize_photo(src: Path, dst: Path, max_dim: int) -> None:
    subprocess.run(
        [
            "ffmpeg", "-i", str(src),
            "-vf", f"scale='min({max_dim},iw)':'min({max_dim},ih)':force_original_aspect_ratio=decrease",
            "-q:v", "1",  # Max quality intermediate
            str(dst), "-y", "-loglevel", "error",
        ],
        check=True,
    )


def optimize_jpeg(src: Path, dst: Path, quality: int) -> None:
    with tempfile.NamedTemporaryFile(suffix=".ppm", delete=True) as tmp:
        subprocess.run(
            ["djpeg", "-outfile", tmp.name, str(src)],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["cjpeg", "-quality", str(quality), "-optimize", "-outfile", str(dst), tmp.name],
            check=True, capture_output=True,
        )


def copy_metadata_strip_gps(src: Path, dst: Path) -> None:
    """Copy EXIF from original, then strip GPS data."""
    try:
        subprocess.run(
            ["exiftool", "-TagsFromFile", str(src), "-all:all", "-GPS*=",
             "-SerialNumber=", "-CameraSerialNumber=",
             "-overwrite_original", str(dst)],
            check=True, capture_output=True,
        )
    except FileNotFoundError:
        print("  WARNING: exiftool not installed, metadata not copied. Run: brew install exiftool",
              file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Full sharing pipeline: resize + optimize + strip GPS")
    parser.add_argument("input_dir", type=Path, help="Directory containing photos")
    parser.add_argument("--max-dim", type=int, default=2048, help="Max long-edge pixels (default: 2048)")
    parser.add_argument("--quality", type=int, default=85, help="mozjpeg quality 0-100 (default: 85)")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory (default: <input>/album)")
    parser.add_argument("--glob", type=str, default="*.JPG", help="File glob pattern (default: *.JPG)")
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir / "album").resolve()
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
        final = output_dir / photo.name

        try:
            # Step 1: Resize to intermediate temp file
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as resized:
                resize_photo(photo, Path(resized.name), args.max_dim)

                # Step 2: Optimize with mozjpeg
                optimize_jpeg(Path(resized.name), final, args.quality)

            # Step 3: Copy metadata from original, strip GPS
            copy_metadata_strip_gps(photo, final)

            out_size = final.stat().st_size
            total_in += in_size
            total_out += out_size
            count += 1
            print(f"[{count}/{len(photos)}] {photo.name}: {in_size // 1024}KB -> {out_size // 1024}KB")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {photo.name}: {e}", file=sys.stderr)

    print()
    print(f"Pipeline: resize({args.max_dim}px) -> optimize(q{args.quality}) -> strip GPS")
    print(f"Processed: {count} files")
    print(f"Input:     {total_in / 1_048_576:.1f} MB")
    print(f"Output:    {total_out / 1_048_576:.1f} MB")
    if total_in > 0:
        print(f"Ratio:     {total_out * 100 / total_in:.1f}%")
    print(f"Saved:     {(total_in - total_out) / 1_048_576:.1f} MB")
    print(f"Output in: {output_dir}")


if __name__ == "__main__":
    main()
