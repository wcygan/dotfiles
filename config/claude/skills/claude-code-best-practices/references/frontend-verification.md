---
title: Frontend Verification (Chrome Extension & Desktop Preview)
canonical_url: https://code.claude.com/docs/en/chrome
fetch_before_acting: true
---

# Frontend Verification

> Before setting up frontend verification, WebFetch https://code.claude.com/docs/en/chrome for the latest.

## The Key Principle

**Give Claude a way to verify its output.** Once Claude can see the result of its changes — in a browser, via screenshots, through console logs — it will iterate until the result is correct. Without verification, frontend work is guesswork.

## Option 1: Chrome Extension (CLI & VS Code)

Connect Claude Code to your Chrome browser for live debugging, design verification, and web app testing.

### Prerequisites

- Google Chrome or Microsoft Edge
- [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) v1.0.36+
- Claude Code v2.0.73+
- Direct Anthropic plan (Pro, Max, Teams, Enterprise)

### Quick Start

```bash
# Start with Chrome integration
claude --chrome

# Or enable from within a session
/chrome
```

### Enable by Default

Run `/chrome` and select "Enabled by default" to avoid passing `--chrome` each session.

### Capabilities

- **Live debugging**: read console errors and DOM state, then fix the causing code
- **Design verification**: build UI from a mock, then open in browser to verify
- **Web app testing**: test form validation, check visual regressions, verify user flows
- **Authenticated apps**: interact with Google Docs, Gmail, Notion — anything you're logged into
- **Data extraction**: pull structured information from web pages
- **Session recording**: record browser interactions as GIFs

### Example Workflows

```text
# Test local web app
I just updated the login form. Open localhost:3000, try submitting
with invalid data, and check if error messages appear correctly.

# Debug with console
Open the dashboard and check the console for errors on page load.

# Design verification
Build this component to match the mockup, then open it and compare.
```

### How It Works

Claude opens new tabs for browser tasks. It shares your browser's login state, so authenticated apps work automatically. Actions run in a visible Chrome window in real time. When Claude hits a login page or CAPTCHA, it pauses and asks you to handle it.

## Option 2: Desktop App Preview

The Desktop app bundles a built-in browser that Claude can use to start dev servers and test changes automatically.

### How It Works

Claude starts your dev server, opens an embedded browser, and auto-verifies changes after every edit. It takes screenshots, inspects DOM, clicks elements, fills forms, and fixes issues it finds.

### Features

- Auto-starts dev server based on project config
- Embedded browser for instant verification
- Persistent cookies/local storage across restarts
- Works for both frontend and backend (API endpoint testing)

### Configure

Edit `.claude/launch.json` for custom dev commands. Enable/disable in Settings → Claude Code → Preview.

### When to Use Which

| Feature | Chrome Extension | Desktop Preview |
|---------|-----------------|-----------------|
| Platform | CLI, VS Code | Desktop app only |
| Browser | Your Chrome/Edge | Built-in embedded |
| Auth state | Your browser sessions | Separate (with persist option) |
| Setup | Install extension + `--chrome` | Built-in, no setup |
| Best for | Authenticated apps, complex testing | Quick iteration, auto-verify |

## Tips

- **Always verify frontend changes** — "write code, then check it" is dramatically better than "write code and hope"
- Chrome extension tends to be more reliable than similar MCP-based approaches
- For backend APIs: Desktop preview can test endpoints and view server logs too
- Use GIF recording to document UI changes for PRs
