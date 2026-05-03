# Anthropic Skill Best Practices — Key Takeaways

Source: "The Complete Guide to Building Skills for Claude" (Anthropic, Jan 2026)

## Critical Rules We Must Follow

1. **SKILL.md naming** — Must be exactly `SKILL.md` (case-sensitive) ✅ We have this
2. **Folder naming** — kebab-case only ✅ `visualize/`
3. **No README.md inside skill folder** — All docs in SKILL.md or references/ ⚠️ Need to check
4. **YAML frontmatter** — Must have `---` delimiters, `name` and `description` required
5. **No XML tags** (`<` or `>`) in frontmatter — security restriction
6. **Description must include WHAT and WHEN** — trigger phrases are critical
7. **SKILL.md under 5,000 words** — move detailed docs to references/
8. **No "claude" or "anthropic" in skill name** — reserved

## Progressive Disclosure (3 levels)
- **Level 1 (YAML frontmatter)**: Always in system prompt. Minimal — just enough to trigger.
- **Level 2 (SKILL.md body)**: Loaded when skill is relevant. Full instructions.
- **Level 3 (references/)**: Linked files loaded only as needed.

## Our Category
We are **Category 1: Document & Asset Creation** — creating consistent, high-quality output.

## Key Patterns
- **Pattern 3: Iterative refinement** — matches our eval loop approach
- **Pattern 5: Domain-specific intelligence** — our design system knowledge

## What We Should Fix
1. Check if we have README.md inside skill folder (forbidden)
2. SKILL.md might be too long (>5000 words) — move more to references/
3. Ensure YAML description includes clear trigger phrases
4. Add `metadata` fields (author, version)
5. Consider adding `license: MIT` to frontmatter
6. Add `allowed-tools` if applicable
