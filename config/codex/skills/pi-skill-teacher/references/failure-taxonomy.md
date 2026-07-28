# Failure Taxonomy

Classify the observed failure before editing the target Pi skill.

| Failure | Evidence | Bounded response |
| --- | --- | --- |
| Invocation | Forced JSONL lacks the expanded skill marker | Fix command construction or skill name; do not change domain content |
| Natural discovery | Pi never reads the intended `SKILL.md` | Verify trust/catalog and description once; then record the routing limitation and use forced activation unless discovery is required |
| Reference routing | Skill expands but required focused references are not read | Make the router's first action and relative paths explicit |
| Retrieval | Required reference is read but the relevant rule is not used | Improve headings, focus, contrast, or decision tables |
| Reasoning | Pi applies a retrieved rule incorrectly | Add a general decision procedure or contrasting example |
| Answer mapping | Reasoning names the right option text but emits another letter | Add the rule-to-text-to-letter audit or use a deterministic helper |
| Schema | Correct choice appears with missing/extra IDs or invalid JSON | Tighten output instructions and score schema separately |
| Strict format | Correct JSON is fenced or surrounded by prose | Track separately; make it a hard gate only when required |
| Batch interference | Independent items pass while a batch fails | Keep independent certification primary; reduce or route batch context |
| Evaluator | Scorer reports a miss inconsistent with the JSONL evidence | Repair and baseline the evaluator before changing the Pi skill |
| Runtime | Pi exits nonzero or produces no final assistant message | Preserve stderr and exit status; classify separately from domain knowledge and do not silently retry certification |
| Certification drift | Manifest, skill, project state, runtime identity, or thinking levels differ from the lock | Invalidate the transaction and freeze again before any new certification |
| Permission | Pi invokes an unauthorized tool or mutation | Tighten the tool allowlist and stop for any new authority |

## Diagnosis order

Use this order because later layers depend on earlier ones:

```text
evaluator health
-> runtime completion
-> certification drift
-> invocation
-> natural discovery when applicable
-> reference routing
-> retrieval
-> reasoning
-> answer mapping
-> schema
-> strict formatting
```

Change only one coherent layer per cycle. If a scorer bug is found, rescore the
unchanged log and record the correction; do not count it as model improvement.

## Plateau

After two non-improving cycles, pivot to a meaningfully different strategy
inside scope, such as:

- split an overloaded reference;
- replace prose with a decision table;
- add a deterministic helper for mechanical work;
- change from batches to independent items; or
- add a general counterexample.

Stop at the declared patience threshold. Never expose the hidden key, weaken the
scorer, remove difficult cases, or redefine success to manufacture progress.
