# Issue #55551: CTE hang or result wrong when multiple Apply is used

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/55551
- Status: closed
- Type: type/bug
- Created At: 2024-08-21T04:23:05Z
- Closed At: 2024-08-22T05:15:21Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-6.6, affects-7.0, affects-7.1, affects-7.2, affects-7.3, affects-7.4, affects-7.5, affects-7.6, affects-8.0, affects-8.1, affects-8.2, affects-8.3, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #55553: planner: fix CTE hang or wrong result when multiple Apply is used
  URL: https://github.com/pingcap/tidb/pull/55553
  State: closed
  Merged At: 2024-08-22T05:15:19Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/rule_decorrelate.go
  - tests/integrationtest/r/cte.result
  - tests/integrationtest/t/cte.test
  PR Summary: What problem does this PR solve? Problem Summary: is used to find all correlated columns which is inside CTE definition and its corresponding Apply is outside of CTE definition. Check the following diagram,  should **NOT** return , because 's corresponding Apply is , which is inside CTE definition. Why need : For those CTE whose result of  is not empty, we need to re-compute the definition of CTE. What changed and how does it work?
- Fix PR #55643: planner: fix CTE hang or wrong result when multiple Apply is used (#55553)
  URL: https://github.com/pingcap/tidb/pull/55643
  State: closed
  Merged At: 2024-09-04T02:58:22Z
  Changed Files Count: 3
  Main Modules: cmd/explaintest, planner/core
  Sample Changed Files:
  - cmd/explaintest/r/cte.result
  - cmd/explaintest/t/cte.test
  - planner/core/rule_decorrelate.go
  PR Summary: This is an automated cherry-pick of #55553 What problem does this PR solve? Problem Summary: is used to find all correlated columns which is inside CTE definition and its corresponding Apply is outside of CTE definition. Check the following diagram,  should **NOT** return , because 's corresponding Apply is , which is inside CTE definition. Why need : For those CTE whose result of  is not empty, we need to re-compute the definition of CTE.
- Fix PR #56200: planner: fix CTE hang or wrong result when multiple Apply is used (#55553)
  URL: https://github.com/pingcap/tidb/pull/56200
  State: closed
  Merged At: 2024-09-25T08:04:14Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/rule_decorrelate.go
  - tests/integrationtest/r/cte.result
  - tests/integrationtest/t/cte.test
  PR Summary: This is an automated cherry-pick of #55553 What problem does this PR solve? Problem Summary: is used to find all correlated columns which is inside CTE definition and its corresponding Apply is outside of CTE definition. Check the following diagram,  should **NOT** return , because 's corresponding Apply is , which is inside CTE definition. Why need : For those CTE whose result of  is not empty, we need to re-compute the definition of CTE.
- Fix PR #56261: planner: fix CTE hang or wrong result when multiple Apply is used (#55553)
  URL: https://github.com/pingcap/tidb/pull/56261
  State: closed
  Merged At: 2024-10-12T05:11:28Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/rule_decorrelate.go
  - tests/integrationtest/r/cte.result
  - tests/integrationtest/t/cte.test
  PR Summary: This is an automated cherry-pick of #55553 What problem does this PR solve? Problem Summary: is used to find all correlated columns which is inside CTE definition and its corresponding Apply is outside of CTE definition. Check the following diagram,  should **NOT** return , because 's corresponding Apply is , which is inside CTE definition. Why need : For those CTE whose result of  is not empty, we need to re-compute the definition of CTE.
- Fix PR #56263: planner: fix CTE hang or wrong result when multiple Apply is used (#55553)
  URL: https://github.com/pingcap/tidb/pull/56263
  State: closed
  Merged At: 2024-11-06T11:26:09Z
  Changed Files Count: 3
  Main Modules: cmd/explaintest, planner/core
  Sample Changed Files:
  - cmd/explaintest/r/cte.result
  - cmd/explaintest/t/cte.test
  - planner/core/rule_decorrelate.go
  PR Summary: This is an automated cherry-pick of #55553 What problem does this PR solve? Problem Summary: is used to find all correlated columns which is inside CTE definition and its corresponding Apply is outside of CTE definition. Check the following diagram,  should **NOT** return , because 's corresponding Apply is , which is inside CTE definition. Why need : For those CTE whose result of  is not empty, we need to re-compute the definition of CTE.
- Fix PR #56265: planner: fix CTE hang or wrong result when multiple Apply is used (#55553)
  URL: https://github.com/pingcap/tidb/pull/56265
  State: closed
  Merged At: 2024-11-06T10:32:45Z
  Changed Files Count: 3
  Main Modules: cmd/explaintest, planner/core
  Sample Changed Files:
  - cmd/explaintest/r/cte.result
  - cmd/explaintest/t/cte.test
  - planner/core/rule_decorrelate.go
  PR Summary: This is an automated cherry-pick of #55553 What problem does this PR solve? Problem Summary: is used to find all correlated columns which is inside CTE definition and its corresponding Apply is outside of CTE definition. Check the following diagram,  should **NOT** return , because 's corresponding Apply is , which is inside CTE definition. Why need : For those CTE whose result of  is not empty, we need to re-compute the definition of CTE.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
