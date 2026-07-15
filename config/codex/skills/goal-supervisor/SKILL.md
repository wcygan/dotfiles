---
name: goal-supervisor
description: "Supervise a difficult Codex task through a separate visible worker task. Use when the user asks for a supervisor/worker workflow, delegated implementation with oversight, evidence-based steering, independent verification, or distinct goals across Codex tasks."
---

# Goal Supervisor

Supervise a difficult implementation in a separate visible Codex task while the current task owns oversight and acceptance.

## Shared loop contract

Before delegation, read and apply ../loop-protocol/SKILL.md completely. Treat each observe, compare, steer, and verify pass as one bounded cycle with explicit progress and stopping evidence.

Goal Supervisor specializes that baseline by assigning mutation to one visible worker, keeping acceptance with the supervisor, and using distinct goal state only when this workflow was explicitly invoked. Its rules may tighten the shared protocol but never weaken its scope, authority, one-writer, rollback, wakeup, or terminal-evidence boundaries.

## Operating model

- Treat the supervisor and worker as separate tasks with separate context, permissions, and goal state. A goal created in one task never creates or updates a goal in the other.
- Use a visible Codex task for the worker. Internal subagents are implementation details of the current task; they are not visible tasks and are not a substitute for this workflow.
- Keep the supervisor responsible for scope, steering, independent verification, and the final completion decision. The worker is responsible for implementation and its own narrow validation.
- Check which task-management and goal tools are actually available before acting. Codex Desktop commonly exposes `list_projects`, `create_thread`, `read_thread`, and `send_message_to_thread`; use the names and schemas present in the current session. Never invent a tool or imply that an unavailable capability exists.

## Model profile

Use this standing profile unless the user explicitly requests different settings:

- **Supervisor:** `gpt-5.6-sol` with `high` reasoning. The current visible task is the supervisor, so its model must be selected before invoking this workflow; task-creation tools cannot change the calling task's model.
- **Worker:** `gpt-5.6-terra` with `medium` reasoning. Pass these values explicitly when creating the worker task, using the model and reasoning fields exposed by the available task-creation tool.

When the session exposes the supervisor's current model settings, verify them before delegation. If it does not, state that the supervisor profile is assumed rather than verified. If either model or reasoning level is unavailable on the selected host, stop and report the mismatch instead of silently substituting another profile.

Keep the worker on Terra with medium reasoning for follow-up turns by omitting model overrides when steering it. Change either role's profile only when the user explicitly requests the change.

## 1. Define acceptance before delegation

Read the current project instructions and inspect the real checkout. Record:

- the requested deliverable and non-goals;
- files or systems the worker may change;
- permission boundaries, including whether commits, pushes, deployments, or external writes are allowed;
- the narrow validation command and any broader project preflight;
- observable completion criteria;
- the starting branch, checkout path, and `git status --short` when Git is involved.

Resolve material ambiguity before starting the worker. Preserve existing user changes and do not silently broaden authority.

## 2. Establish distinct goals

Use goal tools only when the user explicitly requests goal-driven pursuit. Explicitly invoking this skill for the supervisor/worker workflow counts as that request.

1. Create the supervisor goal in the current task. Phrase it around supervising, steering, independently verifying, and accepting the deliverable.
2. Put a separate implementation goal in the worker prompt and instruct the worker to create that goal in its own task before editing.
3. Read the worker task after it starts. If the session exposes the worker's goal tool events or goal state, verify creation there. Otherwise require the worker to report its goal creation and status, and label that evidence as worker-reported rather than independently observed. Never infer it from the supervisor's goal state.
4. Keep the supervisor goal active through recoverable technical obstacles. Mark it complete only after independent acceptance checks pass.

Example goal split:

- Supervisor: `Supervise and independently verify <deliverable>; accept it only when <checks> pass.`
- Worker: `Implement <deliverable> within <scope>; keep working through technical obstacles until <checks> pass.`

## 3. Create the worker in the correct environment

Use the available project-listing capability before creating the task. Match the saved Codex project to the actual repository or workspace; do not create project-scoped work in a generic or guessed location.

Choose the environment deliberately:

- **Shared checkout:** Use the project's local environment when the worker can be the only writer. While it runs, the supervisor may inspect but must not edit the shared checkout. This avoids racing writes and ambiguous ownership.
- **Worktree:** Use an isolated worktree when both tasks may need to write, when experimentation is risky, or when the worker needs branch isolation. Record the returned checkout details and inspect that exact worktree during verification. Do not assume changes appear in the supervisor checkout.

If neither supported environment provides the required source state, stop and explain the mismatch instead of creating the task in the wrong place.

Create one visible worker task with a prompt containing:

- the exact implementation goal and an instruction to create it locally;
- the verified project path and applicable instruction files to read;
- scope, non-goals, and permission limits;
- the writer/isolation rule;
- acceptance criteria and validation commands;
- a requirement to report its goal creation result and final goal status;
- a requirement to report concrete evidence: changed files, command exit results, and unresolved uncertainty;
- a requirement not to mark its goal complete merely because code was written.

Create the worker with `model: "gpt-5.6-terra"` and medium reasoning. Use the exact reasoning field name exposed by the tool, such as `thinking: "medium"`. This standing profile is the user's explicit preference; do not omit it and fall back to the general Codex default.

## 4. Monitor and steer with evidence

Store the worker task identifier and host or checkout details returned by task creation. Then repeat this loop while the supervisor goal is active:

1. Read the worker task, including relevant command output when available.
2. Compare its current state with the acceptance criteria and the actual checkout.
3. Separate progress, a recoverable error, inactivity, and a genuine blocker.
4. Send a follow-up only when it adds concrete information or a needed correction.
5. Re-read after the worker responds; do not assume a message was followed.

Use corrective prompts with this shape:

```text
Observed: <specific gap or failure>
Evidence: <file, diff, command output, or requirement>
Required correction: <bounded next action>
Validate with: <exact check>
Stop and report if: <permission boundary or genuine blocker>
```

Avoid vague prompts such as "keep trying". Do not take over edits in a shared checkout until the worker has stopped or explicitly relinquished writer ownership.

## 5. Verify independently

A worker's completion message and copied test output are leads, not acceptance evidence. After the worker reports completion:

1. Read its final task state. Confirm its implementation goal status only through goal state or tool evidence the current session exposes; otherwise record the status as worker-reported. This limitation does not relax deliverable verification.
2. Inspect the target checkout directly: status, untracked files, diff, and relevant file contents.
3. Compare the final state with the recorded baseline so user-owned changes are not attributed to the worker.
4. Check scope, maintainability, secrets, generated state, and permission compliance.
5. Run the narrowest meaningful validation yourself.
6. Run the broader project preflight when the repository instructions or blast radius require it.
7. If a check fails, send the failure evidence and a bounded correction back to the worker, then repeat verification.

Use exit status and relevant output as evidence. Do not accept "tests passed" without either independently rerunning the tests or inspecting an equally authoritative artifact.

## 6. Respect stopping and wakeup boundaries

Stop or ask the user when work requires new authority, an irreversible action, unavailable credentials, a material product choice, or access outside the approved scope. Treat a hard problem as recoverable until evidence shows a genuine blocker; follow the active goal tool's blocker rules rather than declaring one early.

Do not promise continuous supervision after ending the current turn. If monitoring must resume later, use an available and authorized goal continuation, heartbeat, automation, or other wakeup mechanism. If none exists, state that supervision resumes only when the task is invoked again.

Honor user cancellation immediately. Do not commit, push, merge, deploy, archive tasks, or mutate external systems unless the user authorized that action.

## Completion criteria

Complete the supervisor goal only when all of these are true:

- the worker operated in the intended project and environment;
- the worker's goal status is either externally observed or clearly labeled worker-reported, and the deliverable itself is final;
- the final diff contains only authorized changes;
- the supervisor independently inspected the deliverable;
- required narrow and broad checks pass;
- no unresolved permission issue, blocker, or material uncertainty remains;
- the final report identifies the worker task, changed files, validation commands and results, and any residual risk.

Example invocation:

```text
$goal-supervisor Have a separate Codex task implement the requested parser in this project. Keep that worker as the only writer, steer it from this task, independently rerun the tests, and do not commit or push.
```
