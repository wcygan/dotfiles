# Compression

Use this when studying block compression, column encodings, dictionary encoding, prefix compression, or storage-size tradeoffs.

## Mental Model

Compression reduces bytes at the cost of CPU and sometimes random-access complexity. Data systems often compress at block or page boundaries so reads can decompress only the relevant unit. The best encoding depends on data distribution and access pattern.

## Key Invariants

- Compression boundaries match the read and recovery unit.
- Metadata identifies codec, compressed length, and uncompressed length.
- Corruption detection happens before trusting decompressed data.

## Implementation Exercise

Implement prefix compression with restart points for sorted string keys inside a block and measure encoded size.

## Tests And Failure Cases

Decode from restart points, corrupted lengths, and empty strings. Verify round trips and bounds checks.

## Online References

- [Parquet Encodings](https://parquet.apache.org/docs/file-format/data-pages/encodings/)
- [ORC File Format Specification](https://orc.apache.org/specification/ORCv1/)
- [Zstandard Documentation](https://facebook.github.io/zstd/)
