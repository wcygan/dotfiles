# Distributed Transactions

Use this when a transaction spans shards, services, logs, or storage engines with separate failure domains.

## Mental Model

Distributed transactions make multiple participants agree on commit or abort. The key tension is atomicity under coordinator failure. Two-phase commit gives atomicity with blocking. Newer systems reduce coordination, make execution deterministic, or weaken guarantees for availability.

## Key Invariants

- Every participant reaches the same final decision.
- A prepared participant can recover enough state to honor the final decision.
- Coordinator failure has a defined recovery or blocking behavior.

## Implementation Exercise

Build a 2PC simulation with coordinator log records, participant prepare records, and crash/restart recovery.

## Tests And Failure Cases

Crash the coordinator after collecting votes but before notifying all participants. Verify recovery decisions.

## Online References

- [Highly Available Transactions](https://www.vldb.org/pvldb/vol7/p181-bailis.pdf)
- [Calvin: Fast Distributed Transactions for Partitioned Database Systems](https://www.cs.umd.edu/~abadi/papers/calvin-sigmod12.pdf)
- [Percolator: Large-scale Incremental Processing](https://research.google/pubs/pub36726/)
- [PostgreSQL PREPARE TRANSACTION](https://www.postgresql.org/docs/current/sql-prepare-transaction.html)
