# Issue #64423: Analyze a small table costs a lot of memory

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64423
- Status: closed
- Type: type/bug
- Created At: 2025-11-11T07:52:42Z
- Closed At: 2026-02-28T10:32:42Z
- Labels: affects-7.1, affects-7.5, affects-8.1, affects-8.5, affects-9.0, component/statistics, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- The table is small, it only has 80MB data. But the analyze statement costs more than 2GB memory. check the memory cost in the dashboard:

## Linked PRs
- Fix PR #65446: executor: optimize analyze column memory usage
  URL: https://github.com/pingcap/tidb/pull/65446
  State: closed
  Merged At: 2026-01-30T06:16:17Z
  Changed Files Count: 9
  Main Modules: pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col.go
  - pkg/executor/analyze_col_v2.go
  - pkg/statistics/builder.go
  - pkg/statistics/builder_test.go
  - pkg/statistics/fmsketch_test.go
  - pkg/statistics/main_test.go
  - pkg/statistics/sample.go
  - pkg/statistics/sample_test.go
  - pkg/statistics/statistics_test.go
  PR Summary: What problem does this PR solve? Problem Summary: As  said, the memory reduced from 2.7G to 2.1G. It's not a big improvement. But for an order-of-magnitude improvement in memory footprint, we’d need to optmize the Datum structure, which involves significant effort and risk. What changed and how does it work?
- Fix PR #66166: executor: optimize analyze column memory usage (#65446)
  URL: https://github.com/pingcap/tidb/pull/66166
  State: open
  Merged At: not merged
  Changed Files Count: 9
  Main Modules: pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col.go
  - pkg/executor/analyze_col_v2.go
  - pkg/statistics/builder.go
  - pkg/statistics/builder_test.go
  - pkg/statistics/fmsketch_test.go
  - pkg/statistics/main_test.go
  - pkg/statistics/sample.go
  - pkg/statistics/sample_test.go
  - pkg/statistics/statistics_test.go
  PR Summary: This is an automated cherry-pick of #65446 What problem does this PR solve? Problem Summary: As  said, the memory reduced from 2.7G to 2.1G. It's not a big improvement. But for an order-of-magnitude improvement in memory footprint, we’d need to optmize the Datum structure, which involves significant effort and risk. What changed and how does it work?
- Fix PR #66747: executor, statistics: release analyze collector memory eagerly
  URL: https://github.com/pingcap/tidb/pull/66747
  State: closed
  Merged At: 2026-03-10T22:49:38Z
  Changed Files Count: 4
  Main Modules: pkg/executor, pkg/statistics
  Sample Changed Files:
  - pkg/executor/analyze_col.go
  - pkg/executor/analyze_col_v2.go
  - pkg/executor/analyze_test.go
  - pkg/statistics/sample.go
  PR Summary: What problem does this PR solve? Problem Summary: After extended stats was removed, analyze no longer needs to retain column s until the end of the build flow. The obsolete retention path keeps sampled values alive longer than necessary and inflates analyze memory usage. What changed and how does it work? Release column collector memory immediately after histogram / TopN materialization in analyze v1/v2, and add a regression test for the v2 release timing.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
