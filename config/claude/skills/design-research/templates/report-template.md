# Design Research Report: [Site Name]

**URL:** [target-url]
**Date:** [current-date]
**Purpose:** [What the engineer wants to implement]

---

## Visual Overview

Screenshots captured:
- **Full page:** `design-research-output/full-page.png`
- **Viewport (desktop):** `design-research-output/viewport.png`
- **Mobile:** `design-research-output/mobile.png`
- **Tablet:** `design-research-output/tablet.png`
- **Dark mode:** `design-research-output/dark-mode.png` (if applicable)

[Brief visual description of the site's overall aesthetic]

---

## Design System

### Color Palette

**Primary Colors:**
- Primary: `#XXXXXX`
- Secondary: `#XXXXXX`
- Accent: `#XXXXXX`

**Neutral Colors:**
- Gray 50: `#XXXXXX`
- Gray 100: `#XXXXXX`
- Gray 200: `#XXXXXX`
- Gray 300: `#XXXXXX`
- Gray 400: `#XXXXXX`
- Gray 500: `#XXXXXX`
- Gray 600: `#XXXXXX`
- Gray 700: `#XXXXXX`
- Gray 800: `#XXXXXX`
- Gray 900: `#XXXXXX`

**Semantic Colors:**
- Success: `#XXXXXX`
- Error: `#XXXXXX`
- Warning: `#XXXXXX`
- Info: `#XXXXXX`

### Typography

**Font Families:**
- Headings: [Font name]
- Body: [Font name]
- Monospace: [Font name]

**Type Scale:**
- H1: [size/weight/line-height]
- H2: [size/weight/line-height]
- H3: [size/weight/line-height]
- H4: [size/weight/line-height]
- Body: [size/weight/line-height]
- Small: [size/weight/line-height]

**Font Loading:**
- Strategy: [How fonts are loaded]
- Source: [Google Fonts/Self-hosted/System fonts]

### Spacing System

**Base unit:** Xpx

**Scale:**
- xs: Xpx
- sm: Xpx
- md: Xpx
- lg: Xpx
- xl: Xpx
- 2xl: Xpx
- 3xl: Xpx

**Grid/Container:**
- Max width: Xpx
- Gutter: Xpx
- Columns: X

### Shadows & Effects

**Box Shadows:**
- sm: [shadow values]
- md: [shadow values]
- lg: [shadow values]
- xl: [shadow values]

**Border Radius:**
- sm: Xpx
- md: Xpx
- lg: Xpx
- full: [value]

**Transitions:**
- Default duration: Xms
- Easing: [easing function]

---

## Components

### Navigation

**Structure:**
```html
[Simplified HTML structure]
```

**Key styles:**
- [Important CSS patterns]

**States:**
- Default: [description]
- Hover: [description]
- Active: [description]
- Mobile: [description]

**Accessibility:**
- [ARIA attributes, keyboard navigation]

---

### Buttons

**Variants:**

#### Primary Button
- Background: [color]
- Text: [color]
- Hover: [changes]
- Active: [changes]
- Disabled: [changes]

#### Secondary Button
- Background: [color]
- Text: [color]
- Hover: [changes]

#### Ghost/Text Button
- [Styles]

**Structure:**
```html
[Button markup]
```

---

### Forms

**Input Fields:**
- Default state: [styles]
- Focus state: [styles]
- Error state: [styles]
- Disabled state: [styles]

**Validation:**
- [How errors are shown]
- [Validation patterns]

---

### Cards

**Structure:**
```html
[Card markup]
```

**Variants:**
- [Different card types observed]

**Interactive states:**
- [Hover, active states if applicable]

---

### [Other Components]

[Document any other notable components: modals, alerts, tabs, etc.]

---

## Layout Patterns

### Page Structure

**Layout approach:** [Flexbox/Grid/Hybrid]

**Container widths:**
- Mobile: X
- Tablet: X
- Desktop: X
- Wide: X

**Sections:**
- [How page sections are structured]

### Responsive Strategy

**Approach:** [Mobile-first/Desktop-first/Fluid]

**Breakpoints:**
- sm: Xpx
- md: Xpx
- lg: Xpx
- xl: Xpx
- 2xl: Xpx

**Mobile adaptations:**
- [Key changes at mobile breakpoint]

---

## Technology Stack

### Frontend Framework
- **Framework:** [React/Vue/Svelte/Vanilla]
- **Version:** [if detectable]

### Meta-framework
- **Framework:** [Next.js/Nuxt/SvelteKit/None]
- **Rendering:** [SSR/SSG/CSR/Hybrid]

### Component Library
- **Library:** [Material UI/shadcn/Chakra/Custom/None]

### CSS Approach
- **Method:** [Tailwind/CSS Modules/Styled Components/Vanilla CSS]
- **Preprocessor:** [Sass/PostCSS/None]

### Icon System
- **Library:** [Heroicons/Lucide/Font Awesome/SVG sprites]

### Animation
- **Library:** [Framer Motion/GSAP/CSS only]

### Other Notable Libraries
- [State management, routing, etc.]

---

## Implementation Recommendations

### Quick Start Stack

Recommended tools to replicate this design:

```bash
# Suggested setup
npx create-[framework]@latest my-project
cd my-project
npm install [recommended-packages]
```

**Recommended packages:**
- [List of npm packages that match the site's tech stack]

### Design Tokens Setup

Create a centralized design system:

**1. Colors** (`tokens/colors.ts` or `styles/colors.css`)
```css
:root {
  --color-primary: #XXXXXX;
  --color-secondary: #XXXXXX;
  /* ... */
}
```

**2. Typography** (`tokens/typography.ts`)
```typescript
export const typography = {
  fontFamily: {
    heading: '...',
    body: '...',
  },
  fontSize: {
    xs: '...',
    sm: '...',
    /* ... */
  }
}
```

**3. Spacing** (`tokens/spacing.ts`)
```typescript
export const spacing = {
  xs: '4px',
  sm: '8px',
  /* ... */
}
```

### Component Architecture

Suggested structure:

```
/src
  /components
    /ui              # Atomic components
      Button.tsx
      Input.tsx
      Card.tsx
      Badge.tsx
    /layout          # Layout components
      Header.tsx
      Footer.tsx
      Container.tsx
      Navigation.tsx
    /features        # Feature-specific components
      [feature]/
  /styles
    globals.css
    tokens.css
  /lib
    utils.ts
```

### Key Patterns to Replicate

1. **[Pattern 1]**
   - Implementation: [How to build this]
   - Example: [Code snippet]

2. **[Pattern 2]**
   - Implementation: [How to build this]
   - Example: [Code snippet]

3. **[Pattern 3]**
   - Implementation: [How to build this]
   - Example: [Code snippet]

### Responsive Implementation

```css
/* Mobile-first approach */
.component {
  /* Mobile styles (default) */
}

@media (min-width: 768px) {
  /* Tablet styles */
}

@media (min-width: 1024px) {
  /* Desktop styles */
}
```

### Accessibility Checklist

- [ ] Semantic HTML structure
- [ ] ARIA labels where needed
- [ ] Keyboard navigation support
- [ ] Focus indicators
- [ ] Color contrast ratios (WCAG AA minimum)
- [ ] Screen reader testing

---

## Performance Observations

### Image Optimization
- [WebP/AVIF usage, lazy loading, responsive images]

### Font Loading
- [How fonts are loaded to avoid FOUT/FOIT]

### Code Splitting
- [Evidence of lazy loading, route-based splitting]

### CSS Delivery
- [Critical CSS, async loading]

---

## Unique Patterns & Gotchas

[Any unique implementation details, interesting patterns, or potential gotchas to be aware of]

---

## Additional Resources

### Similar Open-Source Examples
- [Link to similar component libraries or templates]

### Design System References
- [If they publish a design system or styleguide]

### Further Reading
- [Any relevant documentation or resources]

---

## Next Steps

1. **Setup project structure**
   - Initialize with recommended framework
   - Install dependencies
   - Configure tooling (TypeScript, ESLint, etc.)

2. **Establish design tokens**
   - Create color palette
   - Define typography scale
   - Set up spacing system
   - Configure breakpoints

3. **Build UI component library**
   - Start with Button component
   - Add Input and form components
   - Build Card component
   - Create layout components

4. **Implement page layouts**
   - Header/Navigation
   - Footer
   - Main content areas
   - Responsive adaptations

5. **Add interactions**
   - Hover states
   - Click interactions
   - Form validation
   - Animations/transitions

6. **Optimize & polish**
   - Performance optimization
   - Accessibility audit
   - Cross-browser testing
   - Responsive testing

---

**Research artifacts:** All screenshots and detailed analysis files are available in `design-research-output/`
