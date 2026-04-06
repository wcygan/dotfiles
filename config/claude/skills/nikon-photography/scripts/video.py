# /// script
# requires-python = ">=3.11"
# ///
"""Process video files: compress, extract frames, resize."""

import argparse
import subprocess
import sys
from pathlib import Path


def get_file_size(path: Path) -> int:
    return path.stat().st_size


def cmd_compress(args: argparse.Namespace) -> None:
    """Re-encode MOV/MP4 to HEVC at given CRF quality."""
    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir / "compressed").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    videos = sorted(list(input_dir.glob("*.MOV")) + list(input_dir.glob("*.mov"))
                    + list(input_dir.glob("*.MP4")) + list(input_dir.glob("*.mp4")))
    if not videos:
        print(f"No video files in {input_dir}")
        sys.exit(1)

    total_in = 0
    total_out = 0

    for i, video in enumerate(videos, 1):
        in_size = get_file_size(video)
        out_name = video.stem + ".mp4"
        dst = output_dir / out_name

        print(f"[{i}/{len(videos)}] {video.name} ({in_size / 1_048_576:.0f} MB) -> {out_name}")
        print(f"  Encoding HEVC CRF {args.crf}, preset {args.preset}...")

        try:
            subprocess.run(
                [
                    "ffmpeg", "-i", str(video),
                    "-c:v", "libx265", "-crf", str(args.crf), "-preset", args.preset,
                    "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart",
                    "-tag:v", "hvc1",  # Apple compatibility
                    str(dst), "-y", "-loglevel", "error",
                ],
                check=True,
            )
            out_size = get_file_size(dst)
            total_in += in_size
            total_out += out_size
            ratio = out_size * 100 // in_size if in_size > 0 else 0
            print(f"  {in_size / 1_048_576:.0f} MB -> {out_size / 1_048_576:.0f} MB ({ratio}%)")
        except subprocess.CalledProcessError as e:
            print(f"  ERROR: {e}", file=sys.stderr)

    print()
    print(f"Processed: {len(videos)} videos")
    print(f"Input:     {total_in / 1_073_741_824:.2f} GB")
    print(f"Output:    {total_out / 1_073_741_824:.2f} GB")
    if total_in > 0:
        print(f"Ratio:     {total_out * 100 / total_in:.1f}%")
    print(f"Saved:     {(total_in - total_out) / 1_073_741_824:.2f} GB")
    print(f"Output in: {output_dir}")


def cmd_extract_frames(args: argparse.Namespace) -> None:
    """Extract still frames from a video at regular intervals."""
    video = args.target.resolve()
    if not video.exists():
        print(f"File not found: {video}")
        sys.exit(1)

    output_dir = (args.output_dir or video.parent / f"{video.stem}_frames").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting frames from {video.name} every {args.interval}s...")
    subprocess.run(
        [
            "ffmpeg", "-i", str(video),
            "-vf", f"fps=1/{args.interval}",
            str(output_dir / f"{video.stem}_%04d.jpg"),
            "-q:v", "2", "-y", "-loglevel", "error",
        ],
        check=True,
    )

    frames = list(output_dir.glob("*.jpg"))
    print(f"Extracted {len(frames)} frames to {output_dir}")


def cmd_resize(args: argparse.Namespace) -> None:
    """Resize videos for sharing."""
    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir / "video_share").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    videos = sorted(list(input_dir.glob("*.MOV")) + list(input_dir.glob("*.mov"))
                    + list(input_dir.glob("*.MP4")) + list(input_dir.glob("*.mp4")))
    if not videos:
        print(f"No video files in {input_dir}")
        sys.exit(1)

    max_dim = args.max_dim
    total_in = 0
    total_out = 0

    for i, video in enumerate(videos, 1):
        in_size = get_file_size(video)
        out_name = video.stem + ".mp4"
        dst = output_dir / out_name

        print(f"[{i}/{len(videos)}] {video.name} -> {max_dim}px, HEVC CRF {args.crf}")

        try:
            subprocess.run(
                [
                    "ffmpeg", "-i", str(video),
                    "-vf", f"scale='min({max_dim},iw)':'min({max_dim},ih)':force_original_aspect_ratio=decrease",
                    "-c:v", "libx265", "-crf", str(args.crf), "-preset", args.preset,
                    "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart",
                    "-tag:v", "hvc1",
                    str(dst), "-y", "-loglevel", "error",
                ],
                check=True,
            )
            out_size = get_file_size(dst)
            total_in += in_size
            total_out += out_size
            print(f"  {in_size / 1_048_576:.0f} MB -> {out_size / 1_048_576:.0f} MB")
        except subprocess.CalledProcessError as e:
            print(f"  ERROR: {e}", file=sys.stderr)

    print()
    print(f"Processed: {len(videos)} videos")
    print(f"Input:     {total_in / 1_073_741_824:.2f} GB")
    print(f"Output:    {total_out / 1_073_741_824:.2f} GB")
    if total_in > 0:
        print(f"Saved:     {(total_in - total_out) / 1_073_741_824:.2f} GB")
    print(f"Output in: {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Video processing for Nikon Z5 II footage")
    parser.add_argument("input_dir", type=Path, help="Directory containing videos")
    parser.add_argument("command", choices=["compress", "extract-frames", "resize"],
                        help="Subcommand")
    parser.add_argument("target", type=Path, nargs="?", default=None,
                        help="Target file (for extract-frames)")
    parser.add_argument("--crf", type=int, default=22, help="CRF quality (default: 22, lower=better)")
    parser.add_argument("--preset", type=str, default="medium",
                        help="Encoding preset (default: medium)")
    parser.add_argument("--max-dim", type=int, default=1920, help="Max dimension for resize (default: 1920)")
    parser.add_argument("--interval", type=int, default=5, help="Frame extraction interval in seconds (default: 5)")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory")
    args = parser.parse_args()

    commands = {
        "compress": cmd_compress,
        "extract-frames": cmd_extract_frames,
        "resize": cmd_resize,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
