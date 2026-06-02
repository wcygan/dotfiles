# Issue #61501: planner: support a hint or var like `index-join-first` to indicate the planner to prefer `IndexJoin` over other joins

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61501
- Status: open
- Type: type/enhancement
- Created At: 2025-06-05T01:05:18Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- We've met this problems multiple times, so it might be better to support a hint or variable like to indicate the optimizer always choose if possible in such scenarios:

## Linked PRs
- Fix PR #66596: planner: support index_join_first() hint to prefer index join
  URL: https://github.com/pingcap/tidb/pull/66596
  State: open
  Merged At: not merged
  Changed Files Count: 10
  Main Modules: pkg/planner/core, pkg/parser, pkg/util
  Sample Changed Files:
  - pkg/parser/ast/misc.go
  - pkg/parser/hintparser.go
  - pkg/parser/hintparser.y
  - pkg/parser/misc.go
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/rule_join_reorder.go
  - pkg/util/hint/hint.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? support index_join_first() hint to prefer index join

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
