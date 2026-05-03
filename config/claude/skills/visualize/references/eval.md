# Evaluation Rubric — Quick Reference

Condensed scoring guide. Full protocol in `eval/SKILL.md`.

## 8 Dimensions

| # | Dimension | Weight | What to Check |
|---|-----------|--------|---------------|
| D1 | First Impression | 15% | 2-second gut reaction. Professional? Clear focal point? |
| D2 | Typography | 15% | Hierarchy, sizes, line-height, max 2 fonts |
| D3 | Color | 10% | Harmonious palette, WCAG AA, accent purpose, both themes |
| D4 | Layout | 15% | Consistent spacing, whitespace, responsive, alignment |
| D5 | Content | 15% | Accurate, clear message in 5s, right density, zero filler |
| D6 | Interactivity | 10% | Menu, theme, download, print, navigation, hover states |
| D7 | Technical | 10% | Zero errors, <200KB, semantic HTML, print CSS, a11y |
| D8 | Shareability | 10% | Would you tweet this? Better than Gamma/Canva? |

## Scoring Anchor Points

| Score | Meaning | Comparable To |
|-------|---------|---------------|
| 10 | Perfection | Apple keynote, NYT data viz |
| 9 | Impressive | Stripe's blog, top Dribbble shot |
| 8 | Professional | Good Gamma template, polished Figma prototype |
| 7 | Acceptable | Average corporate deck, basic Canva output |
| 6 | Mediocre | Default PowerPoint, generic template |
| 5 | Poor | Ugly but functional |
| ≤4 | Broken | Layout issues, missing features, embarrassing |

## Quality Gates

| Gate | Overall | Min per Dimension | Action |
|------|---------|-------------------|--------|
| 🚀 VIRAL | ≥ 9.5 | ≥ 9 | Ship + promote everywhere |
| ✅ SHIP | ≥ 9.0 | ≥ 8 | Ready for release |
| ⚠️ GOOD | ≥ 8.0 | ≥ 7 | Fix before featuring |
| 🔧 NEEDS WORK | ≥ 7.0 | any < 7 | Fix + re-evaluate |
| ❌ FAIL | < 7.0 | any < 5 | Major rework |

## Target: SHIP (≥ 9.0) for all outputs. VIRAL (≥ 9.5) for showcase examples.

## Common Deductions

| Issue | Dimension | Points Lost |
|-------|-----------|-------------|
| Menu missing | D6 | -4 |
| Placeholder/lorem ipsum | D5 | -5 |
| Broken at mobile | D4 | -3 |
| No entrance animations | D1, D8 | -2 each |
| Clashing colors | D3 | -3 |
| All text same size | D2 | -3 |
| Console errors | D7 | -2 each |
| Light theme broken | D3, D6 | -2 each |
| Too much text per slide | D5 | -3 |
| No hover states | D6 | -1 |
| No print styles | D7 | -2 |
| Cramped spacing | D4 | -3 |
| Generic/forgettable | D1, D8 | -2 each |
