---
allowed-tools: Read, Bash(fd:*), Bash(rg:*), Bash(jq:*)
description: Create visual diagrams and flowcharts from code or data
---

## Context

- Target: $ARGUMENTS
- Current directory: !`pwd`
- Code files: !`fd "\.(go|rs|ts|js|py|java|cpp|c)$" . | wc -l | tr -d ' ' || echo "0"` files
- Config files: !`fd "(docker-compose|kubernetes|k8s|\.yaml|\.json)$" . | head -5 || echo "No config files"`
- Data models: !`rg "(struct|class|interface|type)" . | head -5 || echo "No models found"`

## Your task

Generate visual representations of code, data, or system architecture:

1. **Identify Visualization Type** - Determine what needs to be visualized from the target
2. **Analyze Structure** - Extract key entities, relationships, and flows
3. **Create Diagram** - Generate appropriate visual representation
4. **Provide Context** - Explain the diagram and key insights

**Visualization Types:**

- **Code Architecture**: Component relationships, module dependencies
- **Data Flow**: How data moves through the system
- **Entity Relationships**: Database schemas, object models
- **System Architecture**: Services, APIs, infrastructure
- **Process Flow**: Business logic, user journeys

**Output Formats:**

- **Mermaid diagrams** for flowcharts, sequence diagrams, entity relationships
- **ASCII art** for simple structures
- **Structured text** for complex hierarchies
- **PlantUML** for detailed system diagrams

Analyze the target and create the most appropriate visualization for understanding the system.
