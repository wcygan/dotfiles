# Issue #67138: When CTE contains ORDER BY, the subquery error returns NULL

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67138
- Status: closed
- Type: type/bug
- Created At: 2026-03-19T03:37:59Z
- Closed At: 2026-03-23T15:31:00Z
- Labels: affects-8.5, affects-9.0, contribution, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 2. What did you expect to see? (Required) sql results are the same (should both return test) 3. What did you see instead (Required) not same 4. What is your TiDB version? (Required) v8.5.5

## Linked PRs
- Fix PR #67231: planner/core: fix wrong results caused by rule_project_eliminate for queries with Apply
  URL: https://github.com/pingcap/tidb/pull/67231
  State: closed
  Merged At: 2026-03-23T15:30:58Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/rule_eliminate_projection_test.go
  - pkg/planner/core/rule_eliminate_projection.go
  PR Summary: What problem does this PR solve? Problem Summary: There is a replaceMap in : <col-9, col-6>, which means we should replace all  to . But since  only outputs  and ,[ this piece of code]() prevents the replacement from happening. Because it assumes that all target columns to be replaced must come from the child output schema. This is true in normal cases, but correlated columns do not actually come from the child output schema—they are instead set explicitly during the execution of Apply.
- Fix PR #67246: planner/core: fix wrong results caused by rule_project_eliminate for queries with Apply (#67231)
  URL: https://github.com/pingcap/tidb/pull/67246
  State: closed
  Merged At: 2026-03-24T10:42:58Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/rule_eliminate_projection_test.go
  - pkg/planner/core/rule_eliminate_projection.go
  PR Summary: This is an automated cherry-pick of #67231 What problem does this PR solve? Problem Summary: There is a replaceMap in : <col-9, col-6>, which means we should replace all  to . But since  only outputs  and ,[ this piece of code]() prevents the replacement from happening.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
