---
description: Crawl documentation site to learn how a technology works
---

Scan and crawl the documentation URL provided to build comprehensive understanding of the technology.

**Input:** A documentation URL (e.g., `https://docs.temporal.io`, `https://kubernetes.io/docs`)

**Crawling strategy:**

1. **Start page**: Fetch the provided URL first
2. **Navigation discovery**: Identify sidebar, table of contents, or navigation links
3. **Priority pages** (fetch in order):
   - Getting started / Quickstart
   - Core concepts / Overview
   - Architecture / How it works
   - API reference (key endpoints/methods only)
   - Configuration / Setup
   - Best practices / Patterns
   - Common pitfalls / Troubleshooting
4. **Depth limit**: Stay within documentation domain, max 10-15 pages
5. **Skip**: Changelogs, release notes, contributor guides, translations

**Process:**

1. Fetch starting URL, extract navigation structure
2. Identify and prioritize key documentation pages
3. Fetch high-value pages sequentially (use WebFetch tool)
4. Extract and synthesize core knowledge
5. Build mental model of the technology

**Output format:**

# Documentation Scan: {Technology Name}

## Overview
Brief description of what this technology is and solves (2-3 sentences)

## Core Concepts
- **Concept 1**: Definition and purpose
- **Concept 2**: Definition and purpose
- **Concept 3**: Definition and purpose

## Architecture
How the system is structured, key components and their relationships

## Quick Start Essentials
Minimal steps to get running:
```
1. Install: {command}
2. Configure: {key config}
3. Run: {command}
```

## Key APIs / Interfaces
Most important methods, endpoints, or commands with brief descriptions

## Configuration Options
Critical settings and their defaults

## Common Patterns
Recommended ways to use the technology

## Gotchas & Pitfalls
- Known issues or surprising behaviors
- Common mistakes to avoid

## When to Use / When Not to Use
- Good fit scenarios
- Anti-patterns or poor fits

## Pages Scanned
- [Page title](url) - brief note
- [Page title](url) - brief note

---

**Execution notes:**
- Use WebFetch tool to retrieve each page
- Extract content intelligently, skip boilerplate/navigation
- If a page redirects, follow the redirect
- If access is blocked, note it and continue with other pages
- Synthesize, don't just copy-paste

**Example usage:**
- `/doc-scan https://docs.temporal.io`
- `/doc-scan https://connectrpc.com/docs`
- `/doc-scan https://kubernetes.io/docs/concepts/`

---

Scan documentation starting at: $ARGUMENTS
