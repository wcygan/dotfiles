# Evaluation Design

Build an evaluation that measures whether Pi can apply reusable rules, not
whether it can recognize memorized wording.

## Manifest ownership

Keep the manifest, answer key, rendered prompts, JSONL logs, and skill
checkpoints in a temporary runtime directory outside the target repository.
Only the controller reads the `answer` and optional `rule` fields.

Each case uses this shape:

```json
{
  "id": "D01",
  "split": "dev",
  "question": "Which route is correct?",
  "choices": {
    "A": "First option",
    "B": "Second option",
    "C": "Third option",
    "D": "Fourth option"
  },
  "answer": "C",
  "rule": "Controller-only explanation of the expected rule.",
  "required_reads": ["references/rules.md"]
}
```

`split` should be `dev`, a focused `dev-*` subtype such as `dev-hard`,
`dev-exposed`, `holdout`, or `certification`. `dev-exposed` identifies former
certification cases that were observed before a later skill edit. Case IDs and
letter positions must not appear in the target Pi skill.

Run `scripts/validate-eval-manifest.mjs` before the baseline and before every
freeze. It checks IDs, choices, answer labels, splits, required-read paths, and
certification answer balance, then prints the manifest fingerprint.

## Evaluation classes

Use three separate classes:

1. **Baseline:** no target skill and normally no tools.
2. **Forced:** explicit skill path, slash expansion, and an instruction naming
   the skill.
3. **Natural:** ordinary discovery with evidence that Pi read the target
   `SKILL.md`.

Do not compare scores from different providers, model IDs, tool boundaries,
thinking levels, prompt templates, or repository revisions as if they were the
same experiment.

Also record whether the configured model supports reasoning. If reasoning is
declared disabled or cannot be verified, medium/high results are separate
observed settings, not evidence that one setting caused deeper reasoning. Use
repeated development probes when the comparison itself matters.

## Question construction

Simple procedural skills usually need 5–10 cases. Complex skills need 10–25.
Cover:

- direct routing and terminology;
- multi-step or compositional decisions;
- exceptions and precedence;
- safety and state boundaries;
- exact path or format distinctions;
- negative cases where no action is appropriate;
- plausible but subtly incorrect distractors; and
- transfer to wording not used by the skill.

Balance answer positions without making them mechanically predictable. Do not
show a sample answer object whose placeholder letters are all the same.

## Independent items and batches

Primary certification uses one case per fresh `--no-session` invocation. This
prevents earlier answers, position patterns, or context load from contaminating
later cases.

After independent evaluation, use a batch as a secondary stress test for:

- long-context retrieval;
- reference-selection discipline;
- answer-letter transcription;
- cross-question interference; and
- output-schema compliance.

Report independent and batch scores separately.

## Holdout integrity

Freeze the certification set before the final skill changes. Do not inspect a
failure, update the skill, rerun the same case, and call the result a holdout
pass. Once observed, that case is development data.

Certification is one transaction across every required thinking level:

1. validate the manifest;
2. hash the full manifest and target skill package;
3. record project state, provider, model, Pi version, and thinking levels;
4. run every case at every level without exposing intermediate scores;
5. verify the lock before and after each invocation; and
6. reveal the aggregate only after the transaction finishes.

After tuning on any certification result:

1. move every observed case into `dev-exposed`;
2. create a new unseen certification set;
3. freeze the skill;
4. run each new case exactly once per required thinking level; and
5. make no further edits before recording the certification result.

## Saturation

A development set needs harder cases before teaching when either level reaches
90%, fewer than three cases expose a capability gap, or most misses are
formatting-only. It is fully saturated when both required thinking levels meet
the declared accuracy threshold, activation is perfect, and remaining failures
do not expose a new capability gap.

Increase difficulty by adding new behaviors and interactions, not by merely
rephrasing answers already encoded in the skill. Preserve old cases as
regressions.

## Scoring dimensions

Track at least:

- skill activation;
- required reference reads;
- answer correctness;
- exact answer schema;
- strict JSON-only formatting;
- tool or permission violations; and
- evaluator health.

A tolerant JSON extractor may score semantic correctness while strict formatting
fails. Keep both results visible.

## Cost-aware funnel

Estimate invocations before starting:

```text
baseline cases x thinking levels
+ focused reruns per edit cycle
+ milestone regressions
+ certification cases x thinking levels
+ optional discovery and batch probes
```

Use affected cases for narrow edits. Run full development regressions after
broad changes and before certification/final acceptance. This preserves causal
evidence without repeating the most expensive suite after every small wording
change.
