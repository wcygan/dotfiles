# Flowchart Patterns

Use this reference for Mermaid flowcharts, icon nodes, image nodes, subgraphs, classes, and edge labels.

Sources:
- Flowchart syntax: https://mermaid.js.org/syntax/flowchart.html
- Icon pack registration: https://mermaid.js.org/config/icons.html

## Contents

- [Basic Form](#basic-form)
- [Useful Shapes](#useful-shapes)
- [Icon Shape](#icon-shape)
- [Image Shape](#image-shape)
- [Subgraphs](#subgraphs)
- [Styling](#styling)
- [Edge Labels](#edge-labels)
- [Syntax Hygiene](#syntax-hygiene)

## Basic Form

```mermaid
flowchart LR
    api["API"] -- "writes" --> db[("Postgres")]
```

Use `LR` for pipeline and request flow. Use `TD` for decisions, lifecycles, and runbooks.

## Useful Shapes

```mermaid
flowchart LR
    api["Process"]
    db[("Database")]
    decision{"Decision?"}
    queue[["Queue / topic"]]
    file[/"File or input"/]
```

Use the expanded shape syntax when the semantic shape matters:

```mermaid
flowchart TD
    store@{ shape: cyl, label: "Database" }
    docs@{ shape: docs, label: "Documents" }
    prepare@{ shape: hex, label: "Prepare" }
```

## Icon Shape

Register the icon pack in the renderer first. Then use the flowchart `icon` shape:

```mermaid
flowchart LR
    pg@{ icon: "logos:postgresql", form: "rounded", label: "Postgres", pos: "b", h: 56 }
    kafka@{ icon: "logos:kafka", form: "rounded", label: "Kafka", pos: "b", h: 56 }
    pg --> kafka
```

Parameters:

- `icon`: registered `pack:name`.
- `form`: `square`, `circle`, or `rounded`.
- `label`: visible text.
- `pos`: `t` or `b`.
- `h`: icon height.

## Image Shape

Use image nodes when the renderer can fetch a trusted image URL and the target logo is not available as an Iconify icon.

```mermaid
flowchart LR
    custom@{ img: "https://example.com/approved-logo.svg", label: "Custom service", pos: "b", h: 64, constraint: "on" }
    api["API"] --> custom
```

Use approved local or hosted assets. Record the asset source next to the diagram when the logo source matters.

## Subgraphs

```mermaid
flowchart LR
    subgraph app["Application"]
        api["API"]
        worker["Worker"]
    end

    subgraph data["Data"]
        pg[("Postgres")]
        redis[("Redis")]
    end

    api --> worker
    worker --> pg
    api --> redis
```

Use subgraphs for ownership, deployment boundaries, trust zones, and data planes.

## Styling

Use classes for semantic meaning:

```mermaid
flowchart LR
    api["API"] --> db[("Database")]
    classDef service fill:#e0f2fe,stroke:#0369a1,color:#0f172a
    classDef store fill:#fef3c7,stroke:#b45309,color:#0f172a
    class api service
    class db store
```

Use colors to communicate one dimension: service type, risk, status, owner, or environment.

## Edge Labels

Label edges with the thing that moves:

```mermaid
flowchart LR
    api -- "order.created" --> kafka
    worker -- "activity task" --> temporal
    flink -- "upsert customer_360" --> tidb
```

Use thick arrows for critical paths:

```mermaid
flowchart LR
    checkout["Checkout"] ==> payment["Payment"]
```

Use dotted arrows for async, optional, or eventually consistent paths:

```mermaid
flowchart LR
    app["App"] -. "metrics" .-> prometheus["Prometheus"]
```

## Syntax Hygiene

Quote labels with punctuation:

```mermaid
flowchart LR
    a["POST /orders"]
```

Capitalize or quote terminal labels that say `End`:

```mermaid
flowchart TD
    finish["End"]
```

Add a space or capitalization when an edge target starts with `o` or `x`:

```mermaid
flowchart LR
    a --- Ops
```

Keep chained one-line syntax readable. Expand dense chains when the source will be maintained by humans.
