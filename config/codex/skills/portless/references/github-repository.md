# GitHub Repository

Source: https://github.com/vercel-labs/portless
Checked: 2026-05-23

Use this reference for README-level details that go beyond the short docs pages: LAN mode, Tailscale/Funnel sharing, Safari/DNS behavior, proxying between Portless apps, repository development, and reset behavior.

## Repository Identity

The repository is `vercel-labs/portless`. The publishable package lives in `packages/portless/`, and the repo is a pnpm workspace using Turborepo.

The README frames Portless as a development tool that replaces port-number URLs with stable named `.localhost` URLs.

## Repo Development

Requirements for developing Portless itself:

- Node.js 24+
- pnpm 11
- macOS, Linux, or Windows

Useful repo commands from the README:

```sh
pnpm install
pnpm build
pnpm test
pnpm test:coverage
pnpm lint
pnpm type-check
pnpm format
```

Use these commands only when working on the Portless repository itself, not when configuring a downstream app to use Portless.

## LAN Mode

LAN mode makes services reachable from phones or other devices on the same Wi-Fi through mDNS `.local` domains:

```sh
portless proxy start --lan
portless proxy start --lan --https
portless proxy start --lan --ip 192.168.1.42
```

Operational notes:

- Portless advertises services as `<name>.local`.
- Portless can auto-detect and follow LAN IP changes.
- `--ip <address>` or `PORTLESS_LAN_IP` pins a LAN address.
- `PORTLESS_LAN=1` makes LAN mode the default.
- `PORTLESS_LAN=0` can override remembered LAN mode for one start.
- macOS uses built-in `dns-sd`.
- Linux needs `avahi-publish-address` from `avahi-utils`.
- Windows LAN mode is not supported in the README notes.

Framework notes:

- Next.js LAN mode needs `.local` origins in `allowedDevOrigins`, including wildcard worktree-prefixed hosts.
- Vite, React Router, SvelteKit, and Astro are handled through additional allowed-host injection.
- Expo and React Native get framework-specific host handling; iOS may need local networking allowances.

## Tailscale Sharing

Use Tailscale sharing when the user wants teammates on a tailnet to access the dev server:

```sh
portless myapp --tailscale next dev
```

The app remains available locally and also gets a tailnet HTTPS URL. Additional Tailscale-shared apps use ports such as `8443`, `8444`, and so on.

Expose publicly through Tailscale Funnel:

```sh
portless myapp --funnel next dev
```

Prerequisites:

- Tailscale CLI installed and connected with `tailscale up`.
- Tailscale HTTPS certificates enabled.
- Funnel enabled for the tailnet and node when using `--funnel`.

Environment defaults:

```sh
PORTLESS_TAILSCALE=1
PORTLESS_FUNNEL=1
```

Do not enable Funnel casually. It exposes the dev server publicly and should be user-directed.

## Safari And DNS

Some Safari configurations may not resolve `.localhost` subdomains through the browser path. Portless can sync current route hostnames into `/etc/hosts`:

```sh
portless hosts sync
portless hosts clean
```

Auto-sync is on by default for route hostnames, including `.localhost`, custom TLDs, and LAN `.local`. Disable with:

```sh
PORTLESS_SYNC_HOSTS=0
```

Because these commands modify `/etc/hosts`, ask before running them.

## Proxying Between Portless Apps

When a frontend dev server proxies API requests to another Portless app, the proxy must rewrite the `Host` header. Otherwise Portless can route back to the frontend and create a loop.

Vite shape:

```ts
server: {
  proxy: {
    "/api": {
      target: "https://api.myapp.localhost",
      changeOrigin: true,
      ws: true,
    },
  },
}
```

webpack-dev-server shape:

```js
devServer: {
  proxy: [{
    context: ["/api"],
    target: "https://api.myapp.localhost",
    changeOrigin: true,
  }],
}
```

Portless sets `NODE_EXTRA_CA_CERTS` for child processes so Node.js trusts the local CA. For Node.js processes not started by Portless, either set `NODE_EXTRA_CA_CERTS=~/.portless/ca.pem` or use plain HTTP with `--no-tls`.

Portless can detect this routing loop and return a `508 Loop Detected` response with guidance.

## Startup Service

Commands:

```sh
portless service install
portless service status
portless service uninstall
```

The service uses Portless defaults: HTTPS on port 443 with `.localhost` names. macOS and Linux use a root-owned service so port 443 can bind at boot. Windows uses a Task Scheduler startup task. Ask before installing or removing services.

## Reset

Reset Portless state:

```sh
portless clean
```

This removes proxy state, system state, the local CA trust entry when Portless installed it, and the Portless hosts block. It may prompt for admin privileges. Custom cert/key files are not deleted.
