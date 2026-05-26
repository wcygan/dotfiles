# Core Loop

Use this reference when executing `$autoresearch loop`.

## Baseline

1. Create a temporary run artifact directory as described in `artifact-policy.md`.
2. Save the target contract.
3. Run the verify command.
4. Parse the baseline metric.
5. Run the guard command when present.
6. Record iteration `0` as the baseline.

## Iteration Phases

For each iteration:

1. **Review**: read the last run rows, current best metric, and recent diffs or experiment commits.
2. **Hypothesize**: choose one focused change that can plausibly improve the metric.
3. **Modify**: edit only files inside the scope.
4. **Checkpoint**: create an experiment commit or patch snapshot according to `git-safety.md`.
5. **Verify**: run the verify command and parse the new metric.
6. **Guard**: run the guard command when present.
7. **Decide**: keep only if the metric improves in the configured direction and the guard passes.
8. **Rollback**: revert the current experiment change when verify, guard, parsing, or metric direction fails.
9. **Log**: append the outcome, metric, delta, status, and short rationale.

## Status Values

Use these run statuses consistently:

| Status | Meaning |
| --- | --- |
| `baseline` | Initial metric before changes. |
| `keep` | Metric improved and guard passed. |
| `discard` | Metric regressed or failed to improve. |
| `guard-failed` | Metric improved but guard failed. |
| `verify-failed` | Verify command failed. |
| `metric-error` | Verify output did not parse to a number. |
| `no-op` | No coherent change was made. |
| `blocked` | Safety, repo state, or missing context stopped the run. |

## Stopping Rules

Stop when:

- The success threshold is reached.
- The bounded iteration count is exhausted.
- Three eval checkpoints recommend stopping for plateau.
- The guard exposes a real regression that needs human direction.
- Scope conflicts with user edits or files outside the contract.

## Finalization

On successful completion:

1. Capture the final metric, best iteration, kept changes, and validation commands in the final response.
2. Run the broadest relevant guard for the changed scope.
3. Clean run artifacts according to `artifact-policy.md`.

On blocked, failed, or interrupted completion:

1. Keep run artifacts.
2. Report the artifact path.
3. Summarize the exact reason the loop stopped and what can resume it.
