# Issue #65867: TiDB：runtime error: invalid memory address or nil pointer dereference

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65867
- Status: closed
- Type: type/bug
- Created At: 2026-01-28T07:02:48Z
- Closed At: 2026-02-25T10:52:59Z
- Labels: affects-8.5, contribution, first-time-contributor, impact/panic, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- This table  always being ‘inset’and 'delete' , and suddenly the following error popped up: It recovers after doing the steps below, but the issue keeps coming back frequently. table info and field :

## Linked PRs
- Fix PR #66251: planner: fix a nil pointer bug caused by nil TopN
  URL: https://github.com/pingcap/tidb/pull/66251
  State: closed
  Merged At: 2026-02-14T04:46:41Z
  Changed Files Count: 2
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/core/integration_test.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix a nil pointer bug caused by nil TopN What changed and how does it work? planner: fix a nil pointer bug caused by nil TopN
- Fix PR #67106: planner: fix a nil pointer bug caused by nil TopN
  URL: https://github.com/pingcap/tidb/pull/67106
  State: closed
  Merged At: 2026-03-18T13:01:15Z
  Changed Files Count: 2
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/core/integration_test.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix a nil pointer bug caused by nil TopN What changed and how does it work? planner: fix a nil pointer bug caused by nil TopN
- Fix PR #67840: planner: fix a nil pointer bug caused by nil TopN
  URL: https://github.com/pingcap/tidb/pull/67840
  State: closed
  Merged At: 2026-04-17T08:27:48Z
  Changed Files Count: 2
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/core/integration_test.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix a nil pointer bug caused by nil TopN What changed and how does it work? planner: fix a nil pointer bug caused by nil TopN

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
