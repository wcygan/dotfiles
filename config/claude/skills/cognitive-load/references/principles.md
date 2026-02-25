# Cognitive Load Principles

## The Working Memory Constraint

The average developer holds ~4 chunks in working memory simultaneously. Every unnecessary concept, pattern, indirection, or naming convention consumes a chunk. When all four are occupied by extraneous concerns, none remain for the actual problem.

> "Cognitive load is how much a developer needs to think to complete a task. It's not about simplicity — it's about how much working memory your code demands."

## Two Types of Cognitive Load

### Intrinsic Cognitive Load
The inherent difficulty of the task itself. Writing a distributed consensus algorithm is inherently complex. This load cannot be reduced — it IS the work.

### Extraneous Cognitive Load
Created by how information is presented, how code is structured, how architecture is organized. This is entirely within our control. Most "complex" codebases are complex not because the problem is hard, but because the solution introduces unnecessary mental overhead.

**The entire goal**: identify and eliminate extraneous cognitive load so that all working memory is available for intrinsic load.

## The Deep Module Principle

From John Ousterhout's *A Philosophy of Software Design*:

> "The best components provide powerful functionality yet have simple interfaces."

**Deep module**: Simple interface, complex implementation. The complexity is hidden.
- Unix I/O: 5 basic calls (`open`, `read`, `write`, `lseek`, `close`) hiding hundreds of thousands of lines
- A good hash map: `.get()`, `.set()`, `.delete()` hiding rebalancing, collision resolution, resizing

**Shallow module**: Complex interface for minimal functionality. The complexity is exposed.
- A class with 12 configuration options that wraps a single function call
- A microservice with 8 API endpoints that delegates to one database query

**Metric**: If your interface is as complex as your implementation, the module is too shallow.

## Familiarity Is Not Simplicity

Code you wrote feels simple because you've internalized its mental model. But each unique architectural choice, naming convention, and structural decision adds to the learning burden for newcomers.

> "No simplifying force acts on code except deliberate choices you make." — Dan North

**The 40-minute test**: If a new developer is confused for more than 40 minutes continuously when onboarding to your codebase, the code needs improvement — not the developer.

**The newcomer test**: Before defending your architecture, have someone unfamiliar with it review it. Their confusion reveals your extraneous load.

## Limit Choices

> "Reduce cognitive load by limiting the number of choices." — Rob Pike

When a language or framework offers 5 ways to do something, a reader must understand why THIS way was chosen. That "why" occupies working memory.

Go's design philosophy: fewer features means less time wondering "why not the other way?"

C++ counter-example: 21 ways to initialize a variable after "uniform initialization syntax" was added. Each occurrence forces readers to consider alternatives.

**Orthogonal features** (each solves a distinct problem) are fine. **Overlapping features** (multiple ways to solve the same problem) compound cognitive load.

## The Debugging Multiplier

> "Debugging is twice as hard as writing code. Therefore, if you write code as cleverly as you can, you are by definition not smart enough to debug it." — Brian Kernighan

Write code at half your ability level. The reader (including future you) needs the remaining capacity for debugging.

## Key Quotes

- **Rob Pike** (Unix, Go): "A little copying is better than a little dependency."
- **John Ousterhout**: "The best components provide powerful functionality yet have simple interfaces."
- **Dan North**: "No simplifying force acts on code except deliberate choices you make."
- **Brian Kernighan**: "Debugging is twice as hard as writing the code in the first place."
- **Fred Brooks**: Software systems are "perhaps the most intricate and complex" things humanity makes.
- **Andrej Karpathy** (on cognitive load): "Probably the most true, least practiced viewpoint."

## Success Stories: Boring Wins

| System | Approach | Result |
|--------|----------|--------|
| Instagram (early) | Python monolith on Postgres | 14M users, 3 engineers |
| Unix | Monolithic kernel | Dominant for 50+ years |
| Raft consensus | Designed for understandability | Replaced Paxos in practice |
| Linux vs Hurd | Monolithic vs microkernel | Linux won decisively |

The pattern: systems designed for understandability outlast systems designed for theoretical elegance.
