---
description: Deep dive into codebase to understand specific topics, patterns, or implementations
---

Perform a comprehensive deep dive analysis of the codebase based on the user's query.

**Analysis approach:**

1. **Launch 2-3 parallel exploration agents** to gather information efficiently:
   - Use Task tool with subagent_type=Explore for multi-file analysis
   - Each agent investigates different aspects or locations
   - Synthesize findings after parallel completion

2. **Investigation areas** (adapt based on query):
   - **Architecture patterns**: How components are structured and interact
   - **Implementation details**: How specific features/functionality work
   - **Configuration flows**: How configs are loaded, merged, applied
   - **Dependencies**: What tools/libraries are used and why
   - **File organization**: Where things live and naming conventions
   - **Integration points**: How different parts connect
   - **Historical context**: Git history for why things are the way they are

3. **Output format:**
   ```markdown
   # Deep Dive: [Topic]
   
   ## Overview
   [High-level summary in 2-3 sentences]
   
   ## Key Findings
   [Bulleted list of main discoveries with file:line references]
   
   ## Architecture/Flow
   [Explain how it works - diagrams in text if helpful]
   
   ## File Locations
   [Map of relevant files and their purposes]
   
   ## Code Examples
   [Relevant snippets with explanations]
   
   ## Patterns & Conventions
   [What patterns are followed, what to know for changes]
   
   ## Related Components
   [What else connects to this]
   ```

4. **Quality standards:**
   - Include specific file:line references for all claims
   - Provide code snippets for concrete examples
   - Explain *why* things are done this way (context from CLAUDE.md/AGENTS.md)
   - Note any cross-platform considerations (macOS/Ubuntu/Fedora)
   - Identify entry points and key integration boundaries

5. **Scope guidance:**
   - If query is vague, ask clarifying questions first
   - If query is too broad, break into focused sub-topics
   - If query is narrow, expand to show related context
   - Always explain how findings relate to the overall system

**Example queries this handles:**
- "How does fish shell configuration work?"
- "Explain the Nix flake structure"
- "Where are symlinks created and how?"
- "How does cross-platform testing work?"
- "What's the CI/CD pipeline doing?"
- "How are aliases and abbreviations loaded?"

**Remember:**
- Use parallel agents for speed (2-3 agents, not 8)
- Prioritize breadth first, then depth
- Connect findings to project goals (reproducibility, cross-platform)
- Keep responses structured but concise
