# Design Bake-Off (parallel worktrees)

When you want to **compare multiple aesthetic directions** for the same surface, don't serialize — fan out. Spawn N parallel `frontend-design-agent` instances, each in its own git worktree with a pre-assigned aesthetic, then review the candidates side-by-side in the browser.

This is the sharpest tool the skill offers. Use it when the right direction is unclear and you're willing to spend an hour exploring before committing.

## When to use

- Fresh landing page, no prior visual direction established
- Rebranding or major refresh — want to pressure-test a few directions
- Stakeholder debate about "is it warm or sharp? editorial or brutalist?"
- You have a rough idea and want to see the extremes

## When NOT to use

- The direction is already decided — just delegate once
- Small tweaks to an existing design — overkill
- Fewer than 2 candidates (obviously — that's just single delegation)
- More than 4 candidates — decision fatigue + port sprawl, pick your top 4 first

## The pattern

N parallel `frontend-design-agent` instances (2–4), each in its own worktree, each assigned one aesthetic. No debate, no dependency between them — **intentional divergence** so you get N different design candidates to compare side-by-side.

### Picking the N aesthetics (critical — don't skip)

Don't guess the candidates — build them *with the user* through two rounds of `AskUserQuestion`. The goal is N directions that are **genuinely different from each other** (different color temperature, different type neighborhoods, different motion philosophy) and that all fit the product's domain pool in `frontend-aesthetic/references/domain-matching.md`.

`AskUserQuestion` accepts multiple questions in a single turn — batch related prompts into one turn instead of serializing one question at a time.

**Round 1 — gather constraints.** In a single `AskUserQuestion` turn, ask whatever you can't infer from the code and current project state. Typical questions:

- Product domain or closest analogue (so you can pick the right pool in `domain-matching.md`).
- Number of slots (2–4).
- Hard no-gos (brand colors to preserve, fonts already licensed, aesthetics to avoid).
- Boldness target — "show me the extremes" vs. "three takes on the same mood."
- Any reference sites / moodboard links the user already has in mind.

**Round 2 — propose and approve.** Read `frontend-aesthetic/references/domain-matching.md`, pick N candidates from the matching domain's pool that diverge along multiple axes, and write one line per slot (direction + distinguishing twist — type pairing, palette, motion note). Send the draft back through `AskUserQuestion`:

- One question per proposed slot: *approve as-is / revise / replace with a different direction*.
- Include a free-text option on each so the user can steer ("swap the display face", "push the palette further", etc.).

Iterate Round 2 until every slot is explicitly approved. Only then spawn the agents.

**Hard rules**:
- No fixed default triad. The right pool depends on the product; every direction in `domain-matching.md` is on the table until you've matched the domain.
- If two proposed slots could plausibly produce the same output, merge them and propose something bolder for the freed slot.
- Don't skip the approval round, even when you're confident. The user reviews the rendered candidates later — surprise candidates bias that review.

Each approved slot carries:
- An **aesthetic** (from the domain pool, named with its distinguishing twist)
- A **dev-server port** so you can open all N simultaneously
- A **worktree** so commits don't collide and you can flip between them with `cd`

## Mechanics

### 1. Pick the candidates

Run the two-round `AskUserQuestion` flow described above. Once every slot is user-approved, restate the final roster for the record:

```
Bake-off for <surface>:
  1. <direction> — <one-line distinguishing twist (type / palette / motion)>
  2. <direction> — <one-line distinguishing twist>
  3. <direction> — <one-line distinguishing twist>
```

Keep each description to one line — the agent reads its own skill for depth.

### 2. Spawn the subagents in parallel

Use **one message with multiple `Agent` tool calls**. This is essential — sequential calls serialize the work and defeat the purpose.

```
Three parallel Agent calls, each with:
  subagent_type: frontend-design-agent
  isolation: worktree
  description: "Bake-off <N>: <aesthetic>"
  prompt: (see template below)
```

`isolation: worktree` is load-bearing — without it, all three agents fight over the same working tree and the last writer wins.

### 3. Prompt template per slot

```
## Task
Bake-off slot #<N> of <total>. Design the <surface> for <project/route>.
Aesthetic: <one-line direction + distinguishing twist, as approved in Round 2>.
Dev server port: <unique port per slot, e.g., 7071/7072/7073>.

## Constraints
- Stack: Bun + TanStack Start + Tailwind v4 (+ shadcn/ui if installed)
- Preloaded skills: bun-tanstack-start, tailwind-v4-tokens, frontend-aesthetic
- Do NOT compromise toward the middle. This slot exists to explore an extreme.
- Other slots are running in parallel with different aesthetics — do not coordinate.

## Expectations
1. Commit to the assigned aesthetic verbatim — do not drift toward "safe".
2. Enforce tokens — no hex, no raw color scales.
3. Start the dev server on port <N> via `bun --bun vite dev --port <N>`.
4. Run it, verify it renders, leave the server running when you report back.
5. Commit your work on a descriptive branch in this worktree.
6. Report in the standard agent output format, plus the branch name and dev URL.
```

### 4. Review side-by-side

After all N agents return, open each port in a separate browser tab:
- http://localhost:7071
- http://localhost:7072
- http://localhost:7073

Compare in context. Take screenshots. Pick a winner (or a hybrid).

### 5. Merge the winner, discard the rest

```sh
# Pick the winning branch
jj git fetch   # or: git fetch --all

# In the main checkout, restore the winner's files
jj new --to <winning-branch>   # or a git-equivalent flow

# Optional: keep the losers as a reference
git worktree list
# leave them, or `git worktree remove` when done
```

Never "mix" two bake-off branches. If the winner needs tweaks from a loser, delegate a fresh single-agent run against the winner with specific edits.

## Rules

- **No cross-talk between slots.** Each agent is blind to the others. Intentional divergence is the whole point.
- **Genuinely different aesthetics.** If two slots could plausibly be the same output, merge them and use the slot for something bolder.
- **One winner.** Do not ship a Frankenstein of three. Pick one, commit to it, iterate from there.
- **Clean up worktrees.** Leftover worktrees from last week's bake-off will confuse future sessions. `git worktree list` → remove the losers.

## Anti-patterns

- **Running 5+ candidates in parallel.** Decision fatigue; pick your top 3–4.
- **"Safe + bold + bolder".** The safe slot will always win by default — skip it. Run only bold directions.
- **Omitting port assignments.** Two dev servers on the same port is an instant bug.
- **Skipping `isolation: worktree`.** Non-negotiable for parallel design work.
- **Reading other slots' output mid-flight.** Don't. It biases your review later.

## Why this works

Single delegation produces *one* thoughtful answer. Bake-off produces *three different* thoughtful answers — which is what you actually want when direction is unsettled. The worktree isolation makes the parallelism cheap and the cleanup trivial.

## Canonical sources

- Worktree isolation: https://code.claude.com/docs/en/sub-agents#worktree-isolation
- Parallel Claude sessions: https://code.claude.com/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees
