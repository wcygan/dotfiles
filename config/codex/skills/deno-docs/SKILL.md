---
name: deno-docs
description: Use when working with Deno runtime documentation, Deno CLI commands, deno.json/package.json configuration, TypeScript support, Node/npm compatibility, modules and imports, permissions, web development, testing, debugging, JSX, environment variables, or @std packages. Use official Deno docs as source of truth and load only the relevant reference file before giving precise guidance or changing Deno code.
---

# Deno Docs

Use this skill to route Deno runtime questions to the right official docs before giving implementation advice or editing code.

## Workflow

1. Identify the Deno topic in the user request, repo files, or command output.
2. Read `references/doc-map.md` only when the right official page is not obvious.
3. Fetch the current official page from `https://docs.deno.com/...` before making precise claims about CLI flags, config fields, permissions, APIs, examples, or recommended patterns.
4. When editing a project, inspect local context before changing code: `deno.json`, `deno.jsonc`, `package.json`, import specifiers, lockfiles, tasks, and the installed `deno --version` when available.
5. Verify with the narrowest meaningful Deno command first, usually `deno check`, `deno test`, `deno lint`, or the affected `deno task`.

## Navigation Heuristics

- New Deno projects, runtime overview, zero-config TypeScript, secure defaults, built-in toolchain, and installation: start with Runtime Overview.
- Type checking, strict mode, JavaScript type checking, declaration files, browser/web worker libs, or global type augmentation: start with TypeScript.
- Node.js migration, npm packages, `node:` built-ins, `package.json`, `node_modules`, CommonJS, lifecycle scripts, or Node compatibility gaps: start with Node and npm Compatibility.
- Imports, `jsr:`, `npm:`, `node:`, URL imports, import maps, vendoring, dependency updates, lockfiles, or publishing modules: start with Modules and Dependencies.
- `deno.json`, `deno.jsonc`, tasks, formatter/linter config, compiler options, permissions, `nodeModulesDir`, `links`, `include`/`exclude`, or package config interplay: start with Configuration.
- Fresh, Next.js, Astro, SvelteKit, Vite, frontend frameworks, or server-side web apps on Deno: start with Web Development.
- `Deno.test`, `@std/assert`, mocking, snapshots, coverage, sanitizers, test permissions, or filtering tests: start with Testing.
- Chrome DevTools, VS Code debugging, inspector flags, breakpoints, logging, or source maps: start with Debugging.
- Standard library package selection or imports under `@std/*`: start with Standard Library.
- `Deno.env`, `.env`, `--env-file`, `@std/dotenv`, or Deno-specific environment variables: start with Environment Variables.
- JSX, React, Preact, JSX compiler options, import sources, or `jsxImportSource`: start with JSX.
- CLI execution flags, permissions on scripts, watch mode, `--check`, lock/reload/cache flags, or inspector flags on `deno run`: start with `deno run`.
- One-off package execution, `deno x`, `dx`, npm/JSR binary execution, or temporary CLIs: start with `deno x`.
- Adding dependencies to `deno.json` or `package.json`, JSR vs npm specifiers, or dependency aliases: start with `deno add`.

## Quality Rules

- Prefer official Deno docs over memory. Treat the bundled map as navigation, not an API snapshot.
- Use Deno's LLM-oriented docs indexes when broad orientation is useful; fetch the specific page for exact syntax or behavior.
- Preserve Deno's security model in examples. Avoid broad `-A` unless the user explicitly needs all permissions or the docs page recommends it for that workflow.
- Prefer idiomatic Deno imports and config: `jsr:` for Deno-native packages, `npm:` for npm packages, `node:` for Node built-ins, and import-map aliases in `deno.json` when the project already uses them.
- Do not assume Node behavior when Deno has a different default, especially for permissions, type checking, module resolution, `node_modules`, environment access, and package scripts.
- When docs and the local installed Deno version disagree, call out the mismatch and trust the installed version for code changes.
- Keep quotes short; summarize docs rather than copying full examples or long passages.

## Reference Map

- `references/doc-map.md`: official Deno docs indexes and runtime pages grouped by topic.
