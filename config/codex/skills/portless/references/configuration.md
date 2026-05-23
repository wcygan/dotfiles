# Configuration

Source: https://portless.sh/configuration
Checked: 2026-05-23

Use this reference when adding `portless.json`, using the package.json `"portless"` key, configuring workspaces, choosing precedence, setting environment variables, inspecting state, or controlling port assignment.

## Default Config

Bare command:

```sh
portless
```

Defaults:

- Run the `"dev"` script.
- Infer the app name from package metadata, git root, or directory.
- Route through the Portless proxy when the command is a server.

## portless.json

Minimal name override:

```json
{ "name": "myapp" }
```

Then:

```sh
portless
```

Expected URL:

```text
https://myapp.localhost
```

## Fields

Top-level fields:

- `name`: base app name; worktree prefix still applies.
- `script`: package script to run; default is `"dev"`.
- `appPort`: fixed child-process port instead of auto-assignment.
- `proxy`: whether to route through the proxy; auto-detected by default.
- `apps`: workspace package overrides keyed by relative path.
- `turbo`: set `false` to use direct spawning instead of Turborepo in multi-app mode.

Each `apps` entry supports the same per-app fields: `name`, `script`, `appPort`, and `proxy`.

When `apps` is present, top-level fields apply only in single-app mode.

## package.json "portless" Key

String shorthand:

```json
{
  "name": "@myorg/web",
  "portless": "myapp"
}
```

Object form:

```json
{
  "name": "@myorg/web",
  "portless": {
    "name": "myapp",
    "script": "dev:app"
  }
}
```

The package.json `"portless"` key overrides matching `portless.json` app entries. CLI flags override both.

## Monorepos

One root `portless.json` can cover all workspace packages. Portless discovers packages from `pnpm-workspace.yaml` or package manager workspaces in `package.json`.

Example:

```json
{
  "apps": {
    "apps/web": { "name": "myapp" },
    "apps/api": { "name": "api.myapp" }
  }
}
```

From the repo root:

```sh
portless
```

Start just one package:

```sh
cd apps/web
portless
```

Override script:

```sh
portless --script start
```

Without an `apps` map, hostnames use a `<package>.<project>.localhost` convention. The project name comes from the most common npm scope across workspace packages, falling back to the root directory name.

## Turborepo

For Turborepo, put `portless` in the `dev` script and keep the actual app command in another script:

```json
{
  "scripts": {
    "dev": "portless",
    "dev:app": "next dev"
  },
  "portless": { "name": "myapp", "script": "dev:app" }
}
```

The root `pnpm dev` can still run through Turbo. Portless detects the package manager and runs the configured app script through the proxy. People without Portless can run the real app script directly.

## Precedence

Name precedence:

```text
CLI --name > package.json "portless" > portless.json app entry > package.json inference
```

Script precedence:

```text
CLI --script > package.json "portless" > portless.json app entry > "dev"
```

App port precedence:

```text
CLI --app-port > PORTLESS_APP_PORT > package.json "portless" > portless.json app entry > auto-assigned
```

## Environment Variables

Configuration:

- `PORTLESS_PORT`: proxy port.
- `PORTLESS_HTTPS=0`: disable HTTPS.
- `PORTLESS_LAN=1`: enable LAN mode.
- `PORTLESS_TLD`: custom TLD instead of `localhost`.
- `PORTLESS_APP_PORT`: fixed app port instead of random assignment.
- `PORTLESS_SYNC_HOSTS=0`: disable `/etc/hosts` sync.
- `PORTLESS_STATE_DIR`: override state directory.
- `PORTLESS=0`: bypass the proxy.

Repository README also documents:

- `PORTLESS_WILDCARD=1`: allow unregistered subdomains to fall back to parent route.
- `PORTLESS_TAILSCALE=1`: share apps on Tailscale by default.
- `PORTLESS_FUNNEL=1`: expose apps through Tailscale Funnel by default.

Injected into child processes:

- `PORT`: assigned app port.
- `HOST`: usually `127.0.0.1`, with framework exceptions.
- `PORTLESS_URL`: public local URL.
- `PORTLESS_TAILSCALE_URL`: Tailscale URL when active.
- `NODE_EXTRA_CA_CERTS`: CA path when HTTPS is active.

## State Directory

Default state directory:

```text
~/.portless
```

Override:

```sh
PORTLESS_STATE_DIR=/path/to/state
```

State files:

- `routes.json`: route hostname to port mappings.
- `routes.lock`: concurrent write lock.
- `proxy.pid`: running proxy process ID.
- `proxy.port`: proxy listen port.
- `proxy.log`: proxy daemon logs.
- `proxy.lan`: remembered LAN mode and last LAN IP.

## Port Assignment

Apps get a random port in `4000-4999` unless a fixed app port is configured. Portless sets `PORT` and usually `HOST` before running the child command.

For frameworks that ignore `PORT`, Portless can inject `--port` and a matching `--host` when needed.
