# Failure Catalog

Known failure modes of `/debate` and how the lead session should handle each. Consult this when something in the workflow goes sideways.

## Table of contents

- [Phase 0 failures (framing)](#phase-0-failures-framing)
- [Phase 1–3 failures (debate execution)](#phase-13-failures-debate-execution)
- [Phase 4 failures (judge synthesis)](#phase-4-failures-judge-synthesis)
- [Phase 5 failures (cleanup)](#phase-5-failures-cleanup)

## Phase 0 failures (framing)

### Topic is open-ended, not contested

**Detection**: Inference produces vague labels, or the "positions" read like "explore X" rather than "argue for X."

**Response**: Stop. Tell the user:
> This topic looks open-ended rather than contested. `/debate` works best when positions are nameable upfront. For exploratory analysis with parallel lenses, `/brainstorm` is a better fit. Would you like to switch, or can you narrow the topic to 2–4 named positions?

### Topic has no real contest

**Detection**: Inference finds only 1 meaningful position; the "other side" is a strawman.

**Response**: Stop. Tell the user:
> This topic does not appear genuinely contested — one position seems clearly correct. Spawning a debate team would waste tokens. Would you like a single-agent analysis instead, or do you see a contest I missed?

### Inference yields 5+ positions

**Detection**: The topic naturally decomposes into too many options (e.g., "which language should we use" across 8 candidates).

**Response**: Stop and ask the user to narrow to the top 2–4 contenders before running the debate. Offer `/brainstorm` as an alternative.

### User rejects proposed positions repeatedly

**Detection**: After 3 rounds of Phase 0 correction, the user is still rewriting positions.

**Response**: The topic is probably not ready for a debate. Suggest clarifying the underlying question first (perhaps via `/clarify` or `/brainstorm`) and coming back.

## Phase 1–3 failures (debate execution)

### Debater output is malformed

**Detection**: Missing required sections (position statement, arguments, assumptions), or output is clearly off-topic.

**Response**:
1. Re-prompt that single debater once with a more explicit template.
2. If the second attempt is still malformed, proceed with what you have and note the degradation in the final decision doc under Section 2 (confidence).
3. Do not abort the whole debate over one malformed output.

### Debater errors or times out mid-run

**Detection**: The agent-team harness surfaces a spawn/execution error.

**Response**: Abort the debate. Render a clear message to the user:
> Debater {SLOT} failed during Phase {N}. The debate cannot produce a valid decision with a missing voice. Cleanup has been run; you can retry.

Do **not** produce a partial synthesis from 2 of 3 debaters — the composition is load-bearing.

### Debater attempts to change position

**Detection**: A debater's rebuttal or swap output concedes its own position is wrong and adopts another side.

**Response**: This is a pinning violation (the primary collapse failure mode). Re-prompt that debater with the pinning rule restated explicitly:
> Reminder: you are pinned to {POSITION} for the entire debate. You may concede specific points but you may not abandon your position. Please re-do this phase.

If it happens twice for the same debater, note it in the final decision doc's confidence justification.

### Debaters collapse toward agreement in Phase 2

**Detection**: Rebuttal outputs read like endorsement, or all debaters agree on most points.

**Response**: This is early sycophantic collapse. Proceed to Phase 3 (the steelman swap is designed to break exactly this). If Phase 3 also collapses, note low confidence in the final doc and flag it to the user:
> The debaters converged early. The decision below should be treated as low-confidence; consider re-running with sharper position labels or switching to `/brainstorm`.

### Phase 3 steelman is too weak

**Detection**: A debater's steelman of the opposing position is a caricature or a rebuttal in disguise.

**Response**: Re-prompt with the steelman instruction restated and an explicit "no 'but my side is still right'" constraint. Once. Then proceed regardless.

## Phase 4 failures (judge synthesis)

### Judge declares a genuine tie

**Detection**: Judge returns `"no clear winner on axis X"` in Section 1.

**Response**: **This is a valid output, not a failure.** Render the decision doc as-is. The `tied_on_axis` field is a first-class result of the skill, not an error path.

### Judge skips the irreducible trade-offs section

**Detection**: Section 4 has fewer than 2 bullets, or the bullets are restated key reasoning.

**Response**: Re-prompt the judge with the minimum-disagreement quota restated:
> Section 4 requires at least 2 irreducible trade-offs — costs of the recommendation the decision does NOT resolve. If you cannot name 2, you have not engaged deeply enough with the losing positions. Please produce Section 4 again.

If the second attempt still fails the quota, note it in the rendered output and downgrade confidence to `low`.

### Judge is visibly biased toward one debater's style

**Detection**: Decision reasoning parrots one debater's exact phrasing or only cites arguments from one side.

**Response**: Re-prompt the judge with the neutrality rule restated and an explicit instruction to cite arguments from all positions. Once.

### Judge refuses to produce output

**Detection**: Judge asks for more information, defers to the user, or produces meta-commentary instead of the decision doc.

**Response**: Re-prompt once with the template structure restated. If it still refuses, abort and tell the user:
> The judge could not produce a structured decision for this topic. This usually means the topic is not resolvable on the evidence the debate surfaced. Consider running `/brainstorm` to explore the question more openly.

## Phase 5 failures (cleanup)

### A teammate fails to shut down

**Detection**: The agent-team cleanup reports an orphan session.

**Response**: Retry cleanup from the lead session. Never delegate cleanup to another teammate — that violates agent-team's cleanup rules and can leave state inconsistent. If retry fails, surface the error to the user with instructions to manually terminate.

### Lead session loses track of a teammate

**Detection**: A spawned teammate does not appear in the agent-team roster.

**Response**: Run `agent-team` diagnostics to find the orphan. Do not spawn a replacement; that produces a 5-agent debate with undefined composition. Abort and ask the user to clean up manually.
