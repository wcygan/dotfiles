# Deno Docs Map

Use this file to choose which official Deno page to fetch. Do not treat it as a versioned API snapshot; fetch the current page before relying on flags, config fields, examples, or recommendations.

## Official Indexes

- [LLM index](https://docs.deno.com/llms.txt): official compact entry point with links to runtime, Deploy, Sandbox, examples, and Deno AI skills.
- [LLM summary](https://docs.deno.com/llms-summary.txt): compact overview of documentation sections.
- [LLM full guide](https://docs.deno.com/llms-full-guide.txt): short agent-oriented runtime guide with CLI, permissions, config, modules, Node compatibility, tests, HTTP server, Deploy, and Sandbox examples.
- [Full docs dump](https://docs.deno.com/llms-full.txt): large full-content dump; fetch only when broad local search is more useful than one page.

## Runtime Fundamentals

- [Runtime Overview](https://docs.deno.com/runtime/): Deno runtime overview, installation, secure defaults, TypeScript support, built-in toolchain, Node/npm compatibility.
- [TypeScript](https://docs.deno.com/runtime/fundamentals/typescript/): Type checking, `deno check`, `deno run --check`, JavaScript `// @ts-check`, declaration files, browser/web worker libs, global type augmentation.
- [Node and npm Compatibility](https://docs.deno.com/runtime/fundamentals/node/): npm packages, `node:` built-ins, `package.json`, `node_modules`, CommonJS, lifecycle scripts, Node migration behavior.
- [Modules and Dependencies](https://docs.deno.com/runtime/fundamentals/modules/): `jsr:`, `npm:`, `node:`, URL imports, import maps, vendoring, lockfiles, dependency updates, module publishing.
- [Configuration](https://docs.deno.com/runtime/fundamentals/configuration/): `deno.json`, `deno.jsonc`, `package.json`, imports, tasks, lint/fmt options, lockfile, `nodeModulesDir`, compiler options, unstable features, include/exclude, exports, permissions, proxies.
- [Web Development](https://docs.deno.com/runtime/fundamentals/web_dev/): framework workflows for Fresh, Next.js, Astro, SvelteKit, Vite, and related web app patterns.
- [Testing](https://docs.deno.com/runtime/fundamentals/testing/): `Deno.test`, discovery, assertions, mocking, snapshots, coverage, filters, permissions, sanitizers.
- [Debugging](https://docs.deno.com/runtime/fundamentals/debugging/): Chrome DevTools, VS Code, inspector flags, source maps, breakpoints, and debugging setup.

## Reference Guides

- [Standard Library](https://docs.deno.com/runtime/reference/std/): package index for modular JSR packages under `@std/*`.
- [Environment Variables](https://docs.deno.com/runtime/reference/env_variables/): `Deno.env`, `.env`, `--env-file`, `@std/dotenv`, setting variables in commands, special environment variables.
- [JSX](https://docs.deno.com/runtime/reference/jsx/): JSX and React/Preact configuration, compiler options, JSX import sources.
- [deno run](https://docs.deno.com/runtime/reference/cli/run/): script execution, permissions, type checking, dependency/cache flags, config flags, watch mode, env files, inspector options.
- [deno x](https://docs.deno.com/runtime/reference/cli/x/): one-off npm/JSR binary execution, `dx` alias, permissions, dependency/cache flags.
- [deno add](https://docs.deno.com/runtime/reference/cli/add/): adding JSR/npm dependencies, package aliases, import map updates, and dependency arguments.

## Related Official Pages

- [Security and Permissions](https://docs.deno.com/runtime/fundamentals/security/): sandbox model and `--allow-*` permission design.
- [HTTP Server](https://docs.deno.com/runtime/fundamentals/http_server/): `Deno.serve`, request handling, WebSockets, HTTP/HTTPS server patterns.
- [Linting and Formatting](https://docs.deno.com/runtime/fundamentals/linting_and_formatting/): `deno lint`, `deno fmt`, rule and formatter configuration.
- [Workspaces](https://docs.deno.com/runtime/fundamentals/workspaces/): monorepo and multi-package project configuration.
- [CLI Reference](https://docs.deno.com/runtime/reference/cli/): all `deno` subcommands and flags.
- [Deno API Reference](https://docs.deno.com/api/deno/): runtime APIs under the `Deno` namespace.
- [Standard Library on JSR](https://jsr.io/@std): package pages, versions, exports, and API docs for `@std` modules.
