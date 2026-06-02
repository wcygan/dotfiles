# Issue #54652: planner, txn: `select ... for update` using Plan Cache can not lock data correctly in some cases

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/54652
- Status: closed
- Type: type/bug
- Created At: 2024-07-16T03:41:29Z
- Closed At: 2024-07-17T03:18:00Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, report/customer, severity/critical, sig/planner, sig/transaction, type/bug

## Customer-Facing Phenomenon
- The second exec-statement's plan has no Lock:

## Linked PRs
- Fix PR #54661: planner: fix the issue of reusing wrong point-plan for "select ... for update"
  URL: https://github.com/pingcap/tidb/pull/54661
  State: closed
  Merged At: 2024-07-17T03:17:59Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/ddl
  Sample Changed Files:
  - pkg/ddl/tests/metadatalock/mdl_test.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/core/tests/prepare/prepare_test.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Fix PR #54680: planner: fix the issue of reusing wrong point-plan for "select ... for update" (#54661)
  URL: https://github.com/pingcap/tidb/pull/54680
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/ddl
  Sample Changed Files:
  - pkg/ddl/tests/metadatalock/mdl_test.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/core/tests/prepare/prepare_test.go
  PR Summary: This is an automated cherry-pick of #54661 What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Fix PR #54742: planner: fix the issue of reusing wrong point-plan for "select ... for update" (#54661)
  URL: https://github.com/pingcap/tidb/pull/54742
  State: closed
  Merged At: 2024-07-18T14:40:31Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/ddl
  Sample Changed Files:
  - pkg/ddl/tests/metadatalock/mdl_test.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/core/tests/prepare/prepare_test.go
  PR Summary: This is an automated cherry-pick of #54661 What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Related PR #54773: planner: Select-For-Update should skip the FastPlan
  URL: https://github.com/pingcap/tidb/pull/54773
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/BUILD.bazel
  - pkg/planner/core/casetest/plan_test.go
  - pkg/planner/core/point_get_plan.go
  - pkg/sessiontxn/txn_rc_tso_optimize_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? should skip the .
- Fix PR #54891: planner: fix the issue of reusing wrong point-plan for "select ... for update" (#54661)
  URL: https://github.com/pingcap/tidb/pull/54891
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/ddl
  Sample Changed Files:
  - pkg/ddl/tests/metadatalock/mdl_test.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/core/tests/prepare/prepare_test.go
  PR Summary: This is an automated cherry-pick of #54661 What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Fix PR #54892: planner: fix the issue of reusing wrong point-plan for "select ... for update" (#54661)
  URL: https://github.com/pingcap/tidb/pull/54892
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/planner/core, ddl/metadatalocktest
  Sample Changed Files:
  - ddl/metadatalocktest/mdl_test.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/core/tests/prepare/prepare_test.go
  PR Summary: This is an automated cherry-pick of #54661 What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Fix PR #54938: planner: fix the issue of reusing wrong point-plan for "select ... for update" (#54661)
  URL: https://github.com/pingcap/tidb/pull/54938
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/planner/core, ddl/metadatalocktest
  Sample Changed Files:
  - ddl/metadatalocktest/mdl_test.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/core/tests/prepare/prepare_test.go
  PR Summary: This is an automated cherry-pick of #54661 What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Fix PR #55123: planner: fix the issue of reusing wrong point-plan for "select ... for update" (#54661)
  URL: https://github.com/pingcap/tidb/pull/55123
  State: closed
  Merged At: not merged
  Changed Files Count: 560
  Main Modules: pkg/ddl, tests/integrationtest, pkg/disttask, pkg/executor, pkg/planner/core, pkg/lightning
  Sample Changed Files:
  - DEPS.bzl
  - WORKSPACE
  - br/OWNERS
  - br/pkg/config/kv.go
  - br/pkg/conn/BUILD.bazel
  - br/pkg/conn/conn.go
  - br/pkg/conn/conn_test.go
  - br/pkg/restore/client.go
  - br/pkg/restore/client_test.go
  - br/pkg/restore/db_test.go
  - br/pkg/restore/import.go
  - br/pkg/restore/import_retry_test.go
  - br/pkg/restore/split/mock_pd_client.go
  - br/pkg/restore/split/split.go
  - br/pkg/restore/split/split_test.go
  - br/pkg/restore/split_test.go
  - br/pkg/restore/util_test.go
  - br/pkg/storage/memstore.go
  - br/pkg/storage/storage.go
  - br/pkg/stream/stream_status.go
  PR Summary: This is an automated cherry-pick of #54661 What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Fix PR #55124: planner: fix the issue of reusing wrong point-plan for "select ... for update" (#54661)
  URL: https://github.com/pingcap/tidb/pull/55124
  State: closed
  Merged At: 2024-08-01T10:06:12Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/ddl
  Sample Changed Files:
  - pkg/ddl/tests/metadatalock/mdl_test.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/core/tests/prepare/prepare_test.go
  PR Summary: This is an automated cherry-pick of #54661 What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Fix PR #55743: planner: fix the issue of reusing wrong point-plan for "select ... for update" (#54661)
  URL: https://github.com/pingcap/tidb/pull/55743
  State: closed
  Merged At: 2024-09-05T02:04:54Z
  Changed Files Count: 6
  Main Modules: planner/core, ddl/metadatalocktest
  Sample Changed Files:
  - ddl/metadatalocktest/mdl_test.go
  - planner/core/plan_cache.go
  - planner/core/plan_cache_test.go
  - planner/core/plan_cache_utils.go
  - planner/core/plan_cache_utils_test.go
  - planner/core/prepare_test.go
  PR Summary: This is an automated cherry-pick of #54661 What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Fix PR #57239: planner: fix the issue of reusing wrong point-plan for "select ... for update" (#54661)
  URL: https://github.com/pingcap/tidb/pull/57239
  State: closed
  Merged At: 2024-11-08T09:57:46Z
  Changed Files Count: 5
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/plan_cache.go
  - planner/core/plan_cache_test.go
  - planner/core/plan_cache_utils.go
  - planner/core/plan_cache_utils_test.go
  - planner/core/prepare_test.go
  PR Summary: This is an automated cherry-pick of #54661 What problem does this PR solve? Problem Summary: planner: fix the issue of reusing wrong point-plan for "select ... for update" What changed and how does it work? Encode more txn state into the plan cache key, and check whether the key has changed before reusing point-get plans.
- Related PR #65908: planner: activate stale-read txn when autocommit=0
  URL: https://github.com/pingcap/tidb/pull/65908
  State: closed
  Merged At: 2026-02-05T03:49:54Z
  Changed Files Count: 5
  Main Modules: pkg/session
  Sample Changed Files:
  - pkg/sessiontxn/BUILD.bazel
  - pkg/sessiontxn/staleread/BUILD.bazel
  - pkg/sessiontxn/staleread/provider.go
  - pkg/sessiontxn/staleread/provider_test.go
  - pkg/sessiontxn/txn_context_test.go
  PR Summary: What problem does this PR solve? Problem Summary: When  and  is set, each  statement recalculates its own  instead of reusing the same snapshot. This causes inconsistent reads across multiple statements within what users expect to be a single transaction. What changed and how does it work? Changed  to  when  in . This triggers  in .This ensures:

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
