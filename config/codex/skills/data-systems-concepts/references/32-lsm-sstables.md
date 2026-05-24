# LSM Trees And SSTables

Use this when studying log-structured storage, memtables, immutable sorted files, sparse indexes, Bloom filters, and compaction.

## Mental Model

An LSM tree optimizes writes by buffering updates in memory and flushing immutable sorted files. Reads search recent memory plus older sorted files. Compaction rewrites files to reduce read amplification, remove overwritten values, and reclaim deletes.

## Key Invariants

- Each SSTable is immutable and sorted by key.
- Newer levels or sequence numbers take precedence over older data.
- Tombstones remain until all older values they cover are gone.

## Implementation Exercise

Build a memtable that flushes sorted key-value records to immutable files, then add lookup over memory and files.

## Tests And Failure Cases

Write duplicate keys and tombstones across files. Verify latest-value lookup and tombstone behavior.

## Online References

- [The Log-Structured Merge-Tree](https://dsf.berkeley.edu/cs286/papers/lsm-acta1996.pdf)
- [LevelDB Implementation Notes](https://github.com/google/leveldb/blob/main/doc/impl.md)
- [RocksDB Overview](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview)

