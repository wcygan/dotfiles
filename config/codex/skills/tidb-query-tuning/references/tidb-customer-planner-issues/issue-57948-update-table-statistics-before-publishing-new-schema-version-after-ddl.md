# Issue #57948: Update table statistics before publishing new schema version after DDL

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/57948
- Status: open
- Type: type/feature-request
- Created At: 2024-12-03T14:41:10Z
- Labels: affects-8.5, component/statistics, report/customer, sig/planner, type/feature-request

## Customer-Facing Phenomenon
- **Is your feature request related to a problem? Please describe:** After DDL on large 800GB table, statistics were cleared, leading to degraded performance cause by bad query plans (eg: full table scans).

## Linked PRs
- Fix PR #58729: planner: Ensure index without stats survives for skyling pruning | tidb-test=pr/2465
  URL: https://github.com/pingcap/tidb/pull/58729
  State: closed
  Merged At: 2025-01-21T16:38:18Z
  Changed Files Count: 7
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/logical_plans_test.go
  - pkg/planner/util/path.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Enhanced CompareCandidates logic within SkyLinePruning to allow an index without statistics to survive so that it can be preferenced above a tablescan if it has more equals predicates than other available choices.
- Fix PR #59110: planner: notify skyline pruning of index statistics availability
  URL: https://github.com/pingcap/tidb/pull/59110
  State: closed
  Merged At: 2025-01-26T02:24:53Z
  Changed Files Count: 2
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/find_best_task.go
  PR Summary: Extend support for skyline pruning recognition of index without statistics to existing rules. By passing the "pseudo" result of the index from the CompareCandidates function for the "successful" index - it allows the later checking in SkyLinePruning to keep that index to prioritize above a table scan if tidb_opt_prefer_range_scan global variable is set. This change is a minor addition to address prior customer concerns that a newly created index that does NOT yet have statistics may be selected by the existing CompareCandidates code - and the index WITH statistics is pruned. But the cost of the index that used defaults (since no statistics) may have a higher cost than tablescan. What problem does this PR solve? Problem Summary:
- Fix PR #59227: planner: Ensure index without stats survives for skyling pruning | tidb-test=pr/2465 (#58729)
  URL: https://github.com/pingcap/tidb/pull/59227
  State: open
  Merged At: not merged
  Changed Files Count: 7
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/logical_plans_test.go
  - pkg/planner/util/path.go
  PR Summary: This is an automated cherry-pick of #58729 What problem does this PR solve? Problem Summary: What changed and how does it work? Enhanced CompareCandidates logic within SkyLinePruning to allow an index without statistics to survive so that it can be preferenced above a tablescan if it has more equals predicates than other available choices.
- Related PR #62725: planner: improve index pseudo-estimation with column stats | tidb-test=pr/2570
  URL: https://github.com/pingcap/tidb/pull/62725
  State: closed
  Merged At: 2025-08-08T18:51:52Z
  Changed Files Count: 12
  Main Modules: pkg/planner, pkg/planner/core, pkg/statistics
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/cross_estimation.go
  - pkg/planner/cardinality/row_count_column.go
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_out.json
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_xut.json
  - pkg/planner/core/stats.go
  - pkg/statistics/handle/handletest/handle_test.go
  - pkg/statistics/statistics_test.go
  - pkg/statistics/table.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Previously, if there weren't valid statistics on an index, we would use pseudo-estimation for the cardinality. However, there are cases where we could make a more accurate estimation because we have statistics on the underlying columns, but we didn't make use of this information. With this change, if our index stats are invalid it checks for valid column statistics and uses those that are available.
- Fix PR #62931: planner: refactor compareCandidates
  URL: https://github.com/pingcap/tidb/pull/62931
  State: closed
  Merged At: 2025-08-13T19:44:03Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/find_best_task.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #63545: planner: notify skyline pruning of index statistics availability (#59110) | tidb-test=pr/2608
  URL: https://github.com/pingcap/tidb/pull/63545
  State: closed
  Merged At: 2025-09-19T17:40:07Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/logical_plans_test.go
  PR Summary: This is an automated cherry-pick of #59110 Extend support for skyline pruning recognition of index without statistics to existing rules. By passing the "pseudo" result of the index from the CompareCandidates function for the "successful" index - it allows the later checking in SkyLinePruning to keep that index to prioritize above a table scan if tidb_opt_prefer_range_scan global variable is set. This change is a minor addition to address prior customer concerns that a newly created index that does NOT yet have statistics may be selected by the existing CompareCandidates code - and the index WITH statistics is pruned. But the cost of the index that used defaults (since no statistics) may have a higher cost than tablescan. What problem does this PR solve?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
