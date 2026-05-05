---
name: deepsec
description: Drive vercel-labs/deepsec — the agent-powered vulnerability scanner — from a Bun + Claude Code workflow. Runs init/scan/process/triage/revalidate/export, authors the bootstrap INFO.md ritual, and helps grow custom matchers. Auto-triggers on deepsec, .deepsec/, AI_GATEWAY_API_KEY, vulnerability scanner, security scan, deepsec.config.ts, writing matchers, vercel sandbox microvm. Keywords deepsec, vulnerability scan, security audit, code audit, AI Gateway, Vercel Sandbox, vulnerability scanner.
context: fork
argument-hint: [init|scan|process|matchers|<freeform>]
---

# deepsec (Bun + Claude Code)

Runbook for using `vercel-labs/deepsec` — Vercel Labs' agent-powered vulnerability scanner — from a **Bun runtime** in the **Claude Code** harness.

This skill **runs as a forked subagent**: when invoked, a child agent executes the deepsec workflow end-to-end and reports back. Use it for first scans, recurring scans, or growing the matcher set without flooding the parent context with scan output.

## What deepsec is

CLI that fans coding agents (Claude / Codex via Vercel AI Gateway) over a repo to find lurking vulns. Pipeline: `scan` (regex matchers, no AI) → `process` (AI investigation) → `revalidate` (FP cull) → `export`. Costs are real — large scans can run thousands of dollars. Flag this before kicking off `process`.

## Hard rules (Bun + Claude Code variant)

1. **Bun replaces pnpm/npx in the consumer path.** Use `bunx deepsec init`, `bun install`, `bun run deepsec <cmd>`. **Never** run `pnpm` inside the user's `.deepsec/` install.
2. **Exception: contributing to deepsec itself.** If `cwd` is the deepsec monorepo (has `pnpm-workspace.yaml` + `packageManager: pnpm@8.x`), keep pnpm — do not switch to bun. Workspace protocol differs.
3. **`bun run deepsec`, not `bun --bun deepsec`.** The CLI wants Node ≥22 semantics. Plain `bun run` delegates correctly; `--bun` forces the Bun runtime and can break Node-only deps the scanner relies on.
4. **`AI_GATEWAY_API_KEY` is the single source of truth** for credentials in CI/scaled runs. For local dev, deepsec auto-uses the user's existing Claude/Codex subscriptions — do not prompt for keys if a subscription is already active.
5. **Cost gate before `process`.** Print an estimate (file count × matcher hits, or scan-output candidate count) and confirm before running `bun run deepsec process`. `scan` is cheap; `process` is not.
6. **Bootstrap INFO.md is mandatory after `init`.** This is the step the README explicitly delegates to "your coding agent" — that's the forked child. See [install-and-first-scan](references/install-and-first-scan.md).
7. **Run scanner commands from the target repo's root**, not from inside `.deepsec/` for `init`, but from inside `.deepsec/` for `scan`/`process`/`export`. Read the README workflow in [install-and-first-scan](references/install-and-first-scan.md) — the cwd flips.

## Decision tree

| Situation | Branch |
|---|---|
| User has never scanned this repo | [install-and-first-scan](references/install-and-first-scan.md) |
| `.deepsec/` already exists; just need to run a command | [command-reference](references/command-reference.md) |
| User wants to find more issues / refine signal / write a plugin | [matchers-and-plugins](references/matchers-and-plugins.md) |

## Subagent contract

When this skill fires:

1. Parse the argument (`init`, `scan`, `matchers`, freeform) and pick the relevant reference doc.
2. Verify Bun is present (`bun --version`) before running any command. Fail fast if not.
3. Stream a one-line progress update at each phase boundary. Do not dump full scan output to the parent.
4. On completion, emit a digest: counts by severity, top 3 findings (title only), path to the export dir.
5. **Stop and ask** the parent before destructive or expensive ops: `process`, `revalidate`, `sandbox process`, `export --format` that would overwrite an existing dir.

## Verification before claiming done

- [ ] `.deepsec/data/<id>/INFO.md` exists and is ≤100 lines (per Vercel's guidance — verbose context dilutes scan signal).
- [ ] No `pnpm` invocations leaked into the consumer path.
- [ ] Cost-bearing commands (`process`, sandbox runs) ran only after explicit user confirmation.
- [ ] Findings exported to a path the user expects, not buried inside `.deepsec/`.
- [ ] `cwd` was correct for each command (init in repo root, scan/process inside `.deepsec/`).

## Upstream

- Repo: https://github.com/vercel-labs/deepsec
- Announce: https://vercel.com/blog/introducing-deepsec-find-and-fix-vulnerabilities-in-your-code-base
- License: Apache 2.0
