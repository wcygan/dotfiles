---
title: FAQ
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/FAQ
fetch-when: Debugging unexpected behavior; something "feels wrong" and you want the upstream-acknowledged list of gotchas.
---

# FAQ (condensed)

The wiki's FAQ captures the operator's most-hit pitfalls.

**Volume sizing.** A "volume" is a disk *file*, not a physical disk. Default 30 GB each, 8 max per server. Override: `weed master -volumeSizeLimitMB=...` and `weed volume -max=...`. Different replication codes / collections / TTLs / disk types / S3 buckets get separate volume sets.

**Memory pressure.** Volume servers load the per-file index into RAM (~16 bytes/entry). High file counts → high RAM. Convert cold volumes to erasure-coded (`.sdx` sorted files) to move the index to disk. See [erasure-coding](erasure-coding.md).

**All-SSD clusters.** Leave disk-type flags empty. If you need to segregate hot paths, use path-specific filer configuration.

**Large volumes (>30 GB).** Older versions capped at 30 GB. Use `_large_disk` builds (17-byte entries, up to 8 TB per volume). Migration: remove `.idx`, `weed fix`, restart. Not compatible with standard builds.

**Disk space not freed after delete.** Deletion marks blobs; space reclaimed during volume vacuum (default 30% garbage threshold). Force via `weed shell`:
```
volume.vacuum -garbageThreshold=0.0001
```

**Inconsistent file sizes across replicas.** For 010-replicated volumes, sizes may differ momentarily due to failed writes or staggered compaction. Confirmed writes are strongly consistent; eventual consistency applies only to lazy operations like vacuum.

**Automatic chunking for large files.** `weed filer`, `weed mount`, `weed filer.copy` auto-chunk 500 MB–10 GB+ files. TB-scale works; metadata scales linearly with chunk count.

**gRPC port.** Derived as HTTP port + 10000. Custom gRPC: `<host>:<port>.<grpcPort>` in CLI args.

**Upgrades.** Minor-version upgrades are backward compatible. `standard → _large_disk` requires manual `.dat` copy + `weed fix` regen.

**Dashboards.**
- Master: `http://host:9333`
- Volume: `http://host:8080/ui/index.html`
- Admin (optional): `http://host:23646`
