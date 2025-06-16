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
   - Styling with Tailwind

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
- Styling with Tailwind CSS
- Optimizing performance
- Testing Fresh applications
- Deploying to production

## Usage Example

```
/context-load-deno-fresh
```
