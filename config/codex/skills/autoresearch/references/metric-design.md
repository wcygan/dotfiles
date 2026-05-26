# Metric Design

Use this reference when designing the metric, verify command, guard command, or parsing strategy.

## Metric Requirements

A loop metric must be:

- Numeric.
- Repeatable on the local machine.
- Cheap enough for the requested iteration count.
- Sensitive to the scoped changes.
- Parsed by a clear extractor.
- Paired with a direction: `higher_is_better` or `lower_is_better`.

If the metric is noisy, run the baseline more than once and record the range before deciding whether an iteration improved.

## Verify Command

The verify command should exit 0 and print one parseable number. Prefer commands that already exist in the repo.

Examples:

```sh
npm test -- --coverage | awk '/All files/ { gsub("%", "", $10); print $10 }'
pytest --cov --cov-report=term | awk '/TOTAL/ { gsub("%", "", $4); print $4 }'
cargo test --workspace 2>&1 | scripts/count_failures.sh
```

Screen verify commands before running them. Block commands that include destructive filesystem operations, fetch-and-execute pipelines, embedded credentials, production writes, or unbounded process creation.

## Guard Command

The guard protects behavior that the metric does not capture. Good guards include:

```sh
npm test
npm run build
cargo test --workspace
go test ./...
make test-pre
```

Use a narrower guard for fast inner loops and a broader guard before final success.

## Metric Extractors

Prefer shell pipelines for simple extraction. Use `$uv-scripts` when extraction needs structured parsing, TSV/JSONL analysis, statistical smoothing, report generation, or cleanup. A reusable extractor should use `uv run --script` with PEP 723 metadata.

## Improvement Decision

For `higher_is_better`, keep an iteration when `new_metric > previous_best` and guard passes.

For `lower_is_better`, keep an iteration when `new_metric < previous_best` and guard passes.

For noisy metrics, define a minimum improvement threshold in the target contract.
