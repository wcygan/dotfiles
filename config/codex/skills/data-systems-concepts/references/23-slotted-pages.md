# Slotted Pages

Use this when implementing variable-length records inside fixed-size pages.

## Mental Model

A slotted page separates stable record identifiers from physical record placement. The slot directory grows from one side of the page while cell data grows from the other. Records can move within the page while slot IDs remain stable.

## Key Invariants

- Slot entries point to valid cell ranges.
- Free space is the gap between slot directory and cell area.
- Moving a cell updates the slot and preserves the logical record ID.

## Implementation Exercise

Implement insert and get for variable-sized cells, then add delete with tombstoned slots and page compaction.

## Tests And Failure Cases

Insert variable-size records until the page is full. Delete middle records and verify slot ID stability after compaction.

## Online References

- [PostgreSQL Storage Page Layout](https://www.postgresql.org/docs/current/storage-page-layout.html)
- [SQLite B-Tree Pages](https://www.sqlite.org/fileformat.html#b_tree_pages)
- [CMU 15-445 Storage Notes](https://15445.courses.cs.cmu.edu/fall2024/notes/03-storage1.pdf)

