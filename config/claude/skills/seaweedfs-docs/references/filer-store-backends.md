---
title: Filer store backends
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Choosing-a-Filer-Store
fetch-when: Picking or migrating a filer metadata store; diagnosing filer-store performance issues.
---

# Filer store backends

The filer's metadata store is configurable. The right choice depends on HA needs, directory-mutation patterns, and operational complexity you're willing to carry.

## Supported backends

| Backend | Type | HA-capable | Notes |
|---|---|---|---|
| **leveldb2** | Embedded KV | No | Default for `weed mini`. Process-local. No multi-filer. |
| **sqlite** | Embedded SQL | No | Single-file; easy backup. |
| **leveldb3** | Embedded KV | No | Newer leveldb format; per-bucket dbs. |
| **postgres / postgres2** | SQL | Yes | Production HA choice for small-to-mid clusters. |
| **mysql / mysql2** | SQL | Yes | Same tier as postgres. |
| **mongodb** | Document | Yes | Less common. |
| **redis / redis2 / redis3** | KV | Yes | Very fast reads; memory-bounded. |
| **cassandra / cassandra2** | Wide-column | Yes | Scales horizontally; tombstone gotcha below. |
| **elastic7** | Search | Yes | Rarely used. |
| **etcd** | KV (raft) | Yes | Small metadata only. |
| **tikv / ydb / cockroachdb / tidb / memsql** | Distributed SQL | Yes | Heavy stacks; overkill for most homelabs. |

## Decision rules of thumb

1. **Single-node dev / proof-of-concept** → leveldb2. Zero config.
2. **Small HA (< ~10 M files)** → postgres or mysql. Plenty of headroom, well-understood ops, trivial backup.
3. **High metadata op rate with hot-dir patterns** → route the hot paths to redis via path-specific store.
4. **Massive scale (100 M+ files)** → cassandra or scylla.
5. **Avoid** mixing cassandra with write-heavy directories (`/tmp`, stage dirs) — tombstones accumulate and degrade scans. Route those specific paths to redis.

## The tombstone gotcha

The wiki page `Choosing-a-Filer-Store` highlights one case study: `/tmp` as a staging dir with frequent churn on Cassandra → read performance degraded over time. Fix was path-specific filer store routing that directory to Redis.

## HA implication for SeaweedFS operator

The operator's `filer.replicas: N` only works if the backend is shareable. Leveldb2 (embedded) defeats HA — two filer pods will each have a private view. For `filer.replicas: 2+` you must configure an external store in the filer `config:` block.

## Anton note

anton's SeaweedFS install (ADR 0019) currently uses the operator's default embedded leveldb backend under `filer.replicas: 2`. Phase 1 shakeout proved this *does* hold client traffic across filer-pod kills — surviving filer serves, replaced pod takes ~60s to rejoin but clients see zero errors. If that behavior ever stops being acceptable, migrate to an external Postgres backend and delete the leveldb PVC.
