# Issue #64572: planner: unexpected low out-of-range estimation on index stats

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64572
- Status: closed
- Type: type/bug
- Created At: 2025-11-19T14:21:22Z
- Closed At: 2025-11-20T08:20:51Z
- Labels: affects-7.5, affects-8.1, affects-8.5, epic/cardinality-estimation, report/customer, severity/major, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- Extremely low estimation.

## Linked PRs
- Fix PR #64582: planner: out of range col stats only if loaded | tidb-test=pr/2631
  URL: https://github.com/pingcap/tidb/pull/64582
  State: closed
  Merged At: 2025-11-20T08:20:50Z
  Changed Files Count: 4
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - tests/integrationtest/r/imdbload.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #64591: planner: out of range col stats only if loaded | tidb-test=pr/2631 (#64582)
  URL: https://github.com/pingcap/tidb/pull/64591
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - tests/integrationtest/r/imdbload.result
  PR Summary: This is an automated cherry-pick of #64582 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #64593: planner: out of range col stats only if loaded | tidb-test=pr/2631 (#64582)
  URL: https://github.com/pingcap/tidb/pull/64593
  State: closed
  Merged At: 2025-11-20T16:32:14Z
  Changed Files Count: 1
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  PR Summary: This is an automated cherry-pick of #64582 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
