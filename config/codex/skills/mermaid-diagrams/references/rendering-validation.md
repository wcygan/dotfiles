# Rendering And Validation

Use this reference to check Mermaid diagrams before handing them off.

Sources:
- Mermaid usage guide: https://mermaid.js.org/config/usage.html
- Mermaid Live Editor: https://mermaid.live/
- Mermaid CLI docs: https://mermaid.js.org/config/mermaidCLI.html

## Fast Validation Path

1. Save standalone diagrams as `.mmd`.
2. Paste the source into https://mermaid.live/ for syntax and layout inspection.
3. Render through the target docs platform when the user names one.
4. Use a local CLI render when the repository already has `mmdc`, Node, or a docs build that renders Mermaid.

## Local CLI Render

Use Mermaid CLI when available:

```sh
npx -y @mermaid-js/mermaid-cli -i path/to/diagram.mmd -o /tmp/diagram.svg
```

Include icon packs when the source uses `logos:*`, `simple-icons:*`, or another Iconify pack:

```sh
npx -y @mermaid-js/mermaid-cli \
  --iconPacks @iconify-json/logos @iconify-json/simple-icons \
  -i path/to/diagram.mmd \
  -o /tmp/diagram.svg
```

Use PNG output when the user needs screenshots:

```sh
npx -y @mermaid-js/mermaid-cli -i path/to/diagram.mmd -o /tmp/diagram.png
```

Use the repo's existing docs build when Mermaid is rendered by Docusaurus, VitePress, MkDocs, Astro, or another site generator.

## Browser Embed For Icon Packs

Use a browser harness when the diagram depends on Iconify registration:

```html
<!doctype html>
<html lang="en">
  <body>
    <pre class="mermaid">
architecture-beta
    service pg(logos:postgresql)[Postgres]
    service kafka(logos:kafka)[Kafka]
    pg:R --> L:kafka
    </pre>

    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

      mermaid.registerIconPacks([
        {
          name: "logos",
          loader: () =>
            fetch("https://unpkg.com/@iconify-json/logos@1/icons.json").then((res) =>
              res.json()
            ),
        },
      ]);

      mermaid.initialize({ startOnLoad: true });
    </script>
  </body>
</html>
```

Use this harness for `architecture-beta`, flowchart icon shapes, and custom icon packs.

## Debug Checklist

- Confirm the first non-comment line is the diagram type.
- Confirm every node ID is declared before `architecture-beta` edges reference it.
- Quote labels with punctuation, slashes, parentheses, brackets, or reserved words.
- Register Iconify packs before using `logos:*` or `simple-icons:*`.
- Pass `--iconPacks @iconify-json/logos @iconify-json/simple-icons` when rendering icon diagrams with Mermaid CLI.
- Check the target renderer version for `architecture-beta`, icon shapes, and beta diagram support.
- Simplify dense chains into one edge per line when parser errors point near an edge.
- Use built-in icons while isolating renderer-specific icon-pack failures.

## Delivery Notes

Report validation in concrete terms:

- `Validated with Mermaid Live Editor on 2026-05-23.`
- `Rendered locally with @mermaid-js/mermaid-cli to /tmp/diagram.svg.`
- `Syntax checked in target Markdown renderer.`
- `Icon rendering requires registering logos and simple-icons packs in the host page.`
