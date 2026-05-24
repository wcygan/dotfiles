# Anti-Entropy And Repair

Use this when studying replica divergence, read repair, background repair, Merkle trees, hinted handoff, or reconciliation.

## Mental Model

Anti-entropy is background convergence. Replicas compare summaries, identify differences, and exchange missing or newer data. The repair strategy depends on version metadata, tombstone handling, and how expensive full comparison is.

## Key Invariants

- Each replica can describe what version of data it has.
- Repair preserves deletes and conflict metadata.
- Background convergence does not violate foreground consistency expectations.

## Implementation Exercise

Build two divergent key-value maps, summarize them with per-range hashes, and repair only ranges that differ.

## Tests And Failure Cases

Include deletes, old versions, and conflicting concurrent writes. Verify that repair keeps the correct resolution metadata.

## Online References

- [Dynamo Paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Apache Cassandra Repair](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/repair.html)
- [Riak Active Anti-Entropy](https://docs.riak.com/riak/kv/latest/learn/concepts/active-anti-entropy/index.html)
