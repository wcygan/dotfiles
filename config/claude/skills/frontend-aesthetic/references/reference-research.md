# Reference Research

The job: before writing any code, study 3–5 real, credible sites in the user's space and synthesize what they share. The output of this step is a single short paragraph stating the consensus and your one signature departure.

This file is the workflow. It says nothing about specific aesthetic territories — those are descriptive labels, not prescriptive picks.

## Step 1 — pick references

In priority order:

1. **Sites the user named.** Always lead with these. If they said "I like Linear and Vercel," those are your first two. Do not silently swap them out.
2. **Sites in the same domain** the user implicitly belongs to. See [domain-matching](./domain-matching.md) for canonical lists per domain.
3. **One nearby-but-different reference** to triangulate. If everything else is restrained, include one slightly louder peer to see what's optional and what's the consensus.

Aim for **3–5 references**. Fewer than 3 and you can't tell the consensus from the outlier. More than 5 and you'll smear into mush.

## Step 2 — visit each one

For each reference, look at the **landing page or marketing surface**, not the app shell. Spend a minute per site. If you have browser access, use it. If not, work from memory + descriptions, and acknowledge that limitation.

Take notes along these axes:

| Axis | What to record |
|---|---|
| **Typography** | Display family + body family + any mono. Size of the largest headline. Tracking. Display weight vs body weight. |
| **Palette** | Background base (light/dark, warm/cool). Text color. How many accent colors? Where do they appear (links, CTAs, status, emphasis)? Saturation level. |
| **Layout rhythm** | Container width. Hero composition (centered vs asymmetric). Section density. Card/list/full-bleed mix. Any signature layout move (split screen, oversized numerals, etc.)? |
| **Motion** | Is there an entrance animation on load? Any scroll-driven reveals? Are individual elements animated on hover, or is the page mostly still? |
| **Copy voice** | Does the headline sell a feeling or describe a feature? Is the tone confident-quiet, energetic, technical, warm? |
| **Signature** | The one thing that makes *this* site recognizable — a specific layout move, a font choice, a color, a copy device. |

## Step 3 — synthesize the consensus

Look at your notes. For each axis, ask: **what do most of them do?**

- If 4 of 5 references use a sans-serif display + sans-serif body in different weights, that's the consensus. Match it.
- If 3 of 5 use a single accent color and 2 use two-color systems, the consensus is "one accent."
- If they all run on a contained text width (~max-w-3xl-ish), match that. Don't go full-bleed because it feels distinctive.

Note the axes where references **disagree**. These are degrees of freedom — places where you can pick a position without departing from the neighborhood.

## Step 4 — pick one signature

Within the degrees of freedom (or, more rarely, by going one step beyond the consensus on a single axis), pick **one** signature that distinguishes the result from a generic copy. Examples:

- A more confident type scale than the references (their largest headline is `text-5xl`; you go `text-7xl`).
- A single saturated accent color where references use muted ones (still one accent — just hotter).
- A particular layout move (oversized section numerals, hanging eyebrow, split hero).
- A specific copy device (a colon-after-noun headline pattern, a one-word section label).

Don't pick a signature on every axis — that's how you get the four-variants disaster. One.

## Step 5 — state the synthesis

Write a single paragraph (3–5 sentences) and surface it to the user **before coding**. Format:

> Based on `<refs>`, the consensus is: `<typography>`, `<palette>`, `<layout rhythm>`, `<motion>`. They mostly differ on `<axis>`, where I'm picking `<position>` because `<reasoning>`. My one signature is `<one signature>` — defended because `<reason>`.

Example (real, for a Nu-Sync-style indie infra collective):

> Based on Linear, Vercel (post-2024), Railway, and Render, the consensus is: a sans-serif system (Inter or similar) with strong weight contrast between display and body, near-monochrome dark palette with one cool accent (cyan/electric blue), contained text width with strong vertical rhythm, mostly-still pages with a subtle on-load entrance, and confident-quiet copy that leads with what you can do. They differ on accent saturation. My one signature is a slightly larger hero scale (`text-7xl` instead of `text-5xl`) — defended because indie collectives can be more declarative than infra companies that need to look responsible.

Wait for a nod or a redirect. The synthesis is the artifact the user reviews — not the code.

## What to avoid

- **Inventing aesthetic territory names** ("brutalist," "lo-fi zine," "Swiss") and treating them as picks. They're descriptive labels for what *exists in references*; they're not menu items.
- **Picking 3 references that all look the same** — you'll just match one site. Include at least one near-but-different reference.
- **Overweighting the user's first reference** — if they said "Linear" and you have 4 other dev-tool peers, average across all 5; don't reproduce Linear.
- **Synthesizing without surfacing.** If the user never sees your synthesis paragraph, they can't redirect before you've spent effort on the wrong direction.

## When the user has no references

If the user says "I don't have references" or "you decide":

1. Pick 4–5 from the canonical list in [domain-matching](./domain-matching.md) for their domain.
2. Tell them which you used: "I'm using Linear, Vercel, Stripe, and Render as references because this reads as a developer-tools product. Say if you'd rather I anchor on different sites."
3. Proceed with the synthesis step. Their feedback on the synthesis is your real direction signal.
