# Pages And File Formats

Use this when studying how a database stores records, pages, headers, checksums, free space, offsets, and file-level metadata.

## Mental Model

A file format is an on-disk contract. Pages bound I/O and recovery. Records inside pages need a layout that supports lookup, growth, deletion, and versioning. The first design question is which bytes are stable enough for recovery and future compatibility.

## Key Invariants

- Page headers identify enough structure to parse the page.
- Offsets and lengths point inside page bounds.
- Versioning or magic values detect incompatible formats.

## Implementation Exercise

Define a fixed page size, page header, cell region, and slot directory. Write encode/decode round trips.

## Tests And Failure Cases

Fuzz offset and length fields. Verify that parsing rejects out-of-bounds records.

## Online References

- [PostgreSQL Storage Page Layout](https://www.postgresql.org/docs/current/storage-page-layout.html)
- [SQLite Database File Format](https://www.sqlite.org/fileformat.html)
- [LevelDB File Format](https://github.com/google/leveldb/blob/main/doc/table_format.md)

