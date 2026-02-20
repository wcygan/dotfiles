---
title: Naming & Descriptions
description: Rules for skill names and descriptions with good/bad examples
tags: [naming, descriptions, templates, examples]
---

# Naming & Descriptions

## Name Generation

Based on capability, suggest:

| Capability    | Suggested Name           |
|---------------|--------------------------|
| Code Analysis | `code-quality-analyzer`  |
| Test Generation | `test-suite-generator` |
| Documentation | `doc-generator`          |
| Data Processing | `data-processor`       |
| Custom        | descriptive kebab-case   |

**Naming rules:**
- Lowercase letters, numbers, hyphens only
- Max 64 characters
- Descriptive (what it does, not how)
- Examples: `pdf-text-extractor`, `api-doc-generator`, `test-coverage-analyzer`

## Description Template

```
[Primary function]. [Secondary capabilities]. Use when [trigger scenarios]. Keywords: [comma-separated terms].
```

**Requirements:**
1. What it does (functionality)
2. When to use it (trigger conditions)
3. Trigger keywords (terms users might mention)
4. Max 1024 characters total

## Good Examples

✅ "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files, documents, or form processing. Keywords: PDF, extract, document, form, merge"

✅ "Generate comprehensive unit and integration tests with high coverage. Use when adding tests, improving coverage, or implementing TDD. Keywords: test, testing, coverage, unit test, integration test, TDD"

✅ "Analyze code for security vulnerabilities, performance issues, and maintainability problems. Use when reviewing code or conducting security audits. Keywords: security, vulnerability, code review, audit, performance"

## Bad Examples

❌ "Helps with documents" — too vague, no triggers, no keywords
❌ "Processes things" — no triggers, no subject matter
❌ "Does code stuff" — non-descriptive, won't match any user request
