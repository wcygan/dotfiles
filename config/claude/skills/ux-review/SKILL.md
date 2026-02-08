---
name: ux-review
description: >
  Launch a multi-agent UX review of any web application using Playwright CLI to browse live pages.
  Agents analyze landing pages, navigation, user flows, visual design, accessibility, and copy quality,
  then synthesize a prioritized action plan. Use this skill whenever the user wants UX feedback, usability
  analysis, user experience review, interface critique, conversion optimization, or wants to make their
  app more intuitive, user-friendly, or easy to use. Also trigger when the user mentions "review my app",
  "UX audit", "usability review", "how can I improve my site", or similar phrases.
---

# UX Review Skill

A multi-agent UX review system that browses live web applications with Playwright CLI and produces
a prioritized, actionable report for solo developers and small teams.

## Prerequisites

Playwright CLI must be installed. If not available, run:

```bash
npm install -g @playwright/cli@latest
playwright-cli install-browser
playwright-cli install --skills
```

Verify with `playwright-cli --help`.

## Inputs

The user provides:

1. **Target URL** (required) — The application's entry point (landing page, login, dashboard, etc.)
2. **Key user flows** (optional) — Specific paths to test, e.g. "sign up → create project → invite team"
3. **Target audience** (optional) — Who uses this app and what they expect
4. **Focus areas** (optional) — Which review dimensions matter most (see Agent Roster below)
5. **Context file** (optional) — A markdown file with app description, known issues, constraints

If the user doesn't provide optional inputs, use reasonable defaults and note assumptions.

## Agent Roster

Each agent has a specialized lens. All agents use Playwright CLI to interact with the live app.

| # | Agent | Focus | Reference |
|---|-------|-------|-----------|
| 1 | **First Impression** | Landing page clarity, value prop, CTAs, trust signals, load perception | `agents/first-impression.md` |
| 2 | **Information Architecture** | Navigation, page hierarchy, naming, discoverability, mental models | `agents/information-architecture.md` |
| 3 | **User Flow** | Task completion paths, friction, dead ends, error recovery, onboarding | `agents/user-flow.md` |
| 4 | **Visual Design** | Spacing, typography, color, component consistency, responsive hints | `agents/visual-design.md` |
| 5 | **Accessibility** | WCAG compliance, keyboard nav, ARIA, contrast, form labels, error states | `agents/accessibility.md` |
| 6 | **Copy & Microcopy** | Button labels, error messages, empty states, onboarding text, tone | `agents/copy-review.md` |
| 7 | **Synthesizer** | Reads all agent reports → produces prioritized action plan | `agents/synthesizer.md` |

## Workflow

### Phase 1: Setup

1. Confirm the target URL and any user-provided context
2. Ensure Playwright CLI is installed (`playwright-cli --help`)
3. Open a browser session: `playwright-cli open <url>`
4. Take an initial screenshot to confirm the page loaded: `playwright-cli screenshot --filename=landing.png`
5. Capture a snapshot for structural analysis: `playwright-cli snapshot --filename=landing-snapshot.txt`
6. Create the workspace directory for outputs

### Phase 2: Discovery (Main Agent)

Before spawning review agents, do a quick site crawl to understand scope:

1. Capture the landing page snapshot
2. Identify primary navigation links from the snapshot
3. Visit 3-5 key pages (follow nav links) and snapshot each
4. Build a simple sitemap of discovered pages
5. Save discovery results to `workspace/discovery.md`

This discovery output is shared with all review agents as context.

### Phase 3: Parallel Review (Sub-agents)

Spawn agents 1-6 in parallel. Each agent receives:

- The target URL
- The discovery file (`workspace/discovery.md`)
- Their specific agent instructions (from `agents/*.md`)
- The Playwright CLI reference (`references/playwright-guide.md`)
- The heuristics reference (`references/heuristics.md`)
- An output directory for their findings

Each agent:
1. Opens the app in its own Playwright CLI session (`-s=<agent-name>`)
2. Navigates through relevant pages
3. Takes snapshots and screenshots as evidence
4. Writes findings to their output file

If sub-agents are not available, run each review sequentially in the main loop.

### Phase 4: Synthesis

After all reviews complete, the Synthesizer agent:

1. Reads all 6 agent reports
2. Deduplicates overlapping findings
3. Categorizes by severity (Critical / High / Medium / Low)
4. Ranks by impact-vs-effort (essential for solo devs)
5. Produces the final report

### Phase 5: Output

Generate the final deliverable as a markdown report following the template in `references/report-template.md`.

Save to the workspace and present to the user.

## Playwright CLI Quick Reference for Agents

Each agent should use a named session to avoid conflicts:

```bash
# Agent opens its own session
playwright-cli -s=first-impression open <url>

# Navigate
playwright-cli -s=first-impression goto <url>

# Capture page structure (element refs, text, layout)
playwright-cli -s=first-impression snapshot --filename=<name>.txt

# Take visual screenshot
playwright-cli -s=first-impression screenshot --filename=<name>.png

# Interact with elements (using refs from snapshot)
playwright-cli -s=first-impression click <ref>
playwright-cli -s=first-impression type <text>
playwright-cli -s=first-impression fill <ref> <text>

# Check navigation
playwright-cli -s=first-impression tab-list

# Close when done
playwright-cli -s=first-impression close
```

Read `references/playwright-guide.md` for the full command reference.

## Output Structure

```
workspace/
├── discovery.md                    # Site structure from Phase 2
├── screenshots/                    # Visual evidence
│   ├── landing.png
│   ├── nav-*.png
│   └── ...
├── agents/
│   ├── first-impression.md
│   ├── information-architecture.md
│   ├── user-flow.md
│   ├── visual-design.md
│   ├── accessibility.md
│   └── copy-review.md
└── ux-review-report.md             # Final synthesized report
```

## Coordinator Responsibilities

1. Handle Playwright CLI installation if needed
2. Run the discovery phase to build shared context
3. Spawn review agents in parallel (or sequentially if no sub-agents)
4. Ensure each agent uses its own named session (`-s=<name>`)
5. Collect all agent reports
6. Run the synthesizer to produce the final report
7. Clean up browser sessions: `playwright-cli close-all`
8. Present the final report to the user

## Customization

The user can customize the review by:

- **Skipping agents**: "Skip accessibility, focus on user flows and copy"
- **Adding competitor URLs**: Include comparison analysis
- **Specifying user stories**: "Test the checkout flow specifically"
- **Setting priorities**: "I care most about conversion, less about accessibility"
- **Providing context**: "This is a B2B SaaS for project managers"

Adapt the agent roster and instructions accordingly.
