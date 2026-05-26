# Target Contract

Use this reference to turn an open-ended improvement request into a loop that Codex can execute and stop.

## Required Fields

Every loop needs these fields before editing code:

| Field | Purpose |
| --- | --- |
| Goal | Names the improvement in one sentence. |
| Scope | Names files, globs, packages, or modules Codex may edit. |
| Metric | Names the numeric value to optimize. |
| Direction | States `higher_is_better` or `lower_is_better`. |
| Verify | Runs locally and prints a parseable number for the metric. |
| Guard | Runs locally and protects behavior that must keep passing. |
| Iterations | Sets a bounded integer by default. |
| Stop | Names the success threshold, plateau condition, or budget limit. |

If any required field is missing, infer the safe parts from the repo, then ask only for the missing piece that materially changes the loop.

## Contract Template

```text
Goal: <specific outcome>
Scope: <editable files or globs>
Metric: <metric name and numeric extractor>
Direction: higher_is_better | lower_is_better
Verify: <shell command that exits 0 and prints a number>
Guard: <shell command that must keep passing, or none>
Iterations: <integer>
Stop: <target threshold, plateau rule, or budget>
Artifacts: clean_on_success | retain
```

Use `Artifacts: clean_on_success` unless the user asks to preserve logs, charts, traces, or intermediate data.

## Planning Flow

1. Read the repo instructions and relevant project files.
2. Identify the smallest editable scope that can affect the goal.
3. Choose a metric that can be computed repeatedly without subjective judgment.
4. Dry-run the verify command before the first edit.
5. Dry-run the guard command when present.
6. Present the contract before running the loop when the user has not provided all fields inline.

## Good Targets

- Reduce failing test count from 12 to 0.
- Improve coverage from 72.4 to 80.0 or higher.
- Reduce bundle size by at least 5 percent while keeping the build green.
- Lower p95 latency in a local benchmark while keeping correctness tests green.

## Weak Targets

Convert weak targets into a better contract before looping:

- "Make this better" needs a concrete metric.
- "Refactor everything" needs a narrow scope and guard.
- "Improve UX" needs a measurable proxy, screenshot acceptance, or a human review checkpoint.
- "Run until done" needs a bounded iteration cap or threshold.
