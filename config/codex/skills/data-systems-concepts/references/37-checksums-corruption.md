# Checksums And Corruption

Use this when studying torn writes, bit rot, partial writes, page validation, WAL validation, and corruption handling.

## Mental Model

Checksums make corruption visible. They do not repair data by themselves. A storage engine decides where to place checksums based on the unit it wants to validate: log record, page, block, segment, or file. Recovery must treat failed validation as a first-class outcome.

## Key Invariants

- The checksum covers the bytes needed to validate one durable unit.
- Metadata cannot be trusted until validation succeeds.
- Recovery knows whether to stop, skip, repair, or fail closed.

## Implementation Exercise

Add checksums to log records and reject partial or corrupted records during replay.

## Tests And Failure Cases

Flip each byte in a record and verify detection. Truncate the record and verify replay stops safely.

## Online References

- [PostgreSQL Data Checksums](https://www.postgresql.org/docs/current/checksums.html)
- [SQLite WAL File Format](https://www.sqlite.org/walformat.html)
- [ZFS End-to-End Data Integrity](https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Checksums.html)

