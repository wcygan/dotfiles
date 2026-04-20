---
title: Large files
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Data-Structure-for-Large-Files
fetch-when: User is uploading multi-GB files or seeing chunking-related issues.
---

# Large files

SeaweedFS handles big files via a chunk-and-manifest structure managed by the filer. The blob store never sees a single huge object; it sees many ~8 MB chunks tied together by metadata.

## Chunking strategy

- **Small (< ~8 MB)**: stored as a single blob.
- **Medium**: split into multiple chunks. The filer keeps a list of `{fid, offset, size, encryption, compression}` entries, ~40 bytes per chunk.
- **Super-large**: a **manifest chunk** holds up to 1000 child-chunk pointers. So one manifest → up to 1000 × 8 MB = ~8 GB. Multiple levels of manifest → TB-scale.

The manifest is stored on a volume server (same as content blobs), so the filer's metadata store doesn't balloon with chunk lists.

## Practical capacity

One file with 1 level of manifest: ~8 GB. With 2 levels: ~8 TB. The design stops at 2 because multi-level indirection makes read latency unpredictable. For most uses, plenty.

## Upload / download

`weed filer`, `weed mount` (FUSE), and `weed filer.copy` all auto-chunk on upload and reassemble on read. The S3 gateway uses multipart upload semantics — each part is one chunk.

## When this matters for you

- **Client app uploading a 2 GB video**: just PUT it to the filer; chunking is automatic.
- **Restore from backup**: ensure chunks and manifest are all present — a missing chunk in the middle = unreadable file.
- **Erasure-coded warm volumes**: EC encodes at the volume level, so every chunk of a large file goes through EC normally.

## Gotcha

If you're managing `fid`s yourself at the blob-store level (not via filer), you're **not** getting chunking — each POST is one blob, capped by the volume's max size. Use the filer or S3 gateway for anything that could exceed ~8 MB reliably.
