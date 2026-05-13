# Gotchas, limitations, and tonic-migration deltas

Read before debugging anything that "should just work."

## Table of contents

- [JSON requests + view bodies](#json-requests--view-bodies)
- [extern_path orphan rule](#extern_path-orphan-rule)
- [refining_impl_trait lint](#refining_impl_trait-lint)
- [No built-in health or reflection endpoints](#no-built-in-health-or-reflection-endpoints)
- [server feature and tokio/macros](#server-feature-and-tokiomacros)
- [Codegen filename moved in 0.4.0](#codegen-filename-moved-in-040)
- [Toolchain floors: MSRV 1.88 + edition 2024](#toolchain-floors-msrv-188--edition-2024)

For porting from tonic, see `migration-tonic.md`.

## JSON requests + view bodies

A handler can return a borrowed view via the `Encodable<M>` trait to skip
allocation on the proto path. **JSON clients hitting that handler will
receive an `unimplemented` error** — JSON serialization is only wired for
owned proto structs, not views.

Default rule: return owned messages from handlers. Only return views when:

1. You have measured the allocation as a real bottleneck.
2. The RPC will never be called with `content-type: application/json` (e.g.
   internal-only gRPC traffic, no browser/JS clients).

If you do return views, document it on the handler so future maintainers
don't accidentally enable JSON for that endpoint.

## extern_path orphan rule

`connectrpc_build::Config::extern_path(".my.pkg", "::other_crate::my::pkg")`
remaps types to a foreign crate. Because of Rust's orphan rule,
`connectrpc-build` cannot emit `impl Encodable<...>` for types it doesn't own.

Effect: any handler whose request or response type lives behind an
`extern_path` mapping must use owned messages (the view fast-path is
unavailable). This is rarely a concern — it just means you can't squeeze the
view-path optimization out of cross-crate types.

## refining_impl_trait lint

The generated service trait declares each RPC as returning
`ServiceResult<impl Encodable<Out> + ...>`. Handler impls then return one of
`ServiceResult<Out>` (owned), a view, or `MaybeBorrowed<M, V>`. All three
*refine* the trait's impl-trait return — that's the mechanism that lets you
pick the cheapest shape per handler.

`refining_impl_trait_internal` (warn-by-default since Rust 1.86,
[rust-lang/rust#121718](https://github.com/rust-lang/rust/issues/121718))
fires on every handler `impl`. The refinement is intentional and benign:
handler impls are not part of your service's public API, and there is no
spot inside the generated module tree where `#[allow(...)]` could reach
the handler impl from the codegen side.

If you build with `-D warnings`, suppress it where the handler lives:

```toml
# Cargo.toml — workspace or per-crate
[lints.rust]
refining_impl_trait_internal = "allow"
```

Or per-impl:

```rust
#[allow(refining_impl_trait)]
impl GreetService for MyGreet { /* … */ }
```

(The bare `refining_impl_trait` group covers both `_reachable` and
`_internal`.) The codegen-side `#[allow(...)]` block already handles
`impl_trait_redundant_captures` and `unused_qualifications` for the
generated module tree — you only need lint suppressions for your own
handler impls.

## No built-in health or reflection endpoints

There is no `connectrpc::health` or `connectrpc::reflection` module the way
`tonic` has `tonic-health` and `tonic-reflection`. Options:

1. **Define an explicit health RPC in your `.proto`** and implement it. This
   is the simplest path and works for any client.
2. **Add a plain Axum route**: `app.route("/healthz", get(|| async { "ok" }))`.
   Reverse proxies and Kubernetes probes don't need ConnectRPC for liveness.

For gRPC reflection specifically, a Rust server intended to interop with
`grpcurl` users will need to roll a reflection RPC by hand or expose the
service descriptors via a separate endpoint.

## server feature and tokio/macros

In 0.4.2, the `server` feature began enabling `tokio/macros` (it previously
only enabled `tokio/net`). The accept loop in `Server::serve` and
`axum::serve_tls` both use `tokio::select!`, which requires the `macros`
feature.

If you're on an older 0.4 release **and** your downstream `tokio` deps don't
enable `macros` elsewhere in the dependency closure, the build fails with a
missing-macro error. Either upgrade to 0.4.2+ or add
`tokio = { version = "1", features = ["macros"] }` to your `Cargo.toml`.

## Codegen filename moved in 0.4.0

In 0.4.0 (May 2026), generated service stubs moved from `<stem>.rs` to
`<stem>.__connect.rs`. Buffa message types are still in `<stem>.rs`.

If you check codegen into the repo (`buf generate` to a tracked directory,
or `protoc-gen-connect-rust` with a fixed `--connect-rust_out`):
**regenerate and delete the old `<stem>.rs` service files** when bumping
past 0.4.0. Stale 0.3-era service files left next to new
`<stem>.__connect.rs` files produce duplicate-item compile errors.

`build.rs` + `include!(env!("OUT_DIR"))` users are unaffected — the include
file references both names.

## Toolchain floors: MSRV 1.88 + edition 2024

- **Rust 1.88, edition 2024.** This is recent — older toolchains and Linux
  distro packages will not work. Pin a `rust-toolchain.toml`. Downstream
  crates on edition 2021 can still consume `connectrpc` (edition is
  per-crate), but you'll be on the receiving end of any `use<...>`
  precise-capture clauses in generated code.
- **`protoc` v27+** is required at build time when running codegen
  (CONTRIBUTING.md on the repo). CI images that ship older `protoc`
  versions will fail in `connectrpc-build`.
- **Look at release notes before trusting tutorials.** `gh release list -R
  anthropics/connect-rust` shows the current shape — there have been two
  patch releases in 0.4 alone with material additions (`serve_tls`,
  `tokio/macros` fix).

