---
name: consult-codex
description: "Use when Claude should ask OpenAI's Codex CLI for a focused second opinion, independent codebase analysis, architecture review, bug-hypothesis check, implementation critique, or planning help from a separate model. Grounds Codex in the local `config/codex/skills/codex-docs` skill and defaults to read-only headless consultation via `codex exec --sandbox read-only`."
---

# Consult Codex

Use this skill to ask OpenAI's Codex CLI for a bounded consultation from the current working tree. Treat Codex as an external subagent: pass a self-contained request, ask for a specific output, and keep the default path read-only.

## Workflow

1. Decide whether a consultation is useful. Use this for high-uncertainty design, code review, unfamiliar code, debugging hypotheses, or independent validation. Skip it for quick facts or mechanical edits.
2. Inspect the relevant local context yourself first. Codex's answer is advisory; verify claims before acting on them.
3. Write a self-contained request with the objective, repo context, relevant file paths, constraints, and exact question.
4. Prefer the safe default. Use `--unsafe` only when edits or unrestricted command execution are explicitly intended.
5. Run the bundled script from the skill directory:

```bash
scripts/consult_codex.sh "Review the auth flow in src/auth.ts and identify likely race conditions. Do not edit files."
```

For longer prompts, pipe stdin:

```bash
scripts/consult_codex.sh <<'PROMPT'
Inspect the files below and give a concise implementation critique.

- src/server.ts
- src/auth.ts

Do not edit files. Return findings with file paths and line numbers.
PROMPT
```

## Script Behavior

`scripts/consult_codex.sh`:

- Resolves the local Codex docs skill from `$CODEX_DOCS_DIR`, `$DOTFILES_DIR`, this dotfiles checkout, `$HOME/.codex/skills`, or the current repo.
- Grounds Codex by prepending a system block to the prompt that points at `codex-docs/SKILL.md` plus the relevant references: `agents-md.md`, `skills.md`, `subagents.md`, `hooks.md`, `rules.md`, `config-basic.md`, and `config-advanced.md`.
- Runs `codex exec --skip-git-repo-check --color never --sandbox read-only` with `--model` honoring `$CODEX_MODEL` or the user's `config.toml` default.
- Captures the final assistant message via `--output-last-message` and prints it to stdout, suppressing the event-stream noise. Use `--raw-output` to passthrough the full event stream instead.

Useful options:

```bash
scripts/consult_codex.sh --model gpt-5.5 "Pin the model for this call"
scripts/consult_codex.sh --sandbox workspace-write "Allow Codex to write inside the workspace"
scripts/consult_codex.sh --bare "Skip ~/.codex/config.toml and execpolicy rules for deterministic runs"
scripts/consult_codex.sh --output-format json "Stream JSONL events instead of the final message"
scripts/consult_codex.sh --raw-output "Print Codex's full stdout instead of just the last message"
scripts/consult_codex.sh --unsafe "Bypass approvals and sandboxing on a trusted worktree"
scripts/consult_codex.sh --codex-docs /path/to/codex-docs "Use this specific reference copy"
scripts/consult_codex.sh --print-prompt "Show the assembled prompts without calling codex"
scripts/consult_codex.sh --print-command "Show the codex command without running it"
```

## Request Shape

Prefer prompts like:

```text
You are a read-only consultant. Inspect config/fish/config.fish and tests/fish.bats.
Question: what test gap would most likely hide a regression in the recent fish change?
Return: top findings, reasoning, and one recommended verification command.
```

Self-contained beats conversational: Codex has no memory of this Claude session, so include every file path, constraint, and acceptance criterion in the prompt itself.

## Safety

- Default mode is `--sandbox read-only`: Codex can read files and run safe shell commands but cannot edit, create, or delete files. Reads can still touch any path you can read, so don't point prompts at secret directories.
- `--sandbox read-only` blocks `mkdir`, build artifacts, and tempfile creation. If a consultation legitimately needs scratch space, upgrade to `--sandbox workspace-write`.
- `--unsafe` uses `--dangerously-bypass-approvals-and-sandbox`. It is gated by `CONSULT_CODEX_UNSAFE=1` (or the `--unsafe` flag itself), and should only run on trusted worktrees and only when unrestricted command execution is intended.
- `--bare` (sets `--ignore-user-config --ignore-rules`) improves determinism but skips your local model/sandbox defaults and execpolicy; auth still uses `CODEX_HOME`.
- Do not include secrets, credentials, private tokens, or production data in the request.
- Do not accept destructive commands or broad rewrites proposed by Codex without independent review and user confirmation.
- Keep the critical path in Claude. Use Codex's response as evidence to verify, not as an unquestioned source of truth.
