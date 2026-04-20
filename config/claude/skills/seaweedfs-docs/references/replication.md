---
title: Replication
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Replication
fetch-when: User asks what a specific replication code means, why replicas aren't being created, or how to repair under-replicated volumes.
---

# Replication

Replication in SeaweedFS is **per-volume, not per-file**. You pick a code when a volume is created; all writes to that volume copy to N replicas synchronously.

## The xyz code

Three digits, each = number of *extra* copies at that topology level:

| Code | x (other DC) | y (other rack, same DC) | z (other server, same rack) | Total copies |
|------|--------------|-------------------------|------------------------------|--------------|
| 000  | 0 | 0 | 0 | **1** (no replication) |
| 001  | 0 | 0 | 1 | 2 |
| 010  | 0 | 1 | 0 | 2 |
| 100  | 1 | 0 | 0 | 2 |
| 110  | 1 | 1 | 0 | 3 |
| 200  | 2 | 0 | 0 | 3 |
| 220  | 2 | 2 | 0 | 5 |

Total copies = `1 + x + y + z`. Failure tolerance = total − 1.

## How placement works

Volume server exposes its rack and DC at startup:
```sh
weed volume -dir=/tmp/1 -port=8080 -dataCenter=dc1 -rack=r1
```
Master uses those labels to satisfy the code. If no servers match the topology requirement at the time of volume creation, volume creation fails.

## Setting replication

- Cluster default: `weed master -defaultReplication=001`
- Per-request override: `curl http://master:9333/dir/assign?replication=010`
- Per-DC override: `curl http://master:9333/dir/assign?dataCenter=dc1&replication=001`

## Write semantics

All N replicas must ack before the write completes. Strong consistency — a failed partial write surfaces as a failed write to the client. No read-quorum voodoo.

## Auto-repair? No.

> SeaweedFS does not rebalance or ensure the actual replication matches the set level under normal operation.

If a replica is lost (disk failure, node removal), volumes become read-only until you manually run `volume.fix.replication` via [weed shell](weed-shell.md). Use `-doDelete=false` on aging hardware so a failed repair doesn't cascade into more deletions.

## Replication vs erasure coding

Replication is for hot data (fast, simple). Erasure coding reduces storage overhead ~3.6× but with reconstruction cost and ~50% read penalty — suited for warm/cold volumes. EC is applied **asynchronously** to existing replicated volumes via a worker job; they're complementary, not exclusive. See [erasure-coding](erasure-coding.md).

## Anton note

In anton cluster, SeaweedFS runs with `defaultReplication: "000"` because Longhorn underneath already provides replica-count-2 durability on each volume-server PVC. Double-replicating would waste ~2× the storage for no added durability. See ADR 0019.
