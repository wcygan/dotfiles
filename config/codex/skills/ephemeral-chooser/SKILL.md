---
name: ephemeral-chooser
description: "Create, compare, share, and promote temporary component variants with an Ephemeral Chooser. Use when the user asks for several UI variants, a prototype switcher, query-parameter review links, Leva-style tuning controls, or to keep one winner and tear down the chooser and losing prototypes."
---

# Ephemeral Chooser

Build a disposable comparison surface that ends with exactly one canonical
implementation. The chooser is temporary product-development infrastructure,
not a permanent abstraction.

This skill grants no additional authority to edit, delete, install, commit,
push, deploy, or write externally. A review URL records state; it is never
approval to promote a variant. Delete prototypes only after the user explicitly
selects a stable variant ID.

## Reference routing

Read only the references needed for the current phase:

- Read [`references/ephemeral-chooser.html`](references/ephemeral-chooser.html)
  before implementing the chooser shell, query-state adapter, tuning controls,
  selection receipt, or teardown interaction. It is a dependency-free,
  framework-neutral local page containing project-card, save-feedback, and
  filter-summary examples.
- Read [`references/chooser-contract.md`](references/chooser-contract.md)
  before creating a run manifest, promoting a winner, or cleaning temporary
  files and dependencies.

The HTML is a behavior and structure reference. Adapt its appearance to the
target project's existing design system instead of copying its visual styling
blindly.

## Choose the phase

### Explain or plan

When the user asks only to explore, explain, review, or plan, inspect and report
without editing. Define the comparison axes, invariants, manifest, and
promotion boundary.

### Create or revise a chooser

When the user asks to build or change one, implement the chooser and validate
it, but do not promote a winner unless the same request explicitly identifies
one.

### Promote and clean

Require an explicit stable variant ID such as `metrics-first`. Reconfirm the
target and manifest-owned cleanup surface before removing anything.

## Establish the baseline

Before editing:

1. Read the applicable repository instructions.
2. Record the workspace root, branch, revision, and dirty state.
3. Inspect the canonical component, its public API, fixtures, tests, and
   rendered context.
4. Separate pre-existing user changes from chooser-owned work.
5. Define invariants shared by every variant: data, props, behavior,
   accessibility, viewport, and product constraints.
6. Create the manifest described in
   [`references/chooser-contract.md`](references/chooser-contract.md), using
   exact paths and before-hashes rather than globs.

If existing edits overlap the component or cleanup boundary, isolate the
experiment safely or stop for direction. Never overwrite or delete ambiguous
work.

## Build the comparison

1. Include the current component as `current` when one exists, plus two to four
   meaningfully different variants.
2. Use semantic kebab-case IDs and give each variant a one-sentence thesis.
3. Keep shared business logic, fixtures, and mutable input state outside the
   variant implementations.
4. Mount only the selected variant. Do not leave losing variants hidden in the
   DOM, where duplicate IDs, focus targets, effects, and requests can remain
   active.
5. Use native controls or the project's accessible primitives. Selection must
   be keyboard-operable, visibly focused, and announced without moving focus.
6. Use a namespaced query key such as `ec.project-card`. Allowlist IDs, preserve
   unrelated query parameters and the hash, use `history.replaceState`, and
   fall back to `current` for unknown values.
7. Provide an explicit copy-link action. A colleague still needs access to the
   same served preview; query parameters carry state, not the page itself.
8. Keep tuning controls outside the variant subtree and serialize the values
   needed to reproduce the result.

Use Leva only when the project already uses React and the user wants dense live
tuning, or when adding it is explicitly in scope. Keep it in the temporary
entrypoint and record it as a temporary dependency. Use shadcn/ui when it
already matches the project and helps with accessible chooser chrome; do not
introduce either library solely for a framework-neutral proof.

## Review the chooser

Validate the same fixture and state across variants. Browser-check:

- every variant and tuning control;
- URL updates, reload hydration, copied state, and invalid-parameter fallback;
- keyboard selection and focus after finalization;
- desktop and narrow responsive layouts with no horizontal overflow;
- light and dark themes when the project supports them;
- `prefers-reduced-motion` plus any explicit motion control; and
- console errors, duplicate IDs, and unintended background activity.

The create phase is complete when the chooser is reviewable, shareable, and
reproducible, with the manifest and validation evidence reported. Stop and wait
for an explicit selection.

## Promote the winner

1. Record the selected variant ID, control values, review URL, timestamp, and
   user-selection evidence in the manifest.
2. Recheck the selected artifact and target before-hashes. Stop if either
   changed outside the chooser workflow.
3. Materialize the exact winner at the canonical component path before
   deleting any prototype.
4. Render and test the canonical component without relying on chooser state.
5. Rehash every manifest-owned temporary file against its recorded
   `generatedSha256`; retain and report any mismatch.
6. Remove only verified manifest-owned losing variants, routes, selectors,
   query glue, tuning controls, fixtures, assets, and temporary dependencies.
7. Update the lockfile only when dependency pruning requires it.
8. Search for the chooser ID, query key, variant IDs, temporary classes,
   imports, flags, and dependency names.
9. Compare the final diff with the baseline. It should contain the promoted
   product change and required tests or docs, not chooser residue.

If a manifest-owned path has unexpected changes, retain it and report the
blocker instead of deleting it.

## Final report

Report:

- baseline revision and pre-existing dirty state;
- chooser ID, query key, variants, and tuning controls;
- local review URL and validation performed;
- explicit winner and frozen control values;
- files retained, promoted, removed, or blocked;
- exact tests and browser evidence; and
- residue-search result and any remaining risk.

## Invocation examples

```text
$ephemeral-chooser Create an Ephemeral Chooser for ProjectCard with the current
version plus three alternatives. Keep its props and fixture fixed, store the
selection in ec.project-card, and wait for me to choose a winner.
```

```text
$ephemeral-chooser Keep metrics-first from the ProjectCard chooser. Preserve
its current tuning values, promote it to the canonical component, remove only
manifest-owned chooser files and dependencies, then run the recorded checks
and prove no chooser residue remains.
```
