---
title: Style & Formatting
description: Complete Rust style guide rules — indentation, line width, imports, expressions, match, types, Cargo.toml
tags: [style, formatting, rustfmt, imports, match, expressions, cargo]
---

# Style & Formatting

Based on the official Rust Style Guide. Use `rustfmt` to enforce automatically; these rules clarify intent and edge cases.

## Guiding Principles (Priority Order)

1. **Readability** — scan-ability, no misleading formatting
2. **Aesthetics** — visual appeal, cross-language consistency
3. **Specifics** — clean diffs, prevent rightward drift, minimize vertical space
4. **Application** — ease of manual and tool application

## Indentation & Line Width

- **4 spaces** per indent level. Never tabs.
- **100 characters** maximum line width.
- **80 characters** for lines that are entirely comments.
- **Block indent** (preferred) over visual indent.

## Trailing Commas

- Always in multi-line comma-separated lists.
- Never in single-line lists.

## Blank Lines & Whitespace

- Zero or one blank line between items and statements.
- No trailing whitespace on any line.

## Comments

- Prefer `//` over `/* */`.
- Single space after `//`.
- Comments on own line preferred.
- Complete sentences with capital letter and period.

## Imports (`use` Statements)

```rust
// Order: extern crate → use → mod → other items
use std::collections::HashMap;
use std::io::{self, Read, Write};

use serde::{Deserialize, Serialize};

use crate::config::Config;
use crate::error::AppError;
```

- Group: std → external crates → crate-internal (blank line between groups).
- `self` and `super` before other names within a group.
- Single-line preferred. No spaces around braces.
- Normalize: `use a::{b};` → `use a::b;`.

## Functions

```rust
// Fits on one line
fn add(a: i32, b: i32) -> i32 {
    a + b
}

// Does not fit — break after `(`
fn complex_function(
    first_param: &str,
    second_param: u64,
    third_param: Option<Config>,
) -> Result<Output, Error> {
    // body
}
```

- Opening `{` on same line as closing `)` or return type.
- Each parameter on its own block-indented line, trailing comma.

## Structs

```rust
pub struct Config {
    pub host: String,
    pub port: u16,
    pub max_retries: usize,
}
```

- Opening `{` on same line. Each field on own line. Trailing comma. Closing `}` unindented.
- Prefer `struct Foo;` (unit) over `struct Foo()` or `struct Foo {}`.

## Enums

```rust
pub enum Status {
    Active,
    Inactive,
    Pending { since: DateTime<Utc> },
}
```

- Each variant on own line, trailing comma.
- Small struct variants may go on one line.

## Traits & Impls

```rust
pub trait Repository {
    type Error;

    fn find(&self, id: &str) -> Result<Item, Self::Error>;
    fn save(&mut self, item: &Item) -> Result<(), Self::Error>;
}

impl Repository for InMemoryRepo {
    type Error = RepoError;

    fn find(&self, id: &str) -> Result<Item, Self::Error> {
        // ...
    }

    fn save(&mut self, item: &Item) -> Result<(), Self::Error> {
        // ...
    }
}
```

- Opening `{` on same line.
- Prefer `where` clauses over line-breaking bounds.

## Where Clauses

```rust
fn process<T, E>(items: &[T]) -> Result<Vec<T>, E>
where
    T: Clone + Debug + Send,
    E: From<io::Error>,
{
    // body
}
```

- `where` on own line after return type.
- Each bound on own block-indented line, trailing comma.
- `{` on new line after where clause.

## Let Statements

```rust
let name: String = compute_name();
let config = Config::from_env()?;

// Multi-line
let result =
    long_function_call(first_arg, second_arg, third_arg)?;
```

## Match Expressions

```rust
match status {
    Status::Active => handle_active(),
    Status::Inactive => {
        log::info!("inactive");
        handle_inactive()
    }
    Status::Pending { since } if since < cutoff => expire(since),
    _ => default_handler(),
}
```

- Block-indent arms once. Trailing comma (unless arm uses a block).
- Short arms without block. Multi-line arms use `{ }`.
- Guard clause: `if` on same line if it fits; break before `if` and block-indent if not.

## Method Chains

```rust
// Single line if small
let result = items.iter().filter(|x| x.is_valid()).count();

// Multi-line: break before `.`, block-indent
let result = items
    .iter()
    .filter(|item| item.is_valid())
    .map(|item| item.transform())
    .collect::<Vec<_>>();
```

`?` goes on same line as its expression, before the line break.

## Expressions

- **Closures**: `|args| expr`. No extra spaces. Omit `{}` when possible.
- **Ranges**: No spaces: `0..10`, `..x.len()`, `x..=y`.
- **Casts**: Spaces around `as`: `x as u64`.
- **Binary ops**: Spaces around operators. Line-break before operator.
- **Unary ops**: No space. Exception: space after `&mut`.

## Generics

```rust
// No spaces before `<` or after `>`
fn process<T: Clone + Send>(items: Vec<T>) -> Vec<T> { ... }

// Multi-line
fn complex<
    T: Clone + Send + Sync,
    E: Error + From<io::Error>,
>(
    items: Vec<T>,
) -> Result<Vec<T>, E> {
    // body
}
```

## Attributes

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[non_exhaustive]
pub struct Config {
    // ...
}
```

- Each attribute on its own line.
- Single `#[derive(...)]` per item.
- Prefer outer (`#[...]`) over inner (`#![...]`).

## Cargo.toml

```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2021"
description = "A brief description"

[dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }

[dev-dependencies]
assert_matches = "1"
```

- `[package]` first. `name` and `version` first within it, `description` last.
- Blank lines between sections, not within.
- Version-sort within sections.
