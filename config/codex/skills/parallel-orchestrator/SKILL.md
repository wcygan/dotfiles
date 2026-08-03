---
name: parallel-orchestrator
description: "Coordinate bounded Codex multi-agent work through independent lanes, staged concurrency, a concurrency ledger, lane-specific model routing, and root-owned synthesis. Use when the user asks to parallelize substantial work, use multiple agents or V2, run several investigations or implementations concurrently, increase fan-out, or orchestrate independent validation lanes."
---

# Parallel Orchestrator

Split substantial work into independent evidence-producing lanes, scale only
when useful, and keep integration and acceptance with the root task.

## Establish the boundary

Before spawning agents:

1. Read the applicable instructions and inspect the real checkout or system.
2. Record the requested outcome, non-goals, permission boundaries, baseline
   state, completion criteria, and required validation.
3. Separate ready independent work from dependent or tightly coupled steps.
4. Keep coupled or trust-critical mutations under one writer. Permit concurrent
   mutation only when file or subsystem ownership is disjoint.

Do not use multi-agent fan-out for small tasks, cosmetic decomposition, or
ordered work whose inputs are not ready.

## Maintain the concurrency ledger

Create and update a concise ledger before dispatching each wave:

| Lane | Agent | Model / effort | Scope and ownership | Dependencies | Expected value / usage | Validation | Status / evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

Give each lane a stable name. After spawning, record the returned agent ID and
use it for follow-up, interruption, and status operations. Include recursively
spawned agents in the parent lane's assigned concurrency budget.

## Scale in evidence-gated waves

1. Start with the smallest useful fan-out, normally 2–4 ready lanes.
2. Dispatch ready lanes together and continue useful root work that does not
   conflict with them.
3. Expand toward 8 and then 12 spawned lanes only when the ledger contains more
   independent ready work and the expected coverage or latency benefit
   justifies the usage.
4. Treat `agents.max_concurrent_threads_per_session` as the spawned-agent cap,
   excluding the root. With the configured value of 12, the runtime may contain
   twelve spawned agents plus the root task.
5. Stop expanding or retire lanes when work becomes serialized, findings
   duplicate one another, marginal coverage declines, validation is saturated,
   or rate-limit pressure exceeds the remaining value.

The concurrency limit is a ceiling, never a target.

## Route models by lane

- Use `agent_type: "luna_lane"` for narrow, focused, high-volume work such as
  inventories, extraction, classification, bounded research, focused coding,
  and routine validation. Its tracked profile is Luna with medium reasoning.
- Use Terra with medium or high reasoning for routine production investigation
  or implementation that needs sound judgment across a bounded surface.
- Use Sol with medium reasoning for ambiguous, cross-cutting, synthesis-heavy,
  adversarial, or high-consequence lanes.
- Keep the root on Sol for decomposition, conflict resolution, integrated
  verification, and final acceptance.

Prefer the least expensive profile that can reliably satisfy the lane's
completion criteria. If the custom Luna role is unavailable in a stale task,
report the discovery mismatch and use a fresh task before silently substituting
another role. When explicitly overriding a spawned agent's model or reasoning,
use `fork_turns: "none"` or a bounded positive history count; a full-history
fork inherits the parent profile.

## Dispatch bounded prompts

Each lane prompt must state:

- the exact outcome and why the lane exists;
- scope, ownership, dependencies, and non-goals;
- permission boundaries and prohibited external or destructive actions;
- completion criteria and exact validation;
- evidence to return: files, commands, results, uncertainty, and residual risk;
- awareness that other agents may be active and that their edits must not be
  reverted; and
- stop conditions for dependency, authority, overlap, or diminishing value.

Do not leak unnecessary full-thread context. Use only the agent names, schemas,
model overrides, and history controls exposed in the current session. Create a
separate visible task only when the user explicitly asks for that product
surface or needs independent continuation.

## Monitor and reconcile

- Observe by agent ID and update the ledger with concrete progress or evidence.
- Send follow-ups only when they supply missing evidence, resolve a conflict, or
  correct scope. Do not create busywork to keep slots occupied.
- Wait only when a lane blocks further useful root work.
- Treat lane completion reports as leads, not acceptance.
- Inspect the integrated state, resolve contradictory findings, check mutation
  ownership, and rerun validation across the combined result.
- Close or retire completed lanes when no follow-up is needed.

Use goal tools only when the user explicitly requests goal-driven pursuit.
Explicit invocation of this skill requests orchestration, not automatically a
persisted goal.

## Completion

Finish only when the root has reconciled every material lane, independently
verified the integrated result, and reported:

- lanes and models used;
- files or systems changed;
- validation commands and outcomes;
- conflicts or discarded findings;
- usage or concurrency limits encountered; and
- remaining risk or uncertainty.

Example invocation:

```text
$parallel-orchestrator Split this repository audit into independent lanes.
Start with four, expand only if the ledger shows more ready work, and keep final
acceptance in the root task.
```
