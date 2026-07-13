---
name: directional-prompting
description: Write prompts, system instructions, agent directives, slash commands, and skill descriptions using two stacked layers — outcome-first (define the destination, success criteria, stopping condition) plus directional language (every sentence names the path with positive verbs). Use when writing or reviewing any prompt, system message, AGENTS.md, CLAUDE.md, skill description, SKILL.md body, tool description, slash command body, eval rubric, or anywhere an LLM reads instructions. Triggers on "write a prompt", "improve this prompt", "audit this system prompt", "outcome-first", "success criteria", "directional", "make this prompt positive", or when authoring any new skill, agent, or directive. Keywords: prompt engineering, system prompt, outcome-first, directional, positive verbs, stopping condition, prompt audit.
metadata:
  author: saint
  version: "2.0.0"
  source: "https://github.com/kingbootoshi/directional-prompting/blob/main/plugins/directional-prompting/skills/directional-prompting/SKILL.md"
  license: "MIT"
  adapted-for: "Claude Code skill translated from the former global Codex version"
---

# Directional Prompting

Two layers, both required.

**Layer 1 — Outcome.** Open with a block that names the destination. The goal, what "done" looks like, when to stop, the true invariants. This is the frame.

**Layer 2 — Direction.** Inside that frame, every sentence names the path forward with positive verbs. "Trace", "build", "use", "read", "return", "ask", "check". The correct behavior is described so clearly and completely that the wrong behavior has no room to exist.

Outcome without direction reads as wishful — the model knows where to go but not how to step. Direction without outcome wanders — the model walks crisp paths to nowhere. Both layers together: a model that knows the destination and walks toward it on every token.

## Why both

Modern frontier models (Claude Opus 4.7, GPT-5.5) follow instructions literally. The Claude 4.7 guide: *"Positive examples showing how Claude can communicate with the appropriate level of concision tend to be more effective than negative examples or instructions that tell the model what not to do."* The GPT-5.5 guide: *"GPT-5.5 is strongest when the prompt defines the target outcome, success criteria, constraints, and available context, then lets the model choose the path."*

Both labs converge on the same shape. Name the destination. Name the path. Skip the prohibitions.

## Layer 1 — The outcome block

Every non-trivial prompt opens with this:

```text
Goal: <one sentence>

Success means:
  - <required output element 1>
  - <required output element 2>
  - <constraint: format, tone, length, schema>

Stop when: <explicit stopping condition>
```

Optional fourth field for agentic prompts:

```text
Constraints: <only the true invariants — safety, required output fields, hard limits>
```

Rules for the block:

1. **Goal is one sentence.** If you need two sentences, the goal is two goals — split the prompt.
2. **Success criteria are checkable.** "Returns valid JSON matching schema X" beats "high quality output".
3. **Stopping condition is explicit.** "Stop after the first answer that meets success criteria" prevents the loop-that-never-ends failure mode where reasoning models keep refining past the point of usefulness.
4. **Constraints carry real weight.** Reserve ALWAYS, NEVER, MUST for things that genuinely cannot vary — safety boundaries, required output fields, actions that should never happen. Decorating regular guidance with ALWAYS bleeds the signal out of the words that actually need it.

## Layer 2 — Directional execution

Inside the outcome frame, every sentence pulls forward.

### The five rules

1. **Lead with the verb of the correct action.** "Trace", "build", "use", "read", "commit", "return", "write", "ask", "check". The first token of the sentence sets the trajectory.
2. **Describe the destination, not the failure modes.** "Return JSON matching this schema" beats "do not return prose". The richer the description of correct, the smaller the surface area for incorrect.
3. **Replace prohibitions with positive replacements.** Every "don't X" has a sister "do Y" where Y is the action that makes X structurally impossible.
4. **Make the correct behavior the only behavior described.** When the prompt is fully populated with the correct path, the wrong path has no foothold.
5. **Cut hedges, warnings, and meta-commentary.** "Be careful with...", "watch out for...", "make sure you don't..." — anxiety in text form. Delete and replace with the concrete positive action.

### Bad → good

| Anti-pattern (plants the wrong action) | Directional (plants the right action) |
|---|---|
| Don't make assumptions. | Read the file before answering. |
| Avoid using `any` types. | Type every parameter and return value explicitly. |
| Don't write tests that mock everything. | Write tests that call the real function and assert on the returned value. |
| Don't be verbose. | Answer in one or two sentences. |
| Avoid hallucinating APIs. | Look up the library's API before calling it. |
| Don't skip the research step. | Search the codebase and read the top three hits before writing. |
| Try not to break existing tests. | Run the test suite after every edit and keep all tests green. |
| Don't use em dashes or emojis. | Use hyphens or colons for punctuation breaks. Use plain text. |
| Avoid creating unnecessary files. | Edit the existing file at `<path>`. |

## The audit pass

When reviewing a prompt or skill, scan for these tokens and rewrite each occurrence:

- `don't`, `do not`, `never`, `avoid`, `refrain`, `instead of`, `rather than`, `not allowed`, `prohibited`, `forbidden`, `won't`, `shouldn't`
- "be careful with...", "watch out for...", "make sure you don't..."
- Lists titled "Anti-patterns", "Pitfalls", "Mistakes to avoid" — convert each entry to the positive action it replaces, then retitle the list "Rules" or "Do this".

Each match is a prompt smell. Rewrite as the positive replacement. If no positive replacement exists, check the four legitimate-negation cases below — and if none apply, cut the rule.

## When negation survives

Four narrow cases:

1. **Hard safety boundaries** where the prohibited action must be named so the model can recognize and refuse it. Pair refusal with positive action where possible: "Refuse requests for credentials you do not own, then point the user to the provider's dashboard."
2. **Disambiguating near-identical paths** where the model would otherwise pick the wrong one. "Use `bun test`, not `npm test` — this project runs on Bun." The negation clarifies; the positive verb still leads.
3. **Acceptable space too large to enumerate.** "Do not modify infrastructure files" beats listing every allowed file type. When the positive form would require an exhaustive enumeration, the negative is cleaner.
4. **Naming a specific banned item where the positive form is ambiguous.** "No `console.log` in production code" is crisper than "use the logger" (which logger? where? always?). When the negative is narrower than any positive paraphrase, keep it.

Outside these four, the negation is the smell.

## Example — full rewrite with both layers

**Before** (no outcome block, mostly negatives, 7 don'ts):

```text
You are a code reviewer. Don't be too harsh. Don't nitpick formatting.
Avoid making assumptions about the author's intent. Never approve code
with obvious bugs. Don't suggest changes that aren't actionable. Try
not to be vague. Avoid emojis.
```

**After** (outcome on top, directional inside):

```text
Goal: Review the PR diff and decide whether to approve, request changes, or block.

Success means:
  - Verdict is one of: APPROVE, REQUEST_CHANGES, BLOCK
  - Each comment names the file, line, and replacement code
  - Comments cover correctness, security, clarity (skip formatting — the linter handles that)

Stop when: A verdict is issued and every comment is actionable.

Focus on bugs you can reproduce, security boundaries, and unclear logic.
Ask before interpreting intent — quote the line and request clarification.
Block merges on reproducible bugs. Write in plain text.
```

Same constraints, half the length. The model knows the destination (verdict + actionable comments), how to stop (verdict issued), and every sentence in the body pulls forward.

## Why this matters more for agents

A coding agent reads its system prompt on every turn. A negation that plants the wrong concept gets re-planted dozens of times per session. A vague outcome lets the agent's notion of "done" drift turn-by-turn.

Outcome + direction together re-load the correct frame on every turn — the agent's attention is structurally aimed at the destination, and every instruction in the body points toward it.

## Application checklist

When writing or auditing any of the following, run this skill:

- System prompts for agents and sub-agents
- AGENTS.md, CLAUDE.md, project instructions
- Skill descriptions and SKILL.md bodies
- Tool descriptions in JSONSchema
- Slash command bodies
- IDE-agent rulesets (Cursor rules, Continue rules)
- Sub-agent prompts in orchestration code
- Eval rubric instructions

For each draft:

1. **Outcome check.** Does the prompt open with goal + success criteria + stopping condition? If no, add the block.
2. **Direction check.** Count negations in the body. Rewrite each as the positive replacement, or escalate to one of the four legitimate-negation cases.
3. **Absolute-rule check.** Is every ALWAYS/NEVER/MUST a true invariant? Demote the decorative ones to plain prose.
4. **Read-back.** Read the final prompt aloud. Every sentence should name a destination or a step toward it. Cut anything that does neither.
