# Guides & Recipes — Routing

Base: `https://hermes-agent.nousresearch.com`. Content under `/docs/guides/*` is **how-to recipes** — use these when the user wants a worked example, not conceptual reference.

## Symptom → URL

| User situation | Fetch |
|---|---|
| "Give me tips / best practices / gotchas" | `/docs/guides/tips` |
| "How do I write a Hermes plugin?" | `/docs/guides/build-a-hermes-plugin` |
| "I want a daily briefing bot" | `/docs/guides/daily-briefing-bot` |
| "Set up a team assistant on Telegram" | `/docs/guides/team-telegram-assistant` |
| "Use Hermes from Python code" / library usage | `/docs/guides/python-library` |
| "Wire MCP servers into Hermes" (step-by-step) | `/docs/guides/use-mcp-with-hermes` |
| "Customize personality with SOUL.md" (walkthrough) | `/docs/guides/use-soul-with-hermes` |
| "Enable voice mode end-to-end" (walkthrough) | `/docs/guides/use-voice-mode-with-hermes` |
| "Migrate from openclaw" | `/docs/guides/migrate-from-openclaw` |

## Tips cheatsheet (from `/docs/guides/tips`, verified 2026-04-04)

Use these to decide whether the tips page is the right route; always WebFetch for full guidance.

- Be specific in prompts (cite files + line numbers)
- Put project rules in `AGENTS.md` — auto-injected every session
- Let the agent iterate; avoid hand-holding
- `Alt+Enter` / `Ctrl+J` for multi-line input
- `Ctrl+C` to interrupt mid-response; double-tap (within 2s) to exit
- Skills are for recurring 5+ step procedures, memory is for facts
- Keep prompt cache stable → cheaper cached requests
- `/compress` before hitting token limits, `/usage` to check
- Docker sandbox untrusted repos: `TERMINAL_BACKEND=docker`
- Prefer "session" allowlisting over "always" when approving commands

## Conceptual vs recipe rule

- If the user wants to understand **what** something is → use `references/features.md` or `references/user-guide.md`
- If the user wants to **do** something end-to-end → this file
- If the user wants authoritative syntax → `references/reference.md`
