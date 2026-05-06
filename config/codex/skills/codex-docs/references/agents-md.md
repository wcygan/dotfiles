---
canonical_url: https://developers.openai.com/codex/guides/agents-md
last_verified: 2026-05-06
---

# AGENTS.md

Use this reference when the user asks how Codex reads instructions, where to put global or project guidance, how overrides work, or how to change fallback instruction filenames.

Key points from the official docs:

- Codex reads instruction files once per run or launched TUI session.
- Global guidance lives in `CODEX_HOME` and defaults to `~/.codex`.
- At global scope, `AGENTS.override.md` wins over `AGENTS.md`; Codex uses only the first non-empty file at that level.
- At project scope, Codex starts at the project root, walks down to the current working directory, and includes at most one instruction file per directory.
- Project discovery checks `AGENTS.override.md`, then `AGENTS.md`, then configured fallback filenames.
- Merge order is root-to-leaf, so guidance closer to the current directory appears later and can override earlier guidance.
- Empty files are skipped.
- `project_doc_max_bytes` defaults to 32 KiB for the combined instruction chain.
- Configure alternate instruction filenames with `project_doc_fallback_filenames` in `config.toml`.

Common snippets:

```toml
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
project_doc_max_bytes = 65536
```

When advising on this repo, prefer repo-level `AGENTS.md` for project norms and avoid putting machine-specific paths in global guidance.
