---
name: idiomatic-rust
description: Analyze and generate idiomatic Rust code following official style guide, std library conventions, and API design guidelines. Auto-loads when writing, reviewing, or refactoring Rust code. Use when writing Rust, reviewing Rust code, checking Rust idioms, or generating Rust scaffolding. Keywords: rust, idiomatic, ownership, borrowing, lifetime, trait, error handling, pattern matching, clippy, rustfmt, cargo
---

# Idiomatic Rust

Analyze existing Rust code for idiomatic patterns and generate new Rust code that follows official conventions from the Rust Reference, Standard Library, Style Guide, and API Guidelines.

## Analysis Mode

When reviewing Rust code, check these dimensions in order:

1. **Ownership & Borrowing** — correct move/borrow/lifetime usage, minimal cloning
2. **Error Handling** — `Result`/`?` propagation, no unwrap in library code, typed errors
3. **Naming & API Design** — `as_`/`to_`/`into_` conventions, getter naming, casing
4. **Trait Implementations** — derive standard traits, implement `Display`/`Error`/`From`
5. **Iterator & Closure Patterns** — prefer combinators over manual loops
6. **Type Safety** — newtypes, enums over booleans, builder pattern
7. **Style & Formatting** — rustfmt compliance, 100-char lines, trailing commas

Present findings as:
- **Issues**: Non-idiomatic patterns with file:line, explanation, and fix
- **Suggestions**: Improvements that would make code more Rustic
- **Good**: Patterns already done well (brief)

References: [ownership-and-borrowing](references/ownership-and-borrowing.md)
References: [error-handling](references/error-handling.md)
References: [traits-and-types](references/traits-and-types.md)
References: [naming-and-api-design](references/naming-and-api-design.md)
References: [iterators-and-closures](references/iterators-and-closures.md)
References: [style-and-formatting](references/style-and-formatting.md)
References: [concurrency](references/concurrency.md)

## Generation Mode

When writing new Rust code:

- Derive `Debug` on all types; derive `Clone, PartialEq, Eq, Hash, Default` where appropriate
- Use `thiserror` for library errors, `anyhow` for application errors
- Accept borrowed params (`&str`, `&[T]`, `&Path`), return owned types
- Use `impl Into<String>` / `impl AsRef<Path>` for flexible APIs
- Prefer `Result<T, E>` returns; reserve `panic!` for invariant violations
- Use iterators and combinators over manual indexing
- Apply `#[must_use]` on functions whose return value should not be ignored
- Add `#[non_exhaustive]` on public enums and structs with fields
- Write doc comments with examples using `?` (not `unwrap()`)
- Follow rustfmt defaults: 4-space indent, 100-char width, trailing commas in multi-line

## Workflow

1. Read the Rust files under review (or understand the generation request)
2. Load relevant reference files for the specific patterns involved
3. For analysis: identify non-idiomatic patterns, explain why, show idiomatic alternative
4. For generation: write code following all conventions, run `cargo check` if available
5. Suggest `cargo clippy` and `cargo fmt` as final validation
