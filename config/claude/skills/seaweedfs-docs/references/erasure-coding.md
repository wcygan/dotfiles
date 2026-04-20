---
title: Erasure Coding
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Erasure-Coding-for-warm-storage
fetch-when: User is considering EC for storage savings, or sizing network cost of a degraded-read scenario.
---

# Erasure Coding

Applied *after* volumes go cold/read-only. Trades 1.4× storage overhead (vs ~3× for replicated) for slower reads and no-update semantics.

## Default: RS(10,4)

- 10 data shards + 4 parity shards = 14 total per volume
- Rack-aware: shards distribute across disks → servers → racks to survive multiple failure domains
- Tolerates 4 missing shards simultaneously
- Storage overhead: 14/10 = 1.4× raw
- Compare with 5× replication: ~3.6× savings

## Lifecycle

Volumes start as replicated (fast writes). When they fill up and stop being written (defaults: 80% full and untouched for 5 minutes), a worker job converts them to EC:

1. Volume is marked read-only.
2. Data shards + parity shards computed, distributed across cluster.
3. Original volume files can be deleted after verification.

The `erasure_coding` plugin worker runs automatically; configure thresholds in admin UI or via `weed admin`.

## Read path after EC

- Full-shard read (common case): similar to replicated, ~50% slower due to the extra network hop to gather shards.
- Degraded read (some shards missing): reconstruct on-the-fly by pulling parity shards from other disks. Heavier — whole volume shards stream across the network.

## Update semantics

**EC volumes are read-only and delete-only.** You cannot update an object in an EC volume. Writes always go to a new replicated volume; deletes mark the blob as deleted and space is reclaimed on the next compaction/rebuild.

## When to enable

- Archives, backups, compliance retention — infrequent read, no update.
- Cost-sensitive storage tiers where 1.4× vs 3× storage difference matters at TB scale.

## When to avoid

- Hot data with frequent updates.
- Latency-sensitive reads where an extra network hop hurts.
- Small clusters where you can't spread 14 shards across distinct failure domains (minimum 14 disks/servers recommended).

## Anton note

Not wired up yet in anton's SeaweedFS install. Longhorn already provides replica-count-2 durability at the block layer (ADR 0005), so adding EC on top would compound cost. If/when data warrants, EC would be applied to SeaweedFS volumes whose underlying Longhorn PVCs are dropped to replica-count-1 — a meaningful storage-efficiency change that deserves its own ADR.
