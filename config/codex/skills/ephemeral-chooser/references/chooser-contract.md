# Ephemeral Chooser Contract

Use this contract when a chooser will create temporary source, accept a winner,
or remove prototypes. The chooser grants no new authority; the user's request
still determines whether the task may edit, install, delete, commit, push, or
deploy.

## Lifecycle

```text
baselined -> generated -> review-ready -> selected -> promoted -> cleaned
```

`selected` requires an explicit user choice. A URL, last-viewed variant, default
variant, screenshot, model preference, or collaborator comment is not a
selection.

## Manifest

Keep a small manifest in a task-owned or project-approved temporary path. Do not
commit it unless the user asks for durable experiment history.

```json
{
  "schemaVersion": 1,
  "id": "project-card",
  "state": "review-ready",
  "target": "src/components/ProjectCard.tsx",
  "baselineRef": "<git-revision>",
  "queryKey": "ec.project-card",
  "defaultVariant": "current",
  "variants": [
    {
      "id": "current",
      "label": "Current",
      "thesis": "Preserve the existing hierarchy.",
      "path": "src/prototypes/project-card/current.tsx",
      "sha256": "<sha256>"
    },
    {
      "id": "metrics-first",
      "label": "Metrics first",
      "thesis": "Lead with measurable health.",
      "path": "src/prototypes/project-card/metrics-first.tsx",
      "sha256": "<sha256>"
    }
  ],
  "controls": {
    "density": "roomy",
    "motion": "on"
  },
  "ownedFiles": [
    {
      "path": "src/prototypes/project-card/current.tsx",
      "beforeState": "absent",
      "generatedSha256": "<sha256>"
    },
    {
      "path": "src/prototypes/project-card/metrics-first.tsx",
      "beforeState": "absent",
      "generatedSha256": "<sha256>"
    },
    {
      "path": "src/prototypes/project-card/chooser.tsx",
      "beforeState": "absent",
      "generatedSha256": "<sha256>"
    }
  ],
  "editedFiles": [
    {
      "path": "src/components/ProjectCard.tsx",
      "beforeSha256": "<sha256>"
    }
  ],
  "temporaryDependencies": [],
  "selection": null
}
```

Rules:

- Use canonical, exact paths. Never use globs, `~`, or unresolved variables.
- Record every file the chooser creates and every existing file it edits.
- An `ownedFiles` entry is valid only when the path was absent at baseline.
  Record `beforeState: "absent"`, hash the completed generated file, and recheck
  `generatedSha256` immediately before deletion. If the path existed at
  baseline, treat it as an edited file or stop; never claim it as disposable.
- Hash the canonical target before creation and recheck it before promotion.
- Record temporary packages even when they were added as development
  dependencies; imports can still place them in a browser bundle.
- Keep secrets, environment dumps, tokens, and private user data out of the
  manifest.
- If an owned path contains unexpected edits, do not delete it.

## Comparison invariants

Hold these constant unless the user explicitly wants them varied:

- public component API and events;
- fixture data and loading, empty, error, and success states;
- business rules and side effects;
- accessibility semantics and keyboard behavior;
- viewport, theme, locale, and reduced-motion preference; and
- performance measurement method.

One mounted variant should receive the shared state through a common adapter.
Do not duplicate backend calls or business state inside each visual proposal.

## URL state

Use namespaced keys:

```text
?ec.project-card=metrics-first
&ec.save-feedback=status-pill
&ec.project-card.density=compact
```

Validate every value against an allowlist. Preserve unrelated query parameters
and the URL hash. Use stable semantic IDs rather than array indexes. Unknown or
retired IDs fall back to `current`.

Use `history.replaceState` for presentation-only switching so the Back button
is not polluted. Hydrate on load and handle `popstate` when the host can change
the URL through other navigation. The copy action should copy the complete
served URL. A localhost URL is shareable only with someone who can reach that
same server.

## Tuning controls

Variant choice and tuning values are separate axes:

- Variant IDs select a structural or conceptual direction.
- Controls tune values such as timing, density, radius, thresholds, or copy.

Store reproducibility-critical values in the URL or manifest. When a winner is
selected, freeze those values into named constants, tokens, props, or
configuration owned by the promoted component.

Leva is an optional React control surface, not a chooser or persistence layer.
shadcn/ui is optional accessible presentation and source distribution, not the
promotion state machine. Remove chooser-only code and dependencies after
promotion.

## Promotion receipt

Before cleanup, record:

```json
{
  "chooserId": "project-card",
  "variantId": "metrics-first",
  "controls": {
    "density": "compact",
    "motion": "off"
  },
  "reviewUrl": "http://127.0.0.1:4173/?ec.project-card=metrics-first",
  "selectedBy": "user",
  "selectedAt": "<rfc3339>",
  "artifactSha256": "<sha256>"
}
```

Then:

1. Materialize the winner at the canonical target.
2. Validate the target without chooser flags or query parameters.
3. Compare the rendered target with the selected preview.
4. Rehash every manifest-owned temporary file. Delete only files whose current
   hash matches `generatedSha256`, then prune dependencies.
5. Search source, tests, assets, package manifests, lockfiles, and build output
   for residue.
6. Confirm the final diff contains the winner, required tests or docs, and
   nothing from the temporary chooser.

## Acceptance checklist

- Current behavior is available as a baseline variant when applicable.
- Every option has a stable ID and a distinct thesis.
- Only one variant is mounted.
- Selection and controls survive reload through validated URL state.
- Keyboard, focus, narrow layout, dark mode, and reduced motion are verified.
- The user explicitly selected the promoted ID.
- The promoted component works without the chooser.
- Cleanup touched only manifest-owned paths that still matched their recorded
  generated hashes.
- Temporary dependencies and lockfile entries are gone.
- Residue search is clean.
- Pre-existing dirty work remains unchanged.
