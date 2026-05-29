# pi skill anatomy

Table of contents:
- [Frontmatter (pi is lenient)](#frontmatter)
- [Where pi discovers skills](#discovery)
- [How pi surfaces and loads a skill](#loading)
- [Low-freedom authoring, in depth](#low-freedom)
- [Routing: local vs frontier](#routing-local-vs-frontier)

pi implements the [Agent Skills standard](https://agentskills.io/specification). Authoritative offline copy of pi's own skills doc: `/Users/wcygan/Development/pi/packages/coding-agent/docs/skills.md`. Web: https://pi.dev/docs/latest.

## Frontmatter

A pi skill is a directory containing `SKILL.md`. Only two fields matter to pi:

```yaml
---
name: my-skill
description: What it does and exactly when to use it. Be specific.
---
```

- `name` — pi (unlike the strict standard) allows the name to differ from the directory, which is what lets the *same* skill live in a shared dir and be read by Claude, Codex, and pi. Keep them equal anyway unless you have a reason.
- `description` — the **only** thing always in context. pi injects names+descriptions into the system prompt; the body loads only when the model reads the file. Front-load the trigger.
- pi ignores Claude-Code-specific fields (`allowed-tools`, `context: fork`, `model`, hooks). They're harmless to include for cross-harness skills, but **pi will not honor them** — pi has no fork/permission/sub-agent machinery. Don't rely on them for pi behavior.

Everything outside `SKILL.md` is freeform: `scripts/`, `references/`, `assets/`.

## Discovery

pi scans, in order:
- Global: `~/.pi/agent/skills/`, `~/.agents/skills/`
- Project: `.pi/skills/`, and `.agents/skills/` in cwd + ancestors up to repo root
- Packages: `skills/` dirs or `pi.skills` in `package.json`
- Settings: the `skills` array in `~/.pi/agent/settings.json` (this machine points it at `~/.claude/skills` and `~/.codex/skills`)
- CLI: `--skill <path>` (repeatable; loads even with `--no-skills`)

Rules worth knowing:
- In `~/.pi/agent/skills/` and `.pi/skills/`, loose root `.md` files each count as a skill.
- In `~/.agents/skills/` and project `.agents/skills/`, loose root `.md` files are **ignored** — you need a `<name>/SKILL.md` directory.
- `--no-skills` disables discovery but explicit `--skill` paths still load.

## Loading

1. At startup pi extracts every skill's name + description into the system prompt (XML, per the spec).
2. When a task matches, the model is *expected* to `read` the full `SKILL.md` — **but small models often don't on their own.** Force it two ways:
   - `/skill:<name>` command (args after it are appended as `User: <args>`). Requires `enableSkillCommands` (default on; toggle in `/settings`).
   - Name the skill explicitly in the prompt: `"Use the <name> skill to …"`.
3. The model then follows the instructions, resolving relative paths for scripts/assets.

Because step 2 is unreliable on small models, **a pilot that doesn't `/skill:` the skill by name is testing whether the model *finds* the skill, not whether the skill *works*.** Pin it with `/skill:name` while iterating on content.

## Low freedom

The single biggest lever for small-model reliability. Match instruction style to how fragile the step is:

| Terrain | Use when | Style |
|---------|----------|-------|
| Narrow bridge | destructive, exact sequence, or small model | exact commands, "do not modify X", closed lists |
| Winding road | a preferred pattern with minor variation | pseudocode / parameterized template |
| Open field | many valid approaches, frontier model only | goals + heuristics |

Concrete moves that raise small-model success:
- Replace "choose an appropriate type" with a **closed list** the model picks from.
- Replace "if needed" with an explicit **condition + command** ("if `git diff --staged` is empty, print X and stop").
- Give the **exact command**, not a description of it.
- State the **stop condition** and what to print as output — small models over-run otherwise.
- End with a **self-check block** the model verifies before finishing.

## Routing: local vs frontier

The first authoring decision is *whether the task belongs on the local model at all* (the [Step 0 gate](../SKILL.md) in the SKILL.md body). Score two axes:

- **Complexity** — mechanical/bounded vs. needs judgment or large-context synthesis.
- **Sensitivity** — value of keeping the data on the machine.

| Route | Task profile | Examples |
|-------|--------------|----------|
| **Local pi skill** | repeated, mechanical, machine-verifiable | commit-message drafting · changelog from a git range · config entry per a fixed policy · dependency-bump summaries · dead-symlink reports · log/CSV → JSON extraction · label/triage classification · docstring boilerplate |
| **Frontier model** | judgment, taste, large-context reasoning, or no possible validator | architecture decisions · security review · ambiguous multi-file refactors · API design · prose with a voice · root-causing a subtle bug |
| **Hybrid (escalate)** | mechanical core + an occasional hard case | rename-symbol-across-repo (local does the edits, escalates on conflicts) · PR triage (local buckets the clear ones, frontier takes the unclear) |

Rules of thumb:
- **No validator ⇒ frontier.** If you can't name a machine check (regex, test, type-check, re-scan), a small model will be confidently wrong and the skill can't catch it. That difficulty is the routing signal — don't ship it validator-less.
- **Long-context synthesis ⇒ frontier.** Reasoning over a large codebase exceeds what a small executor does reliably, even inside its context window.
- **Private + repeated + cheap-to-verify ⇒ local.** This is the bulk of agent traffic worth offloading.

**Your local tier sets the ceiling.** A 1.5B–7B model is realistically classification/extraction only; this machine's **27B Qwen handles light multi-file edits and simple reasoning**, so the local column extends further — but the validator rule never relaxes.

### Hybrid: build the escape hatch in

A hybrid skill runs locally but must name where to bounce out. Make it an explicit, low-freedom step:

> "If `<ambiguous condition>`, do not guess — stop and print `ESCALATE: <reason>` so a frontier model takes over."

This keeps the small model from confidently mishandling the hard 20% the skill was never meant to cover.

### Keep the library small

Routing accuracy *decays as the skill library grows* — large libraries develop "black-hole" skills that wrongly capture unrelated requests. Start with 3–5 sharply-described local skills, not 30; tight `description` fields are what keep the model selecting the right one.
