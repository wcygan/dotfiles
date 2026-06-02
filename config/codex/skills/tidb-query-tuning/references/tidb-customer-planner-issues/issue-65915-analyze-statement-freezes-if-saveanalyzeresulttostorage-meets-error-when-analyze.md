# Issue #65915: `ANALYZE` statement freezes if `SaveAnalyzeResultToStorage` meets error when analyzeing partitioned table

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65915
- Status: closed
- Type: type/bug
- Created At: 2026-01-29T12:15:28Z
- Closed At: 2026-02-27T12:15:49Z
- Labels: affects-8.5, component/statistics, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- Analyze statement freezes forever, and can't be ed.

## Linked PRs
- Fix PR #66169: executor, statistics: avoid analyze hang on save error
  URL: https://github.com/pingcap/tidb/pull/66169
  State: closed
  Merged At: 2026-02-27T12:15:48Z
  Changed Files Count: 4
  Main Modules: pkg/executor, pkg/statistics
  Sample Changed Files:
  - pkg/executor/analyze.go
  - pkg/executor/analyze_test.go
  - pkg/executor/analyze_worker.go
  - pkg/statistics/handle/storage/save.go
  PR Summary: What problem does this PR solve? Problem Summary: ANALYZE on heavily partitioned tables can hang when saving stats fails (for example, lock wait timeout), because save workers exit early and analyze workers block on result channels. What changed and how does it work? Add a failpoint to simulate save errors and a unit test that asserts ANALYZE returns an error instead of hanging.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
