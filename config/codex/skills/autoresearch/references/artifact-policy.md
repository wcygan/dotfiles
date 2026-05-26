# Artifact Policy

Use this reference whenever the autoresearch loop creates, reads, or deletes run files.

## Artifact Location

Create temporary artifacts under:

```text
.autoresearch/runs/<YYYYMMDD-HHMMSS>-<slug>/
```

Typical files:

```text
target.txt
iterations.tsv
baseline.json
evals-summary.md
patches/
logs/
```

Keep artifacts out of commits unless the user explicitly asks to preserve a run.

## Cleanup Rule

Clean up autoresearch artifacts after successful completion.

Successful completion means:

- the target contract stopping rule is met, or
- the bounded iteration budget completes with at least one kept improvement and all final guards pass, or
- `$autoresearch evals` finishes reading prior artifacts and produces the requested answer.

Before cleanup, capture the useful summary in the final response: baseline, final metric, kept changes, final validation command, and any follow-up recommendation.

## Retention Rule

Keep artifacts when:

- the run is blocked, failed, or interrupted
- the user asks to inspect logs
- verify or guard behavior is flaky
- a rollback conflict needs diagnosis
- the loop produced no kept improvement

When retaining artifacts, report the path and the one command or file to inspect first.

## Cleanup Scope

Delete only artifacts created by the current autoresearch run. Do not remove unrelated `.autoresearch` runs unless the user asks for a cleanup sweep.

Use `$uv-scripts` for any reusable cleanup helper. For one-off cleanup, use simple shell commands after verifying the target path is inside `.autoresearch/runs/`.

## Final Response After Cleanup

State that run artifacts were cleaned and include the result summary. Do not claim that logs remain available after deleting them.
