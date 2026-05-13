---
title: Iterators & Closures
description: Idiomatic iterator patterns, combinator chains, closure conventions, and functional Rust style
tags: [iterators, closures, combinators, functional, map, filter, collect]
---

# Iterators & Closures

## Three Iterator Methods on Collections

| Method | Yields | Ownership |
|---|---|---|
| `iter()` | `&T` | Borrows collection |
| `iter_mut()` | `&mut T` | Mutably borrows collection |
| `into_iter()` | `T` | Consumes collection |

`for x in collection` calls `into_iter()` implicitly.

## Prefer Combinators Over Manual Loops

```rust
// BAD: manual loop with mutation
let mut results = Vec::new();
for item in &items {
    if item.is_valid() {
        results.push(item.transform());
    }
}

// GOOD: iterator chain
let results: Vec<_> = items.iter()
    .filter(|item| item.is_valid())
    .map(|item| item.transform())
    .collect();
```

## Essential Combinators

| Combinator | Purpose | Example |
|---|---|---|
| `map` | Transform each element | `.map(\|x\| x * 2)` |
| `filter` | Keep elements matching predicate | `.filter(\|x\| x.is_valid())` |
| `filter_map` | Filter + map in one step | `.filter_map(\|x\| x.parse().ok())` |
| `flat_map` | Map then flatten nested iterators | `.flat_map(\|x\| x.children())` |
| `enumerate` | Add index to each element | `.enumerate()` → `(usize, T)` |
| `zip` | Pair elements from two iterators | `a.iter().zip(b.iter())` |
| `chain` | Concatenate two iterators | `a.iter().chain(b.iter())` |
| `take` / `skip` | Limit or skip elements | `.take(10)`, `.skip(5)` |
| `peekable` | Look ahead without consuming | `.peekable()` then `.peek()` |
| `fold` | Accumulate with initial value | `.fold(0, \|acc, x\| acc + x)` |
| `reduce` | Accumulate without initial value | `.reduce(\|a, b\| a + b)` |
| `any` / `all` | Short-circuit boolean checks | `.any(\|x\| x > 5)` |
| `find` | First matching element | `.find(\|x\| x.id == target)` |
| `position` | Index of first match | `.position(\|x\| x == target)` |
| `cloned` / `copied` | Convert `&T` to `T` | `.copied()` for `Copy` types |
| `flatten` | Flatten nested iterators | `.flatten()` |
| `inspect` | Side effect without consuming | `.inspect(\|x\| debug!("{x:?}"))` |
| `chunks` / `windows` | Slice iteration patterns | (on slices, not Iterator) |

## `collect()` Patterns

```rust
// Turbofish syntax
let v = iter.collect::<Vec<_>>();

// Type annotation
let v: Vec<_> = iter.collect();

// Collect into HashMap
let map: HashMap<_, _> = pairs.into_iter().collect();

// Collect Results — short-circuits on first Err
let results: Result<Vec<_>, _> = items.iter()
    .map(|item| item.validate())
    .collect();
```

## Closures

### Syntax

```rust
|args| expr                    // single expression, return inferred
|args| { statements; expr }    // block body
|args: Type| -> RetType { }   // explicit types (rarely needed)
move |args| expr               // take ownership of captured variables
```

### Capture Rules

- Closures capture by the least restrictive mode needed:
  1. `&T` (immutable borrow) — default
  2. `&mut T` (mutable borrow) — if closure mutates captured value
  3. `T` (move) — if closure consumes captured value, or `move` keyword used

### Closure Traits

| Trait | Can Call | Captures |
|---|---|---|
| `Fn` | Multiple times | Immutable borrows only |
| `FnMut` | Multiple times | May mutably borrow |
| `FnOnce` | Exactly once | May consume captured values |

`Fn` implies `FnMut` implies `FnOnce`.

### Convention: Accept `impl Fn*` in Parameters

```rust
fn retry<F, T, E>(max: usize, mut f: F) -> Result<T, E>
where
    F: FnMut() -> Result<T, E>,
{
    for _ in 0..max {
        match f() {
            Ok(v) => return Ok(v),
            Err(e) if max == 0 => return Err(e),
            _ => continue,
        }
    }
    f()
}
```

## Common Patterns

### Fallible Iteration

```rust
// Process all items, fail on first error
let results: Result<Vec<Output>, Error> = inputs.iter()
    .map(|input| process(input))
    .collect();
```

### Building Strings

```rust
// Join with separator
let csv = values.iter()
    .map(|v| v.to_string())
    .collect::<Vec<_>>()
    .join(", ");

// Or use intersperse (nightly or itertools)
```

### Counting / Grouping

```rust
// Count occurrences
let counts: HashMap<&str, usize> = words.iter()
    .fold(HashMap::new(), |mut map, word| {
        *map.entry(word).or_insert(0) += 1;
        map
    });
```

### Chained Option/Result

```rust
// Option chaining
let display_name = user.nickname
    .as_deref()
    .or(user.first_name.as_deref())
    .unwrap_or("Anonymous");
```

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| `for i in 0..v.len() { v[i] }` | `for item in &v { }` or `v.iter()` |
| `.iter().map().collect()` then `.iter()` again | Chain combinators without intermediate collect |
| `.filter().count() > 0` | `.any()` — short-circuits |
| `.map().flatten()` | `.flat_map()` |
| `.filter().next()` | `.find()` |
| Manual `for` loop building a `Vec` | `.map().collect()` or `.filter_map().collect()` |
