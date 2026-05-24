# Leader Election

Use this when studying leader leases, terms, epochs, split brain, failover, or primary selection.

## Mental Model

Leader election chooses one node to coordinate a scope of work. The election mechanism must connect leadership to a fencing token, term, epoch, or quorum-backed proof. Leadership without fencing creates split-brain writes when old leaders keep acting after losing authority.

## Key Invariants

- A leader has evidence of authority for a specific term or epoch.
- Newer terms supersede older terms.
- Storage and clients reject work from stale leaders when fencing is required.

## Implementation Exercise

Build a term-based election simulation where nodes vote once per term and clients include the leader term with writes.

## Tests And Failure Cases

Delay messages from an old leader and verify that followers reject stale-term writes.

## Online References

- [Raft Extended Paper](https://raft.github.io/raft.pdf)
- [Viewstamped Replication Revisited](https://www.cs.princeton.edu/courses/archive/fall19/cos418/papers/vr-revisited.pdf)
- [ZooKeeper Recipes and Solutions](https://zookeeper.apache.org/doc/current/recipes.html)
