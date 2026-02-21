---
title: Cognitive Biases in Software Decisions
description: Common biases that distort architecture decisions and how agents mitigate them
tags: [biases, cognitive, decision-making, debiasing]
---

# Cognitive Biases in Software Decisions

Understanding these biases is critical because each agent role is specifically designed to counter them.

## The Big Six (Most Impactful in Software)

### 1. Confirmation Bias

**What**: Searching for evidence supporting your preferred approach while ignoring disconfirming data.

**Example**: "We already use React, so let's look at how React solves this" — never evaluating whether React is the right tool.

**Agent mitigation**: The **Critic** is explicitly mandated to argue against the leading option. The **Scout** finds alternatives outside the current frame.

### 2. Anchoring

**What**: The first solution considered dominates evaluation of all alternatives.

**Example**: Senior developer suggests microservices in the first 5 minutes; all subsequent discussion compares everything to that anchor.

**Agent mitigation**: The **Analyst** scores all options independently against quality attributes. The **Scout** introduces options that weren't in the initial set.

### 3. Bandwagon Effect

**What**: "Everyone uses X" substitutes for "X is right for our context."

**Example**: Choosing Kubernetes because it's popular, not because you need container orchestration.

**Agent mitigation**: The **Critic** checks whether popularity is driving the decision. The **WWHTBT** analysis forces you to state what conditions would need to hold — "we'd need the operational maturity to run K8s" is a testable condition.

### 4. Optimism Bias

**What**: Underestimating complexity, timeline, and failure modes.

**Example**: "This refactor will take a sprint" — it takes three.

**Agent mitigation**: The **Critic** runs a pre-mortem explicitly assuming failure. The **Risk register** forces enumeration of what can go wrong.

### 5. Sunk Cost Fallacy

**What**: Prior investment in an approach prevents pivoting when evidence warrants it.

**Example**: "We've already spent two months building the custom ORM, we can't switch now."

**Agent mitigation**: The **Analyst** evaluates options based on future cost/benefit, not past investment. The **WWHTBT** analysis focuses on what's true NOW, not what was true when we started.

### 6. Authority Bias

**What**: The most senior person's opinion ends discussion prematurely.

**Example**: CTO says "use GraphQL" and nobody pushes back.

**Agent mitigation**: Agents don't have organizational hierarchy. The **Critic** will challenge any option regardless of who proposed it.

---

## Secondary Biases

### IKEA Effect
**What**: Overvaluing something because you built it.
**Agent mitigation**: Scout researches external solutions; Analyst scores build-vs-buy objectively.

### Status Quo Bias
**What**: Preferring the current state because change feels risky.
**Agent mitigation**: Analyst includes "do nothing" as a scored option; Critic assesses risks of NOT changing.

### Dunning-Kruger Effect
**What**: Overestimating competence in unfamiliar domains.
**Agent mitigation**: Explorer reveals actual codebase complexity; Scout finds what experts say about the domain.

---

## Using the Bias Checklist

The Critic agent includes a bias check in its output. When reviewing findings:

1. Read the bias check BEFORE reading the recommendation
2. For each flagged bias, ask: "If this bias weren't influencing us, would we still choose the same option?"
3. If the answer is "maybe not," investigate further before deciding

---

## Sources

- Mohanani, R. et al. (2018). "Cognitive Biases in Software Engineering: A Systematic Mapping Study." IEEE Transactions on Software Engineering. https://ieeexplore.ieee.org/document/8506423/
- NASA APPEL (2018). "Mitigating Cognitive Bias in Engineering Decision-Making." https://appel.nasa.gov/2018/04/11/mitigating-cognitive-bias-in-engineering-decision-making/
- Stacy, W. & MacMillan, J. (1995). "Cognitive Bias in Software Engineering." Communications of the ACM.
- Salesforce Engineering. "How Cognitive Biases Can Sabotage Your Thinking." https://engineering.salesforce.com/how-cognitive-biases-can-sabotage-your-thinking-and-lead-you-astray-191af55f7365/
- De Bono, E. (1985). *Six Thinking Hats*. https://thedecisionlab.com/reference-guide/organizational-behavior/six-thinking-hats
- Martin, R. "What Would Have to Be True?" https://rogermartin.medium.com/what-would-have-to-be-true-83dac5bd2189
- Anthropic. "Building Effective Agents." https://www.anthropic.com/research/building-effective-agents
- Anthropic. "How We Built Our Multi-Agent Research System." https://www.anthropic.com/engineering/multi-agent-research-system
