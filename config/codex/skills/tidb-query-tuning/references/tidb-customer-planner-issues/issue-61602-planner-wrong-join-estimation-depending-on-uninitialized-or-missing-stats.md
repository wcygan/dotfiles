# Issue #61602: planner: wrong Join estimation depending on uninitialized or missing stats

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61602
- Status: closed
- Type: type/bug
- Created At: 2025-06-09T11:14:05Z
- Closed At: 2025-06-11T11:46:21Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, epic/cardinality-estimation, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- Root Cause: 1. In join estimation, we use . 2. When deriving NDV from index-stats, we didn't check whether it was loaded or missing. After adding a new index without analyzing, the index-stats might be missing, 3. If it's missing, we'll use the wrong  to calculate join estimation, and finally get a high error result.

## Linked PRs
- Fix PR #61604: planner: fix the wrong join estimation depending on missing or uninitialized stats
  URL: https://github.com/pingcap/tidb/pull/61604
  State: closed
  Merged At: 2025-06-11T11:46:19Z
  Changed Files Count: 5
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/stats.go
  - tests/integrationtest/r/executor/index_lookup_merge_join.result
  - tests/integrationtest/r/explain_complex.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/indexjoin.result
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix the wrong join estimation depending on missing or uninitialized stats What changed and how does it work? planner: fix the wrong join estimation depending on missing or uninitialized stats It's hard to construct test cases for this issue since it depends on stats cache's status. So I tested it locally, and this PR can work for this scenario:
- Fix PR #61673: planner: fix the wrong join estimation depending on missing or uninitialized stats (#61604)
  URL: https://github.com/pingcap/tidb/pull/61673
  State: open
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/stats.go
  - tests/integrationtest/r/executor/index_lookup_merge_join.result
  - tests/integrationtest/r/explain_complex.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/indexjoin.result
  PR Summary: This is an automated cherry-pick of #61604 What problem does this PR solve? Problem Summary: planner: fix the wrong join estimation depending on missing or uninitialized stats What changed and how does it work? planner: fix the wrong join estimation depending on missing or uninitialized stats
- Fix PR #61674: planner: fix the wrong join estimation depending on missing or uninitialized stats (#61604)
  URL: https://github.com/pingcap/tidb/pull/61674
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: tests/integrationtest, cmd/explaintest, pkg/planner/core
  Sample Changed Files:
  - cmd/explaintest/r/explain_complex.result
  - pkg/planner/core/stats.go
  - tests/integrationtest/r/executor/index_lookup_merge_join.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/indexjoin.result
  PR Summary: This is an automated cherry-pick of #61604 What problem does this PR solve? Problem Summary: planner: fix the wrong join estimation depending on missing or uninitialized stats What changed and how does it work? planner: fix the wrong join estimation depending on missing or uninitialized stats
- Fix PR #61675: planner: fix the wrong join estimation depending on missing or uninitialized stats (#61604)
  URL: https://github.com/pingcap/tidb/pull/61675
  State: open
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: tests/integrationtest, cmd/explaintest, pkg/planner/core
  Sample Changed Files:
  - cmd/explaintest/r/explain_complex.result
  - pkg/planner/core/stats.go
  - tests/integrationtest/r/executor/index_lookup_merge_join.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/indexjoin.result
  PR Summary: This is an automated cherry-pick of #61604 What problem does this PR solve? Problem Summary: planner: fix the wrong join estimation depending on missing or uninitialized stats What changed and how does it work? planner: fix the wrong join estimation depending on missing or uninitialized stats
- Fix PR #61676: planner: fix the wrong join estimation depending on missing or uninitialized stats (#61604)
  URL: https://github.com/pingcap/tidb/pull/61676
  State: closed
  Merged At: 2025-07-22T02:43:20Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/stats.go
  - tests/integrationtest/r/explain_complex.result
  PR Summary: This is an automated cherry-pick of #61604 What problem does this PR solve? Problem Summary: planner: fix the wrong join estimation depending on missing or uninitialized stats What changed and how does it work? planner: fix the wrong join estimation depending on missing or uninitialized stats
- Fix PR #61857: planner: fix the wrong join estimation depending on missing or uninitialized stats (#61604)
  URL: https://github.com/pingcap/tidb/pull/61857
  State: closed
  Merged At: 2025-07-09T09:18:42Z
  Changed Files Count: 5
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/stats.go
  - tests/integrationtest/r/executor/index_lookup_merge_join.result
  - tests/integrationtest/r/explain_complex.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/indexjoin.result
  PR Summary: This is an automated cherry-pick of #61604 What problem does this PR solve? Problem Summary: planner: fix the wrong join estimation depending on missing or uninitialized stats What changed and how does it work? planner: fix the wrong join estimation depending on missing or uninitialized stats

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
