---
title: Production Setup
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Production-Setup
fetch-when: User is sizing a new cluster, hitting write hot-spots, or debugging a multi-master quorum problem.
---

# Production Setup

## Master quorum

- **1 master is fine** for small clusters — the master is lightly loaded (handles fid assignment and heartbeats).
- For HA, use **3 or 5** masters. Never 2 — can't reach Raft consensus.
- Start with `-peers=ip1:9333,ip2:9333,ip3:9333` on each.

## Volume servers

- **No forced rebalance.** Adding a server doesn't migrate existing data; new volumes absorb new writes. Rebalancing is network-expensive and manual.
- **Multiple volumes per host** prevents one compaction from blocking all I/O on that host.
- **One disk per `-dir`.** If a host has multiple disks, either comma-separate the `-dir` values with matching `-max` per directory, or run separate `weed volume` processes on different ports.
- **Don't colocate two `-dir`s on the same physical disk** — compaction contention.

## Filer HA

- Single-filer + leveldb2 is acceptable for minimal deployments.
- For HA: run 2+ filers behind a load balancer, sharing an **external** metadata store (Postgres, MySQL, Cassandra, Redis) — embedded leveldb is **not** shareable. See [filer-store-backends](filer-store-backends.md).

## Networking

- Firewall rules needed for: Master 9333/19333, Volume 8080/18080, Filer 8888/18888, S3 8333.
- Multi-homed servers: pass `-ip=<intra-cluster-ip>` for gRPC/cluster traffic, `-ip.bind=<public-ip>` for user-facing HTTP.
- gRPC port = HTTP port + 10000 by default; override with `<host>:<port>.<grpcPort>`.

## Security defaults

- Configure `WEED_S3_SSE_KEK` or `security.toml` *before* handling real data if using SSE-S3 encryption.
- JWT for filer access: see the wiki's "Filer JWT Use" page.
- When exposing volume servers across hosts, enable gRPC TLS via `security.toml`.

## Common production mistakes

1. **2-master "HA"** — not actually HA; use 1 or 3+.
2. **Rebalancing after add** — don't; it wastes bandwidth.
3. **Single-disk multi-dir** — contention.
4. **Embedded leveldb + multi-filer** — impossible, leveldb is process-local.
5. **No monitoring** — enable system metrics (Prometheus endpoints at `/metrics`).

## Sizing rule of thumb

One volume server holds N volumes, each 30 GB by default, mapped in memory with ~16 bytes of metadata per file. 1M small files per volume ≈ 16 MB RAM for its index. For read latency, RAM matters more than the drive (provided the drive is reasonable).

## Adjacent topics

- Filer metadata store tradeoffs → [filer-store-backends](filer-store-backends.md)
- EC for warm data → [erasure-coding](erasure-coding.md)
- Volume-level replication → [replication](replication.md)
