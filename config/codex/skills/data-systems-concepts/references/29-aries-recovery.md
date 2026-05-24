# ARIES Recovery

Use this when studying redo, undo, compensation log records, checkpoints, steal/no-force buffers, or recovery phases.

## Mental Model

ARIES supports high-performance buffer management by allowing dirty uncommitted pages to reach disk and committed pages to remain unflushed. Recovery uses analysis to find the state at crash, redo to repeat history, and undo to roll back loser transactions with compensation records.

## Key Invariants

- Redo is idempotent using pageLSN checks.
- Undo writes compensation log records.
- Checkpoints shorten recovery without replacing the log.

## Implementation Exercise

Model log records for begin, update, commit, abort, and compensation. Implement analysis, redo, and undo over a small page map.

## Tests And Failure Cases

Crash during undo and verify that compensation log records prevent repeating already-undone work.

## Online References

- [ARIES Recovery Paper](https://dl.acm.org/doi/10.1145/128765.128770)
- [CMU 15-445 Recovery Notes](https://15445.courses.cs.cmu.edu/fall2024/notes/21-recovery.pdf)
- [PostgreSQL WAL Internals](https://www.postgresql.org/docs/current/wal-internals.html)
