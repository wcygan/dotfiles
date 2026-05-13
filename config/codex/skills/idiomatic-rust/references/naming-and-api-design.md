---
title: Naming & API Design
description: Rust naming conventions, conversion method patterns, API design guidelines, and documentation standards
tags: [naming, api-design, conventions, documentation, rustdoc]
---

# Naming & API Design

## Naming Conventions

| Entity | Convention | Example |
|---|---|---|
| Types (structs, enums, traits, type aliases) | `UpperCamelCase` | `HttpResponse`, `MyStruct` |
| Enum variants | `UpperCamelCase` | `Some`, `NotFound` |
| Functions, methods | `snake_case` | `read_to_string`, `is_empty` |
| Local variables | `snake_case` | `file_name`, `count` |
| Struct fields | `snake_case` | `first_name`, `created_at` |
| Constants, statics | `SCREAMING_SNAKE_CASE` | `MAX_SIZE`, `DEFAULT_PORT` |
| Macros | `snake_case!` | `vec!`, `println!` |
| Modules | `snake_case` | `std::collections` |
| Crate names | `snake_case` (hyphens in Cargo.toml) | `my-crate` / `my_crate` |
| Lifetimes | Short lowercase with `'` | `'a`, `'ctx` |
| Generic type params | Single uppercase or short CamelCase | `T`, `E`, `K`, `V`, `Item` |

## Conversion Method Naming

| Prefix | Cost | Ownership | Example |
|---|---|---|---|
| `as_` | Free / cheap | Borrows `&self` | `as_str()`, `as_bytes()`, `as_slice()` |
| `to_` | Expensive | Borrows `&self`, returns new value | `to_string()`, `to_vec()`, `to_uppercase()` |
| `into_` | Variable | Consumes `self` | `into_inner()`, `into_bytes()`, `into_iter()` |

## Getter Naming

Use field name directly — **no `get_` prefix**:

```rust
// BAD
fn get_name(&self) -> &str { &self.name }

// GOOD
fn name(&self) -> &str { &self.name }
```

Exception: `get()` for indexed/keyed access (like `HashMap::get()`).

## Iterator Method Naming

- `iter()` → yields `&T`
- `iter_mut()` → yields `&mut T`
- `into_iter()` → yields `T` (consumes collection)

Name iterator types after their producing method: `struct Iter`, `struct IntoIter`.

## Constructor Conventions

- `new()` — primary constructor (static inherent method, not trait)
- `with_capacity()` — constructor with capacity hint
- `from_*()` — named constructors from specific inputs
- `default()` — via `Default` trait for zero-config construction
- No out-parameters; return values instead

```rust
impl Config {
    pub fn new(path: impl AsRef<Path>) -> Result<Self> { ... }
    pub fn from_env() -> Result<Self> { ... }
}
```

## Function Parameter Design

### Accept the Most General Type

```rust
// BAD: too specific
fn process(data: &Vec<u8>) { ... }
fn greet(name: &String) { ... }

// GOOD: accept slices/str
fn process(data: &[u8]) { ... }
fn greet(name: &str) { ... }
```

### Use Generics for Flexibility

```rust
// Accept anything path-like
fn read_file(path: impl AsRef<Path>) -> io::Result<String> { ... }

// Accept anything string-like (when ownership is needed)
fn set_name(&mut self, name: impl Into<String>) { ... }
```

### Prefer `R: Read` and `W: Write` by Value

```rust
fn parse_json<R: Read>(reader: R) -> Result<Value> { ... }
fn write_csv<W: Write>(writer: W, data: &[Record]) -> Result<()> { ... }
```

## Return Type Design

- Return owned types from functions that create values
- Return `&T` from accessor methods on structs
- Return `impl Iterator` for lazy sequences (not `Vec`)
- Return `Result<T, E>` for fallible operations
- Expose intermediate results from computation

## Documentation Standards

### Crate-Level Docs

```rust
//! # My Crate
//!
//! `my_crate` provides utilities for X.
//!
//! ## Quick Start
//!
//! ```rust
//! use my_crate::Widget;
//!
//! let w = Widget::new("example")?;
//! w.process()?;
//! # Ok::<(), my_crate::Error>(())
//! ```
```

### Item-Level Docs

```rust
/// Computes the Levenshtein distance between two strings.
///
/// # Examples
///
/// ```
/// use my_crate::levenshtein;
///
/// assert_eq!(levenshtein("kitten", "sitting"), 3);
/// ```
///
/// # Panics
///
/// Panics if either string exceeds `MAX_LEN`.
///
/// # Errors
///
/// Returns [`ComputeError::InvalidEncoding`] if the input
/// contains invalid UTF-8 sequences.
pub fn levenshtein(a: &str, b: &str) -> Result<usize, ComputeError> { ... }
```

### Doc Comment Rules

- Use `///` (not `/** */`)
- Use `//!` only for module-level or crate-level docs
- Doc comments **before** attributes
- Examples use `?` operator (not `unwrap()`)
- Document: panics, errors, and safety requirements
- Include hyperlinks to related types: `[`Config`]`

## `#[must_use]`

Apply to functions whose return value should not be ignored:

```rust
#[must_use = "this returns the result of the operation, which may be an error"]
pub fn save(&self) -> Result<()> { ... }
```

## Future-Proofing

- Use `#[non_exhaustive]` on public enums and structs with public fields
- Keep struct fields private with accessor methods
- Sealed traits to prevent downstream implementations
- Prefer returning `impl Trait` over concrete types when the concrete type is an implementation detail
