---
name: deno-docs
description: Routes Deno runtime questions to the right official docs page before giving guidance or editing code. Auto-loads on `deno.json`/`deno.jsonc`, `jsr:`/`npm:`/`node:` import specifiers, `Deno.*` API calls, or any `deno` CLI mention. Covers CLI, config, permissions, TypeScript, Node/npm compatibility, modules, testing, debugging, JSX, env vars, and `@std/*`. Keywords deno, deno.json, jsr, deno run, deno test, Deno.serve, @std, deno task, deno x, deno add, deno fmt, deno lint.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Deno Docs

Use this skill to route Deno runtime questions to the right official docs **before** giving implementation advice or editing code. Treat the bundled map as navigation, not an API snapshot — Deno's CLI flags, config fields, and APIs evolve, so always WebFetch the current page before claiming exact behavior.

## Workflow

1. Identify the Deno topic in the user request, repo files, or command output.
2. If the right official page isn't obvious, read `references/doc-map.md`.
3. **WebFetch** the current page from `https://docs.deno.com/...` before making precise claims about CLI flags, config fields, permissions, APIs, examples, or recommended patterns.
4. When editing a project, inspect local context first: `deno.json`, `deno.jsonc`, `package.json`, import specifiers, lockfiles, tasks, and the installed `deno --version` when available.
5. Verify with the narrowest meaningful Deno command: usually `deno check`, `deno test`, `deno lint`, or the affected `deno task`.

## Navigation Heuristics

- New Deno projects, runtime overview, zero-config TypeScript, secure defaults, built-in toolchain, installation → **Runtime Overview**.
- Type checking, strict mode, JS type checking, declaration files, browser/web worker libs, global type augmentation → **TypeScript**.
- Node migration, npm packages, `node:` built-ins, `package.json`, `node_modules`, CommonJS, lifecycle scripts, Node compatibility gaps → **Node and npm Compatibility**.
- Imports, `jsr:`, `npm:`, `node:`, URL imports, import maps, vendoring, dependency updates, lockfiles, publishing modules → **Modules and Dependencies**.
- `deno.json`, `deno.jsonc`, tasks, formatter/linter config, compiler options, permissions, `nodeModulesDir`, `links`, `include`/`exclude`, package config interplay → **Configuration**.
- Fresh, Next.js, Astro, SvelteKit, Vite, frontend frameworks, server-side web apps on Deno → **Web Development**.
- `Deno.test`, `@std/assert`, mocking, snapshots, coverage, sanitizers, test permissions, filtering tests → **Testing**.
- Chrome DevTools, VS Code debugging, inspector flags, breakpoints, logging, source maps → **Debugging**.
- Standard-library package selection or imports under `@std/*` → **Standard Library**.
- `Deno.env`, `.env`, `--env-file`, `@std/dotenv`, Deno-specific environment variables → **Environment Variables**.
- JSX, React, Preact, JSX compiler options, import sources, `jsxImportSource` → **JSX**.
- CLI execution flags, permissions on scripts, watch mode, `--check`, lock/reload/cache flags, inspector flags on `deno run` → **`deno run`**.
- One-off package execution, `deno x`, `dx`, npm/JSR binary execution, temporary CLIs → **`deno x`**.
- Adding dependencies to `deno.json` or `package.json`, JSR vs npm specifiers, dependency aliases → **`deno add`**.

## Quality Rules

- **Prefer official docs over memory.** Treat the bundled map as navigation, not an API snapshot. Use `https://docs.deno.com/llms-full-guide.txt` for broad orientation; fetch the specific page for exact syntax or behavior.
- **Preserve Deno's security model in examples.** Avoid broad `-A` unless the user explicitly needs all permissions or the docs page recommends it for that workflow.
- **Idiomatic imports and config.** `jsr:` for Deno-native packages, `npm:` for npm packages, `node:` for Node built-ins, and import-map aliases in `deno.json` when the project already uses them.
- **Don't assume Node behavior when Deno differs** — especially for permissions, type checking, module resolution, `node_modules`, environment access, and package scripts.
- **When docs and the local installed Deno version disagree**, call out the mismatch and trust the installed version for code changes.
- Keep quotes short — summarize docs rather than copying full examples or long passages.

## Reference Map

- [`references/doc-map.md`](references/doc-map.md) — official Deno docs indexes and runtime pages grouped by topic, with WebFetch-ready URLs.
