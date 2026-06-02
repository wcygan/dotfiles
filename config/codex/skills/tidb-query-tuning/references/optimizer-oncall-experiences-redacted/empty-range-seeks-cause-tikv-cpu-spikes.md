# Empty Range Seeks Cause TiKV CPU Spikes

## User Symptom
- TiKV CPU is high while the query returns very few rows.
- End-to-end latency is bad even though the result set is tiny.

## Investigation Signals
- `total_keys` is much larger than `total_process_keys`.
- Seek-heavy metrics are abnormal.
- The pattern often appears with long `IN` lists or index-join inner-side range amplification.
- `tot_wait` and task counts can also show heavy queueing pressure in TiKV.

## Workaround
- Change the plan with hints or bindings.
- Reduce the size of the `IN` list or split the request.
- Tune `tidb_opt_range_max_size` if range construction is the trigger.
- In some cases, a table scan is less harmful than exploding the number of cop tasks.

## Fixed Version
- No single fix version was recorded. This is a recurring task-amplification pattern.
