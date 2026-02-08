---
name: ui-optimization
description: Analyze and optimize UI components for visual design, accessibility, and performance. Use when the user wants to improve existing UI, refine styling, enhance accessibility, or optimize frontend performance. Keywords: optimize UI, improve component, accessibility, responsive design, CSS optimization, visual polish, refine styling
---

# UI Optimization

Multi-agent workflow to analyze, recommend, and implement UI improvements for existing components and pages.

## Workflow Overview

**Phase 1: Analysis** → **Phase 2: Recommendations** → **Phase 3: Implementation**

## Instructions

### Step 1: Identify Target

Ask the user to specify:
- **Component/page path** - Which file(s) to optimize?
- **Scope** - Specific concerns (accessibility, mobile, performance) or comprehensive analysis?
- **Context** - Is there a design system, brand guidelines, or existing patterns to follow?

If the user provides a screenshot, analyze it visually and ask for the corresponding file path.

### Step 2: Analysis Phase (Parallel Agents)

Launch three specialized agents **in parallel** using the Task tool:

```
Task(subagent_type="ui-optimization:visual-designer", ...)
Task(subagent_type="ui-optimization:accessibility-auditor", ...)
Task(subagent_type="ui-optimization:performance-optimizer", ...)
```

Each agent analyzes the target component and returns findings in their domain.

**Important:** Use a single message with three Task tool calls to run them in parallel.

### Step 3: Synthesize Recommendations

After all agents complete:
1. **Consolidate findings** from all three agents
2. **Prioritize by impact:**
   - 🔴 High: Critical accessibility issues, severe visual problems, major performance blockers
   - 🟡 Medium: Noticeable improvements, minor a11y issues, moderate optimizations
   - 🟢 Low: Polish, nice-to-haves, micro-optimizations
3. **Group related changes** (e.g., color contrast + focus indicators = "accessibility pass")
4. **Estimate effort** (quick win, moderate, significant refactor)

Present recommendations as:

```markdown
## UI Optimization Recommendations

### 🔴 High Priority
1. **Fix color contrast** (Accessibility) - WCAG AA failure on button text
   - Effort: Quick win (~5 min)
   - Change: Update `text-gray-400` to `text-gray-900`

2. **Add keyboard navigation** (Accessibility) - No focus indicators
   - Effort: Moderate (~15 min)
   - Change: Add `:focus-visible` styles to interactive elements

### 🟡 Medium Priority
3. **Improve spacing consistency** (Visual) - Inconsistent margins
   - Effort: Quick win (~10 min)
   - Change: Use design tokens from spacing scale

### 🟢 Low Priority
4. **Optimize animation performance** (Performance) - Layout thrashing
   - Effort: Moderate (~20 min)
   - Change: Use `transform` instead of `top/left`

---

**Which recommendations would you like me to implement?**
(You can select by number or say "all high priority", "1 and 3", etc.)
```

### Step 4: Get User Approval

Wait for the user to select which recommendations to implement. Do NOT proceed to implementation without explicit approval.

### Step 5: Implementation Phase

For each approved recommendation:
1. **Make the change** - Edit files using Edit tool
2. **Explain the change** - Show before/after with educational insights
3. **Test if applicable** - Run relevant tests, check in browser
4. **Atomic commit** (optional) - If user wants, commit each change separately

Follow the dotfiles CLAUDE.md principles:
- Small steps
- Test after changes (if tests exist)
- Atomic commits with clear messages

## Output Format

**After analysis:**
```markdown
## Analysis Complete

Analyzed: `src/components/Button.tsx`

**Visual Designer** - Found 3 issues (2 high, 1 medium)
**Accessibility Auditor** - Found 5 issues (1 high, 4 medium)
**Performance Optimizer** - Found 2 issues (1 medium, 1 low)

Generating prioritized recommendations...
```

**After recommendations:**
Present the prioritized list (see Step 3 format above)

**During implementation:**
```markdown
### Implementing: Fix color contrast

**Before:**
```css
.button { color: #9CA3AF; } /* gray-400 - contrast ratio 2.1:1 ❌ */
```

**After:**
```css
.button { color: #111827; } /* gray-900 - contrast ratio 16.2:1 ✅ */
```

✅ WCAG AA compliant (4.5:1 minimum for normal text)
```

## Notes

- Agents have access to REFERENCE.md for design patterns and best practices
- If analyzing a screenshot without code, surface visual-only recommendations and ask for file paths
- Always respect existing design systems and component libraries (don't fight the framework)
- For large components, recommend breaking analysis into smaller chunks
