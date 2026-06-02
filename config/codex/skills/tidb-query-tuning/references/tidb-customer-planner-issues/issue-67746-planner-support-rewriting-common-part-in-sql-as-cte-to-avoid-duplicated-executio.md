# Issue #67746: planner: support rewriting common part in SQL as CTE to avoid duplicated execution

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67746
- Status: open
- Type: type/enhancement
- Created At: 2026-04-14T03:23:32Z
- Labels: plan-rewrite, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Below is our Plan, TiDB needs to run the join twice, which could increase resources usage:

## Linked PRs
- Fix PR #67776: planner/core: add common subplan extract rule
  URL: https://github.com/pingcap/tidb/pull/67776
  State: open
  Merged At: not merged
  Changed Files Count: 12
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/main_test.go
  - pkg/planner/core/casetest/rule/rule_common_subplan_extract_test.go
  - pkg/planner/core/casetest/rule/testdata/common_subplan_extract_suite_in.json
  - pkg/planner/core/casetest/rule/testdata/common_subplan_extract_suite_out.json
  - pkg/planner/core/casetest/rule/testdata/common_subplan_extract_suite_xut.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/rule/logical_rules.go
  - pkg/planner/core/rule/rule_common_subplan_extract.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: What problem does this PR solve? Problem Summary: Real-world analytical queries (TPCH/TPCDS/BI dashboards, view-merged or decorrelated plans) frequently contain structurally identical join subtrees that are planned and executed independently, duplicating scan

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
