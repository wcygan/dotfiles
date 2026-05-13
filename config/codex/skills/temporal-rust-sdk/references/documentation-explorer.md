# Documentation Explorer

Use this when you need to inspect the source behind Temporal's Rust docs, compare rendered docs with MDX, extract exact code snippets, or discover adjacent pages.

## Source Model

Temporal's rendered docs are backed by MDX files in the public documentation repo:

- Rendered docs root: `https://docs.temporal.io`
- GitHub repo: `https://github.com/temporalio/documentation`
- Raw source URL prefix: `raw.githubusercontent.com/temporalio/documentation/main/docs/`

For most pages, convert:

```text
https://docs.temporal.io/<docs-path>
```

to:

```text
raw.githubusercontent.com/temporalio/documentation/main/docs/<docs-path>.mdx
```

Exception: index pages map to `index.mdx`. For example:
- rendered: `https://docs.temporal.io/develop/rust`
- raw: `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/index.mdx`

The user-provided quickstart anchor follows the direct page pattern:
- rendered: `https://docs.temporal.io/develop/rust/quickstart`
- raw: `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/quickstart.mdx`

## Directory Discovery

Use the GitHub contents API to list available MDX files without cloning:

```bash
curl -L -s 'https://api.github.com/repos/temporalio/documentation/contents/docs/develop/rust?ref=main'
curl -L -s 'https://api.github.com/repos/temporalio/documentation/contents/docs/develop/rust/workflows?ref=main'
curl -L -s 'https://api.github.com/repos/temporalio/documentation/contents/docs/develop/rust/activities?ref=main'
curl -L -s 'https://api.github.com/repos/temporalio/documentation/contents/docs/develop/rust/client?ref=main'
curl -L -s 'https://api.github.com/repos/temporalio/documentation/contents/docs/develop/rust/workers?ref=main'
```

Quote API URLs in zsh because `?ref=main` can be treated as a glob.

## Rust Docs Raw Source Map

| Topic | Rendered page | Raw MDX |
| --- | --- | --- |
| Rust SDK index | `https://docs.temporal.io/develop/rust` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/index.mdx` |
| Quickstart | `https://docs.temporal.io/develop/rust/quickstart` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/quickstart.mdx` |
| Workflow basics | `https://docs.temporal.io/develop/rust/workflows/basics` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/workflows/basics.mdx` |
| Child workflows | `https://docs.temporal.io/develop/rust/workflows/child-workflows` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/workflows/child-workflows.mdx` |
| Continue-As-New | `https://docs.temporal.io/develop/rust/workflows/continue-as-new` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/workflows/continue-as-new.mdx` |
| Message passing | `https://docs.temporal.io/develop/rust/workflows/message-passing` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/workflows/message-passing.mdx` |
| Workflow cancellation | `https://docs.temporal.io/develop/rust/workflows/cancellation` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/workflows/cancellation.mdx` |
| Workflow timers | `https://docs.temporal.io/develop/rust/workflows/timers` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/workflows/timers.mdx` |
| Workflow timeouts | `https://docs.temporal.io/develop/rust/workflows/timeouts` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/workflows/timeouts.mdx` |
| Activity basics | `https://docs.temporal.io/develop/rust/activities/basics` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/activities/basics.mdx` |
| Activity execution | `https://docs.temporal.io/develop/rust/activities/execution` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/activities/execution.mdx` |
| Activity timeouts | `https://docs.temporal.io/develop/rust/activities/timeouts` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/activities/timeouts.mdx` |
| Worker process | `https://docs.temporal.io/develop/rust/workers/worker-process` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/workers/worker-process.mdx` |
| Temporal client | `https://docs.temporal.io/develop/rust/client/temporal-client` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/rust/client/temporal-client.mdx` |
| Environment configuration | `https://docs.temporal.io/develop/environment-configuration` | `https://raw.githubusercontent.com/temporalio/documentation/main/docs/develop/environment-configuration.mdx` |

## Usage Rules

- Prefer rendered docs for human-facing navigation and canonical public URLs.
- Prefer raw MDX when exact code snippets, admonitions, imports, frontmatter, or component-wrapped examples matter.
- Verify a raw URL with `curl -L -s -o /dev/null -w '%{http_code}' <url>` before relying on a newly inferred path.
- If rendered docs and raw MDX appear to diverge, treat the raw `main` branch as the editable source but cite the rendered docs URL in user-facing answers.
- If rendered docs and local sdk-rust source disagree about API details, trust the local source for code changes in this checkout and mention the docs mismatch.
