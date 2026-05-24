# Consensus And Replicated Logs

Use this when studying Raft, Paxos, Zab, replicated state machines, log commitment, or quorum-safe reconfiguration.

## Mental Model

Consensus lets nodes agree on a sequence of commands despite failures. A replicated log is the usual shape: elect a leader, append entries, replicate to a quorum, commit entries, and apply them in order. The safety property is that committed log positions do not change.

## Key Invariants

- At most one value is chosen for each log index.
- A committed entry survives leader changes.
- State machines apply the same committed entries in the same order.
- Membership changes preserve quorum overlap across old and new configurations.

## Implementation Exercise

Implement a minimal Raft log with leader append, follower match indexes, and commit advancement.

## Tests And Failure Cases

Partition the leader, elect a new leader, and verify that conflicting uncommitted entries or configuration changes resolve safely.

## Online References

- [Raft Extended Paper](https://raft.github.io/raft.pdf)
- [Paxos Made Simple](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
- [ZooKeeper System Paper](https://www.usenix.org/legacy/event/atc10/tech/full_papers/Hunt.pdf)
