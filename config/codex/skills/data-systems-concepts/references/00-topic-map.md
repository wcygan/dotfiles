# Topic Map

Use this map to choose the smallest relevant reference file. Start high when the user asks about architecture or dataflow. Move lower when the user asks about storage layout, recovery, indexing, or implementation details.

## High-Level Dataflow

- `01-data-system-architecture.md`: storage, execution, transactions, and recovery as system boundaries.
- `02-log-as-system-abstraction.md`: logs as replayable history and coordination substrate.
- `03-stream-processing.md`: continuous computation over ordered records.
- `04-event-time-watermarks.md`: event time, processing time, late data, and window completion.
- `05-derived-data-materialized-views.md`: projections, indexes, caches, and repair.

## Distributed Systems

- `06-replication-topologies.md`: leader, follower, leaderless, and log-based replication shapes.
- `07-quorum-systems.md` and `08-consistency-models.md`: quorum behavior and client-visible guarantees.
- `09-transactions-isolation.md` through `12-leader-election.md`: transactions, consensus logs, and leadership authority.
- `13-failure-detection-gossip.md` through `19-crdts.md`: failure, partitioning, time, leases, snapshots, repair, and conflict resolution.
- `20-testing-data-systems.md` and `21-model-checking-simulation.md`: how to test the claims.

## Storage Engines

- `22-pages-file-formats.md` through `24-buffer-pools.md`: page layout, slotted pages, and page caching.
- `25-btree-indexes.md` through `27-secondary-indexes.md`: ordered indexes, concurrency, and alternate access paths.
- `28-wal-implementation.md` through `31-snapshotting-checkpoints.md`: logging, recovery, MVCC, and checkpoints.
- `32-lsm-sstables.md` through `39-blob-value-separation.md`: LSMs, compaction, filters, hashes, compression, checksums, columnar files, and large values.

## Online References

- [Architecture of a Database System](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf)
- [Jepsen Consistency Models](https://jepsen.io/consistency/models)
- [Kafka Design](https://kafka.apache.org/documentation/#design)
- [PostgreSQL Internals: Storage Page Layout](https://www.postgresql.org/docs/current/storage-page-layout.html)
- [Raft Extended Paper](https://raft.github.io/raft.pdf)
