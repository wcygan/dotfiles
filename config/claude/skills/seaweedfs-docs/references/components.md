---
title: Components
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Components
fetch-when: User asks which component does what, what the default ports are, or whether a specific role is actually needed in their deployment.
---

# Components

SeaweedFS is a family of processes all embedded in one `weed` binary. You start each role as a subcommand (`weed master`, `weed volume`, etc.) or bundle them with `weed server`.

## Master (`weed master`)

Cluster state + file-ID assignment. Runs Raft; needs an **odd** number of peers (1, 3, 5) for HA. Two masters cannot reach consensus — "2 is worse than 1". A single master is production-acceptable for small clusters because load is minimal.

- Default HTTP port: **9333**
- Default gRPC port: **19333** (HTTP + 10000)
- Multi-master flag: `-peers=ip1:9333,ip2:9333,ip3:9333`
- Failover: automatic leader election

## Volume (`weed volume`)

Stores actual file bytes in append-only 30 GB volume files. Each volume server can own many volumes. Replication is enforced per volume, not per file (see [replication](replication.md)).

- Default HTTP port: **8080**
- Default gRPC port: **18080**
- Flags: `-dir=/data` (can be CSV list for multi-disk), `-max=N` (max volumes per dir), `-master=host:9333`, `-rack=r1`, `-dataCenter=dc1`
- Do **not** put multiple `-dir` entries on the same physical disk — one compaction blocks the other.

## Filer (`weed filer`)

Adds directories + POSIX-like metadata on top of the blob store. Stateless; all state in an external metadata store. Multiple filers can share one store for HA. The filer is what handles the S3 API, WebDAV, FUSE, and HTTP filer clients.

- Default HTTP port: **8888**
- Default gRPC port: **18888**
- Metadata store configured in `filer.toml`; see [filer-store-backends](filer-store-backends.md).

## S3 (`weed s3` or `weed filer -s3`)

AWS-compatible S3 gateway. Can run embedded in the filer process (simpler) or as a separate Deployment (better HA and independent scaling). On the operator side, 1.0.12+ introduces the standalone-S3 Deployment pattern via top-level `spec.s3`.

- Default HTTP port: **8333**
- IAM API is **embedded** in the S3 server on the same port (see [operator-iam](operator-iam.md))

## Admin (`weed admin`) *(optional, newer)*

Web UI for cluster management — volume placement, EC encoding triggers, worker scheduling.

- Default port: **23646** (in `weed mini`)

## Worker (`weed worker`) *(optional)*

Executes background jobs scheduled by the admin server — erasure coding runs, volume vacuum, replication fixes.

## Protocol gateways *(optional)*

- `weed webdav` — WebDAV server (port 7333 in `weed mini`)
- `weed filer -sftp` — SFTP frontend
- `weed nfs` — NFS server
- `weed mount` — FUSE mount (client-side, not a server)

## Quick topology decision

- Dev / throwaway: `weed mini` or `weed server`
- Blob-only app (you manage fids yourself): master + volume
- Filesystem / S3 / Harbor / anything user-facing: master + volume + filer (+ s3)
- HA filer: 2+ filers sharing an external metadata store (see [filer-store-backends](filer-store-backends.md)); embedded leveldb is **not** HA
