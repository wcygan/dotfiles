---
name: frontend-designer
description: One-shot dispatcher for distinctive frontend design work on the Bun + TanStack Start + Tailwind v4 (+ shadcn/ui) stack. Delegates to the `frontend-design-agent` subagent (Opus, preloaded with `bun-tanstack-start` + `tailwind-v4-tokens` + `frontend-aesthetic` skills). Use when building or refreshing landing pages, heroes, marketing surfaces, or any visible public UI. Prefer this over ad-hoc prompting — it guarantees the right stack conventions, token enforcement, and aesthetic direction every time. Keywords frontend design, landing page, hero, marketing page, visual polish, design system, shadcn, tailwind v4, tanstack start, bun.
argument-hint: [what to design]
---

# Frontend Designer (dispatcher)

This skill's job is one thing: **hand the task to the `frontend-design-agent` subagent with the right framing**, so every frontend-design task in this dotfiles environment runs with consistent stack, tokens, and taste.

The agent (Opus, `config/claude/agents/frontend-design-agent.md`) already has the three stack skills preloaded — `bun-tanstack-start`, `tailwind-v4-tokens`, `frontend-aesthetic`. Do not recreate their content here.

## When to use

- "Design a landing page for X"
- "Build a hero for /routes/about"
- "Polish the visual design on this route"
- "Refresh the marketing page"

**Do not use** for CRUD forms, admin tooling, internal dashboards, or API work — those need consistency, not extremity. Use the general-purpose agent or no agent at all.

## What this skill does

When invoked:

1. **Read the pre-flight checks** in [preflight](references/preflight.md) — confirm stack assumptions (Bun, TanStack Start, Tailwind v4) and note what's missing.
2. **Summarize the ask** into one paragraph: the surface, the audience, the desired feeling (if the user hinted), and hard constraints (copy, assets, brand).
3. **Delegate to the `frontend-design-agent` subagent** with a self-contained prompt — see [dispatch](references/dispatch.md) for the exact pattern.
4. **Do not write JSX/CSS directly from the main thread.** Delegation is the whole point.
5. **Relay the agent's output back**, then offer concrete follow-ups (second page with same chrome, dark-mode token pass, extraction of shared components).

## Why delegate instead of doing it inline

Quoting `claude-code-best-practices/references/sub-agents.md`:
> Subagents only see their system prompt plus basic env details — not the main Claude Code system prompt, and not skills inherited from the parent. Pass everything explicitly.

The `frontend-design-agent` has three opinionated skills **preloaded at startup**. If you try to do design work in the main thread, you're relying on those skills to auto-trigger — which is less reliable than explicit preload. The subagent guarantees the context is right before the first JSX tag.

It also isolates the long chain of design-thinking from the main conversation's context budget.

## Foolproof invocation

```
Use the frontend-design-agent subagent to design <whatever the user asked for>.
Preloaded context: bun-tanstack-start, tailwind-v4-tokens, frontend-aesthetic.
Commit to one aesthetic direction before writing JSX.
```

Or the `@`-mention form (guaranteed, no description-matching needed):
```
@"frontend-design-agent (agent)" <task>
```

If the agent file isn't picked up (`/agents` doesn't list it), it was added after session start — restart Claude Code or run `/agents` once.

## Complements

- `bun-tanstack-start` — stack wiring and conventions (preloaded in the agent)
- `tailwind-v4-tokens` — token system and consistency rules (preloaded in the agent)
- `frontend-aesthetic` — taste and aesthetic directions (preloaded in the agent)
- `tailwind` — general v4 reference (not preloaded; available for main thread)
- `tanstack-start` — general framework reference (not preloaded; available for main thread)
- `frontend-design` (Anthropic bundled) — predecessor; this skill supersedes it for this stack

## Design bake-off (parallel iterations)

When the aesthetic direction isn't settled, don't guess — **fan out**. Spawn 2–4 `frontend-design-agent` instances **in parallel**, each in its own git worktree with a different aesthetic assigned, each on its own dev-server port. Compare candidates side-by-side in the browser, pick one, discard the rest.

This is the single sharpest tool this skill offers. See [design-bakeoff](references/design-bakeoff.md) for the full pattern — team composition table, port assignments, prompt template, and cleanup.

Trigger phrases: "try a few directions", "show me some options", "I'm not sure what style", "compare X vs Y".

## References

- [preflight](references/preflight.md) — what to check before delegating
- [dispatch](references/dispatch.md) — exact prompt format for single delegation
- [design-bakeoff](references/design-bakeoff.md) — parallel worktree iteration across N aesthetics
- [when-not-to-use](references/when-not-to-use.md) — anti-triggers; tasks this skill should reject

## Canonical sources

- Claude Code sub-agents: https://code.claude.com/docs/en/sub-agents
- Claude Code skills: https://code.claude.com/docs/en/skills
- Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
