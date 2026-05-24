# B-Tree Indexes

Use this when studying ordered indexes, range scans, fanout, splits, merges, separators, and page-oriented search trees.

## Mental Model

A B-Tree keeps sorted keys in high-fanout pages so lookup and range scan cost scale with tree height. Page splits preserve ordering while creating new separators for parents. Practical B-Trees need concurrency, recovery, and page layout rules in addition to search logic.

## Key Invariants

- Keys are ordered within each node.
- Child ranges match parent separator keys.
- All leaves remain reachable from the root.

## Implementation Exercise

Implement search and leaf split first. Add internal-node split only after leaf invariants are tested.

## Tests And Failure Cases

Insert ascending, descending, and random keys. Verify sorted iteration and search after every split.

## Online References

- [SQLite B-Tree Pages](https://www.sqlite.org/fileformat.html#b_tree_pages)
- [PostgreSQL B-Tree Indexes](https://www.postgresql.org/docs/current/btree.html)
- [Organization and Maintenance of Large Ordered Indexes](https://link.springer.com/article/10.1007/BF00288683)
