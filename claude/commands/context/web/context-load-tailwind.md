# /context-load-tailwind

Load comprehensive documentation context for Tailwind CSS utility-first styling framework.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Core Concepts**: `https://tailwindcss.com/docs/styling-with-utility-classes`
     - Focus on: utility-first principles, design system approach, composition patterns
   - **State Management**: `https://tailwindcss.com/docs/hover-focus-and-other-states`
     - Focus on: pseudo-class variants, interactive states, group/peer modifiers
   - **Responsive Design**: `https://tailwindcss.com/docs/responsive-design`
     - Focus on: mobile-first approach, breakpoints, responsive utilities
   - **Color System**: `https://tailwindcss.com/docs/colors`
     - Focus on: color palettes, opacity modifiers, dark mode variants
   - **Customization**: `https://tailwindcss.com/docs/adding-custom-styles`
     - Focus on: theme customization, arbitrary values, component extraction
   - **Functions & Directives**: `https://tailwindcss.com/docs/functions-and-directives`
     - Focus on: @theme, @utility, @apply directives, CSS integration
   - **Layout System**: `https://tailwindcss.com/docs/aspect-ratio`
     - Focus on: aspect ratios, grid, flexbox, positioning
   - **Spacing & Sizing**: `https://tailwindcss.com/docs/padding`
     - Focus on: spacing scale, sizing utilities, responsive spacing
   - **Typography**: `https://tailwindcss.com/docs/font-family`
     - Focus on: font system, text sizing, line height, letter spacing
   - **Borders & Effects**: `https://tailwindcss.com/docs/border-radius`
     - Focus on: borders, shadows, effects, transforms
   - **Preflight CSS Reset**: `https://tailwindcss.com/docs/preflight`
     - Focus on: CSS normalization, browser consistency, base layer styling

3. **Key documentation sections to prioritize**:
   - Utility-first methodology and benefits
   - Complete class reference and naming patterns
   - State variants and pseudo-class handling
   - Responsive design patterns and breakpoints
   - Color system and palette organization
   - Customization strategies and theme extension
   - Performance optimization and purging
   - Integration with frameworks and build tools

4. **Focus areas for this stack**:
   - Rapid prototyping with utility classes
   - Component composition patterns
   - Responsive design implementation
   - State management through variants
   - Color system and design tokens
   - Custom styling integration
   - Performance optimization
   - Accessibility considerations

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Building responsive interfaces with utility classes
- Implementing interactive states and animations
- Creating consistent design systems
- Customizing Tailwind for specific design needs
- Optimizing performance and bundle size
- Integrating with popular frameworks (React, Vue, Fresh)
- Managing dark mode and theme switching
- Writing maintainable utility-based CSS
- Accessibility best practices with Tailwind
- Migration strategies from traditional CSS

## Framework Integration Patterns

### Deno Fresh Integration

- Use official Tailwind CSS plugin for Fresh 1.6+
- Configure `deno.json` with Tailwind build tasks
- Fresh 2.0 alpha includes built-in Tailwind option
- Implement CSS fallbacks for plugin reliability issues

### React/Preact Patterns

- Component-based utility composition
- Conditional class application with `clsx` or similar
- TypeScript integration for class validation
- Props-based styling patterns

### Build Tool Integration

- PostCSS plugin configuration
- Content detection and purging
- JIT (Just-In-Time) compilation
- Custom build optimization

## Preflight CSS Reset Foundation

**ALWAYS leverage Tailwind's Preflight CSS reset by default for all projects:**

- **Automatic Inclusion**: Preflight is automatically injected when importing Tailwind CSS
- **Cross-Browser Consistency**: Built on modern-normalize for reliable browser normalization
- **Design System Foundation**: Provides neutral starting point for intentional styling choices

### Key Preflight Benefits

- **Removes default margins** from all elements (headings, paragraphs, lists)
- **Resets border styles** for consistent appearance across browsers
- **Normalizes headings** to same font size/weight as body text
- **Unstyled lists** with no bullets/numbers for design flexibility
- **Block-level images** constrained to parent width while preserving aspect ratio
- **Prevents accidental reliance** on browser default styles

### Preflight Best Practices

- **Embrace the reset**: Design with intentional spacing and typography from the start
- **Use role="list"** on unstyled lists for screen reader accessibility
- **Extend via @layer base** for custom base styles when needed
- **Never fight Preflight** - work with its opinionated defaults for consistency

## Design System Best Practices

### Color Strategy

- **Semantic Naming**: Use purpose-based color application
  - Primary: `bg-blue-500`, `text-blue-600`
  - Success: `bg-green-500`, `text-green-700`
  - Warning: `bg-yellow-500`, `text-yellow-700`
  - Error: `bg-red-500`, `text-red-700`
- **60-30-10 Rule**: Dominant (60%), secondary (30%), accent (10%)
- **Dark Mode**: Always implement `dark:` variants
- **Opacity Modifiers**: Use `/` syntax for transparency: `bg-blue-500/20`

### Typography Hierarchy

- **Scale Limitation**: Use max 5-6 sizes for consistency
- **Line Height**: `leading-tight` (1.25) for headings, `leading-relaxed` (1.625) for body
- **Font Weight**: Strategic use from `font-light` to `font-bold`
- **Reading Width**: `max-w-prose` (65ch) for optimal readability

### Spacing System

- **8-Point Grid**: Stick to Tailwind's spacing scale (4, 8, 12, 16, 20, 24...)
- **Consistent Patterns**:
  - Section spacing: `py-16 md:py-24`
  - Card padding: `p-6` or `p-8`
  - Component spacing: `space-y-4` or `space-y-6`
  - Container margins: `container mx-auto px-4`

### Component Patterns

- **Cards**: `bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700`
- **Buttons**:
  - Primary: `bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md transition-colors`
  - Secondary: `bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-700 dark:hover:bg-slate-600`
- **Forms**: `border border-slate-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent`
- **Navigation**: `backdrop-blur-sm bg-white/80 dark:bg-slate-900/80 border-b border-slate-200 dark:border-slate-800`

### Responsive Patterns

- **Mobile-First**: Start with base styles, enhance with `md:`, `lg:`, `xl:`
- **Breakpoint Strategy**:
  - `sm:` (640px) - Large phones, avoid for mobile targeting
  - `md:` (768px) - Tablets and up
  - `lg:` (1024px) - Desktops and up
  - `xl:` (1280px) - Large screens
- **Common Responsive Patterns**:
  - Grid: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`
  - Flex: `flex flex-col md:flex-row gap-4`
  - Typography: `text-3xl md:text-4xl lg:text-5xl`
  - Spacing: `px-4 md:px-6 lg:px-8`

### State Management

- **Interactive States**: Always include `transition-colors duration-200`
- **Hover Effects**: Subtle changes - `hover:bg-slate-50`, `hover:scale-105`
- **Focus States**: Accessible focus rings - `focus:ring-2 focus:ring-offset-2`
- **Loading States**: `animate-pulse` for skeleton loading, `animate-spin` for spinners
- **Group Variants**: `group-hover:`, `group-focus:` for parent-triggered styling

### Performance Optimization

- **Content Detection**: Configure paths in `tailwind.config.js`
- **JIT Mode**: Enabled by default, generates classes on-demand
- **Purge Unused**: Automatic in production builds
- **Component Extraction**: Use `@apply` sparingly for true reusability
- **Bundle Analysis**: Monitor CSS output size

### Accessibility Guidelines

- **Color Contrast**: Ensure WCAG AA compliance (4.5:1 minimum)
- **Focus Management**: Never remove focus outlines, style them instead
- **Touch Targets**: Minimum 44x44px for interactive elements
- **Screen Reader**: Use semantic HTML with Tailwind styling
- **Motion Preference**: Respect `prefers-reduced-motion` in animations

## Tailwind v4.0 Migration Notes

### New Features (Beta)

- CSS-first configuration with `@theme` directive
- Improved performance and smaller bundle sizes
- Better TypeScript integration
- Enhanced arbitrary value support
- New container queries support

### Migration Considerations

- JavaScript config becomes CSS-based
- Some class names may change
- Plugin API updates
- Build tool integration changes

## Usage Example

```
/context-load-tailwind
```

This will load comprehensive Tailwind CSS documentation and best practices into the current context for immediate styling guidance.
