---
name: idiomatic-rust
description: Review, refactor, and generate idiomatic Rust code using official Rust style, standard-library conventions, API guidelines, rustfmt, clippy, and cargo workflows. Use when Codex is writing or reviewing Rust, especially for ownership, borrowing, lifetimes, traits, error handling, iterator usage, async/concurrency, type design, public APIs, or style questions.
---

# Idiomatic Rust

Use this skill to write, review, and refactor Rust that is clear, maintainable, and aligned with common Rust ecosystem conventions.

## Workflow

1. Read the relevant Rust files, `Cargo.toml`, and nearby tests or examples before changing code.
2. Identify the task type: review, bug fix, refactor, API design, or new code generation.
3. Load only the reference files needed for the concrete code under discussion.
4. Prefer the project's existing edition, dependency choices, module layout, and error conventions.
5. Validate with the narrowest meaningful command first, then broaden as risk warrants.

Useful validation commands, when available:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test
```

If a workspace does not support `--all-features` or warning denial, use the local convention instead of forcing new policy.

## Reference Map

- `references/ownership-and-borrowing.md`: moves, borrows, lifetimes, clones, `Copy`/`Clone`, and borrow-friendly API shape.
- `references/error-handling.md`: `Result`, `Option`, `?`, `thiserror`, `anyhow`, panic boundaries, and library/application error choices.
- `references/naming-and-api-design.md`: Rust naming, getters, `as_`/`to_`/`into_`, builders, visibility, and public API ergonomics.
- `references/traits-and-types.md`: standard derives, trait impls, newtypes, enums, marker traits, type aliases, and type-state patterns.
- `references/iterators-and-closures.md`: iterator adapters, closures, `collect`, `try_*` patterns, and when loops are clearer.
- `references/style-and-formatting.md`: rustfmt style, imports, module organization, docs, attributes, and idiom cleanup.
- `references/concurrency.md`: threads, channels, `Arc`, `Mutex`, atomics, async, `Send`/`Sync`, and shared-state patterns.

## Review Guidance

Lead with actionable issues. For each issue, include the file and line, why the current code is non-idiomatic or risky, and the smallest idiomatic fix.

Check these dimensions:

1. Ownership and borrowing: avoid unnecessary clones, awkward lifetimes, needless owned parameters, and borrow checker workarounds.
2. Error handling: prefer typed errors in libraries, contextual errors in applications, `?` for propagation, and avoid `unwrap` or `expect` outside tests or true invariants.
3. API design: follow Rust naming conventions, encode invariants in types, avoid boolean traps in public APIs, and keep generic bounds no broader than needed.
4. Traits and types: derive standard traits when semantically correct; implement `Display`, `Error`, `From`, `TryFrom`, `AsRef`, or `Deref` only when they match the type's meaning.
5. Iterators and control flow: use iterator adapters where they improve clarity, but keep straightforward loops when they are easier to read.
6. Concurrency: make ownership of shared state explicit; avoid holding locks across blocking or async boundaries; prefer message passing when it simplifies ownership.
7. Style: preserve rustfmt-compatible formatting, clear module boundaries, and concise doc comments with compilable examples when practical.

## Generation Guidance

When writing new Rust code:

- Favor simple control flow, explicit types at API boundaries, and names that reveal ownership or conversion behavior.
- Accept borrowed inputs such as `&str`, `&[T]`, and `&Path` unless the function must take ownership.
- Return owned values when returning references would complicate lifetimes for callers.
- Use `Result<T, E>` and `?` for recoverable errors; reserve `panic!` for violated invariants or intentionally failing tests.
- Use `thiserror` for library errors and `anyhow` for application errors when those dependencies already fit the project.
- Derive `Debug` for public types, and derive `Clone`, `Copy`, `PartialEq`, `Eq`, `Hash`, `Default`, `Serialize`, or `Deserialize` only when the semantics are correct.
- Add `#[must_use]` to values where ignoring the result is likely a bug.
- Consider `#[non_exhaustive]` for public enums and public structs with fields when downstream compatibility matters.
- Prefer `From`/`TryFrom` over ad hoc conversion functions.
- Write examples with `?` instead of `unwrap()` unless the example is intentionally about failure.

Do not add dependencies, change error libraries, or rewrite loops into iterator chains solely for style. Match the codebase unless the existing pattern is causing a real correctness, maintainability, or API problem.
