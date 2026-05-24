# WAL Implementation

Use this when implementing write-ahead logging, log records, LSNs, pageLSNs, flush ordering, and crash recovery.

## Mental Model

WAL records the intent or effect of changes before dirty pages reach storage. Recovery relies on the log being durable enough to redo or undo page changes. The key ordering rule is that the log record for a page update reaches stable storage before the page image containing that update.

## Key Invariants

- Every page update has a log record.
- A dirty page is flushed only after its log records are durable.
- Recovery can identify the last complete log record.

## Implementation Exercise

Implement log append with checksummed length-prefixed records, pageLSN tracking, and a redo pass.

## Tests And Failure Cases

Crash after log append, after page write, and in the middle of a log record. Verify restart behavior.

## Online References

- [PostgreSQL WAL Internals](https://www.postgresql.org/docs/current/wal-internals.html)
- [SQLite Write-Ahead Logging](https://www.sqlite.org/wal.html)
- [ARIES Recovery Paper](https://dl.acm.org/doi/10.1145/128765.128770)

