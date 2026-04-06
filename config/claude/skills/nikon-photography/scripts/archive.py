# /// script
# requires-python = ">=3.11"
# ///
"""Losslessly transcode JPEGs to JPEG XL for archival (~20% smaller, perfectly reversible)."""

import argparse
import subprocess
import sys
from pathlib import Path


def transcode_to_jxl(src: Path, dst: Path, effort: int) -> None:
    subprocess.run(
        ["cjxl", str(src), str(dst), "--lossless_jpeg=1", "-e", str(effort)],
        check=True, capture_output=True,
    )


def verify_roundtrip(jxl_path: Path, original: Path) -> bool:
    """Verify that the JXL can be decoded back to a byte-identical JPEG."""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp:
        subprocess.run(
            ["djxl", str(jxl_path), tmp.name],
            check=True, capture_output=True,
        )
        return open(original, "rb").read() == open(tmp.name, "rb").read()


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive JPEGs as lossless JPEG XL")
    parser.add_argument("input_dir", type=Path, help="Directory containing photos")
    parser.add_argument("--effort", type=int, default=7, help="Encoding effort 1-9 (default: 7)")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory (default: <input>/jxl)")
    parser.add_argument("--glob", type=str, default="*.JPG", help="File glob pattern (default: *.JPG)")
    parser.add_argument("--verify", action="store_true", help="Verify roundtrip on first file")
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir / "jxl").resolve()
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
    verified = False

    for photo in photos:
        if photo.is_dir():
            continue
        in_size = photo.stat().st_size
        jxl_name = photo.stem + ".jxl"
        dst = output_dir / jxl_name

        try:
            transcode_to_jxl(photo, dst, args.effort)
            out_size = dst.stat().st_size

            # Verify roundtrip on first file
            if args.verify and not verified:
                if verify_roundtrip(dst, photo):
                    print(f"  VERIFIED: {photo.name} roundtrips perfectly")
                else:
                    print(f"  WARNING: {photo.name} roundtrip mismatch!", file=sys.stderr)
                verified = True

            total_in += in_size
            total_out += out_size
            count += 1
            ratio = out_size * 100 // in_size if in_size > 0 else 0
            print(f"[{count}/{len(photos)}] {photo.name} -> {jxl_name}: {in_size // 1024}KB -> {out_size // 1024}KB ({ratio}%)")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {photo.name}: {e}", file=sys.stderr)

    print()
    print(f"Processed: {count} files")
    print(f"Input:     {total_in / 1_048_576:.1f} MB (JPEG)")
    print(f"Output:    {total_out / 1_048_576:.1f} MB (JPEG XL)")
    if total_in > 0:
        print(f"Ratio:     {total_out * 100 / total_in:.1f}%")
    print(f"Saved:     {(total_in - total_out) / 1_048_576:.1f} MB")
    print(f"Output in: {output_dir}")
    print()
    print("To restore any file to original JPEG: djxl <file>.jxl <file>.jpg")


if __name__ == "__main__":
    main()
