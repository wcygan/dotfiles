# Reflection - Structured Retrospective

Generate a comprehensive retrospective analysis focused on learning and continuous improvement. This command helps capture insights, analyze decisions, and identify actionable improvements from recent work.

## Arguments

Provide the scope for reflection: `sprint`, `project`, `feature`, or a specific time period (e.g., "last week", "December 2024").

If no argument is provided, reflect on the current session/conversation.

Examples:

- `/project:reflection sprint` - Reflect on the most recent sprint
- `/project:reflection "last month"` - Reflect on work from the last month
- `/project:reflection feature-auth` - Reflect on a specific feature implementation

## Reflection Scope: $ARGUMENTS

Please generate a structured retrospective following this format:

### 📍 Context

- **Period/Scope**: What timeframe or work scope is being reflected upon?
- **Key Objectives**: What were the main goals or deliverables?
- **Stakeholders**: Who was involved or impacted?

### ✅ What Went Well

Identify successes and positive outcomes:

- **Technical Achievements**: Code quality improvements, performance gains, successful implementations
- **Process Improvements**: Workflow enhancements, automation wins, efficiency gains
- **Team Collaboration**: Communication highlights, knowledge sharing, pair programming successes
- **Learning Moments**: New skills acquired, problems solved creatively

### 🔄 What Could Be Improved

Analyze challenges and areas for growth:

- **Technical Challenges**: Complex bugs, architectural issues, technical debt
- **Process Bottlenecks**: Slow feedback loops, unclear requirements, tooling issues
- **Communication Gaps**: Misunderstandings, delayed responses, unclear expectations
- **Resource Constraints**: Time pressure, skill gaps, tool limitations

### 💡 Key Learnings

Extract valuable insights:

- **Technical Insights**: New patterns discovered, tools mastered, architectural lessons
- **Process Discoveries**: What workflows worked best, what caused friction
- **Team Dynamics**: How collaboration evolved, communication patterns that emerged
- **Domain Knowledge**: Business logic understood, user needs discovered

### 🎯 Decisions & Outcomes

Review major choices:

- **Key Decisions Made**: Technology choices, architectural decisions, process changes
- **Results**: What were the actual outcomes of these decisions?
- **Retrospective Analysis**: Would we make the same choices knowing what we know now?
- **Alternative Paths**: What other options were considered and why were they not chosen?

### 📊 Metrics & Measurements (if applicable)

Quantify where possible:

- **Velocity/Productivity**: Tasks completed, story points delivered, cycle time
- **Quality Indicators**: Bug counts, test coverage, code review turnaround
- **Team Health**: Morale indicators, burnout signs, collaboration frequency

### 🚀 Action Items

Concrete steps for improvement:

1. **Immediate Actions**: Quick wins that can be implemented right away
2. **Process Improvements**: Workflow changes to test in the next iteration
3. **Technical Improvements**: Refactoring needs, tool adoptions, architecture changes
4. **Learning Goals**: Skills to develop, knowledge to acquire, experiments to run

### 🎉 Celebrations

Acknowledge achievements:

- Individual contributions worth highlighting
- Team milestones reached
- Problems solved elegantly
- Growth demonstrated

---

Generate this reflection by:

1. Analyzing recent git commits, pull requests, and code changes (if reflecting on code work)
2. Reviewing task completions and project progress
3. Considering both technical and human aspects
4. Focusing on learning and growth opportunities
5. Providing specific, actionable insights rather than generic observations
6. Balancing constructive criticism with positive recognition

The goal is to create a reflection that helps the team or individual grow, not just document what happened. Make it insightful, balanced, and forward-looking.
