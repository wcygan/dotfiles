# /context-load-deno-fresh

Load comprehensive documentation context for Deno Fresh web framework development.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Fresh Documentation**: `https://fresh.deno.dev/docs/`
     - Focus on: islands architecture, routing, server-side rendering
   - **Preact Guide**: `https://preactjs.com/guide/v10/getting-started`
     - Focus on: components, hooks, signals, performance
   - **Tailwind CSS**: `https://tailwindcss.com/docs`
     - Focus on: utility classes, responsive design, customization
   - **Fresh Tailwind Integration**: `https://fresh.deno.dev/docs/concepts/styling`
     - Focus on: plugin setup, configuration, migration from Twind
   - **Deno Deploy**: `https://docs.deno.com/deploy/`
     - Focus on: deployment, edge functions, KV storage
   - **Fresh Examples**: `https://github.com/denoland/fresh/tree/main/examples`
     - Focus on: practical implementations, patterns

3. **Key documentation sections to prioritize**:
   - Islands architecture concepts
   - File-based routing system
   - Server-side rendering
   - Client-side hydration
   - Signal-based state management
   - Styling with Tailwind CSS plugin
   - Tailwind configuration and optimization
   - Migration from Twind to Tailwind CSS

4. **Focus areas for this stack**:
   - Zero-config TypeScript setup
   - Islands architecture benefits
   - File-based routing patterns
   - Component composition
   - State management with signals
   - Styling strategies
   - Performance optimization
   - Deployment to Deno Deploy

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Building Fresh applications
- Implementing islands architecture
- Creating reusable components
- Managing application state
- Styling with Tailwind CSS plugin (Fresh 1.6+)
- Configuring Tailwind with ahead-of-time builds
- Migrating from Twind to Tailwind CSS
- Fresh 2.0 alpha features and timeline
- Optimizing performance
- Testing Fresh applications
- Deploying to production

## Fresh Version Notes

- **Fresh 1.6+**: Stable with official Tailwind CSS plugin support
- **Fresh 2.0 Alpha**: Available now with built-in Tailwind option during init
- **Fresh 2.0 Stable**: Expected late Q3 2025 (September)

## Modern UI Design Best Practices

### Typography System

- **Font Stack**: Use system fonts for performance: `font-sans` (Tailwind default)
- **Size Hierarchy**: Limit to 4-5 sizes max (text-sm, text-base, text-lg, text-xl, text-2xl)
- **Line Height**: Use `leading-relaxed` (1.625) for body text
- **Font Weight**: Utilize full range (font-light to font-bold) for hierarchy
- **Reading Length**: Target 50-75 characters per line with `max-w-prose`

### Color System

- **60-30-10 Rule**:
  - 60% dominant color (backgrounds, surfaces)
  - 30% secondary color (cards, sections)
  - 10% accent color (CTAs, highlights)
- **Semantic Colors**: Use Tailwind's semantic naming:
  - `bg-slate-50/100/200` for neutral surfaces
  - `text-slate-600/700/800/900` for text hierarchy
  - `bg-blue-500` for primary actions
  - `bg-green-500` for success states
  - `bg-red-500` for errors/destructive actions
- **Dark Mode**: Use Tailwind's `dark:` variant for all color choices

### Spacing & Layout

- **8-Point Grid**: Use Tailwind's spacing scale (space-2, space-4, space-8)
- **Container**: Use `container mx-auto px-4` for consistent margins
- **Section Spacing**: `py-16 md:py-24` for major sections
- **Component Spacing**: `space-y-4` or `space-y-6` for vertical rhythm
- **Card Padding**: `p-6` for medium density, `p-8` for spacious feel

### Component Patterns

- **Cards**: `bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700`
- **Buttons**:
  - Primary: `bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md transition-colors`
  - Secondary: `bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-700 dark:hover:bg-slate-600`
- **Forms**: `border border-slate-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent`
- **Navigation**: `backdrop-blur-sm bg-white/80 dark:bg-slate-900/80 border-b border-slate-200 dark:border-slate-800`

### Animation & Interaction

- **Transitions**: Always add `transition-all duration-200` for smooth interactions
- **Hover States**: Use scale, shadow, or color changes: `hover:scale-105 hover:shadow-lg`
- **Focus States**: Ensure visible focus rings: `focus:ring-2 focus:ring-offset-2`
- **Loading States**: Use `animate-pulse` or `animate-spin` for feedback

### Responsive Design

- **Mobile-First**: Start with mobile styles, add desktop with `md:` and `lg:`
- **Breakpoint Usage**:
  - `sm:` (640px) - Large phones
  - `md:` (768px) - Tablets
  - `lg:` (1024px) - Desktops
  - `xl:` (1280px) - Large screens
- **Common Patterns**:
  - Grid: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`
  - Flex: `flex flex-col md:flex-row gap-4`
  - Text: `text-3xl md:text-4xl lg:text-5xl`

### Accessibility

- **Color Contrast**: Ensure WCAG AA compliance (4.5:1 for normal text)
- **Focus Indicators**: Never remove focus outlines, style them instead
- **Interactive Sizing**: Minimum 44x44px touch targets
- **Semantic HTML**: Use proper heading hierarchy and ARIA labels

### Performance Patterns

- **Purge CSS**: Fresh's Tailwind plugin handles this automatically
- **Component Extraction**: Use `@apply` sparingly for truly reusable patterns
- **Islands Architecture**: Keep interactive components minimal for hydration
- **Image Optimization**: Use Fresh's built-in image optimization

## Usage Example

```
/context-load-deno-fresh
```
