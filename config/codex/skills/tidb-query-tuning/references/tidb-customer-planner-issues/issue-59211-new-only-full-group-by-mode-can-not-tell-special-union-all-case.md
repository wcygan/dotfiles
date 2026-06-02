# Issue #59211: new-only-full-group-by mode can not tell special union all case

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59211
- Status: closed
- Type: type/bug
- Created At: 2025-01-26T07:27:21Z
- Closed At: 2025-02-12T14:43:15Z
- Labels: affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- the 2nd can run success?

## Linked PRs
- Related PR #59212: planner: fix planner can't error for union-all query when new-only-full-group-check is enabled
  URL: https://github.com/pingcap/tidb/pull/59212
  State: closed
  Merged At: 2025-02-12T14:43:13Z
  Changed Files Count: 7
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/operator/logicalop/logical_projection.go
  - pkg/planner/core/operator/logicalop/logical_union_all.go
  - pkg/planner/core/stringer.go
  - pkg/planner/funcdep/extract_fd_test.go
  - pkg/planner/funcdep/fd_graph.go
  - tests/integrationtest/r/planner/funcdep/only_full_group_by.result
  - tests/integrationtest/t/planner/funcdep/only_full_group_by.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #59355: planner: add a util function of finding common equivs between mutli fds.
  URL: https://github.com/pingcap/tidb/pull/59355
  State: closed
  Merged At: 2025-02-11T10:35:44Z
  Changed Files Count: 3
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/funcdep/BUILD.bazel
  - pkg/planner/funcdep/fd_graph.go
  - pkg/planner/funcdep/fd_graph_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #59554: planner: fix planner can't error for union-all query when new-only-full-group-check is enabled (#59212)
  URL: https://github.com/pingcap/tidb/pull/59554
  State: closed
  Merged At: not merged
  Changed Files Count: 7
  Main Modules: pkg/planner/core, planner/funcdep, tests/integrationtest, planner/core
  Sample Changed Files:
  - pkg/planner/core/operator/logicalop/logical_projection.go
  - pkg/planner/core/operator/logicalop/logical_union_all.go
  - planner/core/stringer.go
  - planner/funcdep/extract_fd_test.go
  - planner/funcdep/fd_graph.go
  - tests/integrationtest/r/planner/funcdep/only_full_group_by.result
  - tests/integrationtest/t/planner/funcdep/only_full_group_by.test
  PR Summary: This is an automated cherry-pick of #59212 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #59555: planner: add a util function of finding common equivs between mutli fds. (#59355)
  URL: https://github.com/pingcap/tidb/pull/59555
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: planner/funcdep, pkg/planner
  Sample Changed Files:
  - pkg/planner/funcdep/BUILD.bazel
  - planner/funcdep/fd_graph.go
  - planner/funcdep/fd_graph_test.go
  PR Summary: This is an automated cherry-pick of #59355 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #59602: planner: fix planner can't error for union-all query when new-only-full-group-check is enabled (#59212)
  URL: https://github.com/pingcap/tidb/pull/59602
  State: closed
  Merged At: 2025-02-25T06:11:28Z
  Changed Files Count: 6
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/logical_plans.go
  - pkg/planner/core/stringer.go
  - pkg/planner/funcdep/extract_fd_test.go
  - pkg/planner/funcdep/fd_graph.go
  - tests/integrationtest/r/planner/funcdep/only_full_group_by.result
  - tests/integrationtest/t/planner/funcdep/only_full_group_by.test
  PR Summary: This is an automated cherry-pick of #59212 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #59603: planner: add a util function of finding common equivs between mutli fds. (#59355)
  URL: https://github.com/pingcap/tidb/pull/59603
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/funcdep/BUILD.bazel
  - pkg/planner/funcdep/fd_graph.go
  - pkg/planner/funcdep/fd_graph_test.go
  PR Summary: This is an automated cherry-pick of #59355 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #60442: planner: fix planner can't error for union-all query when new-only-full-group-check is enabled (#59212)
  URL: https://github.com/pingcap/tidb/pull/60442
  State: closed
  Merged At: 2025-04-12T12:59:58Z
  Changed Files Count: 7
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/operator/logicalop/logical_projection.go
  - pkg/planner/core/operator/logicalop/logical_union_all.go
  - pkg/planner/core/stringer.go
  - pkg/planner/funcdep/extract_fd_test.go
  - pkg/planner/funcdep/fd_graph.go
  - tests/integrationtest/r/planner/funcdep/only_full_group_by.result
  - tests/integrationtest/t/planner/funcdep/only_full_group_by.test
  PR Summary: This is an automated cherry-pick of #59212 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #60443: planner: add a util function of finding common equivs between mutli fds. (#59355)
  URL: https://github.com/pingcap/tidb/pull/60443
  State: closed
  Merged At: 2025-04-12T12:20:01Z
  Changed Files Count: 3
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/funcdep/BUILD.bazel
  - pkg/planner/funcdep/fd_graph.go
  - pkg/planner/funcdep/fd_graph_test.go
  PR Summary: This is an automated cherry-pick of #59355 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
