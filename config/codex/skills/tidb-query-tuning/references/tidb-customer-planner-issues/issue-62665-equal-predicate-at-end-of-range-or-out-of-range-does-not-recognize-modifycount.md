# Issue #62665: Equal predicate at end of range or out of range does not recognize modifyCount

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62665
- Status: closed
- Type: type/bug
- Created At: 2025-07-29T00:05:42Z
- Closed At: 2025-08-02T19:33:52Z
- Labels: affects-8.5, epic/cardinality-estimation, report/customer, severity/minor, sig/planner, type/bug

## Customer-Facing Phenomenon
- The explain output is similar to before the rows were inserted

## Linked PRs
- Fix PR #62695: planner: handle histogram last bucket end value underrepresented
  URL: https://github.com/pingcap/tidb/pull/62695
  State: closed
  Merged At: 2025-08-02T19:33:51Z
  Changed Files Count: 6
  Main Modules: pkg/planner, pkg/statistics
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_column.go
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/statistics/histogram.go
  PR Summary: What problem does this PR solve? Problem Summary: Like what the linked issue describes, the end value in the last histogram bucket could be underrepresented due to stale stats. This PR tries to detect such case precisely by looking at two conditions: 1.  The value should be in last histogram bucket and it should be the upper bound 2. The last bucket end count is much less than the average count of other NDV, indicating this might be a tail write traffic
- Fix PR #62812: planner: handle histogram last bucket end value underrepresented (#62695)
  URL: https://github.com/pingcap/tidb/pull/62812
  State: closed
  Merged At: 2025-09-18T03:25:44Z
  Changed Files Count: 6
  Main Modules: pkg/planner, pkg/statistics
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_column.go
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/statistics/histogram.go
  PR Summary: This is an automated cherry-pick of #62695 What problem does this PR solve? Problem Summary: Like what the linked issue describes, the end value in the last histogram bucket could be underrepresented due to stale stats. This PR tries to detect such case precisely by looking at two conditions: 1.  The value should be in last histogram bucket and it should be the upper bound

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
