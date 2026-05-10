# Schema

Use this when validating external input, deriving TypeScript types from schemas, encoding data back to a wire format, creating branded types, or generating JSON Schema, arbitrary values, pretty printers, or equivalence. Verify exact APIs in the official docs or installed package exports before editing.

Official docs to check first:
- https://effect.website/docs/schema/introduction/
- https://effect.website/docs/schema/getting-started/
- https://effect.website/docs/schema/basic-usage/
- https://effect.website/docs/schema/filters/
- https://effect.website/docs/schema/transformations/
- https://effect.website/docs/schema/classes/
- https://effect.website/docs/schema/error-formatters/
- https://effect.website/docs/schema/json-schema/
- https://effect.website/docs/schema/arbitrary/

## When to Use Schema

Use Schema at boundaries:

- JSON request or response bodies.
- Form data and query params.
- Environment-derived config.
- Database or queue payloads crossing trust boundaries.
- AI/tool outputs and other generated structured data.
- Branded identifiers that must be validated before use.

Inside trusted domain code, plain TypeScript types may be enough. Avoid turning every internal object into a schema unless the project has chosen that style.

## Decode and Encode

Schema describes both:

- Decoding: unknown or encoded input -> domain type.
- Encoding: domain type -> encoded output.

That bidirectional model is why Schema is stronger than a parse-only validator for wire contracts. It also means transformations need careful round-trip thinking: encode behavior should be intentional, not an afterthought.

## Brands and Refinements

Use brands for validated identifiers and constrained primitives:

- `UserId`, `Email`, `Slug`, `NonEmptyString`.
- Values should normally enter the brand through decoding or validation.
- Avoid casting to branded types unless the surrounding code already guarantees validity.

Use filters/refinements for domain constraints, and verify current error-message APIs before promising exact formatter output.

## Classes and Tagged Data

Schema class APIs can be useful when a project wants constructors, defaults, or richer domain objects. Keep class-based schemas consistent with nearby code. Do not mix class schemas, plain structs, and ad hoc interfaces without a reason.

For discriminated unions, prefer explicit tags that TypeScript can narrow and that boundary responses can route.

## Derived Artifacts

Schema can generate or support:

- JSON Schema for OpenAPI/tool contracts.
- Arbitrary values for property-based tests.
- Pretty printers and error formatters.
- Equivalence for structural comparison.

Use these when they remove duplicate sources of truth. Do not add generated artifact plumbing unless the user actually needs it.

## Code Review Checks

- Is validation placed at trust boundaries?
- Does the decoded domain type differ intentionally from the encoded wire type?
- Are branded values created through validation rather than casts?
- Are parse failures modeled as typed failures?
- Are Schema helpers and imports verified against the installed Effect version?
