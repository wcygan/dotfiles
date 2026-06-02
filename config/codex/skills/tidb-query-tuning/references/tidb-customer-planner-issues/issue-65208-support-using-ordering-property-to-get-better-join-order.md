# Issue #65208: support using ordering property to get better join order

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65208
- Status: open
- Type: type/enhancement
- Created At: 2025-12-24T02:53:56Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- The better plan: choose join order of  and use , so we can leverage the ordering property and only need to get 1000 rows from Join output.

## Linked PRs
- Fix PR #63522: planner: Allow leading ordered table to survive (WIP)
  URL: https://github.com/pingcap/tidb/pull/63522
  State: open
  Merged At: not merged
  Changed Files Count: 11
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/operator/physicalop/physical_index_join.go
  - pkg/planner/core/operator/physicalop/physical_topn.go
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/rule_join_reorder.go
  - pkg/planner/core/rule_join_reorder_greedy.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #67305: pkg/planner: add order-aware logical join reorder rule
  URL: https://github.com/pingcap/tidb/pull/67305
  State: closed
  Merged At: 2026-04-03T07:16:30Z
  Changed Files Count: 17
  Main Modules: pkg/planner/core, pkg/planner, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/main_test.go
  - pkg/planner/core/casetest/rule/rule_cdc_join_reorder_test.go
  - pkg/planner/core/casetest/rule/testdata/order_aware_join_reorder_suite_in.json
  - pkg/planner/core/casetest/rule/testdata/order_aware_join_reorder_suite_out.json
  - pkg/planner/core/casetest/rule/testdata/order_aware_join_reorder_suite_xut.json
  - pkg/planner/core/joinorder/BUILD.bazel
  - pkg/planner/core/joinorder/join_order.go
  - pkg/planner/core/joinorder/ordered_leading.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/rule/BUILD.bazel
  - pkg/planner/core/rule/logical_rules.go
  - pkg/planner/core/rule/rule_order_aware_join_reorder.go
  - pkg/planner/core/rule_join_reorder.go
  - pkg/planner/optimize.go
  - pkg/sessionctx/stmtctx/stmtctx.go
  PR Summary: What problem does this PR solve? Problem Summary: The order-aware logic for the new CD-C join reorder path should live in a separate logical rule instead of being mixed into the generic join reorder solver. What changed and how does it work? This PR adds a new logical rule that inspects join groups with propagated TopN / ORDER BY columns, reuses the CD-C  logic, and injects an internal  preference when one ordered leaf can preserve the required ordering with compatible equality filters.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
