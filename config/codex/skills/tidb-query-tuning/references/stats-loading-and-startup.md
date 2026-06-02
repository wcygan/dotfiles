# Statistics Loading and Startup Behavior

Two stats-loading paths matter during TiDB startup and query compilation:

- **Init stats**: what TiDB loads during startup before or while serving traffic
- **Sync load**: what TiDB loads on demand during optimization when the needed histogram, TopN, or other stats objects are not fully in memory

If either path is slow or incomplete, the same SQL can get different plans before and after startup settles.

## Typical symptoms

- Query plans change shortly after TiDB restart
- The first wave of queries after restart is slower than steady-state traffic
- `EXPLAIN` shows unstable estimates during warm-up
- `Statistics -> Sync Load QPS` shows many timeouts

## Init stats evolution by version

### Before v7.1

TiDB loaded all statistics eagerly into memory during startup. On clusters with many tables, this could make startup very slow.

### v7.1: lite-init-stats

TiDB started by loading only stats metadata first, then relied on asynchronous loading for the heavier stats objects.

Trade-off:

- Faster startup
- Higher risk of plan instability during the warm-up period

### v6.5.7 and v7.1: force-init-stats

These versions added a mode that waits for stats initialization to complete before serving traffic.

Use this when:

- Startup latency is less important than predictable first-query plans
- Your workload is sensitive to plan changes immediately after restart

### v7.1.2 and v8.1: concurrently-init-stats

These versions improved startup by initializing stats concurrently, which reduces cold-start pain on clusters with many tables.

## Known fixes for startup-time plan instability

If plans jump after restart and the root cause is stats loading behavior, prefer upgrading to a release that includes the fix:

- v6.5.10
- v7.1.6
- v7.5.2
- v8.1.0

## Sync load

Sync load was introduced so the optimizer can wait briefly for complete column statistics instead of planning against partial metadata only.

### `tidb_stats_load_sync_wait`

This is the maximum time the optimizer waits for sync-loaded stats.

- Higher value: fewer stats-load timeouts, more stable planning, but longer compile latency
- Lower value: faster compile path, but higher risk of planning with incomplete stats

Use it when:

- `Sync Load QPS` shows meaningful timeout volume
- Compilation latency spikes correlate with missing stats objects

## How to diagnose sync load issues

### 1. Check the dashboard

Look at:

- `Statistics -> Sync Load QPS`

If you see many timeouts, the optimizer is frequently planning before full stats are ready.

### 2. Check the TiDB version

If the cluster is older than the fixed releases for known loading issues, upgrading is usually the cleanest fix.

### 3. Decide whether the problem is timeout budget or worker capacity

Use this split:

- **Timeouts are occasional and scattered**: increase `tidb_stats_load_sync_wait`
- **Timeouts are frequent and continuous**: increase stats-load worker capacity if the version requires manual tuning

### `stats-load-concurrency`

On versions where this is manually tuned, raise it when sync load is backlogged.

### v8.2+ adaptive behavior

In newer releases, `stats-load-concurrency = 0` enables adaptive concurrency based on CPU cores.

Implication:

- If you are already on v8.2+ and still see many sync-load timeouts, first tune `tidb_stats_load_sync_wait`
- If that is not enough, the machine may simply need more CPU or a different deployment shape

## Operational guidance

### Prefer upgrade over large startup workarounds

If you are seeing restart-time plan drift on an affected older release, upgrade before building operational complexity around it.

### Use force-init-stats only when the first queries matter more than startup latency

Examples:

- Stateful services that execute latency-sensitive SQL immediately after failover
- Planned maintenance windows where predictable warm-up is more important than the shortest restart time

### Watch startup regressions after changing stats policy

If you change:

- init-stats behavior
- sync-load wait budget
- stats-load concurrency

then validate:

- first-query latency after restart
- plan stability for the top critical queries
- TiDB CPU during warm-up

## Fast decision matrix

| Symptom | Most likely first move |
|--------|-------------------------|
| Plans change after restart on older releases | Upgrade to a fixed release |
| Sync Load timeouts are occasional | Increase `tidb_stats_load_sync_wait` |
| Sync Load timeouts are sustained | Increase stats-load worker capacity or machine CPU |
| Startup is too slow with many tables | Prefer concurrent init on newer releases |
| First queries after restart must be stable | Consider force-init-stats mode |
