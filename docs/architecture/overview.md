# Architecture

Version 0.2 includes all five upstream Tomorrow variants, verified on Pi 1.5.2.
The package changes how Pi draws its interface, not assistant Markdown, prompts,
tools, or session contents.

## Theme and package

Each JSON file under `themes/` is a complete Pi theme. Its `vars` define the
palette and its `colors` map it to the
[Pi theme schema](https://pi.dev/schemas/theme.schema.json). The package manifest
exposes the directory through `pi.themes`. Pi loads the selected JSON, resolves
palette references, and renders the existing interface. There is no project
code in the rendering path and no install script or runtime dependency.

```text
Original palette + Pi role mapping → theme JSON → Pi's built-in renderer
Terminal's default background ──────────────────→ unpainted terminal cells
```

The [upstream Xresources palettes][palette] define the 12 original color
values for each variant. [TextMate][textmate] is the reference for syntax
roles. The original values and syntax comment colors are preserved, even when
an overlay-specific shade is needed for a role such as `toolDiffRemoved`.
Name those shades in `vars` rather than replacing the original values.
[VS Code][vscode] informs Night Blue's deep-blue panels, not other variants'
base palettes. Each theme can be edited independently; no generator is required.

## Display boundary

Pi owns message and tool panel backgrounds, selection, Markdown colors, diffs,
and the HTML export palette. The terminal owns the backdrop of unpainted cells,
including behind ordinary assistant text. `export.pageBg` is HTML-only. Match
that variant's terminal background for the original appearance; see the
[README table](../../README.md) for the five values. The themes never reconfigure
the terminal, and Pi's native bold and heading layout are unchanged.

## Verification

Run `python3 test/check.py` on a Unix system with Pi on `PATH`. The check
measures 26 UI foreground/background pairs per variant against 4.5:1 and replays
the same offline session across all five themes. It checks the original
syntax comment colors separately from UI contrast; not every source syntax
color reaches 4.5:1. `npm pack --dry-run --ignore-scripts` checks the package
boundary independently.

[palette]: https://github.com/chriskempson/tomorrow-theme/tree/ccf6666/Xdefaults
[textmate]: https://github.com/chriskempson/tomorrow-theme/tree/ccf6666/textmate
[vscode]: https://github.com/microsoft/vscode/blob/main/extensions/theme-tomorrow-night-blue/themes/tomorrow-night-blue-color-theme.json
