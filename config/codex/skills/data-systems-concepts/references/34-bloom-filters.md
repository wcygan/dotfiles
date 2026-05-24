# Bloom Filters

Use this when studying probabilistic membership tests, negative lookups, false positives, and read amplification.

## Mental Model

A Bloom filter answers "definitely not present" or "maybe present." Storage engines use it to skip files or pages during negative lookups. The design trades memory for false-positive probability and must match the key count and hash count to the workload.

## Key Invariants

- A properly built Bloom filter has no false negatives for inserted keys.
- False positives are allowed and measured.
- Filter metadata matches the expected number of keys and hash functions.

## Implementation Exercise

Implement a Bloom filter with double hashing. Measure false-positive rate for different bit budgets.

## Tests And Failure Cases

Insert known keys, assert no false negatives, then test many absent keys and estimate false positives.

## Online References

- [Bloom's Original Paper](https://www.cs.princeton.edu/courses/archive/spr05/cos598E/bib/p422-bloom.pdf)
- [LevelDB Table Format](https://github.com/google/leveldb/blob/main/doc/table_format.md)
- [RocksDB Bloom Filter Wiki](https://github.com/facebook/rocksdb/wiki/RocksDB-Bloom-Filter)
