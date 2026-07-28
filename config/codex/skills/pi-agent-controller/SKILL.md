---
name: pi-agent-controller
description: "Control and delegate bounded tasks to the Pi coding agent CLI. Use when composing self-contained Pi prompts, invoking discovered Pi skills, running one-shot `pi --no-session -p` jobs, checking whether a local model is actually available, or independently validating Pi's work."
---

# Pi Agent Controller

Use Pi as a bounded local agent. Give it enough context to complete the task
without relying on an unstated plan or on the calling model's conversation.

## Establish the contract

Before invoking Pi:

1. Read and apply `../pi-coding-agent/SKILL.md` completely for version-current
   CLI behavior and safety rules.
2. Define the outcome, allowed scope, non-goals, validation, and stopping
   conditions.
3. Inspect the target checkout and its instruction files. Preserve existing
   changes and identify whether Pi may only inspect or may also edit.
4. Treat Pi's tool access, file mutations, commits, pushes, and external writes
   as separate authority. Calling Pi grants none of them implicitly.

Pi is an executor whose output must be checked. The caller owns task framing,
permission boundaries, and final acceptance.

## Verify that local inference is available

Do not confuse a configured model with a running model. `pi --list-models` can
show configured entries even when their servers are unavailable.

1. Establish the installed CLI:

   ```bash
   command -v pi
   pi --version
   pi --help
   ```

2. Determine the intended local provider, model, and endpoint from current
   runtime evidence. Redact secrets when inspecting Pi configuration.
3. For the usual llama.cpp endpoint, probe both service health and model
   identity:

   ```bash
   curl --fail --silent --show-error --max-time 2 \
     http://127.0.0.1:8080/health
   curl --fail --silent --show-error --max-time 2 \
     http://127.0.0.1:8080/v1/models
   ```

4. If the endpoint is reachable, run a minimal Pi smoke test with the intended
   provider and model when they are known:

   ```bash
   pi --offline --provider <provider> --model <model-id> \
     --no-session --no-tools -p "Reply exactly: PI_READY"
   ```

`--offline` disables Pi's startup network operations; it does not select a local
provider or prove that a local server is running.

If the probes or smoke test fail, stop before delegating the real task. Report
that the target local model is unavailable, distinguish "nothing is listening
at this endpoint" from "no local model exists anywhere," and include the
observed error. Do not silently fall back to a cloud model.

Suggest this known GLM llama.cpp launch command when it fits the user's intended
model:

```bash
llama-server \
  -hf ggml-org/GLM-4.7-Flash-GGUF:Q4_K \
  --alias glm47-flash \
  --host 127.0.0.1 \
  --port 8080 \
  -c 202752 \
  -ngl 99 \
  --no-ui
```

Starting that server can download a large model and consume substantial memory
and GPU resources. Suggest the command by default; run it only when the user
explicitly asks to start the model. After startup, repeat the health, identity,
and Pi smoke checks.

## Build a self-contained prompt

Read [references/standalone-prompt.md](references/standalone-prompt.md) and
include every section material to the task. A fresh `--no-session` call has no
earlier conversational state, so restate corrections and decisions instead of
referring to "the previous answer."

Prefer concrete context:

- exact checkout and relevant files;
- current behavior and observed evidence;
- desired outcome and explicit non-goals;
- files or systems Pi may change;
- applicable project instructions;
- required commands and observable success criteria;
- permission and stop boundaries;
- the exact report Pi must return.

Attach authoritative files with `@file` arguments when that is clearer than
pasting their contents. Do not attach secrets, credentials, or irrelevant
context.

## Invoke discovered Pi skills directly

Leave skill discovery enabled and use the slash-command form to force one
discovered skill to load without a filesystem path:

```bash
pi --offline --no-session -p \
  "/skill:mysql Review this schema. Require measured evidence and a safe rollout."
```

`/skill:<name>` loads the discovered skill's full instructions and appends the
remaining text as the user task. Do not add `--no-skills` for this pattern.

Use the task's primary skill and make the rest of the prompt self-contained.
Confirm the skill name from Pi's discovered catalog when uncertain rather than
guessing it.

## Choose the least authority Pi needs

For inspection, review, explanation, or planning:

```bash
pi --offline --no-session \
  --tools read,grep,find,ls \
  -p "<self-contained prompt>"
```

For an authorized implementation:

```bash
pi --offline --no-session \
  --tools read,grep,find,ls,bash,edit,write \
  -p "<self-contained prompt>"
```

The built-in tools are `read`, `bash`, `edit`, `write`, `grep`, `find`, and
`ls`. `grep`, `find`, and `ls` are off by default unless enabled. `bash` can
mutate state, so omit it for structurally read-only work. `--no-session`
prevents session persistence; it does not prevent file or external mutations.

Add `--provider` and `--model` when deterministic model selection matters. If
the local discovery integration reliably selects the currently deployed model,
record what it selected and still verify `/v1/models` before the substantive
run.

## Run, observe, and correct

1. Run one bounded Pi call from the intended working directory.
2. Record its exit status and preserve the useful output.
3. Inspect actual files, diffs, and command evidence independently. Treat Pi's
   completion claim as a lead, not proof.
4. If the output is incomplete or unsupported, issue another self-contained
   `--no-session` prompt containing the observed gap, required correction,
   validation, and stop boundary.
5. Stop when acceptance checks pass, the local model is unavailable, Pi reaches
   the stated boundary, or further work needs new user authority.

Do not ask Pi to commit, push, deploy, delete data, or contact external systems
unless the user authorized that exact action.

## Completion report

Report:

- Pi version, working directory, selected provider/model, and discovered skill;
- the command shape and tool allowlist used;
- whether the local endpoint and model identity were verified;
- Pi's result plus the caller's independent validation;
- files or external state changed; and
- any unavailable model, unresolved uncertainty, or permission boundary.

Example invocation:

```text
$pi-agent-controller Use the locally deployed Pi model to review this repository
with its mysql skill. Build a standalone read-only prompt, use no session, and
independently check the result.
```
