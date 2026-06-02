# Huge IN List Falls Back to Index Full Scan

## User Symptom
- A query with a very large `IN` list unexpectedly falls back to `IndexFullScan` and becomes very slow.

## Investigation Signals
- The `IN` list is extremely large.
- Decoding the full plan may be hard because the SQL and plan are both huge.
- The likely trigger is the optimizer range-construction limit controlled by `tidb_opt_range_max_size`.

## Workaround
- Do not send giant `IN` lists directly.
- Split the request into smaller batches or stage the keys in a table and join on it.
- Raise `tidb_opt_range_max_size` only if you explicitly accept the optimizer memory tradeoff.

## Fixed Version
- No general fix was recorded in the handbook.
