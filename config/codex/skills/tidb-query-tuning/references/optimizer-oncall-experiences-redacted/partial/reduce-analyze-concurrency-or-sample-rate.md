# Reduce Analyze Concurrency or Sample Rate

## Status
- Partial
- Confidence: Medium

## User Symptom
- Analyze jobs are extremely slow, repeatedly killed, or create visible CPU pressure.

## When To Use
- Goroutine or profile evidence points to analyze execution itself as the hot path.
- Partition count is high, or the table is very large.
- The cluster is already sensitive to background system load.

## When Not To Use
- The real incident is stale stats on a hot table and lowering concurrency would only delay recovery.
- The current problem is not analyze runtime but analyze correctness.
- There is no evidence that analyze is the main pressure source.

## Risks
- Lower concurrency or sample rate improves stability at the cost of slower stats convergence and potentially lower stats quality.

## Missing Evidence
- The handbook suggests this repeatedly, but does not provide a stable rule for how far to reduce concurrency or sample rate under different table sizes.
