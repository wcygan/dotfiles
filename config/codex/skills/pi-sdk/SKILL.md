---
name: pi-sdk
description: "Build, debug, or explain TypeScript integrations with the Pi coding agent SDK. Use for @earendil-works/pi-coding-agent, createAgentSession, AgentSession, AgentSessionRuntime, ModelRuntime, ResourceLoader, custom tools, SDK events, in-process agent embedding, or questions about the version-matched Pi SDK docs."
---

# Pi SDK

Use the Pi TypeScript SDK for in-process integrations with Pi's coding agent.
Ground every API name, import, option, and event in documentation or types that
match the installed Pi version. Do not infer SDK behavior from the CLI alone.

## Workflow

1. Read [reading.md](references/reading.md) to identify the installed package,
   SDK documentation, version, and any source-checkout mismatch.
2. Read [patterns.md](references/patterns.md) for the part of the SDK the task
   uses: sessions, runtime replacement, events, tools, resources, models, or
   run modes.
3. If the application uses Effect v4, read
   [effect-integration.md](references/effect-integration.md) and the applicable
   branches of the repository's [Effect skill](../effect/SKILL.md).
4. If the application should use a ChatGPT Plus/Pro Codex subscription, read
   [openai-codex-subscription.md](references/openai-codex-subscription.md).
5. Prefer the smallest surface that meets the requirement:
   - SDK for in-process TypeScript control;
   - RPC for process isolation or language-independent control;
   - CLI/print/JSON mode for shell-level automation.
6. Inspect the project’s package manager, TypeScript configuration, and existing
   integration conventions before adding imports or dependencies.
7. Validate with the project’s narrowest meaningful typecheck, test, or smoke
   command. Report the Pi version, package/docs source, files inspected, and
   any mismatch or unverified assumption.

## Safety boundaries

- A session can expose `bash`, `edit`, and `write`; use an explicit read-only
  tool allowlist (`read`, `grep`, `find`, `ls`) for documentation or inspection
  tasks.
- Do not print, copy, commit, or hard-code `auth.json`, API keys, OAuth tokens,
  provider headers, `models.json` secrets, sessions, or machine-specific paths.
- `ModelRuntime` may read Pi credentials and model configuration. Prefer an
  in-memory credential store or explicit non-persisting runtime overrides when
  a test needs credentials, and never expose their values.
- Do not silently fall back from a requested local model or provider to a cloud
  provider. Verify the selected model and endpoint separately.
- Do not install packages, alter Pi settings, or run an agent with write tools
  merely to answer a documentation question.

## API routing

- Basic prompt, streaming text, abort, or cleanup: `AgentSession`.
- New session, switch, fork, clone, or JSONL import: `AgentSessionRuntime`.
- Prompt queueing during a stream: `steer()` versus `followUp()`; read the
  version-matched prompt behavior before choosing.
- Custom tools: `defineTool()` and `customTools`, or an extension when the
  behavior needs lifecycle hooks, commands, or UI.
- Skills, extensions, prompt templates, themes, and context files: use a
  `ResourceLoader`; check `cwd` and `agentDir` discovery semantics.
- Model selection and authentication: use `ModelRuntime`; distinguish model
  resolution from credential availability.
- Effect integration: wrap the SDK at a service/layer boundary; do not spread
  raw `AgentSession` or provider state through unrelated application code.

## Completion checklist

- [ ] Installed `pi` version and package scope were checked.
- [ ] The matching `sdk.md`, types, source, or official docs were read.
- [ ] SDK, RPC, and CLI boundaries are explicit.
- [ ] Tools and credential behavior are least-privilege and non-leaking.
- [ ] The integration was typechecked/tested or the validation limitation is
      stated plainly.
