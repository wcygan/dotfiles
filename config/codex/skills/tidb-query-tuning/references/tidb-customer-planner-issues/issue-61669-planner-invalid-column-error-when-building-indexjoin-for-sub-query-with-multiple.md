# Issue #61669: planner: invalid column error when building IndexJoin for sub-query with multiple Agg

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61669
- Status: closed
- Type: type/bug
- Created At: 2025-06-11T10:02:55Z
- Closed At: 2025-06-11T11:02:02Z
- Labels: affects-8.5, report/customer, severity/major, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- Root Cause: 1. An optimizer bug, when constructing the inner operators under an IndexJoin in , we assume there is at most  Agg. 2. In this SQL with 2 nested sub-queries, there are  Agg under IndexJoin, which breaks our assumption, and causes some errors.

## Linked PRs
- Fix PR #61672: planner: fix the issue that invalid column error when building IndexJoin for sub-query with multiple Agg
  URL: https://github.com/pingcap/tidb/pull/61672
  State: closed
  Merged At: 2025-06-11T11:02:01Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/integration_test.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix the issue that invalid column error when building IndexJoin for sub-query with multiple Agg What changed and how does it work? planner: fix the issue that invalid column error when building IndexJoin for sub-query with multiple Agg
- Fix PR #61727: planner: fix the issue that invalid column error when building IndexJoin for sub-query with multiple Agg (#61672)
  URL: https://github.com/pingcap/tidb/pull/61727
  State: closed
  Merged At: 2025-06-26T06:57:39Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/integration_test.go
  PR Summary: This is an automated cherry-pick of #61672 What problem does this PR solve? Problem Summary: planner: fix the issue that invalid column error when building IndexJoin for sub-query with multiple Agg What changed and how does it work? planner: fix the issue that invalid column error when building IndexJoin for sub-query with multiple Agg

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
