# Reference Pages — Routing

Base: `https://hermes-agent.nousresearch.com`. Use these for **authoritative factual lookups** — exact command signatures, exact flag names, exact environment variable names. Prefer these over feature pages when the user wants syntax, not concept.

## Symptom → URL

| User situation | Fetch |
|---|---|
| "What are all the CLI subcommands?" / "full `hermes` CLI reference" | `/docs/reference/cli-commands` |
| "What slash commands exist inside a session?" | `/docs/reference/slash-commands` |
| "What environment variables does Hermes read?" | `/docs/reference/environment-variables` |
| FAQ / troubleshooting / "why doesn't X work" | `/docs/reference/faq` |

## Routing hints

- **Concept + syntax together?** Fetch both the feature page *and* the reference page. For example: "how does voice mode work and what flags control it?" → `/docs/user-guide/features/voice-mode` + `/docs/reference/cli-commands` + possibly `/docs/reference/environment-variables`.
- **Obscure/short flag disambiguation?** Go straight to `/docs/reference/cli-commands` — don't guess from the CLI conceptual page.
- **Error messages / stuck install / "it hangs"?** Start with `/docs/reference/faq`, then `/docs/user-guide/security` if the issue smells like command approval or sandboxing.
- **Env var defaults** (paths, toggles, backend selection)? `/docs/reference/environment-variables` is authoritative; `config.yaml` docs describe how they interact with file config.

## Common reference questions to watch for

- "What does `--yolo` actually do?" → `cli-commands` + `security`
- "What is `TERMINAL_BACKEND` valid for?" → `environment-variables` + `docker`
- "What slash commands control reasoning effort?" → `slash-commands` (look for `/reasoning`)
- "How do I list sessions from the CLI?" → `cli-commands` (look for `hermes sessions` subcommands)
- "Why did my command get blocked?" → `faq` + `security` (tirith scanner, dangerous-command approval modes)
