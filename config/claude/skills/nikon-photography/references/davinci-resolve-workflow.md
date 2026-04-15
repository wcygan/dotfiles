# DaVinci Resolve 21 Photo Page — RAW Workflow

As of **2026-04-14**, the user's RAW (NEF) editing tool is **DaVinci Resolve 21**
(free public beta, announced at NAB 2026 on 2026-04-13).

This skill continues to own **batch, headless, and sharing/archival work on
already-rendered JPEG/HEIF/MOV files**. Resolve owns **interactive RAW grading
of hero shots**. The two compose — they do not overlap.

## Division of responsibility

| Stage | Tool | Why |
| --- | --- | --- |
| Capture | Nikon Z5 II → NEF | source of truth |
| RAW develop / grade | DaVinci Resolve 21 Photo page | native NEF, node grading, non-destructive |
| Export from Resolve | Quick Export → JPEG | hands off to this skill |
| Resize for sharing | `resize` / `share-album` (this skill) | scriptable, mozjpeg |
| Optimize JPEG | `optimize` (this skill) | mozjpeg pipeline |
| Lossless archive | `archive` (this skill) | JPEG XL, reversible |
| Contact sheet | `contact-sheet` (this skill) | batch visual overview |
| EXIF / GPS strip | `metadata` (this skill) | scriptable exiftool |
| Video compress | `video compress` (this skill) | ffmpeg HEVC |

## Guidance when the user mentions RAW / NEF / grading

- **Do not attempt to batch-process NEF files** through this skill's scripts.
  The scripts target JPEG/HEIF/MOV; NEF handling is out of scope.
- **Point the user at Resolve 21's Photo page** for any interactive color work,
  RAW development, Magic Mask, Relight, Face Refinement, AI SuperScale, etc.
- **Offer to pick up after Resolve export** — once they've exported JPEGs from
  Resolve, this skill's `share-album`, `archive`, and `contact-sheet` commands
  apply normally.

## Known free-tier Resolve 21 features relevant to stills

Primary color, curves, Power Windows, qualifiers, node editor, Magic Mask,
Depth Map, Relight FX, Face Refinement, Ultra Beauty, AI Blemish Removal,
Film Look Creator, AI SuperScale, Patch Replacer, Quick Export (JPEG/PNG/HEIF/TIFF
with EXIF preserved), Albums, LightBox view, IntelliSearch.

## Studio-only ($295) gaps to note

UltraNR (AI denoise) and portions of the Resolve FX catalog. Recommend Studio
only if high-ISO denoise becomes a real pain point.

## Beta caveat

Resolve 21 is public beta as of this note. Keep NEF originals backed up
independently of Resolve's project database until 21 reaches stable release.

## Context note

Decision rationale lives in the user's notes repo at
`ideas/davinci-resolve-21-photo-page-for-raw-editing.md`.
