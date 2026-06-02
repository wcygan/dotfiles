# Issue #53951: projection containing virtual columns should be evaluated before the UnionScan(dirty write content)

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/53951
- Status: closed
- Type: type/bug
- Created At: 2024-06-11T23:48:15Z
- Closed At: 2024-06-13T18:43:56Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, impact/wrong-result, report/customer, severity/critical, sig/planner, type/bug

## Customer-Facing Phenomenon
- The update in the transaction was not read.

## Linked PRs
- Fix PR #53956: planner: return an error when meeting unexpected operator under UnionScan
  URL: https://github.com/pingcap/tidb/pull/53956
  State: closed
  Merged At: 2024-06-12T10:39:00Z
  Changed Files Count: 1
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/builder.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: return an error when meeting unexpected operator under UnionScan What changed and how does it work?
- Fix PR #53968: planner: return an error when meeting unexpected operator under UnionScan (#53956)
  URL: https://github.com/pingcap/tidb/pull/53968
  State: closed
  Merged At: 2024-06-14T07:25:16Z
  Changed Files Count: 1
  Main Modules: executor/builder.go
  Sample Changed Files:
  - executor/builder.go
  PR Summary: This is an automated cherry-pick of #53956 What problem does this PR solve? Problem Summary: planner: return an error when meeting unexpected operator under UnionScan What changed and how does it work?
- Fix PR #53969: planner: return an error when meeting unexpected operator under UnionScan (#53956)
  URL: https://github.com/pingcap/tidb/pull/53969
  State: closed
  Merged At: 2024-11-11T03:23:14Z
  Changed Files Count: 1
  Main Modules: executor/builder.go
  Sample Changed Files:
  - executor/builder.go
  PR Summary: This is an automated cherry-pick of #53956 What problem does this PR solve? Problem Summary: planner: return an error when meeting unexpected operator under UnionScan What changed and how does it work?
- Fix PR #53970: planner: return an error when meeting unexpected operator under UnionScan (#53956)
  URL: https://github.com/pingcap/tidb/pull/53970
  State: closed
  Merged At: 2024-07-08T17:24:02Z
  Changed Files Count: 1
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/builder.go
  PR Summary: This is an automated cherry-pick of #53956 What problem does this PR solve? Problem Summary: planner: return an error when meeting unexpected operator under UnionScan What changed and how does it work?
- Fix PR #53971: planner: return an error when meeting unexpected operator under UnionScan (#53956)
  URL: https://github.com/pingcap/tidb/pull/53971
  State: closed
  Merged At: 2024-08-01T02:26:59Z
  Changed Files Count: 1
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/builder.go
  PR Summary: This is an automated cherry-pick of #53956 What problem does this PR solve? Problem Summary: planner: return an error when meeting unexpected operator under UnionScan What changed and how does it work?
- Fix PR #53981: planner: prevent pushing Projection with virtual columns down to UnionScan
  URL: https://github.com/pingcap/tidb/pull/53981
  State: closed
  Merged At: 2024-06-13T18:43:55Z
  Changed Files Count: 3
  Main Modules: pkg/executor, pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/executor/union_scan_test.go
  - pkg/planner/core/rule_predicate_push_down.go
  - tests/integrationtest/r/explain_generate_column_substitute.result
  PR Summary: What problem does this PR solve? Problem Summary: planner: prevent pushing Projection with virtual columns down to UnionScan What changed and how does it work?
- Fix PR #54014: planner: prevent pushing Projection with virtual columns down to UnionScan (#53981)
  URL: https://github.com/pingcap/tidb/pull/54014
  State: closed
  Merged At: 2024-06-14T08:10:15Z
  Changed Files Count: 3
  Main Modules: cmd/explaintest, executor/union_scan_test.go, planner/core
  Sample Changed Files:
  - cmd/explaintest/r/explain_generate_column_substitute.result
  - executor/union_scan_test.go
  - planner/core/rule_predicate_push_down.go
  PR Summary: This is an automated cherry-pick of #53981 What problem does this PR solve? Problem Summary: planner: prevent pushing Projection with virtual columns down to UnionScan What changed and how does it work?
- Fix PR #54351: planner: prevent pushing Projection with virtual columns down to UnionScan (#53981)
  URL: https://github.com/pingcap/tidb/pull/54351
  State: closed
  Merged At: 2024-07-15T09:36:05Z
  Changed Files Count: 3
  Main Modules: pkg/executor, pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/executor/union_scan_test.go
  - pkg/planner/core/rule_predicate_push_down.go
  - tests/integrationtest/r/explain_generate_column_substitute.result
  PR Summary: This is an automated cherry-pick of #53981 What problem does this PR solve? Problem Summary: planner: prevent pushing Projection with virtual columns down to UnionScan What changed and how does it work?
- Fix PR #54986: planner: prevent pushing Projection with virtual columns down to UnionScan (#53981)
  URL: https://github.com/pingcap/tidb/pull/54986
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: cmd/explaintest, pkg/executor, planner/core
  Sample Changed Files:
  - cmd/explaintest/r/explain_generate_column_substitute.result
  - pkg/executor/union_scan_test.go
  - planner/core/rule_predicate_push_down.go
  PR Summary: This is an automated cherry-pick of #53981 What problem does this PR solve? Problem Summary: planner: prevent pushing Projection with virtual columns down to UnionScan What changed and how does it work?
- Fix PR #57241: planner: prevent pushing Projection with virtual columns down to UnionScan (#53981)
  URL: https://github.com/pingcap/tidb/pull/57241
  State: closed
  Merged At: 2024-11-08T11:13:47Z
  Changed Files Count: 3
  Main Modules: cmd/explaintest, executor/union_scan_test.go, planner/core
  Sample Changed Files:
  - cmd/explaintest/r/explain_generate_column_substitute.result
  - executor/union_scan_test.go
  - planner/core/rule_predicate_push_down.go
  PR Summary: This is an automated cherry-pick of #53981 What problem does this PR solve? Problem Summary: planner: prevent pushing Projection with virtual columns down to UnionScan What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
