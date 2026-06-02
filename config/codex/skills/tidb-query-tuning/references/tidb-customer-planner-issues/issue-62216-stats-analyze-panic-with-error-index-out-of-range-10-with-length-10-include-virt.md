# Issue #62216: stats: analyze panic with error "index out of range [10] with length 10" include virtual column

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62216
- Status: closed
- Type: type/bug
- Created At: 2025-07-04T08:18:50Z
- Closed At: 2025-08-21T02:13:19Z
- Labels: affects-8.5, duplicate, may-affects-6.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. create table with virtual column as index first column 2. insert into some data 3. analyze table

## Linked PRs
- Fix PR #62968: planner: filter generated columns that depend on skipped columns
  URL: https://github.com/pingcap/tidb/pull/62968
  State: closed
  Merged At: 2025-08-18T16:04:38Z
  Changed Files Count: 2
  Main Modules: pkg/executor, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/test/analyzetest/analyze_test.go
  - pkg/planner/core/planbuilder.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? When filtering columns, also skip generated columns that have dependencies on any of the skipped columns to maintain consistency and avoid reference errors in query planning. Another issue is that the predicate should also consider the dependency columns. Otherwise, we will miss some column information when building the analyze executor.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
