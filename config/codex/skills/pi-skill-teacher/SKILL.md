---
name: pi-skill-teacher
description: "Teach Pi a reusable capability through an explicitly invoked evaluation loop: baseline medium and high thinking, create or refine a Pi skill, force deterministic skill loading, verify activation from JSONL events, diagnose failures, harden saturated evaluations, and certify on untouched first-attempt cases. Use with $pi-skill-teacher when a stronger controller should teach a weaker Pi model through project-local skills and multiple-choice evals."
---

# Pi Skill Teacher

Teach a fixed Pi model by improving the reusable skill context available to it.
The controller owns the answer key, skill edits, evaluation design, and final
acceptance. Pi answers bounded evaluations and never receives the hidden key.

## Required composition

Before planning or invoking Pi, read and apply these adjacent global skills
completely:

- `../pi-agent-controller/SKILL.md`
- `../pi-coding-agent/SKILL.md`
- `../loop-protocol/SKILL.md`

Use the installed `pi --help` and the current
[Pi skills documentation](https://pi.dev/docs/latest/skills) for
version-sensitive loading behavior. Stop if a required controller or safety
contract is unavailable.

## Success

Success requires all of the following:

- the intended Pi skill exists and contains reusable rules rather than eval
  answers;
- the target provider, model, thinking level, tools, and prompt shape are fixed
  and recorded;
- every forced evaluation proves that the intended skill was expanded;
- development failures are diagnosed and addressed through bounded skill
  changes;
- an untouched certification set passes on each required thinking level on the
  first independent attempt; and
- answer correctness, activation, reference use, schema, and formatting are
  reported separately.

Do not claim success from a correct answer alone.

## Establish the teaching contract

Before the first skill edit, define:

```text
Capability:
Target project:
Target Pi skill name and path:
Provider and model:
Declared reasoning support:
Thinking levels:
Tool boundary:
Baseline condition:
Development cases:
Untouched certification cases:
Natural-discovery requirement:
Maximum skill-edit cycles:
Plateau rule:
Invocation or token budget:
Runtime evidence directory:
Success thresholds:
Forbidden actions:
```

Safe defaults:

- project-local target skill at `.agents/skills/<name>/`;
- medium and high thinking;
- read-only Pi tools during evaluation;
- one question per fresh `--no-session` invocation;
- 5–10 questions for a simple procedure and 10–25 for a complex capability;
- at most 6 skill-edit cycles;
- stop after 3 cycles without measurable progress;
- estimate the maximum Pi invocations before starting;
- controller as the sole writer;
- runtime manifests, keys, logs, and checkpoints under a temporary directory;
- no commits, pushes, deployments, package installation, or external writes.

Inspect the target checkout's instructions, branch, and dirty state. Preserve
all pre-existing work and establish a checkpoint that covers only
controller-owned skill files.

## Verify Pi before evaluating

Follow `pi-agent-controller` to verify the installed CLI and intended model.
Do not treat a configured model as a running model. Fix the provider, model,
thinking level, tool allowlist, working directory, and Pi version for every
comparison.

Record whether the selected model declares or demonstrates reasoning support.
When its configuration declares reasoning disabled, describe medium and high as
requested Pi settings rather than claiming that a deeper reasoning budget caused
their score difference. Use repeated development probes before drawing causal
conclusions from noisy setting comparisons; certification remains one untouched
attempt per case and level.

Use an isolated `PI_CODING_AGENT_DIR` only for CLI discovery that would
otherwise mutate or fail against live Pi state. Never copy or print
credentials, provider secrets, `auth.json`, or command-backed headers.

## Design the evaluation

Read [evaluation-design.md](references/evaluation-design.md) before creating
cases. Start from [eval-manifest.example.json](assets/eval-manifest.example.json)
and keep the real manifest outside the target repository.

Freeze the development and certification cases before the baseline. Use
[render-mcq.mjs](scripts/render-mcq.mjs) to render one case without exposing
its answer or rule:

```bash
node scripts/validate-eval-manifest.mjs <manifest.json>
node scripts/render-mcq.mjs <manifest.json> <case-id>
```

Measure medium and high without the target skill before changing it. A
closed-book multiple-choice baseline should use no tools and no skills. Record
all misses, malformed responses, and evaluator failures.

## Create or refine the Pi skill

Read [pi-skill-design.md](references/pi-skill-design.md). Keep the target
`SKILL.md` brief and use it as a router to focused `references/`, deterministic
`scripts/`, and static `assets/`.

When required-reference use is an acceptance criterion, use the pure-router
profile: keep answer-bearing operational conclusions in focused references and
leave `SKILL.md` with routing cues, source precedence, safety boundaries, and
report discipline. Include a cue-to-reference table and require every
applicable reference for cross-domain questions.

The target skill may contain:

- durable rules and decision procedures;
- exact source hierarchy or precedence;
- examples that generalize beyond eval wording;
- mechanical self-checks for common failure modes; and
- helper scripts for deterministic operations.

It must not contain the answer key, case IDs, letter patterns, certification
questions, or facts that exist only to overfit the current evaluation.

## Invoke Pi in three distinct modes

Use [run-pi-skill-eval.sh](scripts/run-pi-skill-eval.sh) for consistent
one-shot JSONL runs.

### Baseline

Baseline disables all skill discovery and normally uses no tools:

```bash
scripts/run-pi-skill-eval.sh \
  --activation baseline \
  --cwd <project> \
  --provider <provider> \
  --model <model> \
  --thinking medium \
  --tools none \
  --prompt-file <rendered-question> \
  --output <runtime-dir>/baseline-medium-D01.jsonl
```

### Deterministic forced loading

Forced evaluation uses three independent activation layers:

1. `--skill <skill-path>` supplies the exact skill.
2. `/skill:<skill-name>` expands the full `SKILL.md`.
3. `Use the <skill-name> skill to help solve this:` explicitly assigns it.

The wrapper combines these with `--no-skills`, which disables unrelated
discovery while preserving the explicit skill path:

```bash
scripts/run-pi-skill-eval.sh \
  --activation forced \
  --cwd <project> \
  --skill <project>/.agents/skills/<skill-name> \
  --skill-name <skill-name> \
  --provider <provider> \
  --model <model> \
  --thinking medium \
  --prompt-file <rendered-question> \
  --output <runtime-dir>/forced-medium-D01.jsonl
```

Never infer activation from score. The scorer must find the expanded
`<skill name="...">` block in Pi's user-message event.

### Natural discovery

Natural discovery is a separate capability test. It omits `--no-skills`,
`--skill`, and `/skill:<name>`, then verifies that Pi used `read` on the
intended `SKILL.md`:

```bash
scripts/run-pi-skill-eval.sh \
  --activation natural \
  --cwd <project> \
  --provider <provider> \
  --model <model> \
  --thinking medium \
  --prompt-file <rendered-question> \
  --output <runtime-dir>/natural-medium-T01.jsonl
```

Do not substitute natural discovery for deterministic loading in certification
or production controller runs.

## Score structurally

Use [score-pi-jsonl.mjs](scripts/score-pi-jsonl.mjs); never score the last output
line or rely on prose inspection:

```bash
node scripts/score-pi-jsonl.mjs \
  --manifest <manifest.json> \
  --case <case-id> \
  --log <run.jsonl> \
  --skill-name <skill-name> \
  --skill-path <skill-path>/SKILL.md \
  --activation forced
```

Add `--require-strict` only when unfenced, JSON-only output is part of the
acceptance bar. Otherwise report strict formatting independently from semantic
correctness.

The scorer validates exact choice labels, the expected skill source path,
required reads, runtime completion, and an optional tool allowlist. Pass a
comma-separated case list to `--case` to score a secondary batch without
weakening the independent-item schema.

## Run one bounded teaching cycle

Read [failure-taxonomy.md](references/failure-taxonomy.md).

For each cycle:

1. Run independent development items at the fixed model settings.
2. Score activation, required reference reads, answer correctness, schema, and
   strict formatting.
3. Diagnose the smallest causal failure class.
4. Change one coherent part of the target Pi skill.
5. Preserve a checkpoint of the prior skill version outside the repository.
6. Rerun the affected development items.
7. Record the evidence, delta, decision, and remaining budget.

Run the complete development set at milestones: after a broad routing change,
before certification, and before final acceptance. Do not pay for a full
regression after every narrow wording change when the affected cases provide a
sound causal check.

Use batched questions only as a secondary context-pressure test. A batch miss
after independent passes is evidence of interference or answer-mapping load,
not necessarily missing domain knowledge.

## Harden saturation without leaking the holdout

Harden before editing when either thinking level reaches 90%, fewer than three
cases expose a capability gap, or remaining misses are mostly formatting. Also
harden when both thinking levels saturate the development set:

- add compositional cases spanning multiple rules;
- strengthen distractors with plausible but unsafe or subtly incorrect routes;
- shuffle answer positions and avoid predictable letter distributions;
- add negative, exception, precedence, and boundary cases;
- vary wording and requested output shapes; and
- test independent items before larger batches.

Never tune on a certification miss and continue calling that set untouched.
Relabel every observed certification case as development, then freeze a new
unseen certification set before further edits.

## Certify as one locked transaction

Do not inspect certification results level by level. Freeze the manifest, target
skill package, project state, provider, model, Pi version, and complete thinking
level list before the first certification invocation:

```bash
node scripts/certification-lock.mjs create \
  --manifest <manifest.json> \
  --skill <project>/.agents/skills/<skill-name> \
  --project <project> \
  --provider <provider> \
  --model <model> \
  --pi-version "<pi --version output>" \
  --thinking medium,high \
  --output <runtime-dir>/certification-lock.json
```

Run the complete split through [run-eval-suite.sh](scripts/run-eval-suite.sh).
The suite verifies the lock before and after every case, withholds intermediate
scores, and reports only after all requested levels finish. Any manifest, skill,
project-state, runtime-identity, or level drift invalidates the transaction.
The target project must be a Git worktree so the lock can fingerprint its HEAD,
tracked diff, and untracked files.

```bash
scripts/run-eval-suite.sh \
  --activation forced \
  --split certification \
  --manifest <manifest.json> \
  --output-dir <runtime-dir>/certification \
  --cwd <project> \
  --provider <provider> \
  --model <model> \
  --thinking medium,high \
  --tools read \
  --skill <project>/.agents/skills/<skill-name> \
  --skill-name <skill-name> \
  --lock <runtime-dir>/certification-lock.json \
  --offline
```

If any certification case is observed and a later edit is made, relabel all
observed cases `dev-exposed`, freeze new unseen IDs, and create a new lock.

## Test discovery and batches last

Natural discovery is diagnostic, not production assurance. After trust and
catalog exposure are verified, use a small development-only probe. If Pi still
does not read the intended `SKILL.md`, record a model-routing limitation and use
forced loading; do not spend domain edit cycles on discovery unless natural
invocation is an explicit success requirement.

Run batch stress only after independent certification. Treat fenced or noisy
JSON as a controller-normalization concern unless strict formatting is a
declared downstream requirement.

## Optional nested supervision

When a visible worker teaches Pi, preserve this ownership:

```text
root supervisor -> worker/controller (sole skill writer) -> Pi (read-only)
```

The worker owns hidden answers, skill edits, runtime evidence, and the teaching
goal. The root supervisor independently checks hashes, holdout integrity, diff
scope, final scores, and external state. Neither supervisor should accept the
other actor's completion claim without authoritative evidence.

## Stop and report

Stop on success, budget exhaustion, plateau, unavailable model, evaluator
failure, overlapping user edits, or need for broader authority.

Report:

- Pi version, provider, model, thinking levels, and tool boundary;
- target skill path and files changed;
- no-skill baselines and final development scores;
- untouched certification scores by thinking level;
- forced activation and required-reference evidence;
- natural-discovery evidence, when requested;
- independent versus batch results;
- strict-format compliance as a separate metric;
- requested thinking settings and whether reasoning support was verified;
- invocation, elapsed-time, and token budget used;
- cycles used, changes kept or discarded, and why the loop stopped;
- retained runtime evidence and any unresolved weakness.

Example invocation:

```text
$pi-skill-teacher Teach Pi this repository's release procedure. Build a
project-local Pi skill, baseline medium and high thinking, use multiple-choice
development evals, harden them when saturated, and stop only after a fresh
first-attempt certification with verified skill activation.
```
