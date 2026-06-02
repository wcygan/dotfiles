# Issue #56217: ```read_from_storage``` hint doesn't effect while plan choose the index merge plan

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/56217
- Status: closed
- Type: type/bug
- Created At: 2024-09-23T04:55:44Z
- Closed At: 2024-09-25T12:29:49Z
- Labels: affects-6.5, affects-7.1, affects-7.3, affects-7.5, affects-8.1, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- The hint doesn't effect. The query plan choose the index merge plan instead of tiflash plan.

## Linked PRs
- Related PR #56227: planner: make converge index merge path feel the prefer tiflash hint
  URL: https://github.com/pingcap/tidb/pull/56227
  State: closed
  Merged At: 2024-09-25T12:29:48Z
  Changed Files Count: 4
  Main Modules: pkg/executor, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/test/tiflashtest/BUILD.bazel
  - pkg/executor/test/tiflashtest/tiflash_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/find_best_task.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #56328: planner: make converge index merge path feel the prefer tiflash hint (#56227)
  URL: https://github.com/pingcap/tidb/pull/56328
  State: closed
  Merged At: 2024-11-11T09:44:59Z
  Changed Files Count: 4
  Main Modules: executor/tiflashtest, planner/core
  Sample Changed Files:
  - executor/tiflashtest/BUILD.bazel
  - executor/tiflashtest/tiflash_test.go
  - planner/core/casetest/testdata/plan_suite_out.json
  - planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #56227 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #56329: planner: make converge index merge path feel the prefer tiflash hint (#56227)
  URL: https://github.com/pingcap/tidb/pull/56329
  State: closed
  Merged At: 2024-09-27T09:52:50Z
  Changed Files Count: 4
  Main Modules: pkg/executor, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/test/tiflashtest/BUILD.bazel
  - pkg/executor/test/tiflashtest/tiflash_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #56227 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #56330: planner: make converge index merge path feel the prefer tiflash hint (#56227)
  URL: https://github.com/pingcap/tidb/pull/56330
  State: open
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/executor, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/test/tiflashtest/BUILD.bazel
  - pkg/executor/test/tiflashtest/tiflash_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #56227 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #59072: planner: make converge index merge path feel the prefer tiflash hint (#56227)
  URL: https://github.com/pingcap/tidb/pull/59072
  State: closed
  Merged At: 2025-02-11T07:35:37Z
  Changed Files Count: 2
  Main Modules: executor/tiflashtest, planner/core
  Sample Changed Files:
  - executor/tiflashtest/tiflash_test.go
  - planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #56227 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
