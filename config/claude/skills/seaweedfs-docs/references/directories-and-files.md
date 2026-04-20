---
title: Filer directories and files
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Directories-and-Files
fetch-when: User asks how the filer represents paths, or is debugging a specific metadata operation's performance.
---

# Filer directories and files

The filer is the layer that turns SeaweedFS's flat blob store into a hierarchical filesystem. It maps `<path>` → `{fid, size, chunks, xattrs, ttl, ...}` in a pluggable metadata store.

## What the filer is

A stateless HTTP/FUSE/SFTP/WebDAV/S3 frontend that:

- Persists path-to-fid mappings in an external store (LevelDB, SQLite, Postgres, MySQL, Redis, Cassandra, etc.).
- Resolves master lookups once per volume-id and caches the mapping.
- Handles chunking for large files (see [large-files](large-files.md)).
- Applies per-path configuration (different metadata store per prefix, different volume collection, etc.).

## Operation complexities

| Op | Cost |
|----|------|
| Get file by path | O(log N) for LSM/B-tree backends; O(1) for Redis/hash backends |
| List directory | Ordered scan for tree backends; O(1) for Redis-based |
| Put file | Recursive parent-directory create if missing |
| Rename file | O(1) — metadata swap |
| Rename directory | O(N) — rewrites all child paths |

## Scalability

Filer is "linearly scalable, limited only by the metadata store". Run 2+ behind a load balancer, each pointing at the same external backend. Embedded `leveldb` / `sqlite` are **not shareable** — they're per-process DBs.

## Choosing a backend

See [filer-store-backends](filer-store-backends.md). Common trade-off axes:

- **HA vs simplicity**: external SQL/NoSQL = HA, leveldb = single-node easy
- **Directory mutation patterns**: if one dir sees many updates, tombstone accumulation in Cassandra will bite — use path-specific routing to Redis for that dir
- **Dataset size**: Redis is fast but needs RAM proportional to metadata count

## Per-path config

`filer.toml` supports routing different paths to different stores:
```toml
[leveldb2]
enabled = true
dir = "/data/filerldb2"

[redis]
enabled = true
location = "/tmp/fast-metadata"
# (routing via filer.conf)
```

## Content vs metadata separation

Volume servers keep blob content. The filer only stores `{fid, size, chunks, mime, atime, mtime, xattrs}`. Large files are split into chunks, each a separate blob — the filer stores the *list* of fids, not the bytes.
