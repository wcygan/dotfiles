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

**Always** source candidates from `frontend-aesthetic/references/domain-matching.md`:

1. Identify the product's domain (fintech / dev tool / wellness / games / agency / etc.).
2. Look up the candidate pool for that domain — 4–6 aesthetics that naturally fit.
3. From that pool, pick N candidates that are **genuinely different from each other** (different color temperature, different type neighborhoods, different motion philosophy). The domain-matching doc has explicit "genuinely different" example combinations per domain.
4. Write one line per slot naming the direction + its distinguishing twist.

**Hard rule**: do NOT default to Editorial / Brutalist / Handcrafted. Those are three of 18 directions and only fit specific domains. If you pick them without reading the domain pool, you're pattern-matching on prior examples, not the current product.

### Example team compositions (domain-specific)

These are illustrative — pick fresh per product. Each shows three genuinely-different picks from within one domain's pool.

**Consumer SaaS — productivity tool**

| # | Aesthetic | Port | Branch |
|---|---|---|---|
| 1 | Minimalist-luxury — Didot, extreme whitespace, single charcoal accent | 7071 | (agent returns) |
| 2 | Serif-forward Tech — GT Super + Söhne, warm off-white + deep forest | 7072 | (agent returns) |
| 3 | Dark / Moody — Reckless Neue + mono, near-black base, ember accent | 7073 | (agent returns) |

**Developer tool — CLI / infra**

| # | Aesthetic | Port | Branch |
|---|---|---|---|
| 1 | Terminal — JetBrains Mono end-to-end, green-on-black, typewriter reveals | 7071 | (agent returns) |
| 2 | Swiss — Söhne, strict 12-col grid, monochrome + single red accent | 7072 | (agent returns) |
| 3 | Brutalist — Druk Wide + mono, unapologetic cyan on black, exposed borders | 7073 | (agent returns) |

**Games / entertainment**

| # | Aesthetic | Port | Branch |
|---|---|---|---|
| 1 | Cyberpunk — Orbitron + mono, acid magenta/cyan, HUD hairlines | 7071 | (agent returns) |
| 2 | Y2K — Eurostile, aqua gradients, chrome highlights, shimmer buttons | 7072 | (agent returns) |
| 3 | Lo-fi Zine — VT323, flat neon + pastel, scan-line overlays | 7073 | (agent returns) |

**Wellness / lifestyle**

| # | Aesthetic | Port | Branch |
|---|---|---|---|
| 1 | Pastoral — Canela + botanical accents, sage/clay/bone palette | 7071 | (agent returns) |
| 2 | Minimalist-luxury — Didot Light, cream + cocoa, glacial scroll-reveal | 7072 | (agent returns) |
| 3 | Risograph — PP Editorial New, fluoro pink + teal + black on cream | 7073 | (agent returns) |

**Agency / portfolio — show taste**

| # | Aesthetic | Port | Branch |
|---|---|---|---|
| 1 | Brutalist — Neue Haas Display Black, harsh contrast, exposed structure | 7071 | (agent returns) |
| 2 | Maximalist — clashing serif + script + display, saturated parallax chaos | 7072 | (agent returns) |
| 3 | Editorial — Fraunces + Inter Tight, asymmetric, hanging drop-caps | 7073 | (agent returns) |

Each slot gets:
- An **aesthetic** (from the domain pool, named with its distinguishing twist)
- A **dev-server port** so you can open all N simultaneously
- A **worktree** so commits don't collide and you can flip between them with `cd`

## Mechanics

### 1. Pick the candidates

State them up front:

```
Bake-off for src/routes/index.tsx hero:
  1. Editorial refined  — Fraunces + Inter Tight, oxblood accent
  2. Brutalist bakery   — Neue Haas Display + JetBrains Mono, no accent
  3. Handcrafted zine   — Canela + Söhne, torn-paper textures, warm palette
```

Keep candidate descriptions to one line — the agent reads its own skill for depth.

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
Aesthetic: <one-line direction — "Brutalist bakery" style>.
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
