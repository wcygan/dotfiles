# /// script
# requires-python = ">=3.11"
# ///
"""Manage EXIF metadata: show, strip GPS, list dates, rename by date."""

import argparse
import subprocess
import sys
from pathlib import Path


def check_exiftool() -> None:
    try:
        subprocess.run(["exiftool", "-ver"], check=True, capture_output=True)
    except FileNotFoundError:
        print("ERROR: exiftool not installed. Run: brew install exiftool", file=sys.stderr)
        sys.exit(1)


def cmd_show(args: argparse.Namespace) -> None:
    """Show all EXIF metadata for a file."""
    target = args.target
    if target is None:
        print("Usage: metadata.py show <file>")
        sys.exit(1)
    subprocess.run(["exiftool", str(target)], check=True)


def cmd_strip_gps(args: argparse.Namespace) -> None:
    """Strip GPS coordinates from all photos (preserve other metadata)."""
    input_dir = args.input_dir.resolve()
    photos = sorted(input_dir.glob(args.glob))
    if not photos:
        photos = sorted(input_dir.glob(args.glob.lower()))
    if not photos:
        print(f"No files matching {args.glob} in {input_dir}")
        sys.exit(1)

    print(f"Stripping GPS data from {len(photos)} files...")
    result = subprocess.run(
        ["exiftool", "-GPS*=", "-SerialNumber=", "-CameraSerialNumber=",
         "-overwrite_original"] + [str(p) for p in photos],
        capture_output=True, text=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)


def cmd_dates(args: argparse.Namespace) -> None:
    """List all files with their capture dates."""
    input_dir = args.input_dir.resolve()
    photos = sorted(input_dir.glob(args.glob))
    if not photos:
        photos = sorted(input_dir.glob(args.glob.lower()))
    if not photos:
        print(f"No files matching {args.glob} in {input_dir}")
        sys.exit(1)

    result = subprocess.run(
        ["exiftool", "-DateTimeOriginal", "-FileName", "-T"] + [str(p) for p in photos],
        capture_output=True, text=True, check=True,
    )
    print(result.stdout)


def cmd_rename(args: argparse.Namespace) -> None:
    """Rename files to YYYY-MM-DD_HHMMSS_OriginalName format."""
    input_dir = args.input_dir.resolve()
    photos = sorted(input_dir.glob(args.glob))
    if not photos:
        photos = sorted(input_dir.glob(args.glob.lower()))
    if not photos:
        print(f"No files matching {args.glob} in {input_dir}")
        sys.exit(1)

    print(f"Renaming {len(photos)} files by capture date...")
    print("Preview (no changes yet):")

    # Dry run first
    result = subprocess.run(
        ["exiftool", "-testname", "-d", "%Y-%m-%d_%H%M%S_%%f.%%e",
         "'-TestName<DateTimeOriginal'"] + [str(p) for p in photos],
        capture_output=True, text=True,
    )
    print(result.stdout)

    if args.execute:
        print("\nExecuting rename...")
        subprocess.run(
            ["exiftool", "-d", "%Y-%m-%d_%H%M%S_%%f.%%e",
             "'-FileName<DateTimeOriginal'"] + [str(p) for p in photos],
            check=True,
        )
        print("Done.")
    else:
        print("\nThis was a dry run. Add --execute to actually rename files.")


def main() -> None:
    parser = argparse.ArgumentParser(description="EXIF metadata management")
    parser.add_argument("input_dir", type=Path, help="Directory containing photos")
    parser.add_argument("command", choices=["show", "strip-gps", "dates", "rename"],
                        help="Subcommand")
    parser.add_argument("target", type=Path, nargs="?", default=None,
                        help="Target file (for 'show' command)")
    parser.add_argument("--glob", type=str, default="*.JPG", help="File glob pattern (default: *.JPG)")
    parser.add_argument("--execute", action="store_true", help="Actually execute rename (default: dry run)")
    args = parser.parse_args()

    check_exiftool()

    commands = {
        "show": cmd_show,
        "strip-gps": cmd_strip_gps,
        "dates": cmd_dates,
        "rename": cmd_rename,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
