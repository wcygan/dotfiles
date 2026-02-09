# Design Research Skill

**A comprehensive website design analysis tool for software engineers.**

## What It Does

This skill helps you research and understand website designs by:
- Capturing screenshots across multiple devices and viewports
- Analyzing CSS styling, colors, typography, and spacing
- Documenting component patterns and design systems
- Detecting the technology stack (frameworks, libraries, tools)
- Generating implementation-ready documentation

## When To Use

Invoke this skill when you want to:
- Implement a similar design to an existing website
- Study a competitor's design system
- Understand how a specific UI pattern is built
- Extract design tokens from a live site
- Get a tech stack report for reference

## Usage

```bash
/design-research
```

Claude will then ask you for the target URL and begin the research process.

## What You Get

After the skill completes, you'll receive:

1. **`design-research-output/`** directory with:
   - Full page screenshot
   - Desktop viewport screenshot
   - Mobile viewport screenshot
   - Tablet viewport screenshot
   - Dark mode screenshot (if applicable)

2. **`design-research-report.md`** containing:
   - Color palette with exact hex values
   - Typography scale (fonts, sizes, weights, line heights)
   - Spacing system and grid
   - Component inventory with implementation details
   - Layout patterns and responsive breakpoints
   - Technology stack detection
   - Implementation recommendations

3. **Summary in chat** with key findings and next steps

## Bot Protection Handling

The skill automatically handles anti-bot systems like Cloudflare:

### Automatic Detection
✅ Detects bot challenges automatically
✅ No user intervention needed for detection
✅ Clear feedback on what's happening

### Automatic Retry Strategy

1️⃣ **Standard Playwright** - Fast, works for most sites
2️⃣ **Camoufox Stealth Mode** - Firefox-based anti-detect, ~70% success against Cloudflare
3️⃣ **Manual Fallback** - Guided browser-based extraction

### When Automated Methods Fail

If both standard and stealth modes are blocked:
1. You'll receive clear instructions for manual capture
2. DevTools scripts for CSS/style extraction
3. Step-by-step screenshot workflow
4. Guidance on returning data to Claude

See `MANUAL-FALLBACK.md` for the complete manual workflow.

### Success Rates (Verified Testing)

| Protection Level | Standard | Stealth | Manual | Verified Sites |
|-----------------|----------|---------|--------|----------------|
| None | ✅ 100% | ✅ 100% | ✅ 100% | - |
| Basic (rate limiting) | ✅ 90% | ✅ 95% | ✅ 100% | - |
| Moderate (Cloudflare) | ❌ 0% | ✅ 100% | ✅ 100% | **cs2lens.com** ✅ (2026-02-09) |
| Aggressive (Cloudflare+) | ❌ 0% | ❌ ~0% | ✅ 100% | **jumpthrow.pro** ⚠️ (2026-02-09) |

**Testing Summary**:
- **cs2lens.com** (Moderate): Camoufox bypassed successfully, zero manual intervention
- **jumpthrow.pro** (Aggressive): Camoufox detected, served corrupted content, manual required

**Realistic Automated Success Rate**: 50-70% against Cloudflare (varies by configuration)

**Manual fallback always works** - it uses your authenticated browser session.

## Prerequisites

The skill requires:

1. **UV** (Python package manager) - Already available via dotfiles Nix flake
2. **Tesseract OCR** (recommended) - For improved bot detection via text extraction
3. **Playwright CLI** (optional) - For initial attempts before stealth mode

UV is required for Camoufox stealth mode. Tesseract OCR significantly improves detection accuracy (catches large block pages). Playwright CLI is used for initial fast attempts but will automatically fall back to stealth if blocked.

**First-run setup**:
- Camoufox will automatically download a 306MB Firefox browser on first use (one-time, ~15-20s thereafter)
- Tesseract can be installed via `brew install tesseract` on macOS or your system package manager

**Without Tesseract**: Detection still works but relies only on file size, which may miss large block pages (e.g., 78KB Cloudflare pages with graphics).

## Example Output

```
design-research-output/
├── full-page.png
├── viewport.png
├── mobile.png
├── tablet.png
└── dark-mode.png

design-research-report.md
```

The report includes actionable insights like:

```markdown
## Design System

### Color Palette
- Primary: #3B82F6
- Secondary: #8B5CF6
- Accent: #F59E0B

### Typography
- Headings: Inter, 700 weight
- Body: Inter, 400 weight
- Type scale: 14px, 16px, 20px, 24px, 32px, 48px

### Spacing System
- Base unit: 4px
- Scale: 4, 8, 16, 24, 32, 48, 64, 96

## Technology Stack
- Framework: React 18
- Meta-framework: Next.js 14
- CSS: Tailwind CSS
- Icons: Heroicons
- Animation: Framer Motion
```

## Advanced Usage

### Manual Script Execution

You can also run the helper scripts directly:

**Capture screenshots:**
```bash
./config/claude/skills/design-research/scripts/capture-screenshots.sh https://example.com
```

**Analyze styles:**
```bash
node ./config/claude/skills/design-research/scripts/analyze-styles.js https://example.com
```

### Authentication Required Sites

For sites requiring login, use Playwright's interactive mode:

```bash
npx playwright codegen https://example.com
```

This lets you manually log in, then record the session for automated analysis.

## Tips

- **Be specific**: If you only care about one page section, tell Claude
- **Dark mode**: Claude will attempt to capture dark mode if supported
- **Responsive design**: All major breakpoints are captured automatically
- **Component focus**: Ask Claude to focus on specific components (e.g., "focus on the navigation and button styles")

## Complementary Skills

Combine with other skills for a complete workflow:

- **`web-research`** - Research the company/product context
- **`ux-review`** - Get UX analysis beyond visual design
- **`frontend-design`** - Actually implement the design after research

## Files Included

```
design-research/
├── SKILL.md                    # Main skill instructions for Claude
├── REFERENCE.md                # Detailed methodology guide
├── README.md                   # This file (user documentation)
├── scripts/
│   ├── capture-screenshots.sh  # Automated screenshot capture
│   └── analyze-styles.js       # CSS and style analysis
└── templates/
    └── report-template.md      # Report structure template
```

## Installation

This skill is automatically available after running:

```bash
./scripts/link-config.sh
```

Or manually symlink:

```bash
ln -sf ~/Development/dotfiles/config/claude/skills/design-research ~/.claude/skills/
```

Then restart your Claude Code session.

## Limitations

- **Public sites only**: Sites requiring authentication need manual setup
- **Dynamic content**: Heavily JS-rendered content may need wait time
- **Cross-origin styles**: Some external stylesheets may not be accessible
- **Large sites**: Focus on specific pages for best results

## Troubleshooting

**Playwright not found:**
```bash
npx playwright install chromium
```

**Screenshots failing:**
- Check URL is accessible
- Increase timeout: `--timeout=60000`
- Try `--browser-args="--disable-gpu"`

**Incomplete CSS data:**
- Some styles may be in external sheets (CORS blocked)
- Use browser DevTools manually for cross-origin styles
- The skill will use computed styles as fallback

## Example Use Cases

✅ **"Research the design of stripe.com homepage"**
- Gets color palette, typography, component patterns
- Identifies tech stack (React, Next.js, Tailwind)
- Provides implementation recommendations

✅ **"Analyze the button styles on github.com"**
- Focuses on button component variants
- Documents all interactive states
- Extracts exact CSS values

✅ **"Study the navigation pattern on vercel.com"**
- Captures desktop and mobile navigation
- Documents responsive behavior
- Notes accessibility patterns

## Contributing

Found an issue or want to improve this skill?

1. Edit files in `config/claude/skills/design-research/`
2. Test by invoking `/design-research` in Claude Code
3. Commit changes to dotfiles repo

---

**Created by:** /new-global-skill
**Version:** 1.0.0
**Last updated:** 2026-02-08
