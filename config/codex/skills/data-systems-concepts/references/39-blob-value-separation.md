# Blob And Value Separation

Use this when studying large values, write amplification, LSM value logs, garbage collection, or pointer stability.

## Mental Model

Value separation stores large values outside the main index or LSM structure and keeps pointers in the sorted path. This reduces compaction cost for large values, but it adds garbage collection, pointer validation, and crash-recovery complexity.

## Key Invariants

- Index entries point to durable value locations.
- Value-log garbage collection preserves values still reachable from the index.
- Crashes cannot leave acknowledged values unreachable.

## Implementation Exercise

Build a key-value store that writes large values to an append-only value log and stores durable key-to-offset pointer metadata that can be reconstructed on restart.

## Tests And Failure Cases

Update a key repeatedly, compact the value log, and crash during pointer metadata update. Verify value-log replay or manifest recovery keeps reachable values valid.

## Online References

- [WiscKey Paper](https://www.usenix.org/conference/fast16/technical-sessions/presentation/lu)
- [RocksDB BlobDB](https://github.com/facebook/rocksdb/wiki/BlobDB)
- [BadgerDB Design](https://dgraph-io.github.io/badger/design.html)
