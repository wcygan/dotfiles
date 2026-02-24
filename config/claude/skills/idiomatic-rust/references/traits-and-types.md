---
title: Traits & Type System Patterns
description: Standard trait implementations, derive conventions, newtype pattern, builder pattern, and type safety idioms
tags: [traits, derive, newtype, builder, phantom, generics, type-safety]
---

# Traits & Type System Patterns

## Standard Trait Derive Order

Use a single `#[derive(...)]` per item. Canonical order:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default)]
```

Add `Serialize, Deserialize` at the end when using serde.

## When to Derive What

| Trait | When to Derive |
|---|---|
| `Debug` | **Always** on all public types |
| `Clone` | When all fields are `Clone` and copying makes sense |
| `Copy` | Small stack-only types (newtypes over primitives, small enums) |
| `PartialEq` + `Eq` | Value types that need equality comparison |
| `Hash` | Types used as `HashMap`/`HashSet` keys (must be consistent with `Eq`) |
| `Default` | Types with sensible default values; enables `..Default::default()` |
| `PartialOrd` + `Ord` | Types that need sorting/comparison |

## Key Traits to Implement Manually

### `Display`

For user-facing output. Enables `{}` in format strings and `.to_string()`.

```rust
impl fmt::Display for UserId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "user-{}", self.0)
    }
}
```

### `From<T>` / `Into<T>`

Implement `From`; `Into` is derived automatically. Use for lossless, obvious conversions.

```rust
impl From<u64> for UserId {
    fn from(id: u64) -> Self {
        UserId(id)
    }
}
```

### `TryFrom<T>` / `TryInto<T>`

For fallible conversions:

```rust
impl TryFrom<i64> for UserId {
    type Error = InvalidIdError;

    fn try_from(value: i64) -> Result<Self, Self::Error> {
        if value < 0 {
            return Err(InvalidIdError(value));
        }
        Ok(UserId(value as u64))
    }
}
```

### `AsRef<T>` / `AsMut<T>`

Cheap reference conversions for generic function bounds:

```rust
fn read_file(path: impl AsRef<Path>) -> io::Result<String> {
    fs::read_to_string(path.as_ref())
}
```

### `Error`

Implement for all error types. Provides `source()` chain:

```rust
impl std::error::Error for AppError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            AppError::Io(e) => Some(e),
            _ => None,
        }
    }
}
```

## Newtype Pattern

Wrap a type for type safety without runtime cost:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct OrderId(u64);
// UserId and OrderId are incompatible at compile time
```

## Type Aliases

For ergonomic shorthand within a crate:

```rust
pub type Result<T> = std::result::Result<T, AppError>;
```

## Builder Pattern

Use for types with many optional configuration parameters:

```rust
pub struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
    timeout: Duration,
}

pub struct ServerConfigBuilder {
    host: String,
    port: u16,
    max_connections: Option<usize>,
    timeout: Option<Duration>,
}

impl ServerConfigBuilder {
    pub fn new(host: impl Into<String>, port: u16) -> Self {
        Self {
            host: host.into(),
            port,
            max_connections: None,
            timeout: None,
        }
    }

    pub fn max_connections(mut self, n: usize) -> Self {
        self.max_connections = Some(n);
        self
    }

    pub fn timeout(mut self, t: Duration) -> Self {
        self.timeout = Some(t);
        self
    }

    pub fn build(self) -> ServerConfig {
        ServerConfig {
            host: self.host,
            port: self.port,
            max_connections: self.max_connections.unwrap_or(100),
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
        }
    }
}
```

## Enums Over Booleans

Prefer enums for function parameters that convey meaning:

```rust
// BAD
fn set_visible(visible: bool) { ... }

// GOOD
pub enum Visibility {
    Visible,
    Hidden,
}
fn set_visibility(v: Visibility) { ... }
```

## Visibility Rules

- **Default**: Private (module and descendants only).
- **`pub`**: Accessible anywhere the parent module is accessible.
- **`pub(crate)`**: Visible throughout the crate only. **Prefer over `pub` for internal APIs.**
- **`pub(super)`**: Visible to parent module only.
- Use minimum necessary visibility.

## Trait Objects vs Generics

| Use | Mechanism |
|---|---|
| Static dispatch (monomorphized, zero-cost) | `fn foo(x: impl Trait)` or `fn foo<T: Trait>(x: T)` |
| Dynamic dispatch (one compiled version, vtable) | `fn foo(x: &dyn Trait)` or `Box<dyn Trait>` |
| Heterogeneous collections | `Vec<Box<dyn Trait>>` |
| Return different concrete types | `Box<dyn Trait>` or `impl Trait` (if single type) |

## Sealed Traits

Prevent external implementations:

```rust
mod private {
    pub trait Sealed {}
}

pub trait MyTrait: private::Sealed {
    fn method(&self);
}

// Only types you impl Sealed for can implement MyTrait
```

## `#[non_exhaustive]`

Reserve right to add variants/fields without breaking change:

```rust
#[non_exhaustive]
pub enum Error {
    NotFound,
    PermissionDenied,
}
// Downstream must have `_ =>` catch-all in match
```

## Smart Pointers

| Type | Use Case |
|---|---|
| `Box<T>` | Heap allocation, recursive types, trait objects |
| `Rc<T>` | Single-threaded shared ownership |
| `Arc<T>` | Multi-threaded shared ownership |
| `Cow<'a, T>` | Clone-on-write; borrow when possible, clone when needed |

Only smart pointers should implement `Deref`/`DerefMut`.
