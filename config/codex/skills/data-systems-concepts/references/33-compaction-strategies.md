# Compaction Strategies

Use this when comparing leveled, size-tiered, universal, or time-window compaction.

## Mental Model

Compaction is maintenance work that rewrites immutable files to improve future reads and reclaim space. The strategy controls write amplification, read amplification, space amplification, and tail latency. There is no universal best strategy; workload shape dominates.

## Key Invariants

- Compaction preserves the newest visible value for each key.
- Tombstones are retained until they have covered older data.
- Readers see a consistent view while files are being replaced.

## Implementation Exercise

Simulate leveled and size-tiered compaction over generated SSTables and measure read fanout and bytes rewritten.

## Tests And Failure Cases

Include overlapping ranges, repeated updates, and tombstones. Verify output ordering and latest-value semantics.

## Online References

- [RocksDB Compaction](https://github.com/facebook/rocksdb/wiki/Compaction)
- [LevelDB Implementation Notes](https://github.com/google/leveldb/blob/main/doc/impl.md)
- [Apache Cassandra Compaction](https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/index.html)
