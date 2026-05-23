---
name: playwright-cli
description: Use when driving browser sessions with the `playwright-cli` command, inspecting pages through snapshots and element refs, debugging or generating Playwright tests, recording traces or video, mocking requests, managing storage state, or attaching to `npx playwright test --debug=cli` sessions.
---

# Playwright CLI

Use `playwright-cli` when a task benefits from terminal-driven browser automation, snapshot-based page inspection, or generated Playwright TypeScript. Prefer project-local Playwright and CLI installs when available, and keep browser sessions short-lived unless the task requires persistence.

## Workflow

1. Check whether the command is available:

   ```bash
   command -v playwright-cli
   npx --no-install playwright-cli --version
   ```

2. Choose the command prefix:
   - Use `playwright-cli` when the global command exists.
   - Use `npx playwright-cli` when only the project-local CLI exists.
   - Ask before installing global packages unless the user explicitly requested setup.

3. Open or attach a browser session:

   ```bash
   playwright-cli open https://example.com
   playwright-cli attach tw-abcdef
   playwright-cli snapshot
   ```

4. Use snapshot refs first. Interact with refs such as `e15`; fall back to CSS selectors or Playwright locators when refs are unavailable or unstable.
5. Inspect the command output after each action. `playwright-cli` prints page state, generated code, and snapshots that should guide the next step.
6. Clean up when done:

   ```bash
   playwright-cli close
   playwright-cli close-all
   ```

## Command Selection

- Basic browsing, clicks, forms, tabs, snapshots, storage, network routes, console output, requests, tracing, and video: read `references/command-reference.md`.
- Running or debugging existing Playwright tests with `--debug=cli`: read `references/playwright-tests.md`.
- Generating tests from browser interactions: read `references/test-generation.md`.
- Planning, generating, or healing Playwright tests from a spec: read `references/spec-driven-testing.md`.
- Managing multiple sessions, persistent profiles, browser attach, or cleanup: read `references/session-management.md`.
- Saving, loading, or inspecting cookies, localStorage, sessionStorage, IndexedDB, or storage state: read `references/storage-state.md`.
- Intercepting, mocking, modifying, or blocking requests: read `references/request-mocking.md`.
- Running custom Playwright page/context code: read `references/running-code.md`.
- Capturing traces: read `references/tracing.md`.
- Recording videos or scripted demos: read `references/video-recording.md`.
- Inspecting element ids, classes, `data-*`, ARIA, or computed styles missing from snapshots: read `references/element-attributes.md`.

## Playwright Test Debugging

Run tests without opening the HTML report:

```bash
PLAYWRIGHT_HTML_OPEN=never npx playwright test
```

For interactive debugging, start the test with `--debug=cli`, wait for the printed debugging instructions and `tw-...` session name, then attach:

```bash
PLAYWRIGHT_HTML_OPEN=never npx playwright test path/to/test.spec.ts --debug=cli
playwright-cli attach tw-abcdef
```

Keep the debug process running while inspecting the page, then stop it when finished. Use the generated Playwright TypeScript from CLI actions to update tests, and rerun the narrowest failing test before broadening.

## Quality Rules

- Do not commit storage state files, screenshots, traces, videos, profile directories, or `.playwright-cli/` runtime artifacts unless the user explicitly asks for an artifact.
- Do not use sleeps or `networkidle` as a test fix. Prefer locator assertions, URL assertions, response assertions, or app-specific readiness signals.
- For authenticated or user-data workflows, prefer in-memory sessions. Use `--persistent`, `--profile`, `state-save`, or `state-load` only when persistence is part of the task.
- For UI review or ambiguous visual feedback, use `playwright-cli show --annotate` so the user can point at the live page and provide notes.
- When a spec and the live app disagree, update the spec only for confirmed intended behavior. Ask the user when the difference could be either a regression or a changed requirement.
