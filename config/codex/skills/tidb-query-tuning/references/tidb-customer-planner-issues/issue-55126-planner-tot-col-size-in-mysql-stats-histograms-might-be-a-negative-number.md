# Issue #55126: planner: `tot_col_size` in mysql.stats_histograms might be a negative number 

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/55126
- Status: closed
- Type: type/bug
- Created At: 2024-08-01T07:19:25Z
- Closed At: 2024-08-09T10:42:42Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, component/statistics, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- ![image]() It seems like the negative number is caused by this modification: The current method to maintain the : 1. update  each time when there is a DML statement (see );

## Linked PRs
- Fix PR #55327: planner: add protection to avoid setting `tot_col_size` to negative numbers
  URL: https://github.com/pingcap/tidb/pull/55327
  State: closed
  Merged At: 2024-08-09T10:42:41Z
  Changed Files Count: 3
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/storage/save.go
  - pkg/statistics/handle/storage/stats_read_writer.go
  - pkg/statistics/handle/storage/update.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: add protection to avoid setting  to negative numbers What changed and how does it work? See more details and analysis in the issue. When updating , use  to protect it from becoming a negative number.
- Fix PR #55380: planner: add protection to avoid setting `tot_col_size` to negative numbers (#55327)
  URL: https://github.com/pingcap/tidb/pull/55380
  State: closed
  Merged At: 2024-08-30T07:32:12Z
  Changed Files Count: 3
  Main Modules: statistics/handle
  Sample Changed Files:
  - statistics/handle/ddl.go
  - statistics/handle/handle.go
  - statistics/handle/update.go
  PR Summary: This is an automated cherry-pick of #55327 What problem does this PR solve? Problem Summary: planner: add protection to avoid setting  to negative numbers What changed and how does it work? See more details and analysis in the issue.
- Fix PR #55523: planner: add protection to avoid setting `tot_col_size` to negative numbers (#55327)
  URL: https://github.com/pingcap/tidb/pull/55523
  State: closed
  Merged At: 2024-08-20T10:22:42Z
  Changed Files Count: 3
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/storage/save.go
  - pkg/statistics/handle/storage/stats_read_writer.go
  - pkg/statistics/handle/storage/update.go
  PR Summary: This is an automated cherry-pick of #55327 What problem does this PR solve? Problem Summary: planner: add protection to avoid setting  to negative numbers What changed and how does it work? See more details and analysis in the issue.
- Fix PR #55628: planner: add protection to avoid setting `tot_col_size` to negative numbers (#55327)
  URL: https://github.com/pingcap/tidb/pull/55628
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/storage/save.go
  - pkg/statistics/handle/storage/stats_read_writer.go
  - pkg/statistics/handle/storage/update.go
  PR Summary: This is an automated cherry-pick of #55327 What problem does this PR solve? Problem Summary: planner: add protection to avoid setting  to negative numbers What changed and how does it work? See more details and analysis in the issue.
- Fix PR #55629: planner: add protection to avoid setting `tot_col_size` to negative numbers (#55327)
  URL: https://github.com/pingcap/tidb/pull/55629
  State: closed
  Merged At: 2024-08-24T02:30:14Z
  Changed Files Count: 3
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/storage/save.go
  - pkg/statistics/handle/storage/stats_read_writer.go
  - pkg/statistics/handle/storage/update.go
  PR Summary: This is an automated cherry-pick of #55327 What problem does this PR solve? Problem Summary: planner: add protection to avoid setting  to negative numbers What changed and how does it work? See more details and analysis in the issue.
- Fix PR #56387: planner: Set minimum cost to avoid parent multiplication cost discrepancies
  URL: https://github.com/pingcap/tidb/pull/56387
  State: closed
  Merged At: 2024-09-29T09:35:57Z
  Changed Files Count: 4
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/task.go
  - pkg/planner/util/costusage/cost_misc.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #56411: planner: Set minimum cost to avoid parent multiplication cost discrepancies (#56387)
  URL: https://github.com/pingcap/tidb/pull/56411
  State: closed
  Merged At: 2024-11-12T04:30:12Z
  Changed Files Count: 3
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/casetest/testdata/plan_normalized_suite_out.json
  - planner/core/plan_cost_ver2.go
  - planner/core/task.go
  PR Summary: This is an automated cherry-pick of #56387 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #56412: planner: Set minimum cost to avoid parent multiplication cost discrepancies (#56387)
  URL: https://github.com/pingcap/tidb/pull/56412
  State: closed
  Merged At: 2024-09-30T07:30:15Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/task.go
  PR Summary: This is an automated cherry-pick of #56387 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #56631: planner: set min for high risk plan steps
  URL: https://github.com/pingcap/tidb/pull/56631
  State: closed
  Merged At: 2024-10-29T18:08:36Z
  Changed Files Count: 8
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_size.go
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/plan_cost_ver1.go
  - pkg/planner/core/plan_cost_ver2.go
  - tests/integrationtest/r/explain_complex.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Ensure a minimum number of rows and a minimum row size for each plan operation for the optimizer cost model. And ensure that non-index based operations have a minimum of 1 row processed, and row length of at least 2. Index based operations can be fractional (less than 1) due to index probes being averaged out across all outer to inner probes for joins - thus the minimum of 1 row does not apply to index operations due to risk of biasing away from index joins or index merges. Estimates at zero or below zero are possible in many situations due to realtime insert/update/delete tracking for statistics processing is not transactional (loss of statistics are OK - since it is not user data, and will be corrected n
- Fix PR #56972: planner: set min for high risk plan steps (#56631)
  URL: https://github.com/pingcap/tidb/pull/56972
  State: closed
  Merged At: 2024-11-12T03:13:06Z
  Changed Files Count: 3
  Main Modules: planner/core, statistics/column.go, statistics/table.go
  Sample Changed Files:
  - planner/core/plan_cost_ver1.go
  - statistics/column.go
  - statistics/table.go
  PR Summary: This is an automated cherry-pick of #56631 What problem does this PR solve? Problem Summary: What changed and how does it work? Ensure a minimum number of rows and a minimum row size for each plan operation for the optimizer cost model. And ensure that non-index based operations have a minimum of 1 row processed, and row length of at least 2. Index based operations can be fractional (less than 1) due to index probes being averaged out across all outer to inner probes for joins - thus the minimum of 1 row does not apply to index operations due to risk of biasing away from index joins or index merges.
- Fix PR #56973: planner: set min for high risk plan steps (#56631)
  URL: https://github.com/pingcap/tidb/pull/56973
  State: closed
  Merged At: 2025-06-18T22:37:39Z
  Changed Files Count: 10
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_size.go
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/plan_cost_ver1.go
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - tests/integrationtest/r/explain_complex.result
  - tests/integrationtest/r/planner/core/casetest/partition/partition_pruner.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: This is an automated cherry-pick of #56631 What problem does this PR solve? Problem Summary: What changed and how does it work? Ensure a minimum number of rows and a minimum row size for each plan operation for the optimizer cost model. And ensure that non-index based operations have a minimum of 1 row processed, and row length of at least 2. Index based operations can be fractional (less than 1) due to index probes being averaged out across all outer to inner probes for joins - thus the minimum of 1 row does not apply to index operations due to risk of biasing away from index joins or index merges.
- Fix PR #57142: planner: add protection to avoid setting tot_col_size to negative numbers (#55327) 
  URL: https://github.com/pingcap/tidb/pull/57142
  State: closed
  Merged At: 2024-11-05T13:21:39Z
  Changed Files Count: 3
  Main Modules: statistics/handle
  Sample Changed Files:
  - statistics/handle/ddl.go
  - statistics/handle/handle.go
  - statistics/handle/update.go
  PR Summary: This is an automated cherry-pick of #55327 What problem does this PR solve? Problem Summary: planner: add protection to avoid setting  to negative numbers What changed and how does it work? See more details and analysis in the issue.
- Related PR #61820: planner: set min for high risk plan steps (#56631)
  URL: https://github.com/pingcap/tidb/pull/61820
  State: closed
  Merged At: 2025-06-23T19:42:06Z
  Changed Files Count: 10
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_size.go
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/plan_cost_ver1.go
  - pkg/planner/core/plan_cost_ver2.go
  - tests/integrationtest/r/explain_complex.result
  - tests/integrationtest/r/planner/core/casetest/partition/partition_pruner.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  - tests/integrationtest/t/planner/core/casetest/partition/partition_pruner.test
  PR Summary: This is an automated cherry-pick of #56631 What problem does this PR solve? Problem Summary: What changed and how does it work? NOTE: This issue is a copy of 55126 to ensure the bot approves the cherry pick.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
