# Issue #62672: only full group by check should be case-sensitive

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62672
- Status: closed
- Type: type/bug
- Created At: 2025-07-29T04:22:28Z
- Closed At: 2025-08-04T15:52:10Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- only full group by check error

## Linked PRs
- Related PR #62751: planner: fix the old only full group check should be case-insensitive.
  URL: https://github.com/pingcap/tidb/pull/62751
  State: closed
  Merged At: 2025-08-04T15:52:09Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/parser
  Sample Changed Files:
  - pkg/parser/ast/expressions.go
  - tests/integrationtest/r/executor/aggregate.result
  - tests/integrationtest/t/executor/aggregate.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #62814: planner: fix the old only full group check should be case-insensitive. (#62751)
  URL: https://github.com/pingcap/tidb/pull/62814
  State: open
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/parser
  Sample Changed Files:
  - pkg/parser/ast/expressions.go
  - tests/integrationtest/r/executor/aggregate.result
  - tests/integrationtest/t/executor/aggregate.test
  PR Summary: This is an automated cherry-pick of #62751 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #62815: planner: fix the old only full group check should be case-insensitive. (#62751)
  URL: https://github.com/pingcap/tidb/pull/62815
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: tests/integrationtest, parser/ast
  Sample Changed Files:
  - parser/ast/expressions.go
  - tests/integrationtest/r/executor/aggregate.result
  - tests/integrationtest/t/executor/aggregate.test
  PR Summary: This is an automated cherry-pick of #62751 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #62816: planner: fix the old only full group check should be case-insensitive. (#62751)
  URL: https://github.com/pingcap/tidb/pull/62816
  State: open
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: tests/integrationtest, parser/ast
  Sample Changed Files:
  - parser/ast/expressions.go
  - tests/integrationtest/r/executor/aggregate.result
  - tests/integrationtest/t/executor/aggregate.test
  PR Summary: This is an automated cherry-pick of #62751 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #63557: planner: fix the old only full group check should be case-insensitive. (#62751)
  URL: https://github.com/pingcap/tidb/pull/63557
  State: closed
  Merged At: 2025-09-21T18:41:07Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/parser
  Sample Changed Files:
  - pkg/parser/ast/expressions.go
  - tests/integrationtest/r/executor/aggregate.result
  - tests/integrationtest/t/executor/aggregate.test
  PR Summary: This is an automated cherry-pick of #62751 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #63558: planner: fix the old only full group check should be case-insensitive. (#62751)
  URL: https://github.com/pingcap/tidb/pull/63558
  State: open
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/parser
  Sample Changed Files:
  - pkg/parser/ast/expressions.go
  - tests/integrationtest/r/executor/aggregate.result
  - tests/integrationtest/t/executor/aggregate.test
  PR Summary: This is an automated cherry-pick of #62751 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
