# UX Heuristics Reference

A combined set of Nielsen's 10 Usability Heuristics and modern web-specific heuristics
for evaluating user experience quality.

## Nielsen's 10 Usability Heuristics

### H1: Visibility of System Status
The design should always keep users informed about what is going on, through appropriate
feedback within a reasonable amount of time.

**Check for:**
- Loading indicators for async operations
- Progress bars for multi-step processes
- Confirmation messages after actions
- Active/selected states in navigation
- Real-time validation in forms
- Status indicators (online/offline, saved/unsaved)
- Page title updates on navigation

### H2: Match Between System and Real World
The design should speak the users' language. Use words, phrases, and concepts familiar to
the user, rather than internal jargon.

**Check for:**
- Navigation labels use user language (not developer terms)
- Error messages are human-readable (not error codes)
- Concepts follow real-world conventions (shopping cart, inbox)
- Icons are universally recognized or paired with labels
- Dates, currencies, and units match user expectations

### H3: User Control and Freedom
Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave
the unwanted action without having to go through an extended process.

**Check for:**
- Undo/redo support
- Cancel buttons on forms and dialogs
- Back navigation that works
- Easy logout/exit paths
- Ability to dismiss notifications/modals
- Draft saving and recovery
- Clear "go home" path from any page

### H4: Consistency and Standards
Users should not have to wonder whether different words, situations, or actions mean the
same thing. Follow platform and industry conventions.

**Check for:**
- Consistent button styles for similar actions
- Same terminology throughout
- Standard icon usage (X for close, hamburger for menu)
- Consistent layout patterns across pages
- Form field behavior matches platform defaults
- Link styling consistent and distinguishable

### H5: Error Prevention
Good error messages are important, but the best designs prevent problems from occurring
in the first place.

**Check for:**
- Confirmation dialogs for destructive actions
- Input constraints (max length, format masks)
- Smart defaults that reduce errors
- Disabled states for unavailable actions (with explanation)
- Inline validation before form submission
- Clear required field indicators
- Type-ahead and autocomplete for complex inputs

### H6: Recognition Rather Than Recall
Minimize the user's memory load by making elements, actions, and options visible. The user
should not have to remember information from one page to use on another.

**Check for:**
- Recently used items easily accessible
- Search with suggestions/autocomplete
- Breadcrumbs showing current location
- Context preserved when navigating (filters, selections)
- Labels on icons (not icon-only actions)
- Visible options vs. hidden menus for frequent actions

### H7: Flexibility and Efficiency of Use
Shortcuts — hidden from novice users — can speed up interaction for expert users. Allow
users to tailor frequent actions.

**Check for:**
- Keyboard shortcuts for power users
- Customizable dashboards or views
- Bulk actions for repetitive tasks
- Search as a primary navigation method
- Filters and sorting options
- Quick actions and context menus
- Responsive to different input methods (touch, keyboard, mouse)

### H8: Aesthetic and Minimalist Design
Interfaces should not contain information that is irrelevant or rarely needed. Every extra
unit of information competes with relevant information and diminishes visibility.

**Check for:**
- Content prioritization (most important info is prominent)
- Clean visual hierarchy
- No unnecessary decorative elements that distract
- Progressive disclosure (details available on demand)
- Adequate whitespace
- Focused pages with clear purpose (not everything-on-one-page)

### H9: Help Users Recognize, Diagnose, and Recover from Errors
Error messages should be expressed in plain language (no error codes), precisely indicate
the problem, and constructively suggest a solution.

**Check for:**
- Error messages in plain language
- Specific about what went wrong
- Suggest how to fix the problem
- Preserve user input on error
- Don't blame the user
- Position error messages near the relevant field
- Distinguish between different error types (validation, server, network)

### H10: Help and Documentation
Even though it is better if the system can be used without documentation, it may be
necessary to provide help and documentation. Such information should be easy to search,
focused on the user's task, and list concrete steps.

**Check for:**
- Contextual help (tooltips, inline hints)
- Searchable help center/documentation
- Onboarding tours for new users
- FAQ or common questions addressed
- Contact/support options visible
- Help content is task-oriented, not feature-oriented

---

## Modern Web Heuristics

### M1: Above-the-Fold Optimization
The content visible without scrolling must communicate the core value proposition and
primary action within 5 seconds.

**Check for:**
- Clear headline visible immediately
- Primary CTA above the fold
- No confusion about what the product does
- Fast perceived load time
- No intrusive popups blocking content

### M2: Cognitive Load Reduction
Minimize the mental effort required to use the interface at any point.

**Check for:**
- Limited choices per screen (Miller's Law: 7±2 items)
- Chunking of related information
- Visual grouping with whitespace and borders
- One primary action per screen
- Step-by-step flows instead of complex single forms
- Sensible defaults that reduce decisions

### M3: Progressive Disclosure
Show only what's needed at each step. Reveal complexity gradually as users need it.

**Check for:**
- Simple by default, advanced options available
- Expandable sections for details
- Multi-step wizards vs. overwhelming single forms
- "Show more" patterns for long lists
- Settings organized by frequency of use

### M4: Visual Hierarchy
The visual design should guide the eye to the most important elements first.

**Check for:**
- Clear size/weight hierarchy (headings → body → secondary)
- Color contrast draws attention to primary actions
- Whitespace creates logical grouping
- F-pattern or Z-pattern layout for scanning
- Important info doesn't require scrolling

### M5: Reducing Time-to-Value
Minimize the steps between a user arriving and experiencing the core value of the product.

**Check for:**
- Can users try the product before signing up?
- Is signup minimal (email only, social login)?
- Is onboarding quick and focused?
- Is the first "aha moment" reachable in <3 steps?
- Are empty states that guide rather than just display blank?

### M6: Design System Coherence
The application should feel like it was built from a unified design system, not assembled
from mismatched parts.

**Check for:**
- Consistent component library usage
- Unified color palette and typography scale
- Same border-radius, shadow, and spacing patterns
- Consistent animation/transition behavior
- Components look like they belong together

### M7: Inclusive Design
The application should be usable by the widest possible range of people without adaptation.

**Check for:**
- WCAG 2.1 AA compliance
- Keyboard navigability
- Screen reader compatibility
- Color not the only differentiator
- Sufficient touch targets (44×44px minimum)
- Supports zoom to 200%
- Content readable without CSS

### M8: Conversational Design
User-facing text should feel like a helpful human guiding the user, not a robot issuing commands.

**Check for:**
- Friendly, clear microcopy
- Error messages that help, not blame
- Empty states that suggest next actions
- Confirmations that reassure
- Tooltips that explain "why" not just "what"
- Consistent tone of voice
