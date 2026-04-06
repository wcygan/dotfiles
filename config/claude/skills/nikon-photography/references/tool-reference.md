# Tool Reference — cjxl, cjpeg, ffmpeg, exiftool

## cjxl (JPEG XL encoder)

Part of `libjxl`. Install: `brew install jpeg-xl`

### Lossless JPEG Recompression (archival)

```bash
cjxl input.jpg output.jxl --lossless_jpeg=1 -e 7
```

- `--lossless_jpeg=1` — bit-for-bit reversible JPEG transcoding
- `-e 7` — effort level (1-9). Higher = slower but smaller. 7 is a good balance.
- Reverse with: `djxl output.jxl restored.jpg` (byte-identical to original)
- Typical savings: ~20% smaller than original JPEG

### Lossy JPEG XL

```bash
cjxl input.jpg output.jxl -d 1.0 -e 7
```

- `-d` — distance (0 = mathematically lossless, 1.0 = visually lossless, 2.0 = high quality)
- `-d 1.0` is a good default for high-quality lossy
- Typical savings: 50-70% vs original JPEG

### Threading

```bash
cjxl input.jpg output.jxl --lossless_jpeg=1 -e 7 --num_threads=0
```

- `--num_threads=0` — use all available cores (default)

## djpeg / cjpeg (mozjpeg pipeline)

Part of `libjpeg-turbo` / `mozjpeg`. Install: `brew install mozjpeg`

### Important: cjpeg does NOT read JPEG

`cjpeg` reads BMP, PPM, Targa — not JPEG. To re-optimize existing JPEGs:

```bash
djpeg input.jpg | cjpeg -quality 85 -optimize > output.jpg
```

Or use a temp file approach:

```bash
djpeg input.jpg > /tmp/temp.ppm
cjpeg -quality 85 -optimize -outfile output.jpg /tmp/temp.ppm
```

### Quality Scale

- Range: 0-100
- 95-100: Overkill, very large files
- 85-90: Excellent quality, good compression (recommended for sharing)
- 75-85: Good quality, noticeable only in pixel-peeping
- Below 75: Visible artifacts in gradients/sky

### Key Flags

| Flag | Purpose |
|------|---------|
| `-quality N` | Set quality (0-100) |
| `-optimize` | Optimize Huffman tables (always use) |
| `-progressive` | Progressive JPEG (default in mozjpeg) |
| `-outfile path` | Output file path |

### jpegtran (lossless JPEG optimization)

```bash
jpegtran -optimize -progressive -copy all -outfile output.jpg input.jpg
```

- Losslessly re-encodes with optimal Huffman tables
- `-copy all` preserves all metadata
- Typical savings: 2-5%

## ffmpeg

### Resize Photos (JPEG output)

```bash
ffmpeg -i input.jpg -vf "scale='min(2048,iw)':'min(2048,ih)':force_original_aspect_ratio=decrease" \
  -q:v 2 output.jpg -y -loglevel error
```

- `-q:v` — JPEG quality (1=best, 31=worst). 2 is high quality.
- `force_original_aspect_ratio=decrease` — never upscale, maintain ratio

### Contact Sheet

```bash
ffmpeg -pattern_type glob -i '*.JPG' \
  -vf "scale=320:-1,tile=8x0" contact-sheet.jpg -y -loglevel error
```

- `tile=COLSxROWS` — calculate rows as `ceil(count / cols)`
- `scale=WIDTH:-1` — scale thumbnails, maintain ratio

### Video Re-encode (HEVC)

```bash
ffmpeg -i input.MOV -c:v libx265 -crf 22 -preset medium \
  -c:a aac -b:a 192k -movflags +faststart output.mp4 -y
```

- `-crf` — quality (0=lossless, 18=very high, 22=high, 28=medium). 22 is a great default.
- `-preset` — speed/compression tradeoff (ultrafast to veryslow). medium is balanced.
- `-movflags +faststart` — web-optimized MP4 (moov atom at start)
- Typical savings at CRF 22: 70-85% vs camera's ~150 Mbps

### Video Resize

```bash
ffmpeg -i input.MOV -vf "scale='min(1920,iw)':'min(1920,ih)':force_original_aspect_ratio=decrease" \
  -c:v libx265 -crf 22 -preset medium -c:a aac -b:a 192k output.mp4 -y
```

### Extract Frames

```bash
ffmpeg -i input.MOV -vf "fps=1/5" frame_%04d.jpg -q:v 2 -y
```

- `fps=1/5` — one frame every 5 seconds

## exiftool

Install: `brew install exiftool`

### View Metadata

```bash
exiftool photo.jpg                    # All metadata
exiftool -DateTimeOriginal photo.jpg  # Just capture date
exiftool -GPS* photo.jpg              # GPS data only
exiftool -LensModel -FocalLength photo.jpg  # Lens info
```

### Strip GPS (preserve other metadata)

```bash
exiftool -GPS*= -overwrite_original photo.jpg
exiftool -GPS*= -overwrite_original *.JPG   # batch
```

### Strip ALL Metadata

```bash
exiftool -all= -overwrite_original photo.jpg
```

### Rename by Date

```bash
exiftool '-FileName<DateTimeOriginal' -d '%Y-%m-%d_%H%M%S_%%f.%%e' *.JPG
```

Result: `2026-04-05_104600_DSC_3451.JPG`

### Copy Metadata Between Files

```bash
exiftool -TagsFromFile original.jpg -all:all optimized.jpg
```

Useful after re-encoding with cjpeg (which strips metadata).

## sips (macOS built-in)

Available without installation. Useful as a fallback.

```bash
sips -Z 2048 --out share/ input.jpg          # Resize to fit 2048x2048
sips -g pixelWidth -g pixelHeight input.jpg   # Get dimensions
sips -s formatOptions 85 --out opt/ input.jpg # Re-encode at quality 85
```

- `-Z maxdim` — scale to fit within maxdim x maxdim, maintain ratio
- Doesn't use mozjpeg, so files are larger than cjpeg output
