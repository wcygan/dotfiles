# Issue #61606: TiDB's analyze command cannot correctly handle a virtual generated column if it is the first column

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61606
- Status: closed
- Type: type/bug
- Created At: 2025-06-09T14:03:32Z
- Closed At: 2025-07-10T07:53:53Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, component/statistics, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Create the table: 2. Insert some data: 3. Analyze the table:

## Linked PRs
- Fix PR #62333: executor: fix the issue during analyze when first col is virtual col
  URL: https://github.com/pingcap/tidb/pull/62333
  State: closed
  Merged At: 2025-07-10T07:53:48Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col_v2.go
  - tests/integrationtest/r/executor/analyze.result
  - tests/integrationtest/t/executor/analyze.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? The samples should append  for the virtual generated column first for later use.
- Fix PR #62348: executor: fix the issue during analyze when first col is virtual col (#62333)
  URL: https://github.com/pingcap/tidb/pull/62348
  State: closed
  Merged At: 2025-07-11T16:59:03Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col_v2.go
  - tests/integrationtest/r/executor/analyze.result
  - tests/integrationtest/t/executor/analyze.test
  PR Summary: This is an automated cherry-pick of #62333 What problem does this PR solve? Problem Summary: What changed and how does it work? The samples should append  for the virtual generated column first for later use.
- Fix PR #62370: executor: fix the issue during analyze when first col is virtual col (#62333)
  URL: https://github.com/pingcap/tidb/pull/62370
  State: open
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col_v2.go
  - tests/integrationtest/r/executor/analyze.result
  - tests/integrationtest/t/executor/analyze.test
  PR Summary: This is an automated cherry-pick of #62333 What problem does this PR solve? Problem Summary: What changed and how does it work? The samples should append  for the virtual generated column first for later use.
- Fix PR #62371: executor: fix the issue during analyze when first col is virtual col (#62333)
  URL: https://github.com/pingcap/tidb/pull/62371
  State: closed
  Merged At: 2025-07-16T13:16:00Z
  Changed Files Count: 3
  Main Modules: pkg/executor, pkg/util
  Sample Changed Files:
  - pkg/executor/analyze_col_v2.go
  - pkg/executor/test/analyzetest/analyze_test.go
  - pkg/util/chunk/column.go
  PR Summary: This is an automated cherry-pick of #62333 What problem does this PR solve? Problem Summary: What changed and how does it work? The samples should append  for the virtual generated column first for later use.
- Fix PR #62372: executor: fix the issue during analyze when first col is virtual col (#62333)
  URL: https://github.com/pingcap/tidb/pull/62372
  State: open
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: executor/analyze_col_v2.go, executor/testdata, tests/integrationtest
  Sample Changed Files:
  - executor/analyze_col_v2.go
  - executor/testdata/analyze_test_data.sql
  - tests/integrationtest/r/executor/analyze.result
  PR Summary: This is an automated cherry-pick of #62333 What problem does this PR solve? Problem Summary: What changed and how does it work? The samples should append  for the virtual generated column first for later use.
- Fix PR #62373: executor: fix the issue during analyze when first col is virtual col (#62333)
  URL: https://github.com/pingcap/tidb/pull/62373
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: executor/analyze_col_v2.go, executor/testdata, tests/integrationtest
  Sample Changed Files:
  - executor/analyze_col_v2.go
  - executor/testdata/analyze_test_data.sql
  - tests/integrationtest/r/executor/analyze.result
  PR Summary: This is an automated cherry-pick of #62333 What problem does this PR solve? Problem Summary: What changed and how does it work? The samples should append  for the virtual generated column first for later use.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
