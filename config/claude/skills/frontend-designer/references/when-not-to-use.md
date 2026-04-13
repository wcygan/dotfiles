# When NOT to Use This Skill

The `frontend-design-agent` is tuned for **distinctive, visible surfaces**. Using it for the wrong task produces worse results than not using it — it will pick an aesthetic direction when the task needs consistency, or refuse to hedge when hedging is correct.

## Do not use for

- **CRUD forms**. Use existing shadcn `Form`/`Input`/`Button` primitives directly. Match the app's existing visual language; don't re-declare one.
- **Admin dashboards / internal tooling**. Legibility and consistency matter more than "wow." The statistical center is often *correct* here.
- **Bugfixes or style tweaks to existing components**. If the visual system is already set, surgical edits belong in the main thread.
- **API routes, server functions, data layer work**. Wrong agent entirely.
- **Debugging broken CSS or Tailwind v4 migration issues**. Use the `tailwind` skill and the main thread.
- **Rewriting something into React from scratch**. Agent assumes the app skeleton exists.
- **Accessibility audits, perf audits**. Different agents, different tools.
- **Dashboard chart styling, data-viz theming**. Agent doesn't know D3, Recharts, Visx; it will improvise poorly.

## Do use for

- A brand-new public-facing route (landing, about, pricing, case-study, blog index).
- A hero section or above-the-fold refresh.
- Turning a Figma mock into code where the mock has real visual opinions.
- "Make this page not look like a template."
- Setting up the *first* design tokens + `@theme` block in a fresh TanStack Start app.

## Borderline cases

- **"Polish this page."** → OK if the page is public-facing. Ask for the route.
- **"Make the dashboard nicer."** → Skip this skill. Use `tailwind-v4-tokens` inline for token cleanup.
- **"Add a marketing section to the app homepage."** → OK — that's a visible surface.
- **"Build a settings page."** → Skip. Internal tooling.

## How to reject gracefully

If the task doesn't fit, say so in one sentence and suggest the right path:

> "This is an internal-tooling task — the `frontend-design-agent` is tuned for public surfaces and would over-design it. I'll handle it in the main thread using the existing component library."

Do not silently proceed with the wrong approach.
