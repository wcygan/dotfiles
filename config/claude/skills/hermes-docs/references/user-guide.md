# User Guide (core) — Routing

Base: `https://hermes-agent.nousresearch.com`. WebFetch before answering.

## Symptom → URL

| User situation | Fetch |
|---|---|
| Any CLI flag: `-c`, `--continue`, `--resume`, `-r`, `-w`, `--docker`, `--model`, `--provider`, `--toolsets`, `-s`, `--verbose`, `--yolo` | `/docs/user-guide/cli` |
| `hermes chat -q "..."` single-query mode | `/docs/user-guide/cli` |
| Slash commands (`/help`, `/model`, `/tools`, `/skills`, `/reasoning`, `/compress`, `/usage`, `/background`, `/yolo`, `/title`) | `/docs/reference/slash-commands` (primary) or `/docs/user-guide/cli` |
| Exact CLI command signatures | `/docs/reference/cli-commands` |
| "Where does config live?" / `~/.hermes/` layout | `/docs/user-guide/configuration` |
| `config.yaml` fields, precedence, `${VAR}` substitution | `/docs/user-guide/configuration` |
| API keys / `.env` / `auth.json` / OAuth | `/docs/user-guide/configuration` |
| `hermes config view/edit/set/check/migrate` | `/docs/user-guide/configuration` |
| Credential pools (round_robin / least_used / fill_first / random) | `/docs/user-guide/features/credential-pools` |
| Model selection, aux models, fallback model, reasoning effort | `/docs/user-guide/configuration` then `/docs/user-guide/features/fallback-providers` |
| Named profiles (per-context configs) | `/docs/user-guide/profiles` |
| Sessions overview, SQLite, `~/.hermes/state.db`, JSONL transcripts | `/docs/user-guide/sessions` |
| Resuming a session by id or name | `/docs/user-guide/sessions` |
| `hermes sessions list/rename/prune/export` | `/docs/user-guide/sessions` |
| Title generation, compression lineage | `/docs/user-guide/sessions` |
| `session_search` FTS tool | `/docs/user-guide/sessions` |
| Git worktree mode (`-w`) | `/docs/user-guide/git-worktrees` |
| Docker sandboxing, `TERMINAL_BACKEND=docker`, container hardening | `/docs/user-guide/docker` |
| Checkpoints, rollback of file edits | `/docs/user-guide/checkpoints-and-rollback` |
| Security model, dangerous-command approval (manual/smart/off), `--yolo` | `/docs/user-guide/security` |
| SSRF protection, RFC 1918 blocking, cloud metadata blocking | `/docs/user-guide/security` |
| DM pairing, messaging platform auth, allowlists | `/docs/user-guide/security` |
| tirith pre-exec scanning, homograph/pipe-to-interpreter detection | `/docs/user-guide/security` |
| MCP credential filtering / env passthrough allowlists | `/docs/user-guide/security` or `/docs/user-guide/features/mcp` |
| Telegram / Discord / WhatsApp / Slack messaging gateway | `/docs/user-guide/messaging/` |
| Discord specifics | `/docs/user-guide/messaging/discord` |

## Ground-truth cheatsheet (verified 2026-04-04)

For routing decisions only. Always WebFetch before quoting specifics in answers.

- Config dir: `~/.hermes/` contains `config.yaml`, `.env`, `auth.json`, `SOUL.md`, `memories/`, `skills/`, `cron/`, `sessions/`, `logs/`, `state.db`, `plugins/`
- Precedence: **CLI args → `config.yaml` → `.env` → built-in defaults**
- Session DB: SQLite `~/.hermes/state.db`, transcripts as JSONL under `~/.hermes/sessions/`
- Session resume: `hermes -c` (most recent), `hermes -c "<title substring>"`, `hermes -r <id>` (specific)
- Security layers (in order): user auth → dangerous-command approval → container isolation → MCP credential filter → context-file scanning
