---
name: codex-docs
description: Use when answering questions about OpenAI Codex CLI documentation, including AGENTS.md guidance, skills, subagents, hooks, rules, config.toml basics, advanced configuration, config layers, sandboxing, approvals, and local Codex customization. Use official OpenAI Codex docs as source of truth and load only the relevant reference file.
---

# Codex Docs

Use this skill when the user asks for help with Codex CLI docs or local Codex configuration.

## Workflow

1. Identify the topic: AGENTS.md, skills, subagents, hooks, rules, basic config, or advanced config.
2. Read only the relevant reference file from `references/`.
3. Treat the `canonical_url` in that file as the source of truth. For precise or current answers, fetch the official page before making definitive claims.
4. Keep implementation advice narrow. Do not migrate unrelated Codex state or repo configuration unless the user asks.
5. When editing dotfiles, keep global Codex skills under `config/codex/skills/`; this repo links that path to `~/.codex/skills`.

## Reference Map

- `references/agents-md.md`: instruction discovery, global/project `AGENTS.md`, override files, fallback filenames.
- `references/skills.md`: skill format, discovery locations, triggering, progressive disclosure, plugins.
- `references/subagents.md`: when to use subagents, built-in agents, custom agents, sandbox inheritance.
- `references/hooks.md`: lifecycle hooks, feature flag, hook locations, matchers, input/output contracts.
- `references/rules.md`: command execution rules, rule fields, command splitting, testing rules.
- `references/config-basic.md`: config file locations, precedence, common options, trust behavior.
- `references/config-advanced.md`: profiles, CLI overrides, state locations, providers, MCP, telemetry, environment policy.
- `references/doc-map.md`: quick index of official Codex CLI documentation links.

## Quality Rules

- Prefer official OpenAI Codex docs over memory.
- Cite official docs links when answering user-facing documentation questions.
- If docs appear stale or conflict with observed CLI behavior, state the conflict and verify with the local `codex` version before changing files.
- Keep quotes short; paraphrase the docs instead of copying large sections.
