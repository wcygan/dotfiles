# Issue #67440: index join probe should detect partition key to do some dynamic pruning

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67440
- Status: open
- Type: type/enhancement
- Created At: 2026-03-31T02:11:05Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- bg: t2 is a partition table with 600 partition t2's partition key is DAY(t2.c4) t2.idx_b is a local index

## Linked PRs
- Fix PR #67549: planner: derive static probe pruning conds for index join
  URL: https://github.com/pingcap/tidb/pull/67549
  State: open
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/BUILD.bazel
  - pkg/planner/core/casetest/partition/BUILD.bazel
  - pkg/planner/core/casetest/partition/partition_pruner_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/index_join_partition_pruning.go
  - pkg/planner/property/physical_property.go
  PR Summary: What problem does this PR solve? Problem Summary: For index join over a partitioned probe-side table, the planner only used the probe table's existing pruning conditions. When the join predicates implied a coarse static range on the probe partition key, the probe-side scan could still keep . What changed and how does it work? This change derives coarse static probe-side partition pruning conditions during index join planning and threads them into the probe scan task's partition pruning info.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
