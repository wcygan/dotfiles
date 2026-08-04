# Agent Skill Routes

Distinguish skill ownership before editing or installing anything.

## Project-local Pi skill

- Place a `SKILL.md`-rooted directory at `.agents/skills/<name>/`.
- Pi loads project-local skills only after the project is trusted.
- Interactive Pi can save a trust decision.
- Noninteractive `-p`, JSON, or RPC evaluations should use `--approve` for an
  explicit one-run trust override when no saved decision applies.
- `--no-skills` disables automatic discovery, but an explicit
  `--skill .agents/skills/<name>` still loads that skill.
- For a deterministic controller run, combine `--approve --no-skills` with
  `--skill .agents/skills/<name>` and begin the prompt with `/skill:<name>`.
  Then state: `Use the <name> skill to help solve this: <question>`.
- For a natural project-skill discovery test, omit `--no-skills`, the explicit
  `--skill`, and the `/skill:<name>` expansion. Confirm from the JSON event log
  that Pi read the intended `SKILL.md`; a correct answer alone is not evidence
  that discovery occurred.

The three deterministic layers have different jobs:

1. `--skill` supplies the exact skill path without depending on discovery.
2. `/skill:<name>` expands the complete `SKILL.md` into the prompt.
3. The explicit instruction names the skill as the method for the question.

In JSON-mode certification, verify that the user message contains
`<skill name="<name>" ...>` and that the expected focused references were read.

## Shared global agent skill

- Install curated vendor skills once into `~/.agents/skills` through
  `scripts/install-skills.sh`.
- Pi discovers that shared catalog directly; do not create
  `~/.pi/agent/skills` or a second repository-backed catalog.
- Keep `auth.json`, models, sessions, logs, caches, and other runtime state
  machine-local.

## Global Codex skill

- Place reusable Codex workflows under `config/codex/skills/<name>/`.
- Validate the catalog with `./tests/test-codex-skills.sh`.
- Then run `make test-pre` for repository preflight.

## Curated vendor skill

- Accept only an official publisher.
- Add `<owner>/<repo>@<skill>` to `SKILLS` in
  `scripts/install-skills.sh`.
- The installer uses `bunx skills add "$skill" -g -y`; do not select a Pi
  target, because that recreates duplicate links.
- Install with `make install-skills`.
- Refresh with `scripts/install-skills.sh --update` or `make update-skills`.
- Do not recreate removed Claude skill surfaces as a side effect.
