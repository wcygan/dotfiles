# Issue #52601: Negative WaitGroup counter during the analyze cause TiDB is killed

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52601
- Status: closed
- Type: type/bug
- Created At: 2024-04-15T07:18:33Z
- Closed At: 2024-04-16T11:12:07Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- <img width="1239" alt="image" src="

## Linked PRs
- Fix PR #52604: executor: fix negative WaitGroup counter when to analyze
  URL: https://github.com/pingcap/tidb/pull/52604
  State: closed
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col.go
  - pkg/executor/analyze_col_v2.go
  - pkg/executor/test/analyzetest/BUILD.bazel
  - pkg/executor/test/analyzetest/analyze_test.go
  - pkg/executor/test/analyzetest/panictest/BUILD.bazel
  - pkg/executor/test/analyzetest/panictest/panic_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? fix the shared  which is possible to lead to panic. 1、remove this shared
- Fix PR #52634: executor: remove the retry for analyze
  URL: https://github.com/pingcap/tidb/pull/52634
  State: closed
  Merged At: 2024-04-16T11:12:06Z
  Changed Files Count: 2
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col.go
  - pkg/executor/analyze_col_v2.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? 1、In v7.5, we have optimized the memory usage for analyze. so it is hard to OOM now. 2、If OOM happens， we should tell users about the oom event. we should not change the sample rate of the table.
- Fix PR #52661: executor: remove the retry for analyze (#52634)
  URL: https://github.com/pingcap/tidb/pull/52661
  State: closed
  Merged At: 2024-05-21T07:58:23Z
  Changed Files Count: 2
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col.go
  - pkg/executor/analyze_col_v2.go
  PR Summary: This is an automated cherry-pick of #52634 What problem does this PR solve? Problem Summary: What changed and how does it work? 1、In v7.5, we have optimized the memory usage for analyze. so it is hard to OOM now.
- Fix PR #52662: executor: remove the retry for analyze (#52634)
  URL: https://github.com/pingcap/tidb/pull/52662
  State: closed
  Merged At: 2024-04-18T11:21:07Z
  Changed Files Count: 2
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col.go
  - pkg/executor/analyze_col_v2.go
  PR Summary: This is an automated cherry-pick of #52634 What problem does this PR solve? Problem Summary: What changed and how does it work? 1、In v7.5, we have optimized the memory usage for analyze. so it is hard to OOM now.
- Fix PR #52679: executor: remove the retry for analyze (#52634)
  URL: https://github.com/pingcap/tidb/pull/52679
  State: closed
  Merged At: 2024-06-03T06:11:55Z
  Changed Files Count: 2
  Main Modules: executor/analyze_col.go, executor/analyze_col_v2.go
  Sample Changed Files:
  - executor/analyze_col.go
  - executor/analyze_col_v2.go
  PR Summary: This is an automated cherry-pick of #52634 What problem does this PR solve? Problem Summary: What changed and how does it work? 1、In v7.5, we have optimized the memory usage for analyze. so it is hard to OOM now.
- Fix PR #53702: executor: remove the retry for analyze (#52634)
  URL: https://github.com/pingcap/tidb/pull/53702
  State: closed
  Merged At: 2024-06-03T08:25:25Z
  Changed Files Count: 2
  Main Modules: executor/analyze_col.go, executor/analyze_col_v2.go
  Sample Changed Files:
  - executor/analyze_col.go
  - executor/analyze_col_v2.go
  PR Summary: This is an automated cherry-pick of #52634 What problem does this PR solve? Problem Summary: What changed and how does it work? 1、In v7.5, we have optimized the memory usage for analyze. so it is hard to OOM now.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
