---
description: Create a Typst document (.typ) and compile it to PDF
---

Create a Typst document based on the user's request. You will:

1. **Create the `.typ` file** with proper Typst syntax
2. **Compile it to PDF** using `typst compile`

## Arguments

The user should specify:
- **Document name**: The filename (without extension) - use `$ARGUMENTS` if provided
- **Document type**: article, report, letter, notes, slides, or custom
- **Content requirements**: What the document should contain

## Typst Syntax Reference

### Document Structure

```typst
// Page and text setup
#set page(paper: "us-letter", margin: 2cm)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.52em)
#set heading(numbering: "1.1")

// Title block
#align(center)[
  #text(size: 18pt, weight: "bold")[Document Title]
  #v(0.5em)
  #text(size: 12pt)[Author Name]
  #v(0.3em)
  #text(size: 10pt, fill: gray)[#datetime.today().display()]
]

// Content starts here
= Introduction

Your content...
```

### Headings
```typst
= First Level
== Second Level
=== Third Level
```

### Text Formatting
```typst
*bold text*
_italic text_
`inline code`
#underline[underlined]
#strike[strikethrough]
#highlight[highlighted]
```

### Lists
```typst
// Bullet list
- Item one
- Item two
  - Nested item

// Numbered list
+ First
+ Second
  + Nested numbered

// Definition list
/ Term: Definition here
```

### Links and References
```typst
#link("https://example.com")[Link text]
See @my-label for details.
#figure(
  image("file.png", width: 80%),
  caption: [Figure caption],
) <my-label>
```

### Math
```typst
Inline: $x^2 + y^2 = z^2$

Display:
$ sum_(i=1)^n i = (n(n+1))/2 $
```

### Code Blocks
````typst
```python
def hello():
    print("Hello, world!")
```
````

### Tables
```typst
#table(
  columns: (auto, 1fr, 1fr),
  [Header 1], [Header 2], [Header 3],
  [Row 1], [Data], [Data],
  [Row 2], [Data], [Data],
)
```

## Document Templates

### Article/Report
```typst
#set document(title: "Title", author: "Author")
#set page(paper: "us-letter", margin: (x: 2.5cm, y: 2.5cm))
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true)
#set heading(numbering: "1.1")

// Title
#align(center)[
  #text(size: 20pt, weight: "bold")[Title]
  #v(1em)
  Author Name \
  #text(size: 10pt, fill: gray)[#datetime.today().display()]
]

#v(2em)

// Abstract
#align(center)[
  #block(width: 85%)[
    #text(weight: "bold")[Abstract]
    #par(justify: true)[
      Abstract text here...
    ]
  ]
]

#v(1em)
#outline()
#pagebreak()

= Introduction
```

### Letter
```typst
#set page(paper: "us-letter", margin: 2.5cm)
#set text(font: "Linux Libertine", size: 11pt)

#align(right)[
  Your Name \
  Your Address \
  City, State ZIP \
  #datetime.today().display()
]

#v(2em)

Recipient Name \
Recipient Address \
City, State ZIP

#v(1em)

Dear Recipient,

#v(0.5em)

Letter body...

#v(1em)

Sincerely,

#v(3em)

Your Name
```

### Notes/Simple
```typst
#set page(paper: "us-letter", margin: 2cm)
#set text(size: 11pt)
#set heading(numbering: none)

= Topic

Notes content...
```

## File Organization

**All Typst documents MUST be created in `/typst/<doc>/` folder structure:**

```
/typst/
  my-report/
    my-report.typ
    my-report.pdf
  project-proposal/
    project-proposal.typ
    project-proposal.pdf
```

This keeps documents organized with their compiled output and any assets (images, etc.) in one place.

## Workflow

1. Ask user for document details if not provided:
   - Document name (filename)
   - Document type (article, letter, notes, etc.)
   - Content or outline

2. Create the document folder:
   ```bash
   mkdir -p /typst/<doc>
   ```

3. Create the `.typ` file at `/typst/<doc>/<doc>.typ` with appropriate template and content

4. Compile to PDF:
   ```bash
   typst compile /typst/<doc>/<doc>.typ
   ```

5. If compilation fails, read the error and fix the `.typ` file

6. Confirm success and provide paths:
   - Source: `/typst/<doc>/<doc>.typ`
   - Output: `/typst/<doc>/<doc>.pdf`

## Important Notes

- Typst must be installed (`typst` command available)
- **Always use `/typst/<doc>/` folder structure** - never create loose `.typ` files
- Output PDF will be automatically placed alongside the `.typ` file
- Use `typst watch /typst/<doc>/<doc>.typ` for live preview during editing
- Place any images or assets in the same `/typst/<doc>/` folder for easy reference
- Check https://typst.app/universe for community packages/templates
