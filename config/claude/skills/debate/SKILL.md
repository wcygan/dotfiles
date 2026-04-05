---
name: debate
description: >
  Run a structured multi-agent debate on a contested technical decision and
  return a recommended decision. Spawns 3 pinned debaters plus 1 neutral judge,
  enforces opening/rebuttal/steelman-swap rounds, and resists sycophantic
  collapse through pinned positions and a separate synthesizer. Use when
  positions are nameable upfront and the goal is a decision — not open-ended
  analysis (use /brainstorm for that). Keywords: debate, decision, contested,
  trade-off, A vs B, versus, pick one, argue, adversarial, steelman.
disable-model-invocation: true
argument-hint: [topic or "A vs B"]
---

# Debate

Runs a bounded, structured multi-agent debate on a contested decision and returns a single recommended answer (or an honest "no clear winner" when positions are genuinely tied).

> Before spawning the team, read the `agent-team` skill — `/debate` uses it as a library for spawning, composition, and cleanup. Do not reimplement those mechanics.

## When to use this vs `/brainstorm`

| Use `/debate` when | Use `/brainstorm` when |
|---|---|
| Positions are nameable upfront (A vs B, or 2–4 named options) | Analysis is open-ended; positions emerge from exploration |
| You want a decision | You want a trade-off map and recommendation from parallel lenses |
| The question is contested (multiple defensible answers exist) | You need Explorer/Analyst/Critic working in parallel without messaging |

If the topic is open-ended design ("design our notification system") or has no real contest ("should we use version control"), stop and suggest the alternative.

## Team Composition

**Fixed at 4 agents** for binary and 3-position topics:

| Slot | Role | Source |
|---|---|---|
| Debater A | Pinned to Position A for the entire run | `general-purpose` |
| Debater B | Pinned to Position B for the entire run | `general-purpose` |
| Debater C | Pragmatist (binary) OR Position C (3-option) | `general-purpose` |
| Judge | Neutral synthesizer; never argues a side | `general-purpose` |

For 4-position topics, add a 5th debater slot. This is the only case the team exceeds 4.

**Pinning is the primary collapse defense.** Debaters may not change position regardless of argument quality. Their job is to argue the best case for their side; the judge finds truth.

See [role-prompts](references/role-prompts.md) for the exact prompt templates used when spawning each slot.

## Workflow

Copy this checklist into your working notes and check off phases as you complete them:

```
- [ ] Phase 0: Framing & user confirmation
- [ ] Phase 1: Opening statements (parallel, no messaging)
- [ ] Phase 2: Rebuttal round (targeted SendMessage)
- [ ] Phase 3: Steelman swap round
- [ ] Phase 4: Judge synthesis → decision document
- [ ] Phase 5: Cleanup (shut down all teammates)
```

### Phase 0 — Framing & confirmation

1. Parse `$ARGUMENTS` as the topic. If empty, ask the user for one.
2. Infer 2–4 positions from the topic. Examples:
   - `"monorepo vs polyrepo"` → 2 positions + pragmatist
   - `"Postgres vs MySQL vs SQLite for this workload"` → 3 positions
3. If inference yields fewer than 2 positions, or more than 4, stop and tell the user why (single-agent analysis, or too many positions — split or use `/brainstorm`).
4. Present the proposed team and wait for user confirmation:

```
Debate: "<topic>"

Positions:
  A: <label>
  B: <label>
  C: <label or "Pragmatist / middle ground">

Team: 3 debaters + 1 neutral judge (4 agents total)
Protocol: opening → rebuttal → steelman swap → judge synthesis
Output: decision document (ephemeral)

Shall I proceed, or would you like to rename positions?
```

5. Loop on user corrections until confirmed. Do not spawn until confirmed.

### Phase 1 — Opening statements (parallel)

Spawn all debaters in **parallel** via the agent-team skill. Give each its pinned position and the Debater prompt template.

No inter-agent messaging in this phase — early messaging causes anchoring and collapses positions before they are stated.

Collect all openings before proceeding.

### Phase 2 — Rebuttal

For each debater, forward the **other** debaters' openings via `SendMessage` and ask for:

- Strongest counter to each other position
- Genuine concessions (points where opponents are right)
- Restatement of why their pinned position still holds

Collect all rebuttals before proceeding.

### Phase 3 — Steelman swap

Assign each debater **one** opposing position (rotate-once: A→B, B→C, C→A) and ask them to write the best possible case for it, ignoring their own side.

This is the single most important sycophancy antidote: it forces engagement with opposing logic without asking debaters to change position.

Collect all steelmans before proceeding.

### Phase 4 — Judge synthesis

Send the Judge agent the full structured transcript (openings + rebuttals + steelmans) and the [decision-doc-template](references/decision-doc-template.md). The judge must:

- Produce all 6 required sections in the template
- Include **at least 2 irreducible trade-offs** even when recommending a clear winner
- Return `"no clear winner on axis X"` if positions are genuinely tied — this is a valid output, not a failure
- Write the dissenting position charitably

### Phase 5 — Cleanup

Shut down all 4 teammates per the `agent-team` skill's cleanup rules. The lead session owns cleanup; teammates must not run it.

Render the judge's decision document in the chat. Do not persist to disk (ephemeral by default).

## Output

The final decision document has exactly these sections (see [decision-doc-template](references/decision-doc-template.md)):

1. **Decision** — the recommendation, or "no clear winner on axis X"
2. **Confidence** — low / medium / high + one-sentence justification
3. **Key reasoning** — 3–5 bullets
4. **Irreducible trade-offs** — ≥2 bullets the decision does NOT resolve
5. **What would change this decision** — evidence or conditions that would flip it
6. **Dissenting position** — one charitable paragraph from the strongest losing side

## Failure Modes

See [failure-catalog](references/failure-catalog.md) for detection and handling of:

- Malformed debater output
- Debater error / timeout mid-run
- Topic that should be rejected as open-ended or non-contested
- Judge declaring a genuine tie
- Phase 0 inference producing the wrong positions

## Anti-Patterns

- **Don't let debaters change position.** Pinning is the primary collapse defense; if you relax it, you lose the whole point of the skill.
- **Don't skip Phase 0 confirmation.** Debating the wrong framing wastes tokens and produces confident-wrong output.
- **Don't use `/debate` for open-ended analysis.** That is `/brainstorm`'s job — hand off early.
- **Don't let the judge also debate.** Neutrality is structural, not requested.
- **Don't paper over ties.** "No clear winner on axis X" is a valid, honest output.
- **Don't skip the steelman swap round.** It is the cheapest sycophancy antidote available.
- **Don't let teammates run cleanup.** The lead session owns cleanup per `agent-team`.
- **Don't persist transcripts by default.** Ephemeral is the contract; the user can copy what they want from chat.
- **Don't use free-form SendMessage pingpong between debaters.** The lead drives turn-based exchange; agents never message each other outside a phase the lead initiated.
- **Don't exceed 4 agents for binary / 3-option topics.** Scale only to 5 for 4-option topics; beyond that, split the question or use `/brainstorm`.
