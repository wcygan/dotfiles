# Locking And Latching

Use this when distinguishing logical transaction locks from physical in-memory latches.

## Mental Model

Locks protect logical database objects across transaction boundaries. Latches protect short critical sections inside the engine. Mixing the two concepts leads to either unnecessary blocking or unsafe internal mutation. B-Tree code often needs latches for structure changes and locks for user-visible isolation.

## Key Invariants

- Latches are held for short in-memory operations.
- Locks follow the transaction isolation contract.
- Acquisition order prevents deadlock or includes deadlock detection.

## Implementation Exercise

Build a lock table with shared and exclusive locks, then separately model a page latch used only during page mutation.

## Tests And Failure Cases

Create two transactions that acquire locks in opposite orders and verify deadlock detection or timeout behavior.

## Online References

- [PostgreSQL Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- [Granularity of Locks and Degrees of Consistency](https://dl.acm.org/doi/10.1145/360363.360369)
- [CMU 15-445 Index Concurrency Notes](https://15445.courses.cs.cmu.edu/fall2024/notes/10-indexconcurrency.pdf)
