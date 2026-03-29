---
title: Complete Skill-Building Guide
canonical_url: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
fetch_before_acting: true
---

# Complete Skill-Building Guide (PDF)

> Before building or reviewing skills, WebFetch https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf for the latest.

## Summary

Anthropic's comprehensive guide covering the full skill lifecycle: design, write, test, iterate.

### Key Concepts

**Progressive Disclosure** — Three loading levels:
1. Frontmatter description (always in context)
2. SKILL.md body (loaded on invoke)
3. Reference files (loaded on demand via `References:` links)

**Conciseness** — Default assumption is Claude is already smart. Only include what Claude can't derive from code, tools, or general knowledge.

**Degrees of Freedom** — Match specificity to fragility:
- Exact commands for safety-critical operations
- Goals-only for creative/context-dependent work

**Testing Skills** — Three test types:
1. Triggering tests — does it invoke at the right time?
2. Functional tests — does it produce correct output?
3. Comparison tests — is it better than no skill?

**Feedback Loops** — "Run → check → fix → repeat" pattern. Provide checklists Claude can track.

### Scripts > Generated Code

Bundled scripts in `scripts/` are:
- More reliable than generated code
- Save tokens (no code generation)
- Save time (no generation step)
- Ensure consistency across invocations

### Anti-Patterns

- README.md in skill folders (not loaded by Claude)
- Over-specified instructions for things Claude already knows
- Deeply nested references (keep one level deep)
- Vague descriptions that never trigger
- Missing keywords in description
