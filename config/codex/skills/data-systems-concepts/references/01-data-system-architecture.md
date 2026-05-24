# Data-System Architecture

Use this when a question spans multiple layers: storage, query execution, indexing, transactions, recovery, replication, or operations.

## Mental Model

A data system is a set of cooperating subsystems that turn writes into durable state, indexes, logs, and derived views. Good architecture separates the access path, durability path, concurrency path, and repair path. Most design mistakes come from hiding which subsystem owns a guarantee.

## Key Invariants

- Every durable write has a recoverable representation.
- Every read path has a defined freshness and consistency contract.
- Every derived structure can be rebuilt, repaired, or verified.

## Implementation Exercise

Draw a component map for a toy key-value store, then label the write path, read path, recovery path, and compaction or maintenance path.

## Tests And Failure Cases

Test crash points between log append, index update, and acknowledgment. Check whether restart reconstructs the promised state.

## Online References

- [Architecture of a Database System](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf)
- [CMU 15-445/645 Fall 2024 Course Notes](https://15445.courses.cs.cmu.edu/fall2024/notes/)
- [PostgreSQL Internals Documentation](https://www.postgresql.org/docs/current/internals.html)
