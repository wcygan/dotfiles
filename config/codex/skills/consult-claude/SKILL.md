---
name: consult-claude
description: "Use when Codex should ask Claude Code for a focused second opinion, independent codebase analysis, architecture review, bug-hypothesis check, implementation critique, or planning help from a separate model. Grounds Claude in the local `config/claude/skills/claude-code-best-practices` skill and defaults to read-only headless consultation."
---

# Consult Claude

Use this skill to ask Claude Code for a bounded consultation from the current working tree. Treat Claude as an external subagent: pass a self-contained request, ask for a specific output, and keep the default path read-only.

## Workflow

1. Decide whether a consultation is useful. Use this for high-uncertainty design, code review, unfamiliar code, debugging hypotheses, or independent validation. Skip it for quick facts or mechanical edits.
2. Inspect the relevant local context yourself first. Claude's answer is advisory; verify claims before acting on them.
3. Write a self-contained request with the objective, repo context, relevant file paths, constraints, and exact question.
4. Prefer the safe default. Use `--unsafe` only when edits or unrestricted tool use are explicitly intended.
5. Run the bundled script from the skill directory:

```bash
scripts/consult_claude.sh "Review the auth flow in src/auth.ts and identify likely race conditions. Do not edit files."
```

For longer prompts, pipe stdin:

```bash
scripts/consult_claude.sh <<'PROMPT'
Inspect the files below and give a concise implementation critique.

- src/server.ts
- src/auth.ts

Do not edit files. Return findings with file paths and line numbers.
PROMPT
```

## Script Behavior

`scripts/consult_claude.sh`:

- Resolves the local Claude Code best-practices skill from `$CLAUDE_BEST_PRACTICES_DIR`, `$DOTFILES_DIR`, this dotfiles checkout, `$HOME/.claude/skills`, or the current repo.
- Grounds Claude via `--append-system-prompt`, pointing it to `SKILL.md` plus the relevant references: `headless.md`, `sub-agents.md`, `skill-best-practices.md`, `skills.md`, `tools-reference.md`, and `writing-claude-md.md`.
- Runs Claude headlessly with `-p`, `--model "${CLAUDE_MODEL:-opus}"`, and a read-only `--allowed-tools` / `--disallowed-tools` policy by default.
- Prints Claude's response to stdout.

Useful options:

```bash
scripts/consult_claude.sh --model sonnet "Ask a cheaper model first"
scripts/consult_claude.sh --bare "Use deterministic API-key-backed bare mode"
scripts/consult_claude.sh --output-format json "Return JSON output"
scripts/consult_claude.sh --max-budget-usd 1.00 "Cap spend for this call"
scripts/consult_claude.sh --allowed-tools "Read,Grep,Glob" "Tighten the tool allowlist"
scripts/consult_claude.sh --unsafe "Allow unrestricted Claude Code permissions on a trusted worktree"
scripts/consult_claude.sh --best-practices /path/to/claude-code-best-practices "Use this specific reference copy"
scripts/consult_claude.sh --print-prompt "Show the assembled prompts without calling Claude"
scripts/consult_claude.sh --print-command "Show the Claude command without running it"
```

## Request Shape

Prefer prompts like:

```text
You are a read-only consultant. Inspect config/fish/config.fish and tests/fish.bats.
Question: what test gap would most likely hide a regression in the recent fish change?
Return: top findings, reasoning, and one recommended verification command.
```

## Safety

- Default mode is read-only: `Read`, `Grep`, `Glob`, `WebFetch`, `WebSearch`, and narrow `Bash(cat|ls|git status|git diff|git show|git log *)` patterns are allowed; write-capable tools are denied.
- `--unsafe` uses `--dangerously-skip-permissions`; run it only on trusted worktrees and only when unrestricted tool use is intended.
- `--bare` can improve determinism but requires API-key-backed auth or explicit settings because it skips keychain discovery.
- Do not include secrets, credentials, private tokens, or production data in the request.
- Do not accept destructive commands or broad rewrites proposed by Claude without independent review and user confirmation.
- Keep the critical path in Codex. Use Claude's response as evidence to verify, not as an unquestioned source of truth.
