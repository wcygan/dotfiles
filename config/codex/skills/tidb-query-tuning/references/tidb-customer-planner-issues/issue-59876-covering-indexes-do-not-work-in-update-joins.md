# Issue #59876: Covering indexes do not work in update joins

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59876
- Status: closed
- Type: type/bug
- Created At: 2025-03-03T13:02:43Z
- Closed At: 2026-03-19T09:45:30Z
- Labels: report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #66845: planner: keep covering indexes for read-only tables in update join | tidb-test=pr/2706 
  URL: https://github.com/pingcap/tidb/pull/66845
  State: closed
  Merged At: 2026-03-19T09:45:30Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/operator/physicalop/physical_common_plans.go
  - pkg/planner/util/handle_cols.go
  - tests/integrationtest/r/bindinfo/bind.result
  PR Summary: What problem does this PR solve? Problem Summary: freezes the join output before optimization and disables projection elimination for the update sub-plan. Before this change, the frozen projection kept the full mixed row for every joined table, including read-only source tables. That polluted the required column set with extra writable columns and row handles, so a covering index on the read-only side could not stay as . What changed and how does it work? identify which joined tables are actually updated after

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
