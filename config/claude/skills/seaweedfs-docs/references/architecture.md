---
title: Architecture
canonical-url: https://github.com/seaweedfs/seaweedfs
fetch-when: Explaining SeaweedFS's data model, blob IDs, or why reads are O(1). The README's "Blob Store Architecture" section is the canonical source.
---

# Architecture

SeaweedFS splits into two layers: a **blob store** (master + volume servers) that does O(1) key-value reads, and an optional **filer** that adds a filesystem abstraction on top.

## The split vs. chunk-oriented designs

Traditional distributed filesystems (HDFS, Ceph) chunk each file and keep a central mapping of filenames → chunks on a metadata server. That central server becomes a concurrency bottleneck for small-file workloads.

SeaweedFS inverts this. The master only tracks **volume ID → volume server** (which changes rarely and is small). Per-file metadata lives on the volume server that holds the file. Each entry is ~16 bytes (64-bit key, 32-bit offset, 32-bit size) + map overhead; total reported as ~40 bytes/file on disk. This fits in memory on the volume server, so a read is one disk seek.

## Blob ID format

The master returns a **file ID** (aka `fid`) on assignment: `<volumeId>,<fileKey><fileCookie>` — e.g. `3,01637037d6`.

- `volumeId`: unsigned 32-bit int, picks the volume server
- `fileKey`: unsigned 64-bit int, monotonically growing
- `fileCookie`: unsigned 32-bit int, anti-URL-guessing

Store the fid as a string (~33 bytes as ASCII) or as 16 bytes binary. That's your database field.

## Write path

1. Client POSTs `/dir/assign` to master → gets `{fid, url}`.
2. Client POSTs the blob content to `<url>/<fid>`.
3. Volume server writes to its append-only volume file.

## Read path

1. Client GETs `/dir/lookup?volumeId=N` (cache this — volumes rarely move).
2. Client GETs `<volumeUrl>/<fid>` directly from the volume server.
3. Volume server does one in-memory metadata lookup → one disk seek → returns.

URL variants supported: `<url>/3,01637037d6`, `<url>/3/01637037d6`, with optional `.ext` suffix and `?width=...&height=...&mode=fit|fill` for image resize.

## Filer overlay

Filer is a separate, linearly-scalable stateless server. It maps paths ↔ `{fid, size, chunks, xattrs}` in a pluggable metadata store (Redis, Cassandra, Postgres, MySQL, LevelDB, SQLite, etc. — see [filer-store-backends](filer-store-backends.md)). Large files are chunked; the filer stores a chunk manifest. See [large-files](large-files.md).

## Rack / DC awareness

Volume servers advertise `-rack` and `-dataCenter` flags at startup. The master places volume replicas according to the replication code on the volume (see [replication](replication.md)).
