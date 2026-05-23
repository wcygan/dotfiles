# Getting Started

Source: https://portless.sh/
Checked: 2026-05-23

Use this reference for first-time setup, simple script migration, subdomains, worktrees, custom TLDs, and baseline requirements.

## What Portless Does

Portless replaces `localhost:<port>` URLs with stable named dev URLs such as `https://myapp.localhost`. It runs a reverse proxy on port 443 by default, assigns the app a random local port, and routes requests from the named host to that app.

Basic mapping:

```text
Browser -> Portless proxy on 443 -> app on an assigned local port
```

## Install

Global install is the docs' recommended default:

```sh
npm install -g portless
```

Project dependency:

```sh
npm install -D portless
```

Project install can be useful for reproducibility, but Portless is pre-1.0 and state format changes can require re-running trust setup. Use global install when the priority is one consistent local proxy on the machine.

## Run Modes

Zero-argument mode:

```sh
portless
```

This reads the `"dev"` script from `package.json`, infers the app name from config, package metadata, git root, or directory name, and runs the app through the proxy.

Explicit command with inferred name:

```sh
portless run next dev
```

Explicit URL name:

```sh
portless myapp next dev
```

Expected URL:

```text
https://myapp.localhost
```

## HTTPS Default

HTTPS with HTTP/2 is enabled by default. On first run, Portless generates a local CA and server certificates, trusts the CA, and binds port 443. On macOS and Linux this can require `sudo`.

Use plain HTTP only when needed:

```sh
portless proxy start --no-tls
```

## Assigned App Ports

Portless assigns random app ports in the `4000-4999` range and injects `PORT` into the child process. It also handles common frameworks that ignore `PORT` by adding the right `--port` flag and, when needed, `--host`.

Frameworks called out by the docs include Next.js, Express, Nuxt, Vite, Astro, React Router, Angular, Expo, and React Native.

## package.json Usage

Keep scripts clean and let `portless` wrap the existing dev command:

```json
{
  "scripts": {
    "dev": "next dev"
  }
}
```

Then run:

```sh
portless
```

Direct script wrapping also works:

```json
{
  "scripts": {
    "dev": "portless myapp next dev"
  }
}
```

Prefer the cleaner `portless` plus config shape for larger repos, especially monorepos and Turborepo projects.

## Subdomains

Use dotted names for related services:

```sh
portless api.myapp pnpm start
portless docs.myapp next dev
```

Expected URLs:

```text
https://api.myapp.localhost
https://docs.myapp.localhost
```

## Git Worktrees

`portless run` detects linked git worktrees and prepends the branch name as a subdomain. A main worktree can keep `https://myapp.localhost`, while a `fix-ui` worktree can use `https://fix-ui.myapp.localhost`.

Use `--name` to override the base name while keeping the worktree prefix:

```sh
portless run --name myapp next dev
```

## Custom TLD

Default TLD:

```text
.localhost
```

Use another TLD:

```sh
portless proxy start --tld test
portless myapp next dev
```

Expected URL:

```text
https://myapp.test
```

The docs recommend `.test` for custom dev names, warn against `.local` because it conflicts with mDNS/Bonjour, and warn against `.dev` because browser HSTS behavior forces HTTPS.

## Requirements

- Node.js 24+
- macOS, Linux, or Windows
