# Commands

Source: https://portless.sh/commands
Checked: 2026-05-23

Use this reference when choosing CLI syntax, lifecycle commands, flags, aliases, proxy/service controls, hosts commands, or bypass behavior.

## Zero-Argument Mode

```sh
portless
```

Runs the configured package script, defaulting to `"dev"`, through the proxy. From a monorepo root, starts workspace packages that have the target script.

Override the script for one invocation:

```sh
portless --script start
```

## Run An App

Infer name from project/config:

```sh
portless run
portless run next dev
portless run --name myapp next dev
```

Use explicit name:

```sh
portless myapp next dev
portless api pnpm start
portless docs.myapp next dev
```

Flags:

- `--name <name>`: override inferred base name for `portless run`; git worktree prefixes still apply.
- `--script <name>`: use a package script other than `"dev"`.
- `--app-port <number>`: force the child app port.
- `--force`: override an existing route registered by another process.

Reserved app names are subcommands: `run`, `get`, `alias`, `hosts`, `list`, `trust`, `clean`, `prune`, `proxy`, and `service`. Use `portless run <cmd>` or `portless --name <name> <cmd>` when a name collides.

## Get A Service URL

```sh
portless get backend
```

Use in scripts:

```sh
BACKEND_URL=$(portless get backend)
```

Worktree prefix detection applies by default. Use `--no-worktree` to skip it.

## Static Routes

Register services not managed by Portless, such as Docker containers:

```sh
portless alias my-postgres 5432
portless alias redis 6379
portless alias my-postgres 5432 --force
portless alias --remove my-postgres
```

Aliases persist across stale-route cleanup.

## Route Listing

```sh
portless list
```

Shows active routes and assigned ports.

## Trust

```sh
portless trust
```

Adds the Portless local CA to the OS trust store for generated HTTPS certificates. This can prompt for admin privileges; ask before running it.

## Cleanup

```sh
portless clean
```

Stops the proxy, removes Portless-installed CA trust, deletes allowed Portless state, clears the system state directory and `PORTLESS_STATE_DIR` when set, and removes the Portless block from `/etc/hosts`. Custom cert/key paths are not removed.

Ask before running because it modifies machine state.

## Prune Orphans

```sh
portless prune
portless prune --force
```

Finds dev server processes left behind by crashed Portless sessions. Default behavior terminates orphans and removes stale routes. `--force` sends SIGKILL; only use it when the user asks for forceful cleanup.

## Proxy Control

Start:

```sh
portless proxy start
```

Useful flags:

- `-p, --port <number>`: proxy port; default is `443` with HTTPS or `80` with `--no-tls`.
- `--no-tls`: use plain HTTP.
- `--https`: explicit HTTPS, accepted for compatibility.
- `--lan`: mDNS `.local` domains for real device testing.
- `--ip <address>`: override LAN IP with `--lan`.
- `--tld <tld>`: custom TLD instead of `.localhost`.
- `--cert <path>` and `--key <path>`: custom TLS certificate and key.
- `--foreground`: debug in foreground instead of daemon mode.
- `--wildcard`: let unregistered subdomains fall back to a parent route.

Stop:

```sh
portless proxy stop
```

## OS Startup Service

```sh
portless service install
portless service status
portless service uninstall
```

Startup service install/removal can require administrator privileges. `portless clean` removes the service automatically.

## LAN Mode

```sh
portless proxy start --lan
portless proxy start --lan --https
portless proxy start --lan --ip 192.168.1.42
```

Set default LAN mode:

```sh
export PORTLESS_LAN=1
```

Portless remembers LAN mode via `proxy.lan`. Use `PORTLESS_LAN=0` to override it for one start.

Linux needs `avahi-utils`; macOS has the needed mDNS tool built in. Windows is not supported for LAN mode.

## Hosts

```sh
portless hosts sync
portless hosts clean
```

Auto-sync is enabled by default. Disable with:

```sh
PORTLESS_SYNC_HOSTS=0
```

These commands edit `/etc/hosts`; ask before running them.

## Bypass

```sh
PORTLESS=0 pnpm dev
```

Runs the app command directly without the Portless proxy.

## Info

```sh
portless --help
portless --version
```
