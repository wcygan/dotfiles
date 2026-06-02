# Issue #60242: Planner: Need to ignore the ordering index path even if the index selectivity is 1.

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/60242
- Status: closed
- Type: type/enhancement
- Created At: 2025-03-24T17:42:27Z
- Closed At: 2025-03-26T05:56:01Z
- Labels: affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #60255: planner: change the semantic of `tidb_opt_ordering_index_selectivity_threshold` from `<` to `<=`
  URL: https://github.com/pingcap/tidb/pull/60255
  State: closed
  Merged At: 2025-03-26T05:56:00Z
  Changed Files Count: 4
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_in.json
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/planner/core/find_best_task.go
  PR Summary: What problem does this PR solve? Problem Summary: As said in #42060 and the [doc](), this variable was originally introduced to control the choice between a "filter index" that satisfies the filter conditions and an "ordering index" that satisfies the  clause. The allowed range for this variable is . Obviously, it's meaningless to choose a "filter index" when the selectivity is 1, which basically means there are no filters. So we made the semantic of this variable "less than". This provides a benefit: when setting it to 0, the behavior is not changed, so we can safely use 0 as the default value. However, in a recent ticket, we met another case where there were no indexes satisfying the filters, and the choice was between a tiflash path and an "ordering index" path. In this specific ticket,
- Fix PR #60282: planner: change the semantic of `tidb_opt_ordering_index_selectivity_threshold` from `<` to `<=` (#60255)
  URL: https://github.com/pingcap/tidb/pull/60282
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/planner, pkg/planner/core, statistics/testdata
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_in.json
  - pkg/planner/core/find_best_task.go
  - statistics/testdata/trace_suite_out.json
  PR Summary: This is an automated cherry-pick of #60255 What problem does this PR solve? Problem Summary: As said in #42060 and the [doc](), this variable was originally introduced to control the choice between a "filter index" that satisfies the filter conditions and an "ordering index" that satisfies the  clause. The allowed range for this variable is . Obviously, it's meaningless to choose a "filter index" when the selectivity is 1, which basically means there are no filters. So we made the semantic of this variable "less than". This provides a benefit: when setting it to 0, the behavior is not changed, so we can safely use 0 as the default value.
- Fix PR #60285: planner: change the semantic of `tidb_opt_ordering_index_selectivity_threshold` from `<` to `<=` (#60255)
  URL: https://github.com/pingcap/tidb/pull/60285
  State: closed
  Merged At: 2025-03-27T04:30:07Z
  Changed Files Count: 4
  Main Modules: statistics/testdata, planner/core, statistics/integration_test.go
  Sample Changed Files:
  - planner/core/find_best_task.go
  - statistics/integration_test.go
  - statistics/testdata/integration_suite_in.json
  - statistics/testdata/integration_suite_out.json
  PR Summary: Manual cherry-pick of #60255  What problem does this PR solve? Problem Summary: As said in #42060 and the [doc](), this variable was originally introduced to control the choice between a "filter index" that satisfies the filter conditions and an "ordering index" that satisfies the  clause. The allowed range for this variable is .
- Fix PR #60445: planner: change the semantic of `tidb_opt_ordering_index_selectivity_threshold` from `<` to `<=` (#60255)
  URL: https://github.com/pingcap/tidb/pull/60445
  State: closed
  Merged At: 2025-04-14T10:29:04Z
  Changed Files Count: 4
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_in.json
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #60255 What problem does this PR solve? Problem Summary: As said in #42060 and the [doc](), this variable was originally introduced to control the choice between a "filter index" that satisfies the filter conditions and an "ordering index" that satisfies the  clause. The allowed range for this variable is . Obviously, it's meaningless to choose a "filter index" when the selectivity is 1, which basically means there are no filters. So we made the semantic of this variable "less than". This provides a benefit: when setting it to 0, the behavior is not changed, so we can safely use 0 as the default value.
- Fix PR #60537: planner: change the semantic of `tidb_opt_ordering_index_selectivity_threshold` from `<` to `<=` (#60255)
  URL: https://github.com/pingcap/tidb/pull/60537
  State: closed
  Merged At: 2025-04-16T16:25:57Z
  Changed Files Count: 4
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_in.json
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #60255 What problem does this PR solve? Problem Summary: As said in #42060 and the [doc](), this variable was originally introduced to control the choice between a "filter index" that satisfies the filter conditions and an "ordering index" that satisfies the  clause. The allowed range for this variable is . Obviously, it's meaningless to choose a "filter index" when the selectivity is 1, which basically means there are no filters. So we made the semantic of this variable "less than". This provides a benefit: when setting it to 0, the behavior is not changed, so we can safely use 0 as the default value.
- Fix PR #60538: planner: change the semantic of `tidb_opt_ordering_index_selectivity_threshold` from `<` to `<=` (#60255)
  URL: https://github.com/pingcap/tidb/pull/60538
  State: closed
  Merged At: 2025-04-16T16:26:00Z
  Changed Files Count: 4
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_in.json
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #60255 What problem does this PR solve? Problem Summary: As said in #42060 and the [doc](), this variable was originally introduced to control the choice between a "filter index" that satisfies the filter conditions and an "ordering index" that satisfies the  clause. The allowed range for this variable is . Obviously, it's meaningless to choose a "filter index" when the selectivity is 1, which basically means there are no filters. So we made the semantic of this variable "less than". This provides a benefit: when setting it to 0, the behavior is not changed, so we can safely use 0 as the default value.
- Fix PR #60542: planner: change the semantic of `tidb_opt_ordering_index_selectivity_threshold` from `<` to `<=` (#60255)
  URL: https://github.com/pingcap/tidb/pull/60542
  State: closed
  Merged At: 2025-04-16T16:25:54Z
  Changed Files Count: 4
  Main Modules: statistics/testdata, planner/core, statistics/integration_test.go
  Sample Changed Files:
  - planner/core/find_best_task.go
  - statistics/integration_test.go
  - statistics/testdata/integration_suite_in.json
  - statistics/testdata/integration_suite_out.json
  PR Summary: Manual cherry-pick of #60255  What problem does this PR solve? Problem Summary: As said in #42060 and the [doc](), this variable was originally introduced to control the choice between a "filter index" that satisfies the filter conditions and an "ordering index" that satisfies the  clause. The allowed range for this variable is .
- Fix PR #60588: planner: change the semantic of `tidb_opt_ordering_index_selectivity_threshold` from `<` to `<=` (#60255)
  URL: https://github.com/pingcap/tidb/pull/60588
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/planner, pkg/planner/core, statistics/testdata
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_in.json
  - pkg/planner/core/find_best_task.go
  - statistics/testdata/trace_suite_out.json
  PR Summary: This is an automated cherry-pick of #60255 What problem does this PR solve? Problem Summary: As said in #42060 and the [doc](), this variable was originally introduced to control the choice between a "filter index" that satisfies the filter conditions and an "ordering index" that satisfies the  clause. The allowed range for this variable is . Obviously, it's meaningless to choose a "filter index" when the selectivity is 1, which basically means there are no filters. So we made the semantic of this variable "less than". This provides a benefit: when setting it to 0, the behavior is not changed, so we can safely use 0 as the default value.
- Fix PR #60733: planner: change the semantic of `tidb_opt_ordering_index_selectivity_threshold` from `<` to `<=` (#60255)
  URL: https://github.com/pingcap/tidb/pull/60733
  State: closed
  Merged At: 2025-04-23T12:54:25Z
  Changed Files Count: 4
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/cardinality/testdata/cardinality_suite_in.json
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/planner/core/find_best_task.go
  PR Summary: Manual cherry-pick of #60255  What problem does this PR solve? Problem Summary: As said in #42060 and the [doc](), this variable was originally introduced to control the choice between a "filter index" that satisfies the filter conditions and an "ordering index" that satisfies the  clause. The allowed range for this variable is .

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
