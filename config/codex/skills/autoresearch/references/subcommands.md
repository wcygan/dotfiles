# Subcommands

Use this reference to map `$autoresearch` invocations to the right behavior.

## `$autoresearch plan`

Use when the user has a goal but not a complete target contract.

Output:

- proposed scope
- metric and direction
- verify command
- guard command
- iteration count
- stopping rule
- ready-to-run `$autoresearch loop` block

Dry-run verify and guard commands when safe before presenting the final contract.

## `$autoresearch loop`

Use when the target contract is complete or can be completed with low-risk inference.

Follow:

- `target-contract.md`
- `git-safety.md`
- `metric-design.md`
- `core-loop.md`
- `artifact-policy.md`

## `$autoresearch fix`

Use for error-count reduction loops: tests, type checks, lint, or build failures.

Default contract:

```text
Metric: error count
Direction: lower_is_better
Verify: <target command that reports failures>
Guard: <broader test/build command when available>
Stop: zero errors or iteration cap
```

Fix one error category or failure at a time. Keep the scope tied to error locations unless the user expands it.

## `$autoresearch debug`

Use for hypothesis-driven investigation where the first metric may be "confirmed failing cases remaining".

Prefer read-only reproduction and instrumentation before code edits. Convert the investigation into `$autoresearch fix` once the failing cause is known.

## `$autoresearch evals`

Use for analyzing existing run artifacts. Load `evals.md`, inspect the requested TSV or JSONL, produce the requested summary, and clean temporary eval artifacts on success.

## Future Modes

Add modes such as `security`, `learn`, `reason`, or `ship` only after the core loop proves useful. Keep each mode as a focused reference file instead of expanding `SKILL.md`.
