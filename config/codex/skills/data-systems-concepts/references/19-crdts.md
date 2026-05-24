# CRDTs

Use this when studying conflict-free replicated data types, offline writes, merge functions, monotonic state, and eventual convergence.

## Mental Model

A CRDT encodes updates so independently modified replicas can merge without coordination and converge. State-based CRDTs merge by least upper bound. Operation-based CRDTs disseminate operations with delivery assumptions. The useful test is whether concurrent updates commute or merge deterministically.

## Key Invariants

- Merge is associative, commutative, and idempotent for state-based CRDTs.
- Metadata is sufficient to preserve concurrent information.
- Tombstones or causal context prevent deleted data from reappearing accidentally.

## Implementation Exercise

Implement a grow-only set, two-phase set, and observed-remove set. Compare metadata costs.

## Tests And Failure Cases

Merge state-based replicas in every order. For operation-based CRDTs, test the stated delivery and deduplication assumptions directly.

## Online References

- [CRDT Papers](https://crdt.tech/papers.html)
- [A comprehensive study of Convergent and Commutative Replicated Data Types](https://inria.hal.science/inria-00555588/document)
- [Delta State Replicated Data Types](https://arxiv.org/abs/1410.2803)
