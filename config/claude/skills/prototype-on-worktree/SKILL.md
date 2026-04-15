---
name: prototype-on-worktree
description: >
  Spawn an isolated Opus subagent to build and verify a working prototype on a
  git worktree, then return copy-paste instructions for the user to verify it
  themselves. Use when the user wants to spike, prototype, try, explore, or get
  a working example of an idea without touching the main working tree. Keywords:
  prototype, spike, worktree, try, experiment, proof of concept, POC, working
  example, explore an idea, get something working
disable-model-invocation: false
argument-hint: [what to prototype] [--replicas N for parallel variants]
---

# Prototype on a Worktree

Goal: **$ARGUMENTS**

Spawn a subagent in an isolated git worktree to build a working prototype,
verify it, and hand back instructions the user can run themselves.

## How to run it

Spawn via the `Agent` tool with these exact settings:

- `subagent_type`: `general-purpose`
- `model`: `opus`
- `isolation`: `"worktree"`
- `description`: short (3-5 words) label for the spike
- Do **not** set `maxTurns`.
- **Replicas**: default to **one** subagent. Only spawn multiple (parallel variants
  exploring different approaches) if the user explicitly asked for replicas or
  passed `--replicas N`. When running multiple, send all `Agent` calls in a
  single message so they run concurrently.

## The subagent's prompt (template)

Brief the subagent with a self-contained prompt along these lines. Adjust the
feature description to match `$ARGUMENTS`, but keep the contract sections
verbatim — the structured return is the whole point.

```
You are building a working prototype of: <feature from $ARGUMENTS>

Context: <1-2 sentences of why, plus any constraints the user mentioned>

You are running in an isolated git worktree. Your job:

1. Build the smallest change that demonstrates the idea end-to-end. Prefer
   existing patterns in the repo. Stub/mock external dependencies only when
   strictly necessary — note every stub in your report.

2. Verify your work. Decide verification depth by deployment complexity:
   - LIGHTWEIGHT (single process: TS/Node server, uv script, single Python
     entrypoint, CLI binary, single Go service): boot it yourself and exercise
     it. Pick a non-default port to avoid conflicts (e.g., 3919, 8421). Capture
     real output — request/response, stdout, test results. Tear it down before
     finishing.
   - HEAVY (docker-compose, k8s manifests, multi-service infra, anything
     needing external creds or long-running stateful services): do NOT boot it.
     Run unit/integration tests if they exist and are fast. Otherwise, rely on
     type-checks, linters, and a careful read-through.

3. Commit your changes on the worktree branch with a clear message. Uncommitted
   work will be lost on cleanup.

4. Return a report in EXACTLY this format:

   **Worktree path**: <absolute path>
   **Branch**: <branch name>
   **What I built**: 2-4 bullets, concrete
   **How I verified it**: commands I ran + a short excerpt of real output.
     If I skipped live verification, say why (e.g., "requires docker-compose
     + postgres, deferred to user").
   **How you verify it**: numbered shell commands the user can copy-paste.
     Start with `cd <worktree path>`. For lightweight prototypes, include the
     exact boot command with the non-default port and a probe command (curl,
     test invocation, etc.). For heavy prototypes, list the real steps the
     user must take (e.g., `docker compose up`, env vars to set, endpoints to
     hit). End with a clear pass/fail signal the user should look for.
   **Known gaps**: what's mocked, stubbed, skipped, or hardcoded.
   **Suggested next step**: one sentence on what to do if it works.
```

## After the subagent returns

1. Relay the subagent's report to the user verbatim — especially the
   "How you verify it" section. Don't summarize the verification steps away.
2. If multiple replicas ran, list them side-by-side with a one-line diff of
   their approaches so the user can pick.
3. Remind the user the worktree lives at `.claude/worktrees/<name>` and will
   be prompted for cleanup when they exit — they can `cd` in and poke around
   freely.

## Guardrails

- Never run the subagent without `isolation: "worktree"` — the point is that
  the main working tree stays clean.
- Always Opus. Do not downgrade to Sonnet/Haiku even for "simple" spikes —
  the user has specified Opus.
- Do not set `maxTurns`. Prototypes sometimes need many iterations to get a
  real verification signal.
- If the repo has `.worktreeinclude`, dependencies like `.env` will be
  copied. If not and the prototype needs them, tell the subagent to copy
  specific files explicitly as its first step.
- Fresh worktrees have no `node_modules` / `.venv` / built artifacts. The
  subagent must install deps itself if needed.
