# LaTeX → Typst Translation

For authors migrating documents or habits. Also useful as a reverse-dictionary when LLM priors pattern-match on LaTeX and need to be redirected.

Canonical upstream: https://typst.app/docs/guides/for-latex-users/

## Contents

- [Preamble & structure](#preamble--structure)
- [Common commands](#common-commands)
- [Environments](#environments)
- [Math](#math)
- [Figures and tables](#figures-and-tables)
- [References and citations](#references-and-citations)
- [Lists](#lists)
- [Fonts and styling](#fonts-and-styling)
- [Packages → @preview](#packages--preview)

## Preamble & structure

| LaTeX | Typst |
|---|---|
| `\documentclass{article}` | `#set page(paper: "us-letter")` + `#set text(...)` (no class; use a template) |
| `\usepackage{graphicx}` | built-in (`image` function) |
| `\usepackage{amsmath}` | built-in math mode |
| `\usepackage{pkg}` | `#import "@preview/pkg:x.y.z": *` |
| `\begin{document}` ... `\end{document}` | file body (no explicit markers) |
| `\title{...} \author{...} \maketitle` | inside a template function (`#show: tmpl.with(title: [...], authors: (...))`) |
| `\tableofcontents` | `#outline()` |
| `\newpage` | `#pagebreak()` |
| `\input{other}` / `\include{other}` | `#include "other.typ"` or `#import "other.typ": *` |

## Common commands

| LaTeX | Typst |
|---|---|
| `\newcommand{\x}[1]{...#1...}` | `#let x(arg) = [... #arg ...]` |
| `\renewcommand` | `#let` (just rebinds) |
| `\textbf{x}` | `*x*` or `#strong[x]` |
| `\textit{x}` | `_x_` or `#emph[x]` |
| `\texttt{x}` | `` `x` `` (inline code) or `#raw("x")` |
| `\underline{x}` | `#underline[x]` |
| `\emph{x}` | `#emph[x]` |
| `\footnote{x}` | `#footnote[x]` |
| `\hspace{1em}` | `#h(1em)` |
| `\vspace{1em}` | `#v(1em)` |
| `\noindent` | `#set par(first-line-indent: 0pt)` (or per-par hack with a `par` show rule) |
| `\centering` | `#align(center, ...)` or `#set align(center)` inside a scope |

## Environments

| LaTeX | Typst |
|---|---|
| `\section{X}` | `= X` |
| `\subsection{X}` | `== X` |
| `\subsubsection{X}` | `=== X` |
| `\begin{itemize} \item ... \end{itemize}` | `- ...` per line (or `#list(...)`) |
| `\begin{enumerate} \item ... \end{enumerate}` | `+ ...` per line (or `#enum(...)`) |
| `\begin{quote} ... \end{quote}` | `#quote[...]` |
| `\begin{verbatim} ... \end{verbatim}` | ```` ```...``` ```` |
| `\begin{figure}[h] ... \caption{} \label{} \end{figure}` | `#figure(image("..."), caption: [...]) <label>` |
| `\begin{table}` + `\begin{tabular}` | `#figure(table(columns: n, ...), caption: [...]) <label>` |

## Math

| LaTeX | Typst |
|---|---|
| `$x^2$` | `$x^2$` |
| `\(x\)` / `\[x\]` | `$x$` / `$ x $` (spaces around = display) |
| `$$x$$` | `$ x $` (avoid `$$` — deprecated in LaTeX too) |
| `\alpha, \beta, \Gamma` | `alpha, beta, Gamma` (just the names) |
| `\sin, \cos, \log` | `sin, cos, log` (built-in operators) |
| `\frac{a}{b}` | `a/b` or `frac(a, b)` |
| `\sqrt[n]{x}` | `root(n, x)` |
| `\sum_{i=1}^{n}` | `sum_(i=1)^n` |
| `\int_a^b` | `integral_a^b` |
| `\vec{v}` | `arrow(v)` |
| `\bar{x}` | `overline(x)` or `macron(x)` |
| `\hat{x}` | `hat(x)` |
| `\mathbf{x}` | `bold(x)` |
| `\mathit{x}` | `italic(x)` |
| `\mathbb{R}` | `RR` (built-in for common) or `bb(R)` |
| `\mathcal{L}` | `cal(L)` |
| `\text{foo}` | `"foo"` (upright in math) |
| `\begin{align} a &= b \\ c &= d \end{align}` | `$ a &= b \ c &= d $` (display math with `&` and `\`) |
| `\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}` | `mat(1, 2; 3, 4)` |

## Figures and tables

```latex
\begin{figure}[h]
  \centering
  \includegraphics[width=0.5\textwidth]{img.png}
  \caption{A caption.}
  \label{fig:mylabel}
\end{figure}
See Figure~\ref{fig:mylabel}.
```

```typ
#figure(
  image("img.png", width: 50%),
  caption: [A caption.],
) <fig:mylabel>
See @fig:mylabel.
```

```latex
\begin{table}
  \begin{tabular}{lrr}
    \toprule
    A & B & C \\
    \midrule
    1 & 2 & 3 \\
    \bottomrule
  \end{tabular}
\end{table}
```

```typ
#figure(
  table(
    columns: 3,
    align: (left, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.5pt) } else if y == 3 { (bottom: 0.5pt) },
    [A], [B], [C],
    [1], [2], [3],
  ),
)
```

For professional booktabs-style tables use `@preview/tablex` or `@preview/tabled`.

## References and citations

```latex
\cite{knuth1984}
\citet{knuth1984}         % natbib
\citep{knuth1984}
\bibliography{refs}
\bibliographystyle{plain}
```

```typ
@knuth1984                 // inline citation (style depends on bibliography())
#cite(<knuth1984>)
#cite(<knuth1984>, form: "prose")   // like \citet

#bibliography("refs.bib", style: "ieee")
// Styles: "alphanumeric", "chicago-author-date", "ieee", "apa", "mla", etc.
// Or a path to a CSL file.
// Sources can be .bib (BibLaTeX) or .yml (Hayagriva — Typst-native).
```

## Lists

```latex
\begin{itemize}
  \item First
  \item Second
    \begin{itemize}
      \item Nested
    \end{itemize}
\end{itemize}
```

```typ
- First
- Second
  - Nested
```

```latex
\begin{enumerate}
  \item First
  \item Second
\end{enumerate}
```

```typ
+ First
+ Second

// Or with explicit numbering:
1. First
2. Second
```

## Fonts and styling

| LaTeX | Typst |
|---|---|
| `\fontsize{12pt}{14pt}\selectfont` | `#set text(size: 12pt)` + `#set par(leading: ...)` |
| `\usepackage{fontspec}` + `\setmainfont{...}` | `#set text(font: "...")` (works with any installed font) |
| `\color{red}{x}` | `#text(fill: red)[x]` |
| `\textcolor{red}{x}` | `#text(fill: red)[x]` |
| `{\Large x}` | `#text(size: 1.5em)[x]` |

## Packages → @preview

| LaTeX package | Typst equivalent |
|---|---|
| `amsmath`, `amssymb`, `mathtools` | built-in |
| `graphicx` | built-in `image()` |
| `hyperref` | built-in (`link()`, auto-generated PDF links) |
| `biblatex` / `natbib` | built-in `bibliography()` + Hayagriva/BibLaTeX |
| `tikz` | `@preview/cetz` (+ `@preview/fletcher` for diagrams) |
| `pgfplots` | `@preview/cetz-plot` |
| `beamer` | `@preview/touying` (preferred) or `@preview/polylux` |
| `booktabs` | `@preview/tablex` or `@preview/tabled` |
| `algorithm2e` | `@preview/algorithmic` or `@preview/lovelace` |
| `listings` / `minted` | built-in raw blocks + `@preview/codly` for styling |
| `glossaries` | `@preview/glossarium` |
| `siunitx` | `@preview/unify` |
| `cleveref` | built-in `ref()` with custom supplement |

See [packages](packages.md) for pinned versions.
