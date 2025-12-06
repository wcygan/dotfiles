---
description: Create Mermaid diagram from user request, render to PNG
---

Create a Mermaid diagram based on the user's request.

**Input:** $ARGUMENTS (description of what to visualize)

**Workflow:**

1. **Setup directories** (if they don't exist):
   ```bash
   mkdir -p diagrams/rendered
   ```

2. **Ensure .gitignore excludes rendered output**:
   - Check if `diagrams/rendered` is in `.gitignore`
   - If not, add it (rendered PNGs shouldn't be version controlled)

3. **Create the Mermaid source file**:
   - Filename: `diagrams/{descriptive-name}.mmd`
   - Use kebab-case for filename based on diagram content
   - Write valid Mermaid syntax

4. **Choose appropriate diagram type** based on request:
   - **flowchart/graph**: Process flows, decision trees, workflows
   - **sequenceDiagram**: API calls, message passing, interactions
   - **classDiagram**: OOP structures, relationships
   - **stateDiagram-v2**: State machines, lifecycles
   - **erDiagram**: Database schemas, entity relationships
   - **gantt**: Project timelines, schedules
   - **gitGraph**: Branch strategies, commit flows
   - **mindmap**: Brainstorming, hierarchical concepts
   - **timeline**: Historical events, roadmaps
   - **C4Context/C4Container**: Architecture diagrams
   - **pie**: Proportional data

5. **Render to PNG** using mermaid-cli:
   ```bash
   npx -y @mermaid-js/mermaid-cli mmdc \
     -i diagrams/{name}.mmd \
     -o diagrams/rendered/{name}.png \
     -b transparent
   ```

6. **Report results**:
   - Path to source `.mmd` file
   - Path to rendered `.png` file
   - Brief description of diagram content

**Diagram best practices:**
- Use clear, descriptive node labels
- Keep diagrams focused (one concept per diagram)
- Use subgraphs to group related elements
- Add meaningful edge labels for relationships
- Use appropriate direction (TD, LR, etc.) for readability

**Example output structure:**
```
diagrams/
├── user-auth-flow.mmd      # Source (version controlled)
├── database-schema.mmd
└── rendered/               # Output (gitignored)
    ├── user-auth-flow.png
    └── database-schema.png
```

**If mermaid-cli fails:**
- Suggest installing globally: `npm install -g @mermaid-js/mermaid-cli`
- Or use npx (included in command above)
- Check for syntax errors in .mmd file

---

Now create a diagram for: $ARGUMENTS
