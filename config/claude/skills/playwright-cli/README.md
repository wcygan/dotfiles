# playwright-cli Skill

Global skill for browser automation using the [playwright-cli](https://github.com/mxschmitt/playwright-go) tool.

## Overview

This skill enables Claude to automate browser interactions for:
- Web application testing
- Form filling and submission
- Screenshot and PDF generation
- Data extraction from web pages
- Browser debugging and DevTools inspection

## Activation

The skill activates when users mention browser automation tasks:
- "Navigate to example.com and take a screenshot"
- "Fill out this form on the website"
- "Test the login flow on this site"
- "Extract data from this web page"
- "Debug the console errors on this page"

## Key Features

### Core Commands
- `playwright-cli open` - Launch browser
- `playwright-cli snapshot` - Capture page structure with element IDs
- `playwright-cli click e3` - Click elements by reference
- `playwright-cli screenshot` - Capture screenshots
- `playwright-cli close` - Close browser

### Advanced Capabilities
- Multi-tab workflows
- Cookie and localStorage management
- Network request mocking
- Video recording and tracing
- Test code generation

## Tool Restrictions

This skill is restricted to `Bash(playwright-cli:*)` only - it can only execute playwright-cli commands. This prevents accidental execution of other commands and keeps the skill focused.

## Reference Documentation

Detailed guides are available in the `references/` directory:
- `request-mocking.md` - Mock HTTP requests
- `running-code.md` - Execute custom Playwright code
- `session-management.md` - Manage multiple browser sessions
- `storage-state.md` - Save/restore cookies and localStorage
- `test-generation.md` - Generate Playwright test code
- `tracing.md` - Record browser traces
- `video-recording.md` - Record browser sessions

## Installation

This skill is automatically available in any project that links the dotfiles claude config:

```bash
cd ~/Development/dotfiles
./scripts/link-config.sh
```

The skill will be available at `~/.claude/skills/playwright-cli/`.

## Usage Example

```bash
# User: "Navigate to example.com and click the login button"
# Claude activates playwright-cli skill:

playwright-cli open https://example.com
playwright-cli snapshot
# (reviews element IDs from snapshot output)
playwright-cli click e5  # Clicks login button
playwright-cli screenshot --filename=after-login.png
playwright-cli close
```

## Distribution

This skill is part of the dotfiles repository and distributed to all systems via the config linking script. Any updates to the skill are automatically synchronized across all machines.
