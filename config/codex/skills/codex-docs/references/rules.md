---
canonical_url: https://developers.openai.com/codex/rules
last_verified: 2026-05-06
---

# Rules

Use this reference when the user asks how to control which commands Codex can run outside the sandbox.

Key points from the official docs:

- Rules are experimental.
- Rules files use Starlark syntax.
- Create `.rules` files under a `rules/` folder next to an active config layer.
- User-level rules commonly live at `~/.codex/rules/default.rules`.
- Project-local rules under `<repo>/.codex/rules/` load only when the project `.codex/` layer is trusted.
- Codex scans `rules/` under every active config layer at startup.
- Smart approvals may suggest a `prefix_rule`; review generated prefixes before accepting.
- Admins can enforce restrictive rules from managed requirements.

Core rule shape:

```python
prefix_rule(
    pattern = ["gh", "pr", "view"],
    decision = "prompt",
    justification = "Viewing PRs is allowed with approval",
    match = [
        "gh pr view 7888",
        "gh pr view --repo openai/codex",
    ],
    not_match = [
        "gh pr --repo openai/codex view 7888",
    ],
)
```

Fields:

- `pattern`: required non-empty command prefix list. Elements can be literal strings or unions of literals.
- `decision`: `allow`, `prompt`, or `forbidden`. If several rules match, the most restrictive decision wins.
- `justification`: optional explanation surfaced in approval or rejection flows.
- `match` and `not_match`: inline examples Codex validates when loading the rules file.

Testing:

```bash
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- gh pr view 7888 --json title,body,comments
```

Command splitting:

- For simple linear shell chains, Codex may split commands before applying rules.
- More complex shell features are treated conservatively as the full shell invocation.
