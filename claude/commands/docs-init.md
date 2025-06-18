# /docs-init

Initializes a Docusaurus documentation site in the `/docs` folder and integrates with project's Deno lifecycle harness.

## Usage

```bash
/docs-init [$ARGUMENTS]
```

## Context-Aware Behavior

The command intelligently detects existing documentation and project context:

- **No `/docs` folder exists**: Creates new Docusaurus site with auto-detected project name
- **Empty `/docs` folder**: Initializes Docusaurus in existing folder
- **Existing documentation**: Prompts before overwriting (or skips if already properly configured)
- **Project type detection**: Automatically configures based on `deno.json`, `Cargo.toml`, `go.mod`, etc.
- **Diagram support**: Enables Mermaid diagrams if `$ARGUMENTS` contains "diagrams" or project has existing diagram files

## Description

Creates a complete Docusaurus documentation site in the `/docs` folder with automatic integration into the project's Deno task lifecycle. The command follows docs-as-code principles and sets up a foundation for automated documentation workflows.

### What it creates:

#### 1. Docusaurus Project Structure (`/docs`)

**Core Files:**

- `package.json` - Docusaurus dependencies and npm scripts
- `docusaurus.config.ts` - Site configuration with auto-detected project info and Mermaid support
- `sidebar.js` - Auto-generated sidebar configuration
- `docs/intro.md` - Generated introduction page with project overview
- `docs/api/` - Placeholder for API documentation
- `static/img/` - Static assets directory
- `src/pages/index.tsx` - Simplified homepage without marketing components

**Content Generation:**

- Auto-detects project name from `deno.json`, `package.json`, or directory name
- Generates project description from README.md if available
- Creates initial documentation structure based on project type detection
- Sets up proper meta tags and site configuration
- Reviews and updates `docusaurus.config.ts` with project-relevant information:
  - Corrects project name, organization, and repository URLs
  - Sets appropriate tagline based on project description
  - Configures deployment URL based on project hosting
  - Updates theme colors and branding to match project

#### 2. Deno Integration (`/deno.json` in project root)

Automatically adds a `docs` task to the project's `deno.json`:

```json
{
  "tasks": {
    "docs": "cd docs && npm run start",
    "docs:build": "cd docs && npm run build",
    "docs:serve": "cd docs && npm run serve"
  }
}
```

**Integration Benefits:**

- Single entry point: `deno task docs` starts documentation server
- Consistent with project lifecycle pattern
- Automatic directory navigation handled by Deno tasks
- Supports build and serve commands for production deployment

#### 3. Enhanced Features

**Mermaid Diagram Support (enabled by default):**

```typescript
// Automatically configured in docusaurus.config.ts
import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  markdown: {
    mermaid: true,
  },
  themes: ["@docusaurus/theme-mermaid"],
  // Additional configuration...
};
```

**AI-Enhanced Template (with --template=ai-enhanced):**

- Includes Docusaurus AI chatbot integration
- Pre-configured sitemap generation for AI context
- Enhanced search capabilities
- Interactive documentation features

### Project Type Detection

**Automatic Configuration Based on Project Structure:**

**Go Projects** (presence of `go.mod`):

- Sets up API documentation structure for REST/gRPC services
- Configures code block syntax highlighting for Go
- Creates sections for package documentation

**Rust Projects** (presence of `Cargo.toml`):

- Configures for crate documentation integration
- Sets up API reference structure
- Includes performance and safety documentation templates

**Deno/Node Projects** (presence of `deno.json`/`package.json`):

- Configures for TypeScript/JavaScript syntax highlighting
- Sets up module and API documentation structure
- Includes deployment and npm/JSR publishing guides

**Java Projects** (presence of `pom.xml`/`build.gradle`):

- Configures for Spring Boot/Quarkus documentation patterns
- Sets up API documentation with OpenAPI integration
- Includes deployment and container documentation

### Configuration Files Generated

#### `docusaurus.config.ts`

```typescript
import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "{PROJECT_NAME}",
  tagline: "{AUTO_DETECTED_DESCRIPTION}",
  favicon: "img/favicon.ico",
  url: "https://{PROJECT_NAME}.github.io",
  baseUrl: "/",
  organizationName: "{GITHUB_ORG}",
  projectName: "{PROJECT_NAME}",

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.js",
          editUrl: "https://github.com/{ORG}/{REPO}/tree/main/docs/",
        },
        blog: false, // Disabled by default for technical docs
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  markdown: {
    mermaid: true,
  },
  themes: ["@docusaurus/theme-mermaid"],

  themeConfig: {
    navbar: {
      title: "{PROJECT_NAME}",
      logo: {
        alt: "{PROJECT_NAME} Logo",
        src: "img/logo.svg",
      },
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "Documentation",
        },
        {
          href: "https://github.com/{ORG}/{REPO}",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Docs",
          items: [
            {
              label: "Getting Started",
              to: "/docs/intro",
            },
          ],
        },
        {
          title: "More",
          items: [
            {
              label: "GitHub",
              href: "https://github.com/{ORG}/{REPO}",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} {PROJECT_NAME}. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    mermaid: {
      theme: { light: "neutral", dark: "forest" },
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
```

#### Homepage Customization

The command creates a simplified homepage (`src/pages/index.tsx`) focused on documentation:

```tsx
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import styles from "./index.module.css";

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} Documentation`}
      description="{PROJECT_NAME} documentation and API reference"
    >
      <header className={clsx("hero hero--primary", styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro"
            >
              View Documentation →
            </Link>
          </div>
        </div>
      </header>
    </Layout>
  );
}
```

**Homepage Features:**

- Clean, documentation-focused design without marketing elements
- Proper page metadata with project description
- Single call-to-action button linking to documentation
- No HomepageFeatures component or promotional sections

#### Generated Content Structure

```markdown
docs/
├── intro.md # Project overview and introduction
├── api/ # API documentation
│ ├── overview.md
│ └── reference.md
├── guides/ # How-to guides and tutorials
│ ├── configuration.md
│ └── deployment.md
└── reference/ # Technical reference
├── cli.md
└── troubleshooting.md
```

**Note:** The command automatically cleans up default Docusaurus files:

- Removes `docs/tutorial-basics/` directory
- Removes `docs/tutorial-extras/` directory
- Removes `docs/getting-started.md` (replaced with project-specific content)
- Removes `src/components/HomepageFeatures` component with marketing sections
- Simplifies `src/pages/index.tsx` to show only title, tagline, and "View Documentation →" button

### Integration Features

**GitHub Integration:**

- Auto-detects GitHub repository from git remote
- Configures edit links to GitHub source
- Sets up GitHub Pages deployment configuration

**Git Hooks Support:**

- Creates `.gitignore` for Docusaurus build artifacts
- Optional pre-commit hooks for documentation validation
- Automatic sidebar regeneration on file changes

**CI/CD Ready:**

- Generates GitHub Actions workflow for automatic deployment
- Configures build scripts for production deployment
- Sets up proper caching for npm dependencies

## Examples

### Initialize with context detection:

```bash
/docs-init
```

### Initialize with specific project name:

```bash
/docs-init my-awesome-project
```

### Initialize with automatic Mermaid support:

```bash
/docs-init
```

Note: Mermaid diagram support is now enabled by default for all new documentation sites.

### Force re-initialization:

```bash
/docs-init force
```

## Integration with Other Commands

- Use `/docs-update` after initialization to populate content
- Combine with `/docs-add` to create new documentation sections
- Use with `/ci-gen` to set up automated documentation deployment
- Integrate with `/api-docs` for automatic API documentation generation

## Prerequisites

- Node.js 18+ (for Docusaurus 3.0+)
- npm or yarn package manager
- Git repository (for GitHub integration features)
- Project must have `deno.json` in root for Deno task integration

## Post-Installation

After running `/docs-init`, you can:

1. **Start documentation server:**
   ```bash
   deno task docs
   ```

2. **Build for production:**
   ```bash
   deno task docs:build
   ```

3. **Add new content:**
   ```bash
   /docs-add guide "How to Deploy"
   ```

4. **Update existing docs:**
   ```bash
   /docs-update --source=codebase
   ```
