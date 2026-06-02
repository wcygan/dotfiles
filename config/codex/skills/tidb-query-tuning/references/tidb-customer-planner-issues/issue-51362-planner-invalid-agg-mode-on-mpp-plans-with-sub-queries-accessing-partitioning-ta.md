# Issue #51362: planner: invalid Agg mode on MPP plans with sub-queries accessing partitioning tables under static partition mode

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/51362
- Status: closed
- Type: type/bug
- Created At: 2024-02-27T09:17:30Z
- Closed At: 2024-05-22T06:46:18Z
- Labels: affects-7.5, affects-8.1, report/customer, severity/moderate, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- ERROR 1105 (HY000): other error for mpp stream: Code: 0, e.displayText() = DB::TiFlashException: Different aggregation mode detected, e.what() = DB::TiFlashException,

## Linked PRs
- Related PR #53455: planner: fix mpp final agg couldn't co-exist with other non-final mode
  URL: https://github.com/pingcap/tidb/pull/53455
  State: closed
  Merged At: 2024-05-22T06:46:17Z
  Changed Files Count: 5
  Main Modules: pkg/expression, pkg/planner/core
  Sample Changed Files:
  - pkg/expression/aggregation/BUILD.bazel
  - pkg/expression/aggregation/aggregation.go
  - pkg/expression/aggregation/explain.go
  - pkg/planner/core/enforce_mpp_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #53475: planner: fix mpp final agg couldn't co-exist with other non-final mode (#53455)
  URL: https://github.com/pingcap/tidb/pull/53475
  State: closed
  Merged At: 2024-05-28T07:28:21Z
  Changed Files Count: 5
  Main Modules: pkg/expression, pkg/planner/core
  Sample Changed Files:
  - pkg/expression/aggregation/BUILD.bazel
  - pkg/expression/aggregation/aggregation.go
  - pkg/expression/aggregation/explain.go
  - pkg/planner/core/enforce_mpp_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  PR Summary: This is an automated cherry-pick of #53455 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #53476: planner: fix mpp final agg couldn't co-exist with other non-final mode (#53455)
  URL: https://github.com/pingcap/tidb/pull/53476
  State: closed
  Merged At: 2024-08-01T02:26:52Z
  Changed Files Count: 6
  Main Modules: pkg/expression, pkg/executor, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/test/tiflashtest/BUILD.bazel
  - pkg/executor/test/tiflashtest/tiflash_test.go
  - pkg/expression/aggregation/BUILD.bazel
  - pkg/expression/aggregation/aggregation.go
  - pkg/expression/aggregation/explain.go
  - pkg/planner/core/exhaust_physical_plans.go
  PR Summary: This is an automated cherry-pick of #53455 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #53484: planner: make TestMppAggShouldAlignFinalMode test case stable
  URL: https://github.com/pingcap/tidb/pull/53484
  State: closed
  Merged At: 2024-05-22T09:23:48Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/enforce_mpp_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #54666: planner: make TestMppAggShouldAlignFinalMode test case stable (#53484)
  URL: https://github.com/pingcap/tidb/pull/54666
  State: closed
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/enforce_mpp_test.go
  PR Summary: This is an automated cherry-pick of #53484 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
