# MVCC

Use this when studying multi-version concurrency control, snapshots, visibility, vacuum, transaction IDs, and version chains.

## Mental Model

MVCC lets readers see a stable snapshot while writers create new versions. Visibility rules decide which version each transaction can observe. MVCC moves contention away from readers, but it creates storage cleanup, conflict detection, and long-running snapshot concerns.

## Key Invariants

- Each version records enough creation and deletion metadata for visibility checks.
- A snapshot defines which transaction IDs are visible.
- Garbage collection preserves versions needed by active snapshots.

## Implementation Exercise

Build an in-memory table with version chains and snapshots. Support insert, update, delete, and read at snapshot.

## Tests And Failure Cases

Run a long snapshot while many updates occur. Verify visibility and garbage-collection boundaries.

## Online References

- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL MVCC Introduction](https://www.postgresql.org/docs/current/mvcc-intro.html)
- [Serializable Snapshot Isolation in PostgreSQL](https://arxiv.org/abs/1208.4179)

