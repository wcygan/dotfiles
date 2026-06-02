# Issue #54870: planner: can't push down predicates with generated columns down through UnionScan

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/54870
- Status: closed
- Type: type/bug
- Created At: 2024-07-24T09:25:01Z
- Closed At: 2024-07-29T05:58:17Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, report/customer, severity/major, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #54985: planner: push necessary predicates without virtual column down through UnionScan
  URL: https://github.com/pingcap/tidb/pull/54985
  State: closed
  Merged At: 2024-07-29T05:58:16Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_union_scan.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: push necessary predicates without virtual column down through UnionScan What changed and how does it work?
- Fix PR #54990: planner: push necessary predicates without virtual column down through UnionScan (#54985)
  URL: https://github.com/pingcap/tidb/pull/54990
  State: closed
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_union_scan.go
  PR Summary: This is an automated cherry-pick of #54985 What problem does this PR solve? Problem Summary: planner: push necessary predicates without virtual column down through UnionScan What changed and how does it work?
- Fix PR #54991: planner: push necessary predicates without virtual column down through UnionScan (#54985)
  URL: https://github.com/pingcap/tidb/pull/54991
  State: closed
  Merged At: 2024-08-01T10:05:51Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/rule_predicate_push_down.go
  - tests/integrationtest/r/explain_generate_column_substitute.result
  PR Summary: This is an automated cherry-pick of #54985 What problem does this PR solve? Problem Summary: planner: push necessary predicates without virtual column down through UnionScan What changed and how does it work?
- Fix PR #54992: planner: push necessary predicates without virtual column down through UnionScan (#54985)
  URL: https://github.com/pingcap/tidb/pull/54992
  State: closed
  Merged At: 2024-07-29T06:47:48Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/rule_predicate_push_down.go
  PR Summary: This is an automated cherry-pick of #54985 What problem does this PR solve? Problem Summary: planner: push necessary predicates without virtual column down through UnionScan What changed and how does it work?
- Fix PR #55015: planner: push necessary predicates without virtual column down through UnionScan (#54985)
  URL: https://github.com/pingcap/tidb/pull/55015
  State: closed
  Merged At: 2024-08-29T07:29:57Z
  Changed Files Count: 2
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/integration_test.go
  - planner/core/rule_predicate_push_down.go
  PR Summary: This is an automated cherry-pick of #54985 What problem does this PR solve? Problem Summary: planner: push necessary predicates without virtual column down through UnionScan What changed and how does it work?
- Fix PR #55152: planner: push necessary predicates without virtual column down through UnionScan (#54985) | tidb-test=release-6.5 plugin=release-6.5 
  URL: https://github.com/pingcap/tidb/pull/55152
  State: closed
  Merged At: 2024-08-02T07:35:51Z
  Changed Files Count: 2
  Main Modules: executor/union_scan_test.go, planner/core
  Sample Changed Files:
  - executor/union_scan_test.go
  - planner/core/rule_predicate_push_down.go
  PR Summary: This is an automated cherry-pick of #54985 What problem does this PR solve? Problem Summary: planner: push necessary predicates without virtual column down through UnionScan What changed and how does it work?
- Fix PR #57267: planner: push necessary predicates without virtual column down through UnionScan (#54985)
  URL: https://github.com/pingcap/tidb/pull/57267
  State: closed
  Merged At: 2024-11-11T09:45:35Z
  Changed Files Count: 2
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/casetest/integration_test.go
  - planner/core/rule_predicate_push_down.go
  PR Summary: This is an automated cherry-pick of #54985 What problem does this PR solve? Problem Summary: planner: push necessary predicates without virtual column down through UnionScan What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
