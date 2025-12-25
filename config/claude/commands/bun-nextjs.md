---
description: Set up Next.js project with Bun runtime, optionally with Drizzle ORM
---

Set up a modern Next.js project using **Bun** as the package manager and runtime, with optional **Drizzle ORM** integration for type-safe database access. Also installs the **frontend-design** Claude skill for creating distinctive, production-grade UI.

**Step 1: Gather Project Information**

Ask the user (or infer from context):
1. **Project name**: kebab-case preferred (e.g., `my-app`)
2. **Database integration**: Include Drizzle ORM? (SQLite, PostgreSQL, or MySQL)
3. **Styling**: Tailwind CSS (default), or other preference
4. **Source directory**: Use `src/` directory? (recommended: yes)

**Step 2: Create Next.js App with Bun**

```bash
bun create next-app@latest <project-name>
cd <project-name>
```

During interactive prompts, recommend:
- TypeScript: **Yes**
- ESLint: **Yes**
- Tailwind CSS: **Yes**
- `src/` directory: **Yes**
- App Router: **Yes**
- Import alias: **@/***

**Step 3: Update package.json for Bun Runtime**

Replace the scripts section to use Bun's runtime explicitly:

```json
{
  "scripts": {
    "dev": "bun --bun next dev",
    "build": "bun --bun next build",
    "start": "bun --bun next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "typecheck": "tsc --noEmit"
  }
}
```

**Step 4: Create justfile**

```just
# Next.js with Bun

set shell := ["bash", "-cu"]

# List available recipes
default:
    @just --list

# ─── DEVELOPMENT ──────────────────────────────────────────────────────────────

# Start development server
dev:
    bun --bun next dev

# Start dev server on specific port
dev-port port="3000":
    bun --bun next dev -p {{ port }}

# ─── BUILD ────────────────────────────────────────────────────────────────────

# Build for production
build:
    bun --bun next build

# Start production server
start:
    bun --bun next start

# Analyze bundle size
analyze:
    ANALYZE=true bun --bun next build

# ─── CODE QUALITY ─────────────────────────────────────────────────────────────

# Run ESLint
lint:
    bun next lint

# Fix ESLint issues
lint-fix:
    bun next lint --fix

# Type check
typecheck:
    bun tsc --noEmit

# Run all checks
check: lint typecheck

# ─── DEPENDENCIES ─────────────────────────────────────────────────────────────

# Install dependencies
install:
    bun install

# Update dependencies
update:
    bun update

# Add a package
add *PACKAGES:
    bun add {{ PACKAGES }}

# Add a dev package
add-dev *PACKAGES:
    bun add -D {{ PACKAGES }}

# ─── MAINTENANCE ──────────────────────────────────────────────────────────────

# Clean build artifacts
clean:
    rm -rf .next out node_modules/.cache

# Full clean (including node_modules)
clean-all: clean
    rm -rf node_modules bun.lockb

# Reinstall from scratch
reinstall: clean-all install
```

---

## WITH DRIZZLE ORM (Optional - Only if Requested)

If the user requests database integration, add Drizzle ORM:

**Step 5a: Install Drizzle Dependencies**

For SQLite (simplest, uses Bun's built-in driver):
```bash
bun add drizzle-orm
bun add -D drizzle-kit
```

For PostgreSQL:
```bash
bun add drizzle-orm postgres
bun add -D drizzle-kit
```

For MySQL:
```bash
bun add drizzle-orm mysql2
bun add -D drizzle-kit
```

**Step 5b: Create Database Layer**

Create `db/` directory structure:

```
src/
├── db/
│   ├── index.ts      # Database connection
│   ├── schema.ts     # Table definitions
│   └── migrate.ts    # Migration runner
```

**SQLite Configuration** (`src/db/index.ts`):
```typescript
import { drizzle } from "drizzle-orm/bun-sqlite";
import { Database } from "bun:sqlite";
import * as schema from "./schema";

const sqlite = new Database("sqlite.db");
export const db = drizzle(sqlite, { schema });
```

**PostgreSQL Configuration** (`src/db/index.ts`):
```typescript
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "./schema";

const connectionString = process.env.DATABASE_URL!;
const client = postgres(connectionString);
export const db = drizzle(client, { schema });
```

**Step 5c: Create Schema** (`src/db/schema.ts`):

For SQLite:
```typescript
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  createdAt: integer("created_at", { mode: "timestamp" })
    .$defaultFn(() => new Date()),
});

export const posts = sqliteTable("posts", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  title: text("title").notNull(),
  content: text("content"),
  authorId: integer("author_id")
    .notNull()
    .references(() => users.id),
  createdAt: integer("created_at", { mode: "timestamp" })
    .$defaultFn(() => new Date()),
});
```

For PostgreSQL:
```typescript
import { pgTable, serial, text, timestamp, integer } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content"),
  authorId: integer("author_id")
    .notNull()
    .references(() => users.id),
  createdAt: timestamp("created_at").defaultNow(),
});
```

**Step 5d: Create Migration Runner** (`src/db/migrate.ts`):

For SQLite:
```typescript
import { migrate } from "drizzle-orm/bun-sqlite/migrator";
import { drizzle } from "drizzle-orm/bun-sqlite";
import { Database } from "bun:sqlite";

const sqlite = new Database("sqlite.db");
const db = drizzle(sqlite);

console.log("Running migrations...");
migrate(db, { migrationsFolder: "./drizzle" });
console.log("Migrations complete!");
```

For PostgreSQL:
```typescript
import { migrate } from "drizzle-orm/postgres-js/migrator";
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

const connectionString = process.env.DATABASE_URL!;
const client = postgres(connectionString, { max: 1 });
const db = drizzle(client);

console.log("Running migrations...");
await migrate(db, { migrationsFolder: "./drizzle" });
console.log("Migrations complete!");
await client.end();
```

**Step 5e: Create drizzle.config.ts**:

For SQLite:
```typescript
import type { Config } from "drizzle-kit";

export default {
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dialect: "sqlite",
  dbCredentials: {
    url: "sqlite.db",
  },
} satisfies Config;
```

For PostgreSQL:
```typescript
import type { Config } from "drizzle-kit";

export default {
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
} satisfies Config;
```

**Step 5f: Update package.json Scripts**

Add database scripts:
```json
{
  "scripts": {
    "dev": "bun --bun next dev",
    "build": "bun --bun next build",
    "start": "bun --bun next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "typecheck": "tsc --noEmit",
    "db:generate": "bunx drizzle-kit generate",
    "db:migrate": "bun run src/db/migrate.ts",
    "db:push": "bunx drizzle-kit push",
    "db:studio": "bunx drizzle-kit studio"
  }
}
```

**Step 5g: Update justfile with Database Commands**

Add to justfile:
```just
# ─── DATABASE ─────────────────────────────────────────────────────────────────

# Generate migration from schema changes
db-generate:
    bunx drizzle-kit generate

# Run pending migrations
db-migrate:
    bun run src/db/migrate.ts

# Push schema directly (dev only, no migration files)
db-push:
    bunx drizzle-kit push

# Open Drizzle Studio (database GUI)
db-studio:
    bunx drizzle-kit studio

# Seed database with test data
db-seed:
    bun run src/db/seed.ts
```

**Step 5h: Example Server Action** (`src/app/actions.ts`):

```typescript
"use server";

import { db } from "@/db";
import { users, posts } from "@/db/schema";
import { eq } from "drizzle-orm";
import { revalidatePath } from "next/cache";

export async function getUsers() {
  return db.select().from(users);
}

export async function createUser(name: string, email: string) {
  const result = await db.insert(users).values({ name, email }).returning();
  revalidatePath("/");
  return result[0];
}

export async function getUserPosts(userId: number) {
  return db
    .select()
    .from(posts)
    .where(eq(posts.authorId, userId));
}
```

**Step 5i: Update .gitignore**

Add database-specific ignores:
```gitignore
# Database
*.db
*.db-journal
*.db-wal
*.db-shm

# Drizzle
drizzle/meta/

# Environment
.env*.local
```

**Step 5j: Create .env.local Template**

For PostgreSQL/MySQL, create `.env.local`:
```bash
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

---

## Project Structure Summary

**Without Drizzle:**
```
project-name/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   └── components/
├── public/
├── justfile
├── next.config.ts
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

**With Drizzle:**
```
project-name/
├── src/
│   ├── app/
│   │   ├── actions.ts      # Server actions
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   └── db/
│       ├── index.ts        # Connection
│       ├── schema.ts       # Tables
│       ├── migrate.ts      # Migration runner
│       └── seed.ts         # Optional seed data
├── drizzle/                 # Generated migrations
├── public/
├── justfile
├── drizzle.config.ts
├── next.config.ts
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

---

## Available Commands Summary

| Command | Description |
|---------|-------------|
| `just dev` | Start development server |
| `just build` | Build for production |
| `just start` | Start production server |
| `just lint` | Run ESLint |
| `just typecheck` | TypeScript type check |
| `just check` | All quality checks |

**With Drizzle:**

| Command | Description |
|---------|-------------|
| `just db-generate` | Generate migrations from schema |
| `just db-migrate` | Run pending migrations |
| `just db-push` | Push schema directly (dev) |
| `just db-studio` | Open database GUI |

---

## Key Design Decisions

1. **`bun --bun` flag**: Explicitly uses Bun runtime instead of Node.js for better performance
2. **App Router**: Modern Next.js routing with React Server Components
3. **Server Actions**: Type-safe mutations without API routes boilerplate
4. **SQLite default**: Zero-config database for development; swap to Postgres for production
5. **`bun:sqlite`**: Native Bun module, no external dependencies
6. **justfile**: Cross-platform task runner with clear command documentation

---

## After Setup

1. Start development: `just dev`
2. Open browser: `http://localhost:3000`
3. Edit `src/app/page.tsx` to see hot reload

**With Drizzle:**
1. Define tables in `src/db/schema.ts`
2. Generate migration: `just db-generate`
3. Run migration: `just db-migrate`
4. Use `db` in Server Components/Actions

---

## Deployment Notes

**Vercel** (recommended):
- Works out of the box
- Set `DATABASE_URL` in environment variables for Drizzle

**Self-hosted with Bun:**
```bash
bun --bun next build
bun --bun next start
```

**Docker:**
```dockerfile
FROM oven/bun:1 AS base
WORKDIR /app

FROM base AS deps
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN bun --bun next build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["bun", "server.js"]
```

**Note:** For standalone Docker output, add to `next.config.ts`:
```typescript
const nextConfig = {
  output: "standalone",
};
```

---

## FRONTEND DESIGN SKILL (Always Installed)

The command automatically installs a Claude skill for creating distinctive, production-grade frontend interfaces.

**Step 6: Create Skill Directory**

```bash
mkdir -p .claude/skills/frontend-design
```

**Step 7: Create SKILL.md**

Create `.claude/skills/frontend-design/SKILL.md`:

```markdown
---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics. Keywords: frontend, UI, component, page, design, interface, React, Next.js, Tailwind
---

# Frontend Design Skill

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## When This Skill Activates

- User asks to build a component, page, or interface
- User requests UI/UX improvements
- User mentions design, styling, or visual elements
- User wants to create forms, dashboards, landing pages, etc.

## Design Thinking Process

Before coding, understand context and commit to a **BOLD** aesthetic direction:

### 1. Purpose Analysis
- What problem does this interface solve?
- Who is the target audience?
- What emotions should it evoke?

### 2. Aesthetic Direction
Pick an extreme and commit fully. Options include:
- **Brutally minimal**: Stark, functional, Swiss design influence
- **Maximalist chaos**: Dense, layered, information-rich
- **Retro-futuristic**: 80s/90s computing meets modern
- **Organic/natural**: Soft edges, earth tones, flowing shapes
- **Luxury/refined**: High contrast, elegant typography, restrained palette
- **Playful/toy-like**: Rounded, colorful, bouncy animations
- **Editorial/magazine**: Grid-based, typographic hierarchy, whitespace
- **Brutalist/raw**: Exposed structure, monospace, harsh contrasts
- **Art deco/geometric**: Bold patterns, metallic accents, symmetry
- **Soft/pastel**: Gentle gradients, dreamy, light
- **Industrial/utilitarian**: Function-first, technical, purposeful

### 3. Differentiation Question
Ask: "What's the ONE thing someone will remember about this interface?"

## Implementation Standards

### Typography
**NEVER use**: Inter, Roboto, Arial, system fonts, or other generic choices

**DO use distinctive fonts from Google Fonts or Fontsource**:
- Display: Playfair Display, Bebas Neue, Archivo Black, Space Grotesk, Syne
- Body: Source Serif Pro, Crimson Text, IBM Plex Sans, DM Sans
- Monospace: JetBrains Mono, Fira Code, IBM Plex Mono

Install via Bun:
\`\`\`bash
bun add @fontsource/playfair-display @fontsource/dm-sans
\`\`\`

Or use Next.js font optimization:
\`\`\`typescript
import { Playfair_Display, DM_Sans } from 'next/font/google'

const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-display' })
const dmSans = DM_Sans({ subsets: ['latin'], variable: '--font-body' })
\`\`\`

### Color & Theme
- Use CSS variables for consistency
- Dominant colors with sharp accents outperform timid, evenly-distributed palettes
- Commit to light OR dark theme per component (not wishy-washy neutrals)

Example Tailwind config extension:
\`\`\`typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        canvas: '#0a0a0a',
        ink: '#fafafa', 
        accent: '#ff3366',
        muted: '#666666',
      },
      fontFamily: {
        display: ['var(--font-display)', 'serif'],
        body: ['var(--font-body)', 'sans-serif'],
      },
    },
  },
}
\`\`\`

### Motion & Animation
Prioritize high-impact moments:
- **Page load**: Staggered reveals with animation-delay
- **Scroll-triggered**: Elements that respond to viewport entry
- **Hover states**: Surprising, delightful interactions

Use Tailwind's animation utilities or Motion library:
\`\`\`bash
bun add motion
\`\`\`

\`\`\`tsx
import { motion } from 'motion/react'

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: 'easeOut' }}
>
  Content
</motion.div>
\`\`\`

### Spatial Composition
Break expectations:
- Asymmetric layouts
- Overlapping elements
- Diagonal flow
- Grid-breaking hero sections
- Generous negative space OR controlled density (pick one)

### Backgrounds & Visual Details
Create atmosphere:
- Gradient meshes
- Noise textures (use CSS or SVG filters)
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Grain overlays

\`\`\`css
/* Noise texture overlay */
.noise::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
}
\`\`\`

## Anti-Patterns to Avoid

**NEVER create**:
- Purple gradients on white backgrounds (overused AI aesthetic)
- Generic card layouts with rounded corners and subtle shadows
- Predictable hero → features → testimonials → CTA structure
- Cookie-cutter component libraries without customization
- Safe, inoffensive color schemes that blend together
- Uniform spacing that creates visual monotony

## Project Integration

### File Structure
Place components in the existing project structure:
\`\`\`
src/
├── app/
│   └── page.tsx          # Main pages
├── components/
│   ├── ui/               # Base UI components
│   └── [feature]/        # Feature-specific components
└── styles/
    └── globals.css       # Global styles, CSS variables
\`\`\`

### Tailwind Integration
Extend globals.css for custom utilities:
\`\`\`css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --radius: 0.5rem;
  }
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
\`\`\`

## Output Requirements

When creating interfaces:
1. **Working code**: Functional React/Next.js components
2. **TypeScript**: Proper types for all props
3. **Responsive**: Mobile-first with breakpoint considerations
4. **Accessible**: Semantic HTML, ARIA where needed
5. **Memorable**: At least ONE distinctive visual element

## Example Prompt Handling

User: "Create a pricing page"

Response approach:
1. Don't create generic 3-column pricing cards
2. Choose an aesthetic (e.g., editorial/magazine style)
3. Make pricing tiers visually distinct through layout, not just color
4. Add unexpected elements: animated accents, typographic flourishes
5. Ensure the page is memorable and photographable
```

**Step 8: Create Reference Documentation**

Create `.claude/skills/frontend-design/REFERENCE.md`:

```markdown
# Frontend Design Reference

## Font Pairing Recommendations

### Elegant/Refined
- Display: Playfair Display
- Body: Source Serif Pro

### Modern/Technical
- Display: Space Grotesk
- Body: IBM Plex Sans

### Bold/Impactful
- Display: Bebas Neue
- Body: DM Sans

### Editorial/Magazine
- Display: Syne
- Body: Crimson Text

## Color Palette Starters

### Dark Mode Luxe
\`\`\`css
--bg: #0a0a0a;
--fg: #fafafa;
--accent: #d4af37;
--muted: #525252;
\`\`\`

### Light Brutalist
\`\`\`css
--bg: #ffffff;
--fg: #000000;
--accent: #ff0000;
--muted: #888888;
\`\`\`

### Soft Organic
\`\`\`css
--bg: #f5f0eb;
--fg: #2d2a26;
--accent: #8b7355;
--muted: #a39b8f;
\`\`\`

### Retro Computing
\`\`\`css
--bg: #1a1a2e;
--fg: #00ff41;
--accent: #ff00ff;
--muted: #4a4a6a;
\`\`\`

## Animation Presets

### Stagger Children
\`\`\`tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}
\`\`\`

### Smooth Reveal
\`\`\`tsx
const reveal = {
  initial: { opacity: 0, y: 40 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] }
}
\`\`\`

### Hover Lift
\`\`\`css
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -8px rgba(0,0,0,0.2);
}
\`\`\`

## Tailwind Utilities Cookbook

### Gradient Text
\`\`\`tsx
<span className="bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
  Gradient Text
</span>
\`\`\`

### Glass Effect
\`\`\`tsx
<div className="backdrop-blur-md bg-white/10 border border-white/20 rounded-2xl">
  Glass panel
</div>
\`\`\`

### Animated Border
\`\`\`tsx
<div className="relative">
  <div className="absolute -inset-0.5 bg-gradient-to-r from-pink-600 to-purple-600 rounded-lg blur opacity-75 group-hover:opacity-100 transition duration-1000 group-hover:duration-200 animate-tilt" />
  <div className="relative bg-black rounded-lg p-6">
    Content
  </div>
</div>
\`\`\`
```

---

## Final Project Structure

**Complete structure with all options:**
```
project-name/
├── .claude/
│   └── skills/
│       └── frontend-design/
│           ├── SKILL.md        # Design skill instructions
│           └── REFERENCE.md    # Font pairings, palettes, animations
├── src/
│   ├── app/
│   │   ├── actions.ts          # Server actions (with Drizzle)
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   └── ui/                 # UI components
│   └── db/                     # (with Drizzle)
│       ├── index.ts
│       ├── schema.ts
│       └── migrate.ts
├── drizzle/                    # (with Drizzle)
├── public/
├── justfile
├── drizzle.config.ts           # (with Drizzle)
├── next.config.ts
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

---

## Skill Usage

After setup, the frontend-design skill activates automatically when you ask Claude to:
- "Create a landing page for..."
- "Build a dashboard component"
- "Design a pricing section"
- "Make a hero section with..."

Claude will follow the design thinking process and create distinctive, production-grade interfaces that avoid generic AI aesthetics.
