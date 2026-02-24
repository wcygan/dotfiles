---
title: Error Handling
description: Idiomatic Rust error handling with Result, ?, thiserror, anyhow, and custom error types
tags: [error, result, option, thiserror, anyhow, panic]
---

# Error Handling

## Core Rules

- **`Result<T, E>`** for recoverable errors.
- **`panic!`** only for unrecoverable bugs / violated invariants.
- **`?` operator** is the idiomatic propagation mechanism. Calls `From::from()` to convert error types.
- **`expect("context")`** over `unwrap()` in application code. Provides debugging context.
- **Never `unwrap()` in library code** paths reachable by users.

## The `?` Operator

```rust
fn read_config(path: &Path) -> Result<Config, Box<dyn Error>> {
    let content = fs::read_to_string(path)?;
    let config: Config = toml::from_str(&content)?;
    Ok(config)
}
```

`main()` can return `Result`:

```rust
fn main() -> Result<(), Box<dyn Error>> {
    let config = read_config(Path::new("config.toml"))?;
    run(config)?;
    Ok(())
}
```

## Error Type Design

### Library Errors — Use `thiserror`

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("failed to read config from {path}")]
    ConfigRead {
        path: PathBuf,
        #[source]
        cause: io::Error,
    },

    #[error("invalid format: {0}")]
    InvalidFormat(String),

    #[error("not found: {0}")]
    NotFound(String),
}
```

### Application Errors — Use `anyhow`

```rust
use anyhow::{Context, Result};

fn process() -> Result<()> {
    let data = fs::read_to_string("input.txt")
        .context("failed to read input file")?;
    let parsed = parse(&data)
        .context("failed to parse input data")?;
    Ok(())
}
```

## `Option` vs `Result`

| Use | Type |
|---|---|
| Value may be absent (not an error) | `Option<T>` |
| Operation may fail | `Result<T, E>` |
| Convert absence to error | `opt.ok_or(MyError::NotFound)?` or `opt.ok_or_else(|| ...)` |

## Combinators

```rust
// Option combinators
let len = name.as_ref().map(|n| n.len()).unwrap_or(0);
let upper = name.as_deref().map(str::to_uppercase);

// Result combinators
let port: u16 = env::var("PORT")
    .map_err(|_| ConfigError::Missing("PORT"))?
    .parse()
    .map_err(|_| ConfigError::Invalid("PORT"))?;
```

## `From` Implementations for Error Conversion

```rust
impl From<io::Error> for AppError {
    fn from(err: io::Error) -> Self {
        AppError::Io(err)
    }
}
// Now `?` auto-converts io::Error -> AppError
```

With `thiserror`, use `#[from]`:

```rust
#[derive(Debug, Error)]
pub enum AppError {
    #[error("I/O error")]
    Io(#[from] io::Error),
}
```

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| `unwrap()` in library code | Return `Result` and propagate with `?` |
| `panic!("unexpected")` for expected failures | Use `Result` with descriptive error variant |
| `Box<dyn Error>` in library public API | Define typed error enum with `thiserror` |
| Ignoring `Result` with `let _ =` | Handle or explicitly document why it's safe to ignore |
| String-based errors (`Err("something broke".into())`) | Use typed errors; strings lack structure for matching |
| Matching on error `.to_string()` | Match on error variants or `.kind()` |
