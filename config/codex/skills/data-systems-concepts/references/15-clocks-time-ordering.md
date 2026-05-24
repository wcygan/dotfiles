# Clocks, Time, And Ordering

Use this when studying logical clocks, physical clocks, causal ordering, timestamps, clock uncertainty, or external consistency.

## Mental Model

Time in distributed systems is a tool for ordering, not a single shared fact. Logical clocks summarize happens-before relationships but do not recover exact causality by themselves. Physical clocks provide useful approximations with uncertainty. Systems that expose time-based guarantees need to account for skew, delay, and monotonicity.

## Key Invariants

- Lamport timestamps preserve happens-before in one direction: if `a` happened before `b`, then `clock(a) < clock(b)`.
- Physical-time decisions include uncertainty or synchronization assumptions.
- Causal claims require message or dependency tracking.

## Implementation Exercise

Implement Lamport clocks for a message-passing simulation and use them to demonstrate one-way happens-before ordering.

## Tests And Failure Cases

Create concurrent events with arbitrary scalar order and verify that the implementation does not infer causality from timestamp order alone.

## Online References

- [Time, Clocks, and the Ordering of Events](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)
- [Spanner Paper](https://research.google/pubs/pub39966/)
- [Google Cloud Spanner TrueTime](https://cloud.google.com/spanner/docs/true-time-external-consistency)
