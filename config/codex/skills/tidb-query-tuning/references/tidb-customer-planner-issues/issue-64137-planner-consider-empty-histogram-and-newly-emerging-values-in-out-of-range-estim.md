# Issue #64137: planner: consider empty histogram and newly emerging values in out-of-range estimation for EQ conditions more properly

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64137
- Status: closed
- Type: type/bug
- Created At: 2025-10-27T08:47:23Z
- Closed At: 2025-10-31T10:52:37Z
- Labels: affects-8.5, epic/cardinality-estimation, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- A large estimation error .

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
- Fix PR #64220: planner: set an lower-bound for NDV used in out-of-range estimation for EQ conditions when the Histogram is empty | tidb-test=pr/2623 (#64139)
  URL: https://github.com/pingcap/tidb/pull/64220
  State: closed
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/planner, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  PR Summary: This is an automated cherry-pick of #64139 What problem does this PR solve? Problem Summary: planner: consider empty histogram and newly emerging values in out-of-range estimation for EQ conditions more properly What changed and how does it work? See  for more details.
- Fix PR #64221: planner: set an lower-bound for NDV used in out-of-range estimation for EQ conditions when the Histogram is empty | tidb-test=pr/2623 (#64139)
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
