# Issue #64278: planner chooses wrong plan due to the overestimation of equal condition on index

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64278
- Status: closed
- Type: type/bug
- Created At: 2025-11-05T03:27:13Z
- Closed At: 2025-11-06T08:32:39Z
- Labels: affects-8.1, affects-8.5, epic/cardinality-estimation, report/customer, severity/major, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- this is the plan of v8.5.3, use limit and use the primary key, which is also the order by key. you can see the result is empty, which means the IndexFullScan will scan the whole index, which is suboptimal

## Linked PRs
- Fix PR #64139: planner: set an lower-bound for NDV used in out-of-range estimation for EQ conditions when the Histogram is empty | tidb-test=pr/2623
  URL: https://github.com/pingcap/tidb/pull/64139
  State: closed
  Merged At: 2025-10-31T10:52:36Z
  Changed Files Count: 6
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  PR Summary: What problem does this PR solve? Problem Summary: planner: consider empty histogram and newly emerging values in out-of-range estimation for EQ conditions more properly What changed and how does it work? See  for more details. Hard to create a stable and graceful test case for this issue, so I tested it locally and here is the result:
- Related PR #64221: planner: set an lower-bound for NDV used in out-of-range estimation for EQ conditions when the Histogram is empty | tidb-test=pr/2623 (#64139)
  URL: https://github.com/pingcap/tidb/pull/64221
  State: closed
  Merged At: 2025-10-31T16:45:27Z
  Changed Files Count: 4
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  PR Summary: This is an automated cherry-pick of #64139 What problem does this PR solve? Problem Summary: planner: consider empty histogram and newly emerging values in out-of-range estimation for EQ conditions more properly What changed and how does it work? See  for more details.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
