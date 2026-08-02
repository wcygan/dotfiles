---
name: goal-supervisor
description: "Supervise a difficult Codex task through a bounded native subagent. Use when the user asks for a supervisor/worker workflow, delegated implementation with oversight, evidence-based steering, independent verification, or a separate visible worker task."
---

# Goal Supervisor

Supervise a difficult implementation from the current task while a bounded
worker performs the delegated work. Prefer a native custom subagent; create a
separate visible task only when its distinct product behavior is required.

## Shared loop contract

Before delegation, read and apply ../loop-protocol/SKILL.md completely. Treat
each observe, compare, steer, and verify pass as one bounded cycle with explicit
progress and stopping evidence.

Goal Supervisor specializes that baseline by assigning mutation to one worker,
keeping acceptance with the supervisor, and using distinct goal state only when
the relevant worker surface exposes it. Its rules may tighten the shared
protocol but never weaken its scope, authority, one-writer, rollback, wakeup,
or terminal-evidence boundaries.

## Operating model

- Keep the current task as supervisor. It owns scope, steering, independent
  verification, and the final completion decision.
- Prefer the native subagent tools: spawn `agent_type: "luna_worker"`, steer
  with the available agent-input tool, wait only when blocked on its result,
  and close completed agents when they are no longer needed.
- A native subagent is the default because it loads the reusable custom-agent
  configuration and remains part of the supervisor's orchestration context.
- Use a separate visible task through the task-creation tools only when the user
  explicitly asks for a standalone task, needs a saved project or selectable
  worktree environment, or intends to continue the worker independently.
- Treat native subagents and visible tasks as different surfaces. Never claim a
  custom agent was loaded when the selected creation tool only accepted model
  and reasoning overrides.
- Check which agent, task-management, and goal tools are available before
  acting. Use only the names and schemas present in the current session.

## Worker identity

For a native subagent, record the returned agent ID, nickname, agent type,
selected profile, and workspace when exposed. Use the agent ID for every wait,
steer, or close action; a nickname is only a human-facing label.

For a separate visible-task fallback, record its task ID, host, checkout, model,
reasoning, and title. When task-title management is available:

- Rename the current supervisor task to `[Supervisor] <base title>`.
- Number Luna workers from 1 and name them `[Worker N] <base title>`.
- Name an exceptional Sol worker `[smart-worker] <base title>`.
- Before applying a role, remove all consecutive leading recognized prefixes
  matching `[Supervisor] `, `[Worker N] `, or `[smart-worker] `, then apply
  exactly the intended prefix.
- Verify a rename through its result or a direct task read. Do not rely on stale
  list or search indexing.

If title management is unavailable, continue with recorded IDs. Never treat a
title or nickname as task identity.

## Model profile

Use this standing profile unless the user explicitly requests different
settings:

- **Supervisor:** `gpt-5.6-sol` with `high` reasoning by default; use `xhigh`
  only for especially difficult oversight. The current task must already have
  that profile because worker tools cannot retune it.
- **Preferred worker:** native `agent_type: "luna_worker"`. Its custom agent
  file owns `gpt-5.6-luna`, `max` reasoning, and the bounded delegated-work
  instructions. Do not duplicate model or reasoning overrides when spawning it.
- **Visible-task fallback:** when a separate task is required and its launcher
  has no custom-agent selector, pass `model: "gpt-5.6-luna"` and
  `thinking: "max"`, and include the bounded delegated-work contract in the
  prompt.
- **Exceptional fallback:** use a `gpt-5.6-sol` Smart Worker with `high`
  reasoning only when the user explicitly requests it or concrete task evidence
  shows the preferred Luna profile is unsuitable. Explain the deviation before
  creation and never switch profiles silently.

When the supervisor profile is exposed, verify it before delegation; otherwise
state that it is assumed. If `luna_worker` is not recognized, report the
discovery mismatch and try a fresh task or Codex restart before using an
equivalent profile. Preserve a worker's selected profile on follow-ups by
omitting model and reasoning overrides. Do not promote an existing Luna worker
to Smart Worker after a recoverable error.

## 1. Define acceptance before delegation

Read the project instructions and inspect the real checkout. Record:

- the requested deliverable and non-goals;
- files or systems the worker may change;
- permission boundaries, including commits, pushes, deployments, and external
  writes;
- the narrow validation command and broader project preflight;
- observable completion criteria; and
- the starting branch, checkout path, and `git status --short` when Git applies.

Resolve material ambiguity before spawning. Preserve existing user changes and
do not silently broaden authority.

## 2. Establish goal state

Use goal tools only when the user explicitly requests goal-driven pursuit.
Explicit invocation of this skill counts as that request.

1. Create the supervisor goal in the current task around supervising, steering,
   independently verifying, and accepting the deliverable.
2. Give the worker a separate bounded implementation objective.
3. If the worker surface exposes goal tools, instruct it to create its own goal
   and verify or obtain its reported status. Otherwise treat the delegated
   objective as worker-local runtime state and do not imply a goal object exists.
4. Keep the supervisor goal active through recoverable technical obstacles and
   complete it only after independent acceptance passes.

## 3. Spawn the worker

For the default native path, spawn exactly one worker with:

```text
agent_type: "luna_worker"
fork_context: false
message: <bounded worker prompt>
```

Use `fork_context: true` only when the worker genuinely needs the current
conversation history and that context is safe and useful. Otherwise provide a
lean, self-contained prompt containing:

- the exact implementation objective;
- the verified project path and applicable instruction files;
- scope, non-goals, and permission limits;
- the sole-writer or disjoint-write ownership rule;
- acceptance criteria and validation commands;
- concrete evidence to report: changed files, command exits, and uncertainty;
- whether worker-local goal creation is required and available; and
- stop conditions, including missing authority or overlapping user changes.

For a visible-task fallback, list projects first, select the exact saved
project, and choose local versus worktree deliberately. Keep a shared-checkout
worker as the only writer; when using a worktree, record and verify that exact
checkout. Apply the visible-task model profile and identity rules above.

## 4. Monitor and steer with evidence

Repeat this bounded loop while the supervisor goal is active:

1. Observe worker progress through the matching surface: agent status/results
   for native workers, or direct task reads for visible workers.
2. Compare progress with the acceptance criteria and actual checkout.
3. Separate progress, recoverable error, inactivity, and genuine blocker.
4. Send a follow-up only when it adds concrete evidence or a needed correction.
5. Re-observe after the worker responds; never assume a message was followed.

Use this correction shape:

```text
Observed: <specific gap or failure>
Evidence: <file, diff, command output, or requirement>
Required correction: <bounded next action>
Validate with: <exact check>
Stop and report if: <permission boundary or genuine blocker>
```

For native agents, wait sparingly and only when their result blocks the next
supervisor action. Continue useful non-overlapping supervisor work while they
run. Do not take over edits in a shared checkout until the worker has stopped or
relinquished ownership.

## 5. Verify independently

A worker completion message is a lead, not acceptance evidence. After it stops:

1. Inspect its final status and report. Label worker goal status as
   worker-reported unless independently exposed.
2. Inspect the target checkout directly: status, untracked files, diff, and
   relevant contents.
3. Compare final state with the recorded baseline so user-owned changes are not
   attributed to the worker.
4. Check scope, maintainability, secrets, generated state, and permission
   compliance.
5. Run the narrowest meaningful validation yourself, then the broader preflight
   required by the repository or blast radius.
6. Send bounded failure evidence back to the same worker when correction is
   still possible; then verify again.

Close a completed native agent after its output and changes are safely captured
and no follow-up is needed. Do not archive a visible task unless authorized.

## 6. Respect stopping and wakeup boundaries

Stop or ask the user when work requires new authority, an irreversible action,
unavailable credentials, a material product choice, or access outside scope.
Treat hard technical work as recoverable until evidence establishes a blocker.

Do not promise supervision after ending the current turn. Use an authorized
continuation, automation, or other wakeup mechanism when monitoring must resume.
Honor cancellation immediately. Do not commit, push, merge, deploy, archive,
or mutate external systems unless the user authorized that action.

## Completion criteria

Complete the supervisor goal only when:

- the worker used the intended agent type and workspace, or a disclosed
  visible-task fallback;
- the final diff contains only authorized changes;
- the supervisor independently inspected the deliverable;
- required narrow and broad checks pass;
- no unresolved permission issue, blocker, or material uncertainty remains; and
- the final report identifies the worker, files changed, validation commands,
  results, and residual risk.

Example invocation:

```text
$goal-supervisor Use a Luna worker to implement the parser in this project.
Keep it bounded, steer it with evidence, independently rerun the tests, and do
not commit or push.
```
