# TiFlash Cop Overload Without MPP

## User Symptom
- TiFlash CPU or cop latency spikes during fixed time windows.
- High-frequency read traffic becomes unstable even though query latency may not look catastrophic at first.

## Investigation Signals
- The plan uses `cop[tiflash]` instead of `mpp[tiflash]` or a TiKV path.
- `tidb_enable_tiflash_cop` is enabled.
- TiFlash monitoring shows cop pressure rather than a balanced MPP workload.

## Workaround
- Prefer MPP for analytical traffic when possible.
- Consider turning off `tidb_enable_tiflash_cop` for workloads that bombard TiFlash with high-frequency cop requests.
- Avoid routing point-like or high-frequency OLTP traffic to TiFlash.

## Fixed Version
- No general product fix was identified. This is mainly a workload-to-engine mismatch.
