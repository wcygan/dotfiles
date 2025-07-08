---
allowed-tools: Bash(pwd:*), Bash(basename:*), Bash(git config:*), Bash(npx create-docusaurus:*), Bash(npm install:*), Bash(npm run:*), Write, MultiEdit, Read
description: Scaffold a minimal Docusaurus documentation site with TypeScript and diagram support
---

## Context

- Current directory: !`pwd`
- Project name (from git remote): !`basename -s .git "$(git config --get remote.origin.url 2>/dev/null)" || echo "my-docs"`
- Node.js version: !`node --version 2>/dev/null || echo "Node.js not installed"`
- npm version: !`npm --version 2>/dev/null || echo "npm not installed"`

## Your task

Create a minimal Docusaurus documentation site in `/docs/` folder with TypeScript support and diagram capabilities.

### Step 1: Validate environment

Check that Node.js and npm are installed. If not, inform the user they need to install Node.js first.

### Step 2: Create Docusaurus project

Use npx to create a new Docusaurus project with TypeScript:

```bash
npx create-docusaurus@latest docs classic --typescript
```

Note: Use "docs" as the directory name to match the dotfiles convention.

### Step 3: Set up the minimal configuration

After project creation, update the key configuration files to match the minimal setup:

1. **Update docusaurus.config.ts** with:
   - Simple title and tagline
   - GitHub Pages configuration (if git remote exists)
   - Classic preset with minimal navbar
   - Dark mode by default
   - Syntax highlighting for common languages (bash, typescript, rust, go, java)
   - No blog (set blog: false)

2. **Simplify sidebars.ts** to have a basic structure:
   - getting-started/
   - configuration/
   - reference/

3. **Update package.json** scripts to include standard commands:
   - start, build, serve, deploy, typecheck

### Step 4: Install and configure diagram support

Install the Mermaid diagram plugin:

```bash
cd docs && npm install --save @docusaurus/theme-mermaid
```

Then update docusaurus.config.ts to include:

- Import the mermaid theme
- Add markdown.mermaid = true
- Configure the theme with mermaid support

### Step 5: Create minimal starter content

Create the basic documentation structure:

1. **docs/getting-started/installation.md** - Basic installation guide
2. **docs/getting-started/quick-start.md** - Quick start guide
3. **docs/configuration/index.md** - Configuration overview
4. **docs/reference/index.md** - Reference documentation

Each file should have proper frontmatter with sidebar_position.

### Step 6: Customize the homepage

1. Update src/pages/index.tsx with a simple hero section
2. Create src/components/HomepageFeatures.tsx with 2-3 key features
3. Update src/css/custom.css with minimal styling

### Step 7: Add TypeScript configuration

Ensure tsconfig.json is properly configured for Docusaurus development.

### Step 8: Initialize git (if not in a git repo)

If the current directory is not a git repository, initialize one:

```bash
cd docs && git init
```

### Step 9: Configure Deno tasks for documentation

Update or create `deno.json` in the project root to include documentation tasks:

```json
{
  "tasks": {
    "docs": "cd docs && npm start",
    "docs:dev": "cd docs && npm start",
    "docs:build": "cd docs && npm run build",
    "docs:serve": "cd docs && npm run serve",
    "docs:deploy": "cd docs && npm run deploy",
    "docs:install": "cd docs && npm install"
  }
}
```

This allows you to run documentation commands using Deno:

- `deno task docs` - Start the development server
- `deno task docs:build` - Build the static site
- `deno task docs:serve` - Serve the built site locally
- `deno task docs:deploy` - Deploy to GitHub Pages

### Step 10: Final setup instructions

Provide the user with:

1. Commands to start the development server: `deno task docs` or `cd docs && npm start`
2. Build command: `deno task docs:build` or `cd docs && npm run build`
3. Deployment instructions for GitHub Pages
4. How to use Mermaid diagrams in markdown files

### Example Mermaid diagram usage:

````markdown
```mermaid
graph TD;
    A[Start] --> B{Is it Working?};
    B -->|Yes| C[Great!];
    B -->|No| D[Debug];
    D --> A;
```
````

The site should be minimal, clean, and ready for documentation with full TypeScript support and diagram capabilities.
