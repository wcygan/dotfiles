---
description: Generate tests for code following TDD principles
allowed-tools: Read, Write, Bash(fd:*)
argument-hint: <@file-to-test>
---

## Context
- Target: $ARGUMENTS
- Existing tests: !`fd -g "*test*" -e rs -e go -e ts -e java $(git rev-parse --show-toplevel 2>/dev/null || pwd) -d 3`

## Task
Generate tests following this project's patterns:

1. Read target code and identify test location
2. Follow language conventions:
   - **Go**: table-driven tests, 95%+ coverage
   - **Rust**: unit tests in same file, integration in tests/
   - **Deno/TS**: tests/ directory with unit/integration/e2e
   - **Java**: src/test/ mirror structure
3. Cover happy path + edge cases
4. Write tests BEFORE implementation if TDD mode

Keep tests simple, focused, and maintainable.
