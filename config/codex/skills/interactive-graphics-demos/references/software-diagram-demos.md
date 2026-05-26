# Software Diagram Demos

Use these patterns for interactive demos that explain distributed systems,
storage engines, protocols, queues, logs, routing, or consistency. These demos
are not just decorative diagrams: the drawing should expose a small model with
real invariants.

Good examples include a consistent hashing ring, quorum replication, and Raft
log replication. In each case the demo should make one protocol relationship
legible before it adds controls or motion.

## Start With The Invariant

Name the protocol fact in one sentence:

- Consistent hashing: a key is owned by the next token clockwise.
- Quorums: reads and writes overlap when `R + W > N`.
- Raft replication: a leader commits after the entry is stored on a majority.

Keep this invariant in the model, not in the renderer. The renderer should draw
derived ownership, intersections, message states, and commit status; it should
not decide protocol truth from pixels.

## Model Before Pixels

Use explicit domain state and derived values:

- `tokens`, `keys`, `owner`, `selectedOwner`, `loads`
- `replicas`, `writeSet`, `readSet`, `intersection`
- `rows`, `entries`, `messages`, `leaderCommitIndex`, `ackReplicaCount`

Prefer named statuses over booleans when a cell or message has a lifecycle:
`"empty"`, `"pending"`, `"committed"`, `"failed"`, `"lost"`. Map those statuses
to style in one place with a function such as `entryStyle(entry, unavailable)`.

Keep controls clamped to valid model states. If changing `N` makes a quorum,
selected key, or follower index invalid, update the dependent control before
drawing.

## Semantic Color

Color must mean the same thing everywhere it appears. If a key belongs to a blue
range, the selected key, route, arrow, owner label, and metric should all use
the owner color. Avoid a generic "selected yellow" when selection is inspecting
some other semantic category.

Use a small palette with stable meanings:

- Blue: request, write, pending, primary path, or node A.
- Green: read response, committed, success, or safety condition.
- Gold: overlap, acknowledgement, leader, or selected shared state.
- Red: failure, partition, movement, invalid condition, or lost message.
- Muted gray: inactive, empty, unavailable, or background context.

Legends should describe the semantic role, not just the mark shape. Prefer
"Selected key owner" over "Selected key" when the key color is ownership.

## Geometry Contracts

Do not connect circles, arrows, cells, or labels with arbitrary offsets. Define
ports and shared constants, then draw every related mark from those values.

Useful helpers:

```js
function pointAtAngle(center, radius, angle) {
  return {
    x: center.x + Math.cos(angle) * radius,
    y: center.y + Math.sin(angle) * radius,
  };
}

function entryPort(row, model, entry, side) {
  const entryX = row.x + (entry - 1) * (model.entryWidth + model.entryGap);
  return {
    x: entryX + model.entryWidth / 2,
    y: side === "bottom" ? row.y + ENTRY_HEIGHT : row.y,
  };
}
```

Name visual dimensions:

- `TOKEN_RADIUS`
- `SELECTED_KEY_RADIUS`
- `SELECTED_ROUTE_LINE_WIDTH`
- `ENTRY_HEIGHT`
- `MESSAGE_RADIUS`

When drawing a connection, use the same source of truth as the connected marks.
For example, draw a selected key route on the selected key radius, then turn
inward to the token edge. For log diagrams, route messages from `entryPort`
rather than from row centers.

## Layering

Use a stable drawing order:

1. Passive structure: rings, rows, cells, replica positions.
2. Background semantic regions: ownership arcs, quorum boundary, committed
   prefix.
3. Moving protocol messages or selected paths.
4. Entities and cells: tokens, replicas, log entries, client boxes.
5. Markers and badges: commit index, majority count, quorum rule.
6. Labels and metrics.

Selected paths and moving packets need enough contrast to read, but should not
hide the structure they explain. Use low-alpha trails for repeated background
traffic and full opacity for the current packet or selected path.

## Motion And Scrubbing

Animation should make state changes legible, not invent protocol behavior.

- Use one model time or scrub value as the source of truth.
- Start playback by default so the protocol is visibly active on first load.
- Derive active messages from scenario timings.
- Use easing for packet travel only after the event order is correct.
- Keep lost or partitioned messages visually distinct with dashed paths, red
  endpoints, or explicit stop markers.
- Respect reduced motion by pausing autoplay while leaving scrubbed states
  inspectable.

When a protocol repeats the same cycle, script the repeated scenario explicitly
instead of building unrelated bespoke frames. This keeps the visual story
consistent and makes the later entries feel like repetitions of the same rule.

## Layout And Labels

Software diagrams often have dense labels. Reserve text for the few facts the
viewer needs on this frame:

- Put durable metrics in DOM cards outside the canvas when possible.
- Put short, spatial labels near the object they describe.
- Hide optional badges on narrow widths instead of shrinking them into clutter.
- Use stable dimensions for cells, rows, markers, and controls so animation
  does not shift the layout.

If a label explains a state that is already color-coded, place it close to the
state and use the same color. If it explains an invariant, put it in a stable
center or header position where it will not chase animation.

## Validation

Check the behavior cases that prove the concept:

- For ownership: sample each owner color and any wraparound interval.
- For quorums: test both `R + W > N` and `R + W <= N`, plus failed replicas.
- For logs: pause at request, append, acknowledgement, majority, commit, and
  propagation states.

For visual verification, inspect desktop and mobile widths, toggle optional
layers, and check that connectors meet their endpoints. Pixel checks are useful
for semantic color regressions when the demo is canvas-only.
