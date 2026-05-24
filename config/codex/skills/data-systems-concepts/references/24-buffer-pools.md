# Buffer Pools

Use this when studying page caching, eviction, dirty pages, pin counts, flushing, and interaction with WAL.

## Mental Model

A buffer pool is the memory boundary between logical page access and disk I/O. It tracks which pages are resident, which are dirty, and which are safe to evict. WAL and checkpoints constrain when dirty pages may reach disk.

## Key Invariants

- Pinned pages are not evicted.
- Dirty pages are flushed only in an order compatible with recovery.
- Page IDs map to at most one active frame.

## Implementation Exercise

Build a small buffer pool with fixed frames, page table, pin and unpin, dirty tracking, and LRU eviction.

## Tests And Failure Cases

Try to evict pinned pages, flush dirty pages, and reload evicted pages. Verify page table consistency.

## Online References

- [CMU 15-445 Buffer Pool Notes](https://15445.courses.cs.cmu.edu/fall2024/notes/06-bufferpool.pdf)
- [PostgreSQL Resource Consumption: Shared Buffers](https://www.postgresql.org/docs/current/runtime-config-resource.html)
- [SQLite Architecture: Page Cache And Pager](https://www.sqlite.org/arch.html)
