# Issue #62556: GROUP BY ? in prepared statement causes error in TiDB (MySQL compatible)

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62556
- Status: closed
- Type: type/bug
- Created At: 2025-07-22T09:28:57Z
- Closed At: 2026-03-09T15:55:30Z
- Labels: epic/plan-cache, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- In TiDB 8.5.2, when executing , the following error occurs: And when preparing the statement, a warning is shown:

## Linked PRs
- Fix PR #66387: planner, executor: fix prepared string parameter compatibility in group/order by
  URL: https://github.com/pingcap/tidb/pull/66387
  State: closed
  Merged At: 2026-02-26T13:07:45Z
  Changed Files Count: 2
  Main Modules: pkg/executor, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/test/seqtest/prepared_test.go
  - pkg/planner/core/logical_plan_builder.go
  PR Summary: What problem does this PR solve? Problem Summary: Prepared statements with top-level  (and aggregate ) could treat string parameters like  as positional references at execute time, causing errors such as . This differs from MySQL behavior. What changed and how does it work? Added  in planner resolver path.
- Fix PR #63338: planner: fix GROUP BY ? in prepared statement causes error
  URL: https://github.com/pingcap/tidb/pull/63338
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/expression
  Sample Changed Files:
  - pkg/expression/util.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/plan_cache_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? In Spring ORM, sometimes such prepare statements are generated. Grouping by 0 is illegal, but here it should be of string type.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
