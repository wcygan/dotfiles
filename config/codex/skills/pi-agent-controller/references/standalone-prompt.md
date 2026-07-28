# Standalone Pi Prompt

Use this structure for a fresh `pi --no-session -p` task. Remove sections that
truly do not apply, but do not rely on context from the caller's conversation.

```text
Role
You are responsible for the bounded task below. Work from inspected evidence
and do not assume missing state.

Outcome
<Concrete deliverable or question to answer.>

Working context
- Checkout: <absolute or clearly resolved working directory>
- Relevant files: <paths>
- Current behavior: <observations, errors, or baseline>
- Applicable instructions: <AGENTS.md or other policy files Pi must read>

Scope
- You may: <read or change exact files/systems>
- You must not: <non-goals and prohibited actions>
- Preserve: <existing changes or compatibility constraints>

Task
<The actual work, including important decisions already made.>

Evidence and validation
- Inspect: <authoritative sources>
- Run: <narrow validation commands>
- Success means: <observable completion criteria>

Authority and stop conditions
- Do not commit, push, deploy, delete, or contact external systems unless
  explicitly authorized above.
- Stop and report if: <missing model, credentials, destructive step, material
  ambiguity, or other boundary>

Report
- Result
- Evidence inspected
- Files changed
- Commands and exit status
- Remaining uncertainty or blockers
```

When invoking a discovered Pi skill, put the slash command first and append the
standalone task:

```text
/skill:<skill-name> <standalone task>
```

For repeated `--no-session` calls, copy forward every still-relevant fact and
correction. Do not say only "fix the previous response."
