# Issue #67150: store/copr, executor: tidb_store_batch_size has no effect for tables with non-integer clustered primary key

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67150
- Status: open
- Type: type/unknown
- Created At: 2026-03-19T09:30:11Z
- Labels: contribution, report/customer, sig/execution, sig/planner

## Customer-Facing Phenomenon
- silently has no effect for tables whose primary key is a non-integer clustered index (e.g. , composite PK). The batching optimization only activates for single-integer PK tables.

## Linked PRs
- Fix PR #67260: executor: enable tidb_store_batch_size for non-integer clustered PK tables
  URL: https://github.com/pingcap/tidb/pull/67260
  State: open
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/executor, tests/integrationtest
  Sample Changed Files:
  - pkg/executor/builder.go
  - pkg/executor/executor_pkg_test.go
  - tests/integrationtest/r/executor/jointest/join.result
  - tests/integrationtest/t/executor/jointest/join.test
  PR Summary: What problem does this PR solve? had no effect when performing index joins on tables with a non-integer clustered (common handle) primary key (e.g. , composite PK). The store-batch coprocessor path is gated on , but the  branch in  was calling  which never sets hints. Root cause In , when  is true, KV ranges are built via  (with ) and passed directly to  → . That produces a  with . In :

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
