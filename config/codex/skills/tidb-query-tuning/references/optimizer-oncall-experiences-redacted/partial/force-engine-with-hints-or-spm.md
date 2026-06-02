# Force Engine With Hints or SPM

## Status
- Partial
- Confidence: Medium

## User Symptom
- One SQL is consistently routed to the wrong engine or wrong access path and causes localized latency or storage pressure.

## When To Use
- The problem is concentrated in a small number of SQLs.
- Engine-specific metrics clearly show one path is materially better than the other.
- You need a contained mitigation without changing global cost behavior.

## When Not To Use
- The root cause is still unknown.
- A stale global binding may already be masking the real behavior.
- The same SQL shape appears in many variants, making one-off hinting fragile.

## Risks
- Hints and bindings can fossilize a plan that becomes wrong after later data or schema changes.
- Forcing an engine can hide a product bug that still needs follow-up.

## Missing Evidence
- The handbook has several successful examples, but usually does not spell out the rollback criteria for removing the hint or binding later.
