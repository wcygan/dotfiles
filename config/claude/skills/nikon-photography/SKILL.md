---
name: nikon-photography
description: >
  Manage Nikon Z5 II photo and video libraries. Batch resize, convert to JPEG XL
  or optimized JPEG via mozjpeg, create contact sheets, manage EXIF metadata, prepare
  share-ready albums, and process 4K video. Uses Python scripts via uv run for all
  batch operations. Use when working with JPG, NEF, HEIF, or MOV photo/video files,
  or when the user mentions photos, camera, Nikon, resize, sharing pictures, photo
  library, image optimization, JPEG XL, or contact sheet.
allowed-tools:
  - Bash(uv run *)
  - Bash(ffmpeg *)
  - Bash(cjpeg *)
  - Bash(djpeg *)
  - Bash(cjxl *)
  - Bash(djxl *)
  - Bash(exiftool *)
  - Bash(mkdir *)
  - Bash(cp *)
  - Bash(mv *)
  - Bash(brew install *)
  - Bash(du *)
  - Bash(ls *)
  - Bash(stat *)
  - Bash(sips *)
  - Read
  - Glob
  - Grep
argument-hint: "<command> [options] — resize, optimize, archive, share-album, contact-sheet, metadata, video"
---

# Nikon Photography Assistant

Manage photo and video libraries from the Nikon Z5 II (24.5MP, 6048x4032).
File naming convention: `DSC_NNNN.JPG` or `DSC_NNNN.NEF`.

All batch operations use Python scripts executed via `uv run` (PEP 723 inline
metadata handles dependencies automatically). Scripts live in
`${CLAUDE_SKILL_DIR}/scripts/`.

## Prerequisite Check

Before any operation, verify required tools:

```bash
command -v ffmpeg  || echo "MISSING: brew install ffmpeg"
command -v cjpeg   || echo "MISSING: brew install mozjpeg"
command -v cjxl    || echo "MISSING: brew install jpeg-xl"
command -v exiftool || echo "MISSING: brew install exiftool"
command -v uv      || echo "MISSING: brew install uv"
```

If any tool is missing, tell the user the exact `brew install` command and stop.

## Commands

Route based on `$ARGUMENTS`:

### `resize [max_dim] [quality]` — Resize for sharing

Resize photos to a target long-edge dimension (default: 2048px) preserving
aspect ratio. Outputs to `share/` subdirectory.

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/resize.py" . --max-dim 2048 --quality 2
```

### `optimize [quality]` — Optimize JPEG quality/size

Re-encode JPEGs through djpeg | cjpeg (mozjpeg) pipeline for smaller files
at equivalent visual quality. Default quality: 85.

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/optimize.py" . --quality 85
```

### `archive` — Lossless JPEG XL archival

Losslessly transcode JPEGs to JPEG XL (~20% smaller, perfectly reversible
back to byte-identical original JPEG via `djxl`).

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/archive.py" .
```

### `contact-sheet [columns] [thumb_width]` — Visual overview

Generate a grid contact sheet of all photos for quick review.

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/contact_sheet.py" . --columns 8 --thumb-width 320
```

### `share-album [max_dim] [quality]` — Full sharing pipeline

Complete pipeline: resize + optimize + strip GPS (preserve date/camera info).

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/share_album.py" . --max-dim 2048 --quality 85
```

### `metadata <subcommand>` — EXIF metadata management

- `metadata show <file>` — display all EXIF data
- `metadata strip-gps [dir]` — remove GPS/location from all files
- `metadata dates [dir]` — list files with capture dates
- `metadata rename [dir]` — rename files to `YYYY-MM-DD_HHMMSS_DSC_NNNN.JPG`

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/metadata.py" . <subcommand>
```

### `video <subcommand>` — Video processing

- `video compress [crf]` — re-encode MOV to HEVC at given CRF (default: 22)
- `video extract-frames <file> [interval]` — extract stills every N seconds
- `video resize <max_dim>` — resize video for sharing

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/video.py" . <subcommand>
```

## Safety Rules

1. **NEVER delete or overwrite original files.** Always output to a subdirectory.
2. **Preserve original filenames** in output directories.
3. **Maintain aspect ratio** when resizing — never stretch or distort.
4. **Strip GPS for sharing** but keep date, camera, and lens metadata.
5. **Report progress** — print each filename as it processes.
6. **Summarize results** — file count, input size, output size, compression ratio.

## Camera Reference

For Z5 II specs, resolution options, and format details:
see [z5ii-specs.md](references/z5ii-specs.md)

## Tool Reference

For detailed flags, quality scales, and advanced recipes:
see [tool-reference.md](references/tool-reference.md)

## Sharing Guide

For format choices, audience considerations, and platform limits:
see [sharing-guide.md](references/sharing-guide.md)

## Archival Guide

For long-term storage strategy and JPEG XL reversibility:
see [archival-guide.md](references/archival-guide.md)
