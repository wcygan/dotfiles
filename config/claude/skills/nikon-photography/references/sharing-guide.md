# Photo Sharing Guide

## Choosing Resolution for Sharing

| Target | Long edge | Notes |
|--------|-----------|-------|
| Screen viewing (general) | 2048 px | Good for tablets, laptops, phones |
| Social media / messaging | 1080-1600 px | Fast uploads, messaging-friendly |
| Large prints (up to 20x30) | 4000+ px | Keep near-original resolution |
| Email attachments | 1024-1600 px | Stay under 10 MB total |
| Web galleries | 1600-2048 px | Balance quality and load time |

**Default recommendation: 2048 px long edge** — large enough for any screen,
small enough to share easily. Typical file size: 300-600 KB per photo.

## Format Choices

| Format | Compatibility | Best for |
|--------|--------------|----------|
| JPEG (optimized) | Universal — every device | Sharing with anyone |
| JPEG XL | Chrome, Edge (2026) | Tech-savvy recipients, web hosting |
| HEIF/HEIC | Apple devices | AirDrop, iMessage to Apple users |
| WebP | All modern browsers | Web galleries |

**Default recommendation: Optimized JPEG** — zero compatibility issues.

## Privacy: What to Strip

### Always strip before public sharing:
- **GPS coordinates** — reveals exact location
- **Serial numbers** — camera body serial
- **Owner name** — if set in camera

### Keep for family/friends sharing:
- **Date/time** — useful for organizing
- **Camera/lens info** — fellow photographers appreciate it
- **Orientation** — needed for correct display

### Command:
```bash
exiftool -GPS*= -SerialNumber= -CameraSerialNumber= -overwrite_original *.JPG
```

## Platform-Specific Limits

| Platform | Max image size | Max attachment | Notes |
|----------|---------------|----------------|-------|
| iMessage | No hard limit | 100 MB | Compresses large images |
| WhatsApp | 16 MB per image | — | Heavy re-compression |
| Gmail | — | 25 MB total | Use Google Drive for larger |
| Google Photos | 200 MP | — | Free storage compresses to 16 MP |
| Apple Photos (shared album) | — | — | Downsizes to ~2048 px |
| Facebook | 2048 px wide | — | Re-compresses aggressively |
| Instagram | 1080 px wide | — | Crops to supported ratios |

## Sharing Methods Ranked by Quality

1. **Google Drive / iCloud link** — no recompression, original files
2. **AirDrop** — no recompression, fast for Apple-to-Apple
3. **Email attachment** — no recompression, size limited
4. **Apple shared album** — mild resize, good quality
5. **Google Photos shared album** — compressed but good
6. **Messaging apps** — most recompression, lowest quality

## Recommended Pipeline for Family Sharing

1. Resize to 2048 px long edge
2. Optimize with mozjpeg at quality 85
3. Strip GPS coordinates
4. Share via Google Drive link or Apple shared album

Expected result: 303 photos at ~400 KB each = ~120 MB total (down from 3.4 GB).
