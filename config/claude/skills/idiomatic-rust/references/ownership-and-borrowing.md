---
title: Ownership & Borrowing
description: Rust ownership rules, borrowing conventions, lifetime patterns, and common pitfalls
tags: [ownership, borrowing, lifetimes, move, clone, copy]
---

# Ownership & Borrowing

## Three Ownership Rules

1. Each value has exactly one owner.
2. Only one owner at a time.
3. When the owner goes out of scope, the value is dropped.

## Move vs Copy

- **Move**: Default for heap-allocated types (`String`, `Vec<T>`, `Box<T>`). Assignment transfers ownership; original is invalidated.
- **Copy**: Implicit bitwise copy for stack-only types (`i32`, `f64`, `bool`, `char`, tuples/arrays of `Copy` types). A type cannot implement both `Copy` and `Drop`.
- **Clone**: Explicit deep copy via `.clone()`. Signals "this might be expensive." Use only when genuinely needed.

### Idiomatic Patterns

```rust
// BAD: unnecessary clone
let name = user.name.clone();
process(&name);

// GOOD: borrow directly
process(&user.name);
```

```rust
// BAD: taking ownership when not needed
fn print_name(name: String) { println!("{name}"); }

// GOOD: borrow the parameter
fn print_name(name: &str) { println!("{name}"); }
```

## Borrowing Rules

1. At any time: **one `&mut T` XOR any number of `&T`**.
2. References must always be valid (no dangling references).
3. Borrow scope extends from introduction to **last use** (NLL), not to end of block.

### Conventions

- Default to `&T`; use `&mut T` only when mutation is needed.
- Prefer borrowing over ownership in function parameters.
- Use explicit scopes `{}` to limit borrow duration when fighting the borrow checker.

```rust
// Use scoping to limit mutable borrow
{
    let entry = map.entry(key).or_default();
    entry.push(value);
} // mutable borrow of `map` ends here
let total = map.len(); // now we can borrow immutably
```

## Lifetime Conventions

### Annotation Syntax

`'a` — lowercase, short. Placed after `&`: `&'a str`, `&'a mut T`.

### Three Elision Rules (compiler infers automatically)

1. Each reference parameter gets its own lifetime.
2. If exactly one input lifetime, it's assigned to all output lifetimes.
3. If `&self` or `&mut self` is a parameter, its lifetime is assigned to all outputs.

### When to Annotate

Only when the compiler cannot infer — typically:
- Functions returning references derived from multiple inputs
- Structs holding references

```rust
// Annotation required: two input lifetimes, one output
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

### `'static`

Lives for entire program duration. All string literals are `'static`. Never use to paper over lifetime errors.

### Structs with References

Must declare lifetime parameters. The struct cannot outlive the referenced data.

```rust
struct Excerpt<'a> {
    text: &'a str,
}
```

## Common Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| `.clone()` to satisfy borrow checker | Restructure borrows, use scopes, or accept references |
| `Rc<RefCell<T>>` everywhere | Prefer ownership restructuring; use only when shared mutation is genuinely needed |
| Returning `&String` | Return `&str` instead (more general) |
| `fn foo(v: Vec<T>)` when read-only | Use `fn foo(v: &[T])` — borrows a slice |
| `fn foo(s: String)` when read-only | Use `fn foo(s: &str)` — borrows a string slice |
