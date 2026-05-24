# Log As System Abstraction

Use this when studying append-only logs, event sourcing, replication logs, WAL, Kafka topics, or replayable state machines.

## Mental Model

A log is an ordered record of facts. Systems use logs to decouple acceptance of writes from later indexing, replication, compaction, projection, and recovery. The main design question is what ordering the log provides and what state can be reconstructed from it.

## Key Invariants

- Appended records keep a stable order within their scope.
- Consumers can detect their position and resume from it.
- Replay produces the same state when handlers are deterministic and inputs are complete.

## Implementation Exercise

Build an append-only file with length-prefixed records, offsets, and a replay function that rebuilds an in-memory index.

## Tests And Failure Cases

Truncate records at every byte boundary and verify that replay stops at the last complete record.

## Online References

- [Kafka Design: Log](https://kafka.apache.org/documentation/#design)
- [The Log: What every software engineer should know](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)
- [PostgreSQL WAL Introduction](https://www.postgresql.org/docs/current/wal-intro.html)

