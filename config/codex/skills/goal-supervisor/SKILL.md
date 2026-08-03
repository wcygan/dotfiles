---
name: goal-supervisor
description: "Supervise one or more difficult Codex work lanes through bounded native subagents. Use when the user asks for a supervisor/worker workflow, multi-worker delegated implementation, goal-driven pursuit with oversight, evidence-based steering, independent verification, or a separate visible worker task."
---

# Goal Supervisor

Supervise a difficult outcome from the current task while one or more bounded
workers perform delegated lanes. Keep goal ownership, steering, integration,
and final acceptance with the supervisor.

## Shared contracts

Before delegation, read and apply `../loop-protocol/SKILL.md` completely. Treat
each observe, compare, steer, and verify pass as one bounded cycle with explicit
progress and stopping evidence.

When two or more independent lanes are useful, also read and apply
`../parallel-orchestrator/SKILL.md` completely. Use its concurrency ledger,
staged fan-out, model routing, ownership, and synthesis rules. Goal Supervisor
adds aggregate goal state, lane-level acceptance, and corrective oversight; it
never weakens either shared contract's authority, rollback, budget, plateau,
wakeup, or terminal-evidence boundaries.

## Operating model

- Keep the current task as supervisor. It owns scope, the aggregate goal,
  topology selection, steering, integration, independent verification, and the
  final completion decision.
- Use **single-worker mode** for coupled implementation, one trust-critical
  mutation surface, or work whose steps depend tightly on one another.
- Use **multi-worker mode** when the outcome contains at least two independent
  ready lanes with distinct deliverables, ownership, and validation. Start with
  2–4 workers and expand only through the parallel-orchestrator evidence gates.
- Prefer native subagent tools. Native workers remain in the supervisor's
  orchestration context and can be steered, waited on, interrupted, and closed
  by agent ID.
- Use a separate visible task only when the user explicitly asks for a
  standalone task, needs a saved project or selectable worktree, or intends to
  continue the worker independently.
- Treat native subagents and visible tasks as different surfaces. Never claim a
  custom role was loaded when the selected creation tool accepted only model
  and reasoning overrides.
- Inspect the agent, task-management, and goal tools exposed in the current
  session. Use only their available names and schemas.

Parallel reads, exploration, tests, triage, and independent review are usually
safe first lanes. Keep one mutating owner per checkout, branch, or external
resource. Use separate worktrees or independently bound resources for truly
concurrent mutation; otherwise retain one implementation writer and make the
other lanes read-only. Never create nominally separate write lanes that
converge on the same coupled seam.

## Worker and lane identity

Maintain one supervisor ledger with these fields:

| Lane | Required? | Agent ID | Role / model / effort | Goal or objective | Ownership | Dependencies | Validation | Status / evidence | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Give every lane a stable name. For each native subagent, record the returned
agent ID, nickname, agent type, selected profile, and workspace when exposed.
Use the agent ID for every follow-up, wait, interrupt, or close operation.

For a separate visible-task fallback, record its task ID, host, checkout,
profile, and title. When title management is available:

- Rename the current task to `[Supervisor] <base title>`.
- Number ordinary workers from 1 and name them `[Worker N] <base title>`.
- Name an exceptional Sol worker `[smart-worker] <base title>`.
- Remove all consecutive leading `[Supervisor] `, `[Worker N] `, or
  `[smart-worker] ` prefixes before applying exactly the intended prefix.
- Verify a rename through its result or a direct task read rather than stale
  list or search indexing.

If title management is unavailable, continue with recorded IDs. A title or
nickname is never task identity.

## Model profile

Use this standing profile unless the user explicitly requests otherwise:

- **Supervisor:** `gpt-5.6-sol` with `high` reasoning by default; use `xhigh`
  only for especially difficult oversight. Select that profile before invoking
  the workflow because the current task cannot retune itself.
- **Standard implementation worker:** native `agent_type: "worker"` with
  `model: "gpt-5.6-terra"` and `reasoning_effort: "high"` for bounded
  production work requiring judgment.
- **Economical lane:** native `agent_type: "luna_lane"` for narrow,
  repeatable, read-heavy, high-volume, focused coding, or routine validation
  work. Its custom agent file owns its model and medium reasoning profile.
- **Exceptional worker:** `gpt-5.6-sol` with `high` reasoning only when the user
  requests it or concrete evidence shows Terra is unsuitable. Explain the
  deviation before creation and never switch profiles silently.
- **Visible-task fallback:** when the launcher has no role selector, apply the
  equivalent model and reasoning explicitly and include the bounded worker
  contract in the prompt.

Route each multi-worker lane through the parallel-orchestrator model rules.
When explicitly overriding a native worker's model or reasoning, use
`fork_turns: "none"` or a bounded positive history count. A full-history fork
inherits the parent profile. Preserve a worker's creation-time profile on
follow-ups by omitting model and reasoning overrides.

If a required custom role or model profile is not discovered, report the stale
registry mismatch and try a fresh task or Codex restart before substituting an
equivalent profile. Do not promote an existing worker after a recoverable error.

## 1. Define aggregate and lane acceptance

Read the project instructions and inspect the real checkout. Record:

- the aggregate deliverable and non-goals;
- permission boundaries, including commits, pushes, deployments, and external
  writes;
- the starting branch, checkout path, and `git status --short` when Git applies;
- the narrow validation for each lane and the integrated project preflight;
- observable aggregate completion criteria; and
- each lane's deliverable, required or optional status, ownership, dependencies,
  completion criteria, and stop conditions.

Resolve material ambiguity before spawning. Preserve existing user changes and
do not silently broaden authority. If the work cannot be split without shared
mutation or sequencing conflicts, choose single-worker mode.

## 2. Establish goal state

Use goal tools only when the user explicitly requests goal-driven pursuit.
Explicit invocation of this skill counts as that request.

1. Create one supervisor goal around decomposing, supervising, steering,
   integrating, independently verifying, and accepting the aggregate outcome.
2. Give every worker a separate bounded lane objective. Never treat the
   supervisor goal as shared worker state.
3. If a worker surface exposes goal tools, instruct that worker to create and
   manage its own lane goal. Otherwise keep the objective as worker-local
   runtime state and label its status as worker-reported.
4. Record lane dependencies and whether each lane is required or optional. A
   blocked optional lane may be excluded with a recorded reason; a required
   lane must be accepted, replaced within budget, or reported as blocking the
   aggregate goal.
5. Keep the supervisor goal active through recoverable lane failures. Complete
   it only after every required lane and the integrated result are accepted.

## 3. Dispatch the selected topology

For single-worker mode, spawn one bounded worker. A typical explicit Terra
worker call uses:

```text
agent_type: "worker"
fork_turns: "none"
model: "gpt-5.6-terra"
reasoning_effort: "high"
message: <bounded lane prompt>
```

For multi-worker mode:

1. Build the complete initial ledger before dispatch.
2. Spawn the first 2–4 ready independent lanes together with the role or model
   selected for each lane.
3. Record every returned agent ID before sending follow-ups.
4. Expand only when the parallel-orchestrator ledger shows more independent
   ready work with sufficient expected value.
5. Do not allow recursive delegation unless a lane has explicitly assigned
   child work and concurrency budget.

Provide lean, self-contained prompts rather than unnecessary full-thread
history. Every worker prompt must include:

- the exact lane objective and its contribution to the aggregate outcome;
- the verified project path and applicable instruction files;
- scope, ownership, dependencies, non-goals, and permission limits;
- awareness that other workers may be active and their edits must not be
  reverted;
- lane acceptance criteria and exact validation;
- evidence to report: files, commands, exits, findings, uncertainty, and risk;
- whether worker-local goal creation is required and available; and
- stop conditions for missing authority, dependency, overlap, or diminishing
  value.

For visible-task fallbacks, list projects first and select the exact saved
project. Choose shared checkout versus worktree deliberately and preserve the
same ownership rules.

## 4. Monitor and steer the worker set

Repeat this bounded loop while the supervisor goal is active:

1. Observe every active lane through the matching surface and update its ledger
   row with concrete evidence.
2. Compare each lane with its acceptance criteria, dependencies, and actual
   checkout state.
3. Separate progress, recoverable error, inactivity, dependency wait, optional
   exclusion, and genuine blocker.
4. Send a follow-up only when it adds evidence, resolves a dependency or
   ownership conflict, or supplies a bounded correction.
5. Re-observe after a response; never assume a correction was followed.

Use this correction shape:

```text
Observed: <specific lane gap or failure>
Evidence: <file, diff, command output, or requirement>
Required correction: <bounded next action>
Validate with: <exact check>
Stop and report if: <permission, dependency, overlap, or blocker boundary>
```

Do not wait on workers one by one when other lanes or root work remain useful.
Use the available multi-agent status or wait surface to react to whichever lane
completes or needs attention. One blocked lane must not stall unrelated lanes.
Do not take over a shared mutation surface until its worker stops or explicitly
relinquishes ownership.

Retry or replace a failed lane only when it remains required, the failure is
recoverable, the new attempt is meaningfully different, and budget remains.
Record the replacement rather than silently losing the original evidence.

## 5. Accept lanes and integrate independently

A worker completion message is a lead, not acceptance evidence.

For each lane:

1. Inspect the worker's final status and evidence. Label goal status as
   worker-reported unless directly exposed.
2. Inspect the assigned checkout, files, diff, or external state directly.
3. Confirm ownership and permission compliance and distinguish baseline user
   changes from lane changes.
4. Run the lane's narrow validation independently.
5. Mark the lane accepted, send a bounded correction to the same worker, or
   record an explicit exclusion or blocker.

After required lanes are individually accepted:

1. Reconcile contradictory findings and overlapping assumptions.
2. Inspect the combined diff and untracked files against the original baseline.
3. Run cross-lane, integration, and broader repository validation.
4. Verify the aggregate completion criteria on the integrated state.

Close completed native agents only after their output and changes are safely
captured and no correction remains. Do not archive visible tasks unless
authorized.

## 6. Respect stopping and wakeup boundaries

Stop or ask the user when work requires new authority, an irreversible action,
unavailable credentials, a material product choice, or access outside scope.
Treat hard technical work as recoverable until evidence establishes a blocker.

Apply the parallel-orchestrator concurrency, usage, and diminishing-return
stopping rules. Do not preserve workers merely to fill slots. Honor cancellation
immediately.

Do not promise supervision after ending the current turn. Use an authorized
continuation, automation, or other wakeup mechanism when monitoring must resume.
Do not commit, push, merge, deploy, archive, or mutate external systems unless
the user authorized that action.

## Completion criteria

Complete the supervisor goal only when:

- every required lane is accepted or explicitly reported as blocking;
- optional exclusions and worker replacements are recorded;
- the final integrated state contains only authorized changes;
- the supervisor independently inspected every material lane and the combined
  deliverable;
- required narrow, cross-lane, and broad checks pass;
- no unresolved permission issue or material uncertainty remains; and
- the final report lists every worker ID and profile, lane objective, goal
  status, ownership, evidence, corrections, acceptance result, validation, and
  residual risk.

Example single-worker invocation:

```text
$goal-supervisor Use one Terra high worker to implement this coupled parser
change. Steer it with evidence, independently rerun the tests, and do not commit.
```

Example multi-worker invocation:

```text
$goal-supervisor Supervise this feature through independent implementation,
test, and documentation workers. Keep separate lane goals and ownership, start
with three workers, and accept every lane plus the integrated result yourself.
```
