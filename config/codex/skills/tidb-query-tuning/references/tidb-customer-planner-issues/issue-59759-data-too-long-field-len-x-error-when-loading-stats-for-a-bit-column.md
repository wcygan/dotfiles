# Issue #59759: `Data Too Long, field len X` error when loading stats for a `bit` column

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59759
- Status: closed
- Type: type/bug
- Created At: 2025-02-25T13:38:14Z
- Closed At: 2025-04-15T08:57:08Z
- Labels: affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/major, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- Both async and sync load failed. In tidb log:

## Linked PRs
- Related PR #59768: table: Revert "table: fix the issue that the default value for `BIT` column is wrong (#57303)"
  URL: https://github.com/pingcap/tidb/pull/59768
  State: closed
  Merged At: 2025-02-26T04:38:33Z
  Changed Files Count: 5
  Main Modules: ddl/ddl_api.go, ddl/integration_test.go, executor/write_test.go, types/datum.go, types/datum_test.go
  Sample Changed Files:
  - ddl/ddl_api.go
  - ddl/integration_test.go
  - executor/write_test.go
  - types/datum.go
  - types/datum_test.go
  PR Summary: Reverts pingcap/tidb#57354 because of close #59769 We'll need to reconsider the solution / bugfix for both issues before the next release of 6.5.
- Fix PR #59791: stats: use an alternative function to read the bound from `BLOB` stored in `mysql.stats_buckets`. | tidb-test=pr/2503
  URL: https://github.com/pingcap/tidb/pull/59791
  State: closed
  Merged At: 2025-04-15T08:57:06Z
  Changed Files Count: 5
  Main Modules: pkg/statistics, pkg/types
  Sample Changed Files:
  - pkg/statistics/handle/handletest/BUILD.bazel
  - pkg/statistics/handle/handletest/handle_test.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/save.go
  - pkg/types/datum.go
  PR Summary: What problem does this PR solve? Problem Summary: The stats logic relies on the behavior that type conversion from A to Blob to A is still equal to the original value. However, it's not true for  after What changed and how does it work? Add an extra function to handle the load of  bound specially. It'll not affect the behavior of any expression, but only modify the stats part.
- Related PR #59840: table: Revert "table: fix the issue that the default value for `BIT` column is wrong (#57303)"
  URL: https://github.com/pingcap/tidb/pull/59840
  State: closed
  Merged At: 2025-02-28T09:26:30Z
  Changed Files Count: 8
  Main Modules: tests/integrationtest, pkg/types, pkg/ddl, pkg/executor
  Sample Changed Files:
  - pkg/ddl/ddl_api.go
  - pkg/executor/test/writetest/write_test.go
  - pkg/types/datum.go
  - pkg/types/datum_test.go
  - tests/integrationtest/r/ddl/column.result
  - tests/integrationtest/r/table/tables.result
  - tests/integrationtest/t/ddl/column.test
  - tests/integrationtest/t/table/tables.test
  PR Summary: Reverts pingcap/tidb#57356 because of What problem does this PR solve? We'll need to reconsider the solution / bugfix for both issues before the next release of 7.5.
- Fix PR #60579: stats: use an alternative function to read the bound from `BLOB` stored in `mysql.stats_buckets`. | tidb-test=pr/2503 (#59791)
  URL: https://github.com/pingcap/tidb/pull/60579
  State: open
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/statistics, types/datum.go
  Sample Changed Files:
  - pkg/statistics/handle/handletest/BUILD.bazel
  - pkg/statistics/handle/handletest/handle_test.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/save.go
  - types/datum.go
  PR Summary: This is an automated cherry-pick of #59791 What problem does this PR solve? Problem Summary: The stats logic relies on the behavior that type conversion from A to Blob to A is still equal to the original value. However, it's not true for  after What changed and how does it work?
- Fix PR #60580: stats: use an alternative function to read the bound from `BLOB` stored in `mysql.stats_buckets`. | tidb-test=pr/2503 (#59791)
  URL: https://github.com/pingcap/tidb/pull/60580
  State: closed
  Merged At: 2025-07-14T23:59:45Z
  Changed Files Count: 13
  Main Modules: pkg/statistics, tests/integrationtest, pkg/types, pkg/ddl, pkg/executor
  Sample Changed Files:
  - pkg/ddl/ddl_api.go
  - pkg/executor/test/writetest/write_test.go
  - pkg/statistics/handle/handletest/BUILD.bazel
  - pkg/statistics/handle/handletest/handle_test.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/save.go
  - pkg/types/BUILD.bazel
  - pkg/types/datum.go
  - pkg/types/datum_test.go
  - tests/integrationtest/r/ddl/column.result
  - tests/integrationtest/r/table/tables.result
  - tests/integrationtest/t/ddl/column.test
  - tests/integrationtest/t/table/tables.test
  PR Summary: This is an automated cherry-pick of #59791 What problem does this PR solve? Problem Summary: The stats logic relies on the behavior that type conversion from A to Blob to A is still equal to the original value. However, it's not true for  after What changed and how does it work?
- Fix PR #60581: stats: use an alternative function to read the bound from `BLOB` stored in `mysql.stats_buckets`. | tidb-test=pr/2503 (#59791)
  URL: https://github.com/pingcap/tidb/pull/60581
  State: open
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/statistics, pkg/types
  Sample Changed Files:
  - pkg/statistics/handle/handletest/BUILD.bazel
  - pkg/statistics/handle/handletest/handle_test.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/save.go
  - pkg/types/datum.go
  PR Summary: This is an automated cherry-pick of #59791 What problem does this PR solve? Problem Summary: The stats logic relies on the behavior that type conversion from A to Blob to A is still equal to the original value. However, it's not true for  after What changed and how does it work?
- Fix PR #60583: stats: use an alternative function to read the bound from `BLOB` stored in `mysql.stats_buckets`. (#59791)
  URL: https://github.com/pingcap/tidb/pull/60583
  State: closed
  Merged At: 2025-04-16T06:32:09Z
  Changed Files Count: 5
  Main Modules: pkg/statistics, pkg/types
  Sample Changed Files:
  - pkg/statistics/handle/handletest/BUILD.bazel
  - pkg/statistics/handle/handletest/handle_test.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/save.go
  - pkg/types/datum.go
  PR Summary: This is an automated cherry-pick of #59791 What problem does this PR solve? Problem Summary: The stats logic relies on the behavior that type conversion from A to Blob to A is still equal to the original value. However, it's not true for  after What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
