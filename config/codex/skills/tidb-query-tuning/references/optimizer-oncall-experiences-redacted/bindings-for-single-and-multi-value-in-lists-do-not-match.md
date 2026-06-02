# Bindings for Single- and Multi-Value IN Lists Do Not Match

## User Symptom
- A binding created for `IN (?)` does not work when the same application later sends `IN (?, ?, ?)` or another multi-value variant.

## Investigation Signals
- The normalized digest for `IN (?)` is different from the normalized digest for `IN (...)`.
- The binding exists and is valid, but only one of the two SQL shapes can hit it.

## Workaround
- Create two bindings:
  one for `IN (?)` and another for `IN (...)`.
- Verify both normalized forms before closing the case.

## Fixed Version
- `v7.4`

## Public References
- https://github.com/pingcap/tidb/pull/44601
