# Issue #66919: planner, statistics: use selected partition stats for dynamic pruning

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/66919
- Status: open
- Type: type/enhancement
- Created At: 2026-03-11T13:06:55Z
- Labels: component/statistics, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- TiDB currently prefers dynamic partition pruning for partitioned tables. This avoids building static-pruning plans, but it also means the optimizer usually estimates row counts from the partition table stats path instead of the stats of the actually selected partitions.

## Linked PRs
- Fix PR #66920: planner, statistics: use selected partition stats for dynamic pruning
  URL: https://github.com/pingcap/tidb/pull/66920
  State: open
  Merged At: not merged
  Changed Files Count: 25
  Main Modules: pkg/planner/core, pkg/session, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/ndv_test.go
  - pkg/planner/cardinality/pseudo.go
  - pkg/planner/core/casetest/instanceplancache/others_test.go
  - pkg/planner/core/casetest/plancache/BUILD.bazel
  - pkg/planner/core/casetest/plancache/plan_cache_partition_table_test.go
  - pkg/planner/core/casetest/plancache/plan_cache_partition_test.go
  - pkg/planner/core/casetest/planstats/BUILD.bazel
  - pkg/planner/core/casetest/planstats/plan_stats_test.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/operator/logicalop/logical_datasource.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/core/rule/collect_column_stats_usage.go
  - pkg/planner/core/rule/rule_partition_processor.go
  - pkg/planner/core/stats.go
  - pkg/planner/core/stats/stats.go
  - pkg/planner/core/tests/prepare/BUILD.bazel
  - pkg/planner/core/tests/prepare/prepare_test.go
  PR Summary: What problem does this PR solve? Problem Summary: TiDB uses dynamic partition pruning by default. In some queries that only touch a subset of partitions, cardinality estimation still falls back to the partition table stats path, which is less accurate than using stats merged from the selected partitions. Reusing such partition-specific pruning information through plan cache is also unsafe. What changed and how does it work? Reuse statically-determined partition pruning results in the dynamic pruning path to collect the selected partition IDs for stats estimation.
- Related PR #67139: [DNM] planner, statistics: use selected partition stats for dynamic pruning
  URL: https://github.com/pingcap/tidb/pull/67139
  State: closed
  Merged At: not merged
  Changed Files Count: 22
  Main Modules: pkg/planner/core, pkg/session, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/ndv_test.go
  - pkg/planner/cardinality/pseudo.go
  - pkg/planner/core/casetest/instanceplancache/others_test.go
  - pkg/planner/core/casetest/planstats/BUILD.bazel
  - pkg/planner/core/casetest/planstats/plan_stats_test.go
  - pkg/planner/core/collect_column_stats_usage.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/operator/logicalop/logical_datasource.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_partition_table_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/core/rule_partition_processor.go
  - pkg/planner/core/stats.go
  - pkg/planner/core/tests/prepare/BUILD.bazel
  - pkg/planner/core/tests/prepare/prepare_test.go
  - pkg/sessionctx/stmtctx/stmtctx.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/setvar_affect.go
  PR Summary: What problem does this PR solve? This is cherry pick of Problem Summary: TiDB uses dynamic partition pruning by default. In some queries that only touch a subset of partitions, cardinality estimation still falls back to the partition table stats path, which is less accurate than using stats merged from the selected partitions. Reusing such partition-specific pruning information through plan cache is also unsafe. What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
