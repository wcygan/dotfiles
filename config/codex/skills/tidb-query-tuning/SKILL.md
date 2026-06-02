---
name: tidb-query-tuning
description: Diagnose and optimize slow TiDB queries using optimizer hints, session variables, join strategy selection, subquery optimization, and index tuning. Use when a query is slow, produces a bad plan, or needs performance guidance on TiDB.
---

# TiDB Query Tuning

Use this skill to diagnose and resolve TiDB query performance issues. It follows a rigorous workflow from symptom identification to verified solution.

---

## Workflow

1. **Capture the current plan & clues:**
   - Run `EXPLAIN ANALYZE <query>` to get actual execution stats.
   - Compare `estRows` vs `actRows` — large divergence means stale or missing statistics.
   - Note the most expensive operators (wall time, memory, rows processed).
   - **Use PLAN REPLAYER**: Run `PLAN REPLAYER DUMP EXPLAIN [ANALYZE] <query>;` to export comprehensive on-site information (version, config, stats, plan) to a ZIP file.
   - **Use Debug API**: Use TiDB HTTP API (port 10080) to pull runtime info: `/debug/pprof`, `/stats/dump/{db}/{table}`, or `/schema/{db}/{table}`.
   - **Check Bindings**: Run `SHOW GLOBAL BINDINGS;` to see if existing plan baselines are affecting the query.

2. **Check statistics health:**
   - `SHOW STATS_HEALTHY WHERE Db_name = '<db>' AND Table_name = '<table>';`
   - If health < 80 or `actRows` diverges significantly from `estRows`, run `ANALYZE TABLE <table>;` (or with `ALL COLUMNS` if `@@tidb_analyze_column_options` is not `ALL`) and re-check the plan.
   - For specific indexes: `ANALYZE TABLE <table> INDEX <index_name>;`

3. **Identify the bottleneck pattern:**
   - **Bad join order or strategy** → see `references/join-strategies.md`
   - **`IndexJoin`/`IndexHashJoin` picked the wrong probe index** → see `references/join-strategies.md`, `references/index-selection.md`, and `references/slow-plan-optimization/cases/use-correct-probe-index-for-index-join.md`
   - **Subquery not handled well** → see `references/subquery-optimization.md`
   - **Wrong or missing index** → see `references/index-selection.md`
   - **Optimizer choosing a suboptimal plan despite good stats** → see `references/optimizer-hints.md` and `references/session-variables.md`
   - **Stats are stale or auto analyze cannot keep up** → see `references/stats-health-and-auto-analyze.md`
   - **Plans change after restart or sync stats loading times out** → see `references/stats-loading-and-startup.md`
   - **Need to tune analyze version, column coverage, or memory-heavy stats collection** → see `references/stats-version-and-analyze-configuration.md`
   - **Need a matching field incident, workaround, or fixed-version precedent** → search `references/optimizer-oncall-experiences-redacted/`
   - **Need recent customer issue precedents with linked PRs and merge timestamps** → search `references/tidb-customer-planner-issues/`

4. **Reproduce & Investigate locally:**
   - **Local Reproduction**: Use `tiup playground` and `PLAN REPLAYER LOAD` to reproduce the issue locally. See `references/plan-replayer-testing.md`.
   - **Test Versions**: Verify the fix in newer stable versions or `nightly`.
   - **Deep Code Analysis**: If the cause is still unclear, clone `pingcap/tidb` and analyze the source code. **Read AGENTS.md and .agents/skills in the TiDB repo first.**

5. **Apply the fix:**
   - Prefer the least invasive change: refresh stats → add index → SQL Binding → hint → session variable.
   - **SQL Binding**: Fix plans without code changes: `CREATE GLOBAL BINDING FOR <stmt> USING <hinted_stmt>;`.
   - **Validate index-based join probe paths**: When the plan uses `IndexJoin` or `IndexHashJoin`, inspect the probe-side `access object`, pushed conditions, and whether the path is covering. Do **not** assume the chosen probe index is correct just because the join type is index-based. If another existing index better matches join keys, selective filters, or covering needs, compare it with `USE_INDEX`/`IGNORE_INDEX` and stabilize the winner with a hint or SQL binding.
   - **Binding cleanup safety**: TiDB currently has no batch-delete API for global bindings. Do **not** run `DELETE` on `mysql.bind_info` directly. Use `DROP GLOBAL BINDING ...` for each target binding instead.
   - **If direct delete was already executed**: `ADMIN RELOAD BINDINGS` may still leave stale entries in the in-memory binding cache. In this case, restart the TiDB server to fully clear and rebuild binding cache state.
   - See `references/optimizer-oncall-experiences-redacted/direct-delete-bind-info-leaves-stale-binding-cache.md` for a full reproduction and recovery checklist.
   - **Hints & Variables**: Use hints when the fix is query-specific; use session variables when it applies to a workload pattern.
   - **Bug Report**: If it's a confirmed bug, follow the workflow in `references/bug-report.md`. **Anonymize all sensitive data** before reporting.

6. **Verify the improvement:**
   - Re-run `EXPLAIN ANALYZE` with the fix applied.
   - Confirm `actRows` and execution time improved.
   - If the fix is a hint, document it in a SQL comment so future readers understand why.

## High CPU Workflow

When the customer reports high TiDB CPU usage, use the following workflow before jumping to optimizer conclusions:

0. Treat `clinic-api` as the default entry point. If `clinic-api` is unavailable, require the user to provide the equivalent raw evidence first, including CPU profiles, query history, plans, TopSQL, statement summary, and slow query samples.
1. Define both the problematic time window and a comparable non-problematic baseline window. The baseline should preferably be from the same time-of-day pattern. Pull many TiDB CPU profiles for both sides, ideally around 50 profiles in total if the incident duration allows it.
2. Compare the problem-window and baseline CPU profiles to identify which stacks or functions consume materially more time during the incident.
3. Work backward from the hot stacks and infer what query or plan patterns could produce them. Consider optimizer, executor, compiler, GC, memory tracking, range building, and internal SQL paths instead of assuming all CPU comes from user SQL.
4. Check TopSQL, statement summary, and slow query records in the same time window. Collect the candidate SQLs and their plans, and include internal SQL in the candidate set.
5. Build a minimal candidate query set that best explains the observed CPU symptom. Use correlation analysis, principal-component style reduction, or combinational optimization to find the smallest query combination that remains highly correlated with the incident signal.
6. Compare candidate queries against the observed symptom shape. For example, CPU spikes may correlate better with GC pressure, compiler duration, plan building, or execution hot loops than with raw query count alone. Check correlation, periodicity, and dispersion instead of relying only on top-N totals.
7. Do not treat any candidate as the final conclusion until it is statistically validated and cross-validated across multiple evidence sources. The conclusion must be supported by the incident-vs-baseline profile comparison and must also be consistent with flame graphs, TopSQL, slow query, and statement summary observations.
8. If the candidate set does not explain the symptom with high confidence, or the evidence sources do not validate each other, go back to step 1, expand the profiling sample set, and repeat the comparison with a better baseline or a narrower incident slice.

Use this workflow to decide whether the next step should be query tuning, plan inspection, stats diagnosis, internal SQL investigation, or a product bug report.

## High-signal rules

- **Always check stats first.** Most bad plans in TiDB come from stale or missing statistics, not optimizer bugs.
- **Treat stats maintenance as capacity planning.** If `AUTO ANALYZE` cannot keep up with stats decay, plan quality will drift even when SQL does not change.
- **`EXPLAIN ANALYZE` is the ground truth.** `EXPLAIN` alone shows estimates; `ANALYZE` shows what actually happened.
- **Search known field cases before inventing a new workaround.** The oncall corpus under `references/optimizer-oncall-experiences-redacted/` is useful for symptom matching, investigation signals, and fix-version lookup.
- **Search recent GitHub issue precedents when fix lineage matters.** The corpus under `references/tidb-customer-planner-issues/` is useful when you need linked PRs, merge times, and still-open customer gaps.
- **High CPU conclusions require statistical validation and cross-source confirmation.** Do not stop at a plausible stack or top SQL. Treat the result as final only when the signal is statistically supported and mutually validated by profiles or flame graphs, TopSQL, slow query, and statement summary.
- **Correlated subqueries:** TiDB decorrelates by default. When the subquery is well-indexed and the outer query is selective, `NO_DECORRELATE()` often wins. See `references/subquery-optimization.md`.
- **Join strategies matter:** TiDB supports hash join, index join, merge join, and shuffle joins. The right choice depends on table sizes, index availability, and data distribution. See `references/join-strategies.md`.
- **Join type and probe index are separate checks:** `IndexJoin` and `IndexHashJoin` can still be slow because the optimizer picked the wrong inner probe index. Always inspect the probe-side `access object`, pushed predicates, and whether another existing index better matches join keys and covering needs.
- **Hints are per-query; variables are per-session/global.** Use hints for surgical fixes, variables for workload-wide tuning.
- **TiDB currently has no batch-delete API for global bindings.** Do not delete rows from `mysql.bind_info` directly; use `DROP GLOBAL BINDING` instead.
- **If `mysql.bind_info` was modified directly and reload does not clear bindings, restart TiDB.** `ADMIN RELOAD BINDINGS` might not fully remove stale in-memory binding cache entries after direct table deletes.
- **TiFlash acceleration:** For analytical queries on large tables, push computation to TiFlash replicas using `READ_FROM_STORAGE(TIFLASH[<table>])`. See `references/session-variables.md`.
- **Anonymize sensitive info.** Before reporting bugs, ensure table names, columns, and data are anonymized.
- **Reproduce before suggesting upgrades.** Use TiUP playground to verify if a newer version actually fixes the issue.

## References

- `references/slow-plan-optimization/guide.md` — Slow-plan optimization sub-module with workflow, guardrails, and case catalog.
- `references/clues.md` — Detailed SQLs and metrics for clue collection.
- `references/reproduction.md` — Baseline investigation and known version issues.
- `references/plan-replayer-testing.md` — Local reproduction using TiUP and PLAN REPLAYER.
- `references/bug-report.md` — Standard bug report template and anonymization workflow.
- `references/optimizer-hints.md` — Optimizer hints: syntax, catalog, and when to use each.
- `references/session-variables.md` — Session/global variables that affect plan choice.
- `references/join-strategies.md` — Join algorithms, when TiDB picks each, and how to override.
- `references/subquery-optimization.md` — Decorrelation, semi-join, EXISTS/IN patterns and NO_DECORRELATE.
- `references/index-selection.md` — Index hints, invisible indexes, index advisor, composite index guidance.
- `references/slow-plan-optimization/cases/use-correct-probe-index-for-index-join.md` — Validate and fix wrong probe-index selection for `IndexJoin` and `IndexHashJoin`.
- `references/explain-patterns.md` — Reading EXPLAIN ANALYZE output to identify bottlenecks.
- `references/stats-health-and-auto-analyze.md` — Statistics health, auto analyze backlog diagnosis, and safe concurrency tuning.
- `references/stats-loading-and-startup.md` — Init stats, sync load, restart-time plan instability, and version-based mitigation.
- `references/stats-version-and-analyze-configuration.md` — Stats versioning, analyze coverage, and memory-safe stats collection settings.
- `references/optimizer-oncall-experiences-redacted/` — Redacted optimizer oncall case corpus with user symptoms, investigation signals, workarounds, and fixed versions.
- `references/tidb-customer-planner-issues/README.md` — Generated GitHub issue corpus with one file per customer-driven planner issue, including linked PRs and merge timestamps.

## Scripts

- `scripts/collect_diag_info.sql` — SQL script to collect baseline tuning metadata.
