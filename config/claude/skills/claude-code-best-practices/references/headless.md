---
title: Headless / Agent SDK CLI
canonical_url: https://code.claude.com/docs/en/headless
fetch_before_acting: true
---

# Headless Mode (Agent SDK CLI)

> Before writing headless scripts or CI integrations, WebFetch https://code.claude.com/docs/en/headless for the latest.

## Summary

Run Claude Code programmatically with `claude -p`. Same tools, agent loop, and context management as interactive mode.

### Basic Usage

```bash
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

### Key Flags

- `-p` / `--print` — non-interactive mode
- `--bare` — skip hooks, skills, plugins, MCP, CLAUDE.md (fast, deterministic)
- `--allowedTools` — auto-approve specific tools (permission rule syntax)
- `--output-format` — `text`, `json`, or `stream-json`
- `--json-schema` — enforce structured output shape
- `--continue` / `--resume` — continue conversations
- `--append-system-prompt` — add instructions to system prompt

### Bare Mode

Recommended for CI/scripts. Skips all auto-discovery. Only explicit flags take effect.

```bash
claude --bare -p "Summarize this file" --allowedTools "Read"
```

### Structured Output

```bash
claude -p "Extract functions" --output-format json --json-schema '{"type":"object",...}'
```

Result in `structured_output` field. Use `jq` to parse.

### Streaming

```bash
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

### Common Patterns

- CI commit creation with scoped `--allowedTools "Bash(git *)"`
- PR review pipelines piping `gh pr diff` to Claude
- Automated test fixing with `"Bash,Read,Edit"`
