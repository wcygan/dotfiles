# Snapshotting And Checkpoints

Use this when studying database checkpoints, stream checkpoints, snapshots, restart time, or recovery boundaries.

## Mental Model

A checkpoint records enough durable state to reduce recovery work. It usually does not eliminate the log; it provides a point from which the system can resume scanning. Good checkpoints balance runtime overhead, recovery time, and consistency of captured state.

## Key Invariants

- Checkpoint metadata identifies the log position needed for recovery.
- A completed checkpoint records a valid recovery start position plus enough dirty-page and active-transaction metadata for replay.
- Recovery after checkpoint plus later log replay matches uninterrupted execution.

## Implementation Exercise

Add fuzzy checkpoints to a toy WAL engine: record dirty pages and active transactions, then recover from that point.

## Tests And Failure Cases

Crash during checkpoint writing and verify that recovery uses the previous complete checkpoint.

## Online References

- [PostgreSQL WAL Configuration: Checkpoints](https://www.postgresql.org/docs/current/wal-configuration.html)
- [Apache Flink Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/)
- [Distributed Snapshots](https://lamport.azurewebsites.net/pubs/chandy.pdf)
