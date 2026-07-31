# Reading Pi SDK documentation

Use this procedure before relying on a Pi SDK symbol or option. Pi changes
quickly, and the package scope and docs layout can differ between releases.

## Establish the installed version

Run:

```bash
command -v pi
pi --version
PI_CODING_AGENT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/pi-sdk-agent.XXXXXX")" \
  pi --offline --help
```

The isolated `PI_CODING_AGENT_DIR` protects live Pi settings and sessions if
help initialization needs a writable directory. Do not inspect or print
credentials from the real Pi directory.

## Locate matching local docs

Resolve the CLI path with Node so symlinked user-prefix installs work on macOS,
Linux, and Fedora without assuming a checkout location:

```bash
pi_path="$(command -v pi)"
package_root="$(node -e '
  const fs = require("node:fs");
  const path = require("node:path");
  const cli = fs.realpathSync(process.argv[1]);
  process.stdout.write(path.dirname(path.dirname(cli)));
' "$pi_path")"

node -e '
  const p = require(process.argv[1]);
  console.log(`${p.name} ${p.version}`);
' "$package_root/package.json"
sed -n '1,260p' "$package_root/docs/sdk.md"
```

For a source checkout, inspect `packages/coding-agent/package.json` and
`packages/coding-agent/docs/sdk.md` only after comparing its version with
`pi --version`. The installed package and its types are authoritative for the
runtime being used.

## Fallback order

Use these sources in order:

1. Installed package `docs/sdk.md` and `dist/index.d.ts`.
2. A source checkout whose `packages/coding-agent/package.json` version
   matches the installed CLI.
3. The [official Pi SDK documentation](https://pi.dev/docs/latest/sdk) when
   local docs are absent or stale.

Label answers as version-matched, source-derived, or latest-online when the
sources do not align. Use the official examples under the SDK docs when a
minimal reproduction is needed; do not assume an example's package scope is
valid for an older release.

## Search strategy

Use `rg` against the matching docs and declaration files for a symbol before
searching the whole Pi monorepo:

```bash
rg -n "createAgentSession|AgentSessionRuntime|defineTool|ModelRuntime|ResourceLoader" \
  "$package_root/docs/sdk.md" "$package_root/dist/index.d.ts"
```

If the docs and declarations disagree, report the disagreement and prefer the
declaration plus a minimal typecheck for the installed package. Do not invent
an API from a similarly named CLI or extension method.
