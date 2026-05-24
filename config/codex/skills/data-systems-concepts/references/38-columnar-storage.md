# Columnar Storage

Use this when studying analytic storage, column files, vectorized scans, predicate pushdown, compression, and late materialization.

## Mental Model

Columnar storage groups values by column instead of by row. Analytical scans can read only needed columns and compress similar values effectively. The tradeoff is point updates, tuple reconstruction, and write-path complexity.

## Key Invariants

- Column chunks align to reconstruct rows or row groups.
- Encodings preserve nulls, order where needed, and type metadata.
- Predicate pushdown is correct for encoded statistics and min/max metadata.

## Implementation Exercise

Write a small column chunk format with row groups, per-column min/max, and scan-time predicate pruning.

## Tests And Failure Cases

Verify row reconstruction across nullable columns and predicate behavior at min/max boundaries.

## Online References

- [The C-Store Paper](https://www.vldb.org/conf/2005/papers/p553-stonebraker.pdf)
- [Apache Parquet File Format](https://parquet.apache.org/docs/file-format/)
- [Apache ORC Specification](https://orc.apache.org/specification/ORCv1/)

