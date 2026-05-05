# Growing the matcher set & writing plugins

Built-in matchers cover generic CWE categories. The high-leverage move is **adding project-specific matchers** that give the AI investigator stronger starting points in this codebase.

## When to write new matchers

Write a matcher when:

- After a `process` run, the user has a finding type that came from custom inspection rather than a built-in matcher, and they want to find more like it.
- The codebase has a project-specific primitive (a custom auth helper, a homegrown ORM call, a vendored crypto wrapper) that built-in regex won't recognize.
- A first scan returned suspiciously few candidates for a code area the user knows is risky.

Skip writing a matcher when:

- The category is already covered by built-ins (XSS, SQLi, SSRF, deserialization, etc.). Built-in coverage is the reason `INFO.md` is supposed to skip generic CWE listing.
- The signal would be too noisy (matches every file) — that wastes `process` budget. Tighten the regex first, or move the concern into INFO.md as guidance instead.

## How to write a matcher

The upstream doc is the source of truth: `docs/writing-matchers.md` in the deepsec repo. Read it before authoring. From this skill, the right move is:

1. Open `.deepsec/node_modules/deepsec/docs/writing-matchers.md` (it's installed alongside the package) **or** fetch from upstream:

   ```
   https://raw.githubusercontent.com/vercel-labs/deepsec/main/docs/writing-matchers.md
   ```

2. Identify the project's matcher config — typically `deepsec.config.ts` at `.deepsec/` root. If it doesn't exist, create one. See `docs/configuration.md` (same install tree) for the schema.

3. Add the matcher with:
   - A **tight regex** anchored to project-specific identifiers (function names, decorators, route registrars).
   - A **rationale** comment — why this signals risk.
   - A **severity hint** if the upstream schema supports it; otherwise leave to processing-time judgment.

4. Re-run `bun run deepsec scan` to refresh candidates. `process` only over the new candidates if practical (`--project-id` + selectors per upstream docs).

## Matcher quality bar

| Quality | Signal |
|---|---|
| Good | Hits 5–50 sites in a typical repo; each hit is plausibly risky |
| Acceptable | Hits up to ~200 sites; some FPs expected, but processor culls |
| Bad | Hits >500 sites or every file — burns processor budget on noise |

If a matcher fires too broadly, narrow it with **negative lookarounds** or by requiring co-occurrence with another token. Don't ship broad matchers and hope `process` filters them — that's how scan costs balloon.

## Plugin authoring

For deeper integration (custom enrichment, ownership lookups, bespoke output), deepsec exposes a plugin API. Source of truth:

- `.deepsec/node_modules/deepsec/docs/plugins.md`
- Upstream: https://github.com/vercel-labs/deepsec/blob/main/docs/plugins.md

Plugin checklist:

- [ ] Author in TypeScript; deepsec is `"type": "module"`, ≥Node 22, so target ESM + modern syntax.
- [ ] Run via `bun run` — same Bun-not-`--bun` rule as the CLI itself (Node compat matters for any deps the plugin pulls in).
- [ ] Keep plugin output **structured** — the processor merges into findings, so freeform text dilutes JSON consumers.
- [ ] Test against `samples/webapp/` in the upstream repo before committing.

## When to fetch upstream docs

The skill's reference material here is intentionally thin on schema specifics — they change. For active matcher / plugin work:

```bash
gh api repos/vercel-labs/deepsec/contents/docs/writing-matchers.md --jq .download_url \
  | xargs curl -s
```

…or use `WebFetch` on the raw GitHub URL. Always cross-check the locally installed `node_modules/deepsec/docs/` first — that version is pinned to the user's installed deepsec.
