# Issue #65838: `inl_join` hint shows warning when `tidb_opt_advanced_join_hint=OFF` but silently fails when `ON`

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65838
- Status: open
- Type: type/bug
- Created At: 2026-01-27T07:41:56Z
- Labels: affects-8.5, contribution, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- Executed a query with hint on TiDB v8.5.5 with different settings of :

## Linked PRs
- Fix PR #67838: planner: preserve index join hint warning after advanced join reorder
  URL: https://github.com/pingcap/tidb/pull/67838
  State: open
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/joinorder/join_order.go
  - pkg/planner/core/joinorder/util.go
  - pkg/planner/core/physical_plan_test.go
  - pkg/planner/core/rule_join_reorder.go
  PR Summary: What problem does this PR solve? Problem Summary: When , a side-specific  hint on a join with semijoin-derived children could silently lose its inapplicable warning even though the final plan still did not honor the original hinted join edge. What changed and how does it work? Preserve both children as atomic endpoints during join-group extraction when advanced join hint sees a side-specific index-join hint, so join reorder does not rebind that hint onto a different join edge.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
