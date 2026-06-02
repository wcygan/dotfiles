# Issue #65924: The estRows of equal condition is overestimated when the modify count is zero

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65924
- Status: open
- Type: type/bug
- Created At: 2026-01-30T06:41:56Z
- Labels: affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #66145: planner: Consolidate out-of-range equal to use common func | tidb-test=pr/2684
  URL: https://github.com/pingcap/tidb/pull/66145
  State: open
  Merged At: not merged
  Changed Files Count: 20
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest, pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/test/analyzetest/analyze_test.go
  - pkg/planner/cardinality/row_count_column.go
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/planner/core/casetest/cascades/testdata/cascades_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/partition/testdata/integration_partition_suite_out.json
  - pkg/planner/core/casetest/partition/testdata/integration_partition_suite_xut.json
  - pkg/planner/core/casetest/testdata/stats_suite_out.json
  - pkg/planner/core/casetest/testdata/stats_suite_xut.json
  - pkg/statistics/handle/globalstats/global_stats_test.go
  - pkg/statistics/histogram.go
  - tests/integrationtest/r/executor/issues.result
  - tests/integrationtest/r/executor/partition/partition_with_expression.result
  - tests/integrationtest/r/imdbload.result
  - tests/integrationtest/r/planner/core/cbo.result
  - tests/integrationtest/r/planner/core/integration_partition.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? While this affects 8.5 - it will be very difficult to cherry pick. The goal here is to consolidate all "out-of-range" estimation to use the same logic. It shouldn't matter if you are out-of-range for an equals or a range predicate. This is only targeting stats V2 use.
- Fix PR #66310: planner: out of Range full NDV
  URL: https://github.com/pingcap/tidb/pull/66310
  State: open
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
