# Issue #63235: With the introduction of `isSafeRange`, CPU resources are consumed more heavily.

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63235
- Status: closed
- Type: type/bug
- Created At: 2025-08-27T17:44:59Z
- Closed At: 2025-09-22T17:56:59Z
- Labels: affects-7.5, affects-8.1, affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #63566: planner: optimizer the performance of `IsFullRange` check
  URL: https://github.com/pingcap/tidb/pull/63566
  State: closed
  Merged At: 2025-09-22T17:56:58Z
  Changed Files Count: 1
  Main Modules: pkg/util
  Sample Changed Files:
  - pkg/util/ranger/types.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: optimizer the performance of  check What changed and how does it work? planner: optimizer the performance of  check
- Fix PR #63812: planner: optimizer the performance of `IsFullRange` check (#63566)
  URL: https://github.com/pingcap/tidb/pull/63812
  State: closed
  Merged At: 2025-12-15T02:59:26Z
  Changed Files Count: 1
  Main Modules: pkg/util
  Sample Changed Files:
  - pkg/util/ranger/types.go
  PR Summary: This is an automated cherry-pick of #63566 What problem does this PR solve? Problem Summary: planner: optimizer the performance of  check What changed and how does it work? planner: optimizer the performance of  check
- Fix PR #63813: planner: optimizer the performance of `IsFullRange` check (#63566)
  URL: https://github.com/pingcap/tidb/pull/63813
  State: closed
  Merged At: 2025-10-31T15:06:36Z
  Changed Files Count: 1
  Main Modules: pkg/util
  Sample Changed Files:
  - pkg/util/ranger/types.go
  PR Summary: This is an automated cherry-pick of #63566 What problem does this PR solve? Problem Summary: planner: optimizer the performance of  check What changed and how does it work? planner: optimizer the performance of  check
- Fix PR #63828: planner: remove fullRange check from skyline pruning
  URL: https://github.com/pingcap/tidb/pull/63828
  State: closed
  Merged At: 2025-10-02T14:51:31Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/find_best_task.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? FullRange check was found to be expensive in some scenarios. This PR restructures the skylinePruning logic to reduce reliance on this check. It uses other checks where possible, and also will only call this after other criteria has been validated.
- Fix PR #64056: planner: optimizer the performance of `IsFullRange` check (#63566)
  URL: https://github.com/pingcap/tidb/pull/64056
  State: open
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/util
  Sample Changed Files:
  - pkg/util/ranger/types.go
  PR Summary: This is an automated cherry-pick of #63566 What problem does this PR solve? Problem Summary: planner: optimizer the performance of  check What changed and how does it work? planner: optimizer the performance of  check
- Fix PR #64057: planner: remove fullRange check from skyline pruning (#63828)
  URL: https://github.com/pingcap/tidb/pull/64057
  State: open
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #63828 What problem does this PR solve? Problem Summary: What changed and how does it work? FullRange check was found to be expensive in some scenarios. This PR will only call this after other criteria has been validated.
- Fix PR #64058: planner: remove fullRange check from skyline pruning (#63828)
  URL: https://github.com/pingcap/tidb/pull/64058
  State: closed
  Merged At: 2025-11-01T01:09:48Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #63828 What problem does this PR solve? Problem Summary: What changed and how does it work? FullRange check was found to be expensive in some scenarios. This PR restructures the skylinePruning logic to reduce reliance on this check. It uses other checks where possible, and also will only call this after other criteria has been validated.
- Fix PR #64447: planner: remove fullRange check from skyline pruning (#63828)
  URL: https://github.com/pingcap/tidb/pull/64447
  State: closed
  Merged At: 2025-12-11T20:22:50Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #63828 What problem does this PR solve? Problem Summary: What changed and how does it work? FullRange check was found to be expensive in some scenarios. This PR restructures the skylinePruning logic to reduce reliance on this check. It uses other checks where possible, and also will only call this after other criteria has been validated.
- Related PR #66304: planner: optimize for full range
  URL: https://github.com/pingcap/tidb/pull/66304
  State: closed
  Merged At: 2026-02-19T19:09:06Z
  Changed Files Count: 5
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/stats.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? This PR provides 2 main optimizations: 1) It allows index row count estimation to be skipped if the predicate ranges cover the entire index range.
- Related PR #66313: planner: optimize for full range (#66304)
  URL: https://github.com/pingcap/tidb/pull/66313
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/stats.go
  PR Summary: This is an automated cherry-pick of #66304 What problem does this PR solve? Problem Summary: What changed and how does it work? This PR provides 2 main optimizations:
- Related PR #66314: planner: optimize for full range (#66304)
  URL: https://github.com/pingcap/tidb/pull/66314
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/stats.go
  PR Summary: This is an automated cherry-pick of #66304 What problem does this PR solve? Problem Summary: What changed and how does it work? This PR provides 2 main optimizations:
- Related PR #66695: planner: optimize for full range (#66304) | tidb-test=pr/2708
  URL: https://github.com/pingcap/tidb/pull/66695
  State: open
  Merged At: not merged
  Changed Files Count: 15
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest, pkg/ddl, pkg/executor
  Sample Changed Files:
  - pkg/ddl/tests/partition/db_partition_test.go
  - pkg/executor/test/analyzetest/analyze_test.go
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_out.json
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/logical_plans_test.go
  - pkg/planner/core/stats.go
  - pkg/planner/core/testdata/index_merge_suite_out.json
  - pkg/planner/util/path.go
  - tests/integrationtest/r/imdbload.result
  - tests/integrationtest/r/planner/core/casetest/index/index.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: This is an automated cherry-pick of #66304 What problem does this PR solve? Problem Summary: What changed and how does it work? This PR provides 2 main optimizations:

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
