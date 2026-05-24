# Merkle Trees

Use this when comparing large data sets efficiently, verifying content, repairing replicas, or summarizing ranges.

## Mental Model

A Merkle tree hashes data at leaves and hashes child hashes up the tree. Equal root hashes imply equal content under the assumed hash function. Replicas can compare roots and descend only into differing subtrees, which makes repair efficient for mostly-equal data.

## Key Invariants

- Parent hashes commit to child hashes.
- Leaf ranges are deterministic and comparable across replicas.
- Repair handles deletes and versions, not only key presence.

## Implementation Exercise

Build a range-partitioned Merkle tree over sorted keys and compare two replicas to identify differing ranges.

## Tests And Failure Cases

Change one key, delete one key, and add one key. Verify the comparison returns the smallest differing tree ranges at the chosen leaf granularity.

## Online References

- [Dynamo Paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [RFC 6962: Certificate Transparency Merkle Trees](https://datatracker.ietf.org/doc/html/rfc6962)
- [Apache Cassandra Repair](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/repair.html)
