# Photo Archival Guide

## JPEG XL Lossless Recompression

The single best option for archiving existing JPEG photos.

### How It Works

JPEG XL can losslessly recompress JPEG files by exploiting redundancy in the
JPEG coding format itself. The resulting `.jxl` file is ~20% smaller and can
be **perfectly reconstructed** back to the byte-identical original JPEG.

```bash
# Compress
cjxl photo.jpg photo.jxl --lossless_jpeg=1 -e 7

# Verify: reconstruct and compare
djxl photo.jxl restored.jpg
diff photo.jpg restored.jpg  # identical
```

This is NOT lossy compression — it's a more efficient encoding of the same data.

### Expected Savings

| Input | JPEG XL lossless | Savings |
|-------|-----------------|---------|
| 10 MB JPEG (Fine) | ~8 MB | ~20% |
| 3.4 GB (303 photos) | ~2.7 GB | ~700 MB |

### Effort Levels

| Effort (`-e`) | Speed | Size | Recommendation |
|---------------|-------|------|----------------|
| 1-3 | Fast | Larger | Quick batch jobs |
| 7 | Medium | Good | **Default — best balance** |
| 9 | Slow | Smallest | Maximum compression, 3-5x slower |

### Reversibility Verification

After batch conversion, verify reversibility on a sample:

```bash
djxl sample.jxl /tmp/verify.jpg
cmp original.jpg /tmp/verify.jpg && echo "IDENTICAL"
```

## Archival Storage Strategy

### Recommended Directory Layout

```
Photos/
  Camera/
    Easter 2026/           # Originals (JPEG, keep forever)
      DSC_3451.JPG
      ...
    Easter 2026 - Archive/  # JPEG XL lossless (space savings)
      DSC_3451.jxl
      ...
    Easter 2026 - Share/    # Resized/optimized for sharing
      DSC_3451.JPG
      ...
```

### 3-2-1 Backup Rule

- **3** copies of your data
- **2** different storage media (e.g., SSD + cloud)
- **1** offsite (e.g., cloud storage)

### Keep Originals Until Verified

After JPEG XL conversion:
1. Verify a random sample reconstructs identically
2. Check total file count matches
3. Only then consider removing original JPEGs
4. Better yet: keep originals on a backup drive

## Long-Term Format Considerations

| Format | Longevity | Decoder availability | Notes |
|--------|-----------|---------------------|-------|
| JPEG | Excellent | Universal forever | Gold standard for compatibility |
| JPEG XL | Good | Growing, reference decoder open-source | Reversible to JPEG = safe bet |
| HEIF | Good | Apple + Android native | Less universal than JPEG |
| RAW (NEF) | Depends | Nikon-specific, open-source readers exist | Keep for maximum editing flexibility |

JPEG XL is safe for archival because:
- Open standard (ISO/IEC 18181)
- Reference implementation is open-source (libjxl)
- Chromium support landed 2026
- Lossless mode is perfectly reversible to standard JPEG
