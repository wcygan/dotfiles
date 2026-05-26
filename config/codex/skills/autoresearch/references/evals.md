# Evals

Use this reference for `$autoresearch evals` and for checkpoint analysis during a loop.

## Run Log Shape

Use TSV or JSONL. TSV is enough for most loops:

```text
# metric_direction: higher_is_better
iteration	timestamp	commit	metric	delta	guard	status	description
0	2026-05-25T16:00:00Z	-	72.4	0	pass	baseline	initial state
```

Use `$uv-scripts` for parsing, summarizing, charting, or transforming run logs when shell tools would make the analysis brittle.

## Checkpoint Summary

At each checkpoint, report:

- starting metric to current metric
- kept, discarded, and failed counts
- best iteration and biggest regression
- trend: improving, flat, or worsening
- recommendation: continue, change strategy, broaden guard, or stop

Keep checkpoint output short during active loops.

## Plateau Detection

Recommend stopping when:

- Three consecutive checkpoints show no meaningful improvement.
- Revert or discard rate stays above 80 percent after at least five iterations.
- The best metric has not changed after the configured patience window.
- Improvements require scope outside the target contract.

## Final Evals

The final evals summary should include:

```text
Goal:
Metric:
Baseline:
Final:
Best:
Iterations:
Kept:
Discarded:
Guard:
Recommendation:
```

If the run succeeded, summarize in the chat response and then clean artifacts. If the run failed or was interrupted, leave the eval summary in the artifact directory and report the path.
