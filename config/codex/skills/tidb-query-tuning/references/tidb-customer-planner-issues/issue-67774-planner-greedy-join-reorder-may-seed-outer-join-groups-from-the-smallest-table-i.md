# Issue #67774: planner: greedy join reorder may seed outer-join groups from the smallest table instead of the cheapest first join

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67774
- Status: open
- Type: type/bug
- Created At: 2026-04-15T03:26:07Z
- Labels: planner/join-order, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- The greedy algorithm seeds the join group from the smallest base table. In this case it may start from t2, which effectively leads to starting from t1 left join t2, even though that outer join cannot reduce below t1's row count. As a result, the first greedy choice is driven by base-table size instead of the cumulative cost of the first valid join.

## Linked PRs
- Related PR #67784: planner: add opt-in greedy join reorder start-by-cost switch
  URL: https://github.com/pingcap/tidb/pull/67784
  State: open
  Merged At: not merged
  Changed Files Count: 16
  Main Modules: pkg/planner/core, pkg/session, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/BUILD.bazel
  - pkg/planner/core/join_reorder_side_effect_test.go
  - pkg/planner/core/joinorder/BUILD.bazel
  - pkg/planner/core/joinorder/conflict_detector.go
  - pkg/planner/core/joinorder/join_order.go
  - pkg/planner/core/joinorder/join_order_side_effect_test.go
  - pkg/planner/core/operator/logicalop/logical_projection.go
  - pkg/planner/core/rule_join_reorder.go
  - pkg/planner/core/rule_join_reorder_greedy.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/setvar_affect.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/varsutil_test.go
  - tests/integrationtest/r/planner/core/join_reorder2.result
  - tests/integrationtest/t/planner/core/join_reorder2.test
  PR Summary: What problem does this PR solve? Problem Summary: Greedy join reorder currently seeds each connected join component from the smallest base relation. That heuristic is not always good enough for outer-join groups. In a query like: when t2 < t3 << t1, the greedy path may start from t2, which effectively picks t1 left join t2 as the first join even though the outer join cannot reduce below t1's row

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
