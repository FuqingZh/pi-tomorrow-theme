# Tomorrow Theme for Pi

A port of all five [Tomorrow themes by Chris Kempson][upstream] for Pi.

| Variant | Pi theme name | Matching terminal background |
| --- | --- | --- |
| Tomorrow | `tomorrow` | `#ffffff` |
| Tomorrow Night | `tomorrow-night` | `#1d1f21` |
| Tomorrow Night Eighties | `tomorrow-night-eighties` | `#2d2d2d` |
| Tomorrow Night Blue | `tomorrow-night-blue` | `#002451` |
| Tomorrow Night Bright | `tomorrow-night-bright` | `#000000` |

## Install

Install from GitHub using Pi:

```sh
pi install git:github.com/FuqingZh/pi-tomorrow-theme
```

Restart Pi or run `/reload`, then pick a variant in **/settings → Theme**.

The npm release is pending. Once published, `pi install npm:pi-tomorrow-theme`
will be an alternative to the GitHub install.

## Try from a checkout

```sh
pi --theme ./themes --use-theme tomorrow-night-eighties
```

Run the command from the repository root. Replace `tomorrow-night-eighties`
with any theme name above. This does not change your saved theme.

For the original appearance, match the truecolor terminal background in the
table, especially when using the light Tomorrow variant. The Pi theme colors
areas Pi paints, not the default backdrop behind ordinary replies and blank
cells.

## Preview without a model call

This command runs a synthetic session from the checkout in a disposable Pi
profile. Exit Pi without submitting a prompt. Change `--use-theme` to any of
the five names above, or to `dark` for Pi's built-in baseline.

```sh
(
  repo=$PWD
  scratch=$(mktemp -d) || exit 1
  trap 'rm -rf -- "$scratch"' EXIT
  cp "$repo/test/fixtures/preview.jsonl" "$scratch/preview.jsonl" || exit 1
  cd "$scratch" || exit 1
  PI_CODING_AGENT_DIR="$scratch/agent" PI_OFFLINE=1 pi --no-extensions --no-skills \
    --theme "$repo/themes" --use-theme tomorrow-night-blue \
    --session "$scratch/preview.jsonl"
)
```

## Design and attribution

Each theme preserves the 12 original [Xresources palette][palette] values and
uses the [TextMate themes][textmate] as the syntax reference. Code comments keep
the original colors. Pi-specific roles use related surface colors and, where
needed, separate UI accent shades to keep headings and tool output legible.
The VS Code port informs the Night Blue panel colors; bold remains Pi's normal
bold in every variant.

See [project documentation](docs/README.md) for the design and verification.
The original work is copyright © 2011 Chris Kempson, under the [MIT License](LICENSE).

[upstream]: https://github.com/chriskempson/tomorrow-theme
[palette]: https://github.com/chriskempson/tomorrow-theme/tree/ccf6666/Xdefaults
[textmate]: https://github.com/chriskempson/tomorrow-theme/tree/ccf6666/textmate
