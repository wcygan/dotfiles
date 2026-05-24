# Transactions And Isolation

Use this when studying atomicity, isolation levels, anomalies, snapshot isolation, serializability, or transaction tests.

## Mental Model

A transaction groups operations under a contract for visibility and failure. Isolation controls which interleavings are observable. The practical skill is recognizing anomalies as small histories: dirty reads, lost updates, write skew, phantoms, and serialization cycles.

## Key Invariants

- Commit makes the transaction's effects visible according to the isolation level.
- Abort makes uncommitted effects non-visible and releases transaction resources.
- The isolation level defines which concurrent histories are legal.

## Implementation Exercise

Implement a tiny transaction scheduler for two accounts and inject interleavings that produce lost update and write skew.

## Tests And Failure Cases

Write table-driven histories and classify each anomaly under read committed, repeatable read, snapshot isolation, and serializable.

## Online References

- [A Critique of ANSI SQL Isolation Levels](https://arxiv.org/abs/cs/0701157)
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [Serializable Snapshot Isolation in PostgreSQL](https://arxiv.org/abs/1208.4179)
