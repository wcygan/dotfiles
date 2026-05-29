---
name: authoring-pi-skills
description: Author Agent-Skills-standard SKILL.md files designed to be executed by the pi coding agent — often a small local model (llama.cpp/Qwen). Covers pi skill anatomy and discovery, writing low-freedom procedures with machine-checkable validators for small executors, the author-pilot-refine distillation loop driving pi headlessly, and optional Codex co-authoring. Use when writing or refining a skill that pi will run, or when asked to make a skill work well on a local model. Keywords pi skill, SKILL.md, pi coding agent, local model, llama.cpp, qwen, skill distillation, /skill, pilot, refine.
---

# Authoring pi skills

Write skills that the **pi coding agent** executes — usually with a **small local model** (this machine: llama.cpp serving Qwen3.6-27B at `:8080`). The governing idea is *skill distillation*: a frontier model (you, Claude — or Codex) authors and refines the procedure once; the small local model executes it many times. The frontier model does the expensive thinking at author-time so the local model only has to **follow documented steps and make tool calls**.

That split dictates everything below: **optimize the SKILL.md for the weakest model that will run it.**

> For *how pi itself works* (modes, models.json, the monorepo, this machine's quirks), defer to the existing **`pi-coding-agent`** skill and its `references/`. This skill is only about *authoring skills for pi*.

## Step 0 — local or frontier? Decide before you author

Before writing a line, decide **whether this task should run on the local model at all.** Score it on two axes (the routing consensus across local-AI practice):

- **Complexity** — mechanical and bounded, or does it need judgment / large-context synthesis?
- **Sensitivity** — does the data benefit from never leaving the machine?

Then route:

- **Local pi skill** — *repeated*, *mechanical*, and *machine-verifiable*. This is the 60–80% of agent work worth offloading. → author it per the three rules below.
- **Frontier model** — needs judgment, taste, large-context reasoning, or has **no possible validator**. Don't distill it; a small model will be confidently wrong and the skill can't catch it.
- **Hybrid** — frontier authors and handles the hard case; local executes the mechanical core. The skill runs locally but **names an escape hatch** — "if X is ambiguous, stop and report instead of guessing" — so the hard 20% bounces back to a frontier model.

**The fast test: can you name a machine check (regex, test, type-check, re-scan)?** If no, it's a frontier task — that difficulty *is* the routing signal, not a reason to ship a validator-less local skill.

Full rubric with worked task examples and the hybrid escape-hatch pattern: [references/skill-anatomy.md](references/skill-anatomy.md#routing-local-vs-frontier).

## The three rules that make a skill work on a small model

1. **Low freedom — narrow bridge, not open field.** Give exact commands and *closed enumerations* ("pick one of: feat, fix, docs…"), not "use your judgment." Small models wander on open-ended steps. Reserve high-freedom prose for skills you only run on a frontier model.
2. **A machine-checkable validator.** End with a loop the model can verify itself against — a regex, a `make test-pre`, a type check, a re-scan that must return zero. Self-checks beat "please double-check." This is the article's prized property and the thing that makes refinement converge.
3. **Deep, progressive, self-contained.** One simple entry, complex procedure behind it. Keep `SKILL.md` lean; push detail into `references/` loaded on demand. Reference scripts/assets by **relative path**.

Details, frontmatter, discovery locations, and the local-vs-frontier routing rubric: [references/skill-anatomy.md](references/skill-anatomy.md).

## The author → pilot → refine loop

This is the core workflow. Copy the checklist and tick it off:

```
- [ ] 1. Author the SKILL.md (apply the three rules above)
- [ ] 2. (optional) Get a Codex second draft/critique, reconcile
- [ ] 3. Place it where pi can see it
- [ ] 4. Pilot it headlessly against the local model
- [ ] 5. Read the transcript — find where the small model went wrong
- [ ] 6. Tighten the SKILL.md; repeat 4-5 until it converges
```

**1. Author.** Write `SKILL.md` per the three rules. Start from a worked example: [references/examples.md](references/examples.md) has complete, copy-ready skills (commit-draft, changelog-since-tag, a validator-driven repo edit, a read-only research skill).

**2. Co-author with Codex (optional but recommended for non-trivial skills).** A second model catches procedure gaps a single author misses. Use the **`consult-codex`** skill to get an independent draft or critique, then reconcile the two. Exact invocation: [references/pilot-and-refine.md](references/pilot-and-refine.md#codex-co-authoring).

**3. Place it.** Pick by intended reach:
- `~/.agents/skills/<name>/SKILL.md` — pi reads natively, zero config, harness-neutral. Best for quick local iteration.
- `config/claude/skills/<name>/` in this repo → symlinks to `~/.claude/skills` → visible to Claude Code **and** pi (the `skills` array in `~/.pi/agent/settings.json` points there). Best for skills you want tracked and shared across all three harnesses.

**4–6. Pilot and refine.** Drive pi headlessly against the local model, read the JSON transcript, and tighten. All commands, transcript-reading, and the refine checklist: [references/pilot-and-refine.md](references/pilot-and-refine.md).

Quick smoke test once a skill is placed:
```bash
curl -s --max-time 2 http://127.0.0.1:8080/v1/models | jq -r '.data[].id' || echo "start llama.cpp first"
pi --no-session -p "/skill:<name>"        # local default model runs the skill
```

## Reference index

- [references/skill-anatomy.md](references/skill-anatomy.md) — pi frontmatter, discovery locations, `/skill:name`, low-freedom authoring rules in depth, local-vs-frontier routing rubric.
- [references/examples.md](references/examples.md) — four complete worked pi skills to clone and adapt.
- [references/pilot-and-refine.md](references/pilot-and-refine.md) — headless pilot commands (print/json mode, tool restriction, model pinning), reading transcripts, the Codex co-authoring sub-workflow, the refine loop.
