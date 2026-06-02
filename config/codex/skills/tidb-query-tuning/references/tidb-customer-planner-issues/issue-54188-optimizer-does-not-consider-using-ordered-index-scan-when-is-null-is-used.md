# Issue #54188: optimizer does not consider using ordered index scan when `is null` is used

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/54188
- Status: closed
- Type: type/enhancement
- Created At: 2024-06-24T16:50:31Z
- Closed At: 2024-07-19T18:42:02Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #54253: planner: use ordered index with is null predicate | tidb-test=pr/2368
  URL: https://github.com/pingcap/tidb/pull/54253
  State: closed
  Merged At: 2024-07-19T18:42:01Z
  Changed Files Count: 6
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/util
  Sample Changed Files:
  - pkg/planner/core/casetest/index/BUILD.bazel
  - pkg/planner/core/casetest/index/index_test.go
  - pkg/util/ranger/detacher.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/util/ranger.result
  - tests/integrationtest/t/planner/core/casetest/integration.test
  PR Summary: What problem does this PR solve? Problem Summary: Properly classify columns with null predicates (e.g. ) as constant so index selection can take advantage of that to satisfy a sort in What changed and how does it work? Added checks for is null predicate during planning and fill corresponding data structures marking that column as a constant.
- Fix PR #54290: planner: use ordered index with is null predicate
  URL: https://github.com/pingcap/tidb/pull/54290
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/util
  Sample Changed Files:
  - pkg/planner/core/casetest/index/BUILD.bazel
  - pkg/planner/core/casetest/index/index_test.go
  - pkg/util/ranger/detacher.go
  PR Summary: What problem does this PR solve? Problem Summary: Properly classify columns with null predicates (e.g. ) as constant so index selection can take advantage of that to satisfy a sort in as constant so index selection can take advantage of that to satisfy a sort in: [tidb/pkg/planner/core/find_best_task.go]() Dupe of #54253 with bazel fixes. @ari-e is out for a bit so attempting to unblock this while he is out.
- Related PR #54512: planner: use ordered index with is null predicate
  URL: https://github.com/pingcap/tidb/pull/54512
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/util
  Sample Changed Files:
  - pkg/planner/core/casetest/index/BUILD.bazel
  - pkg/planner/core/casetest/index/index_test.go
  - pkg/util/ranger/detacher.go
  PR Summary: What problem does this PR solve? Problem Summary: Properly classify columns with null predicates (e.g. WHERE a IS NULL) as constant so index selection can take advantage of that to satisfy a sort in as constant so index selection can take advantage of that to satisfy a sort in: [tidb/pkg/planner/core/find_best_task.go]()
- Fix PR #54788: planner: use ordered index with is null predicate | tidb-test=pr/2368 (#54253)
  URL: https://github.com/pingcap/tidb/pull/54788
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/util
  Sample Changed Files:
  - pkg/planner/core/casetest/index/index_test.go
  - pkg/util/ranger/detacher.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/util/ranger.result
  - tests/integrationtest/t/planner/core/casetest/integration.test
  PR Summary: This is an automated cherry-pick of #54253 What problem does this PR solve? Problem Summary: Properly classify columns with null predicates (e.g. ) as constant so index selection can take advantage of that to satisfy a sort in What changed and how does it work? Added checks for is null predicate during planning and fill corresponding data structures marking that column as a constant.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
