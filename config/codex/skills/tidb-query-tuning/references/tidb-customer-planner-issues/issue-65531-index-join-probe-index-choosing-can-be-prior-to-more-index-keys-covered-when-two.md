# Issue #65531: index join probe index choosing can be prior to more index keys covered when two index is not comparable

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65531
- Status: closed
- Type: type/enhancement
- Created At: 2026-01-12T08:33:48Z
- Closed At: 2026-02-25T12:07:28Z
- Labels: affects-8.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Enhancement current plan expected plan

## Linked PRs
- Related PR #65534: planner: index join probe index used cols ndv shouldn't care about range col & add some consideration when two index ndv are quite close
  URL: https://github.com/pingcap/tidb/pull/65534
  State: closed
  Merged At: 2026-02-25T12:07:27Z
  Changed Files Count: 19
  Main Modules: pkg/planner/core, pkg/testkit, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/cbotest/BUILD.bazel
  - pkg/planner/core/casetest/cbotest/cbo_test.go
  - pkg/planner/core/casetest/cbotest/main_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyzeSuiteTestIndexEqualUnknownT.json
  - pkg/planner/core/casetest/cbotest/testdata/analyzeSuiteTestLimitIndexEstimationT.json
  - pkg/planner/core/casetest/cbotest/testdata/analyzeSuiteTestLowSelIndexGreedySearchT.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_in.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/cbotest/testdata/analyzesSuiteTestIndexReadT.json
  - pkg/planner/core/casetest/cbotest/testdata/issue59563.json
  - pkg/planner/core/casetest/cbotest/testdata/issue61792.json
  - pkg/planner/core/casetest/cbotest/testdata/issue62438.json
  - pkg/planner/core/casetest/cbotest/testdata/stats.zip
  - pkg/planner/core/casetest/cbotest/testdata/test.t0da79f8d.json
  - pkg/planner/core/casetest/cbotest/testdata/test.t19f3e4f1.json
  - pkg/planner/core/index_join_path.go
  - pkg/testkit/testkit.go
  - tests/integrationtest/r/planner/core/casetest/index/index.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? as the issue said, sometimes, the index join probe index choosing is more naive, for example in the issue, index_1 and index_2 are in-comparable, then left the decision to the group NDV comparson when compare the group ndv, for index(EQ, EQ, EQ, EQ, col4, col5), the useIndexCols is 4 and we can compute the first 4 EQ's cols group NDV by max each cols' ndv among them.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
