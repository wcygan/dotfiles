# Playwright CLI Reference for UX Review Agents

Quick reference for the Playwright CLI commands most useful during UX reviews.
Always use your assigned session name (`-s=<session>`) to avoid conflicts with other agents.

## Session Management

```bash
# Open browser with named session
playwright-cli -s=<session> open <url>

# Navigate to a different page
playwright-cli -s=<session> goto <url>

# Close your session when done
playwright-cli -s=<session> close

# List all active sessions (coordinator only)
playwright-cli list
playwright-cli close-all
```

## Capturing Page State

### Snapshots (Structured Text — Primary Analysis Tool)
Snapshots return the page's accessibility tree with element references (refs).
This is your primary tool for understanding page structure, text content, and element relationships.

```bash
# Capture snapshot to stdout
playwright-cli -s=<session> snapshot

# Save to file for later reference
playwright-cli -s=<session> snapshot --filename=<name>.txt
```

Snapshots contain:
- All visible text content
- Element types (button, link, heading, input, etc.)
- Element references (e.g., `e21`, `e35`) for interaction
- ARIA roles and labels
- Form field states (checked, selected, disabled)
- Hierarchical structure

### Screenshots (Visual Evidence)
Screenshots capture what the user actually sees — use for visual design assessment.

```bash
# Full page screenshot
playwright-cli -s=<session> screenshot --filename=<name>.png

# Screenshot of a specific element
playwright-cli -s=<session> screenshot <ref> --filename=<name>.png
```

## Interacting with the Page

```bash
# Click an element (use ref from snapshot)
playwright-cli -s=<session> click <ref>

# Type text (into focused element)
playwright-cli -s=<session> type <text>

# Fill a specific input field
playwright-cli -s=<session> fill <ref> <text>

# Check/uncheck checkboxes
playwright-cli -s=<session> check <ref>
playwright-cli -s=<session> uncheck <ref>

# Select dropdown option
playwright-cli -s=<session> select <ref> <value>

# Hover over element
playwright-cli -s=<session> hover <ref>
```

## Navigation

```bash
# Go back/forward
playwright-cli -s=<session> go-back
playwright-cli -s=<session> go-forward

# Reload
playwright-cli -s=<session> reload
```

## Keyboard

```bash
# Press a key
playwright-cli -s=<session> press Tab
playwright-cli -s=<session> press Enter
playwright-cli -s=<session> press Escape
playwright-cli -s=<session> press ArrowDown
```

## Viewport & Responsive Testing

```bash
# Resize to desktop
playwright-cli -s=<session> resize 1440 900

# Resize to tablet
playwright-cli -s=<session> resize 768 1024

# Resize to mobile
playwright-cli -s=<session> resize 375 812
```

## JavaScript Evaluation

```bash
# Scroll down one viewport
playwright-cli -s=<session> eval "window.scrollBy(0, window.innerHeight)"

# Scroll to top
playwright-cli -s=<session> eval "window.scrollTo(0, 0)"

# Get computed styles
playwright-cli -s=<session> eval "JSON.stringify(window.getComputedStyle(document.querySelector('h1')))"

# Count elements
playwright-cli -s=<session> eval "document.querySelectorAll('a').length"

# Check page title
playwright-cli -s=<session> eval "document.title"

# Get all link texts
playwright-cli -s=<session> eval "[...document.querySelectorAll('a')].map(a => a.textContent.trim()).filter(Boolean)"

# Check meta description
playwright-cli -s=<session> eval "document.querySelector('meta[name=description]')?.content"
```

## DevTools / Diagnostics

```bash
# Check console for errors
playwright-cli -s=<session> console error

# List network requests
playwright-cli -s=<session> network

# View all console messages
playwright-cli -s=<session> console
```

## Tabs

```bash
# Open new tab
playwright-cli -s=<session> tab-new <url>

# List tabs
playwright-cli -s=<session> tab-list

# Switch tab
playwright-cli -s=<session> tab-select <index>

# Close tab
playwright-cli -s=<session> tab-close <index>
```

## Best Practices for UX Review Agents

1. **Always snapshot before interacting** — Know what's on the page before clicking
2. **Use refs from snapshots** — Don't guess element selectors, use the provided refs
3. **Screenshot at key moments** — Visual evidence for the report
4. **Check both desktop and mobile** — Resize viewport and re-snapshot
5. **Test error states** — Fill forms incorrectly to see error handling
6. **Check console for errors** — JavaScript errors affect UX
7. **Close your session** — Always clean up when done
