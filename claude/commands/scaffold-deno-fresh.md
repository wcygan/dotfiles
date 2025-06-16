# /scaffold-deno-fresh

Creates a new server-side rendered web application for $ARGUMENT using Deno Fresh 2 framework with islands architecture and zero build step development.

## What it does

1. Creates a new directory with the specified project name
2. Uses Fresh 2's official initializer to generate the project structure
3. Sets up routes with server-side rendering capabilities
4. Creates interactive islands for client-side functionality
5. Configures deno.json with development and build tasks
6. Runs the development server to verify setup

## Example

```
/scaffold-deno-fresh my-fresh-app
```

This creates a production-ready Fresh 2 web application with:

- Server-side rendering with Preact
- Islands architecture for selective hydration
- File-based routing system with improved performance
- TypeScript support out of the box
- Hot reloading development server
- Zero build step development experience
- Optimized production builds
- Fresh 2's enhanced developer experience and performance improvements

## Important Notes

- Uses Fresh 2 which provides significant performance improvements and better developer experience
- Fresh 2 maintains backward compatibility while offering enhanced features
- Automatically includes the latest Fresh 2 patterns and best practices
