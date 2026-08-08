# Universal font glyphs

`TableUiIcons.FontIcons` is the semantic catalog of symbols verified in the bundled
`universal.ttf`. The Wurst constants are the canonical mapping; each declaration keeps
the Unicode code point in a trailing comment.

The catalog is useful for compact status marks, arrows, separators, emphasis, and other
small UI affordances. Use the semantic constant instead of copying a raw Unicode literal:

```wurst
import TableUiIcons

local label = FontIcons.BLACK_STAR + " Best score"
```

## Font setup requirement

This package does not install or bind a font. The consuming map must import its own
`universal.ttf` and bind that font through `war3mapSkin.txt` to the WC3 text font slots
used by the map. Without that setup, Warcraft's fallback fonts may render these symbols
as boxes or omit them. Unicode support here is therefore a property of the consuming map,
not a general Warcraft guarantee.

Before adding a symbol, verify it against the consuming map's font `cmap`; do not rely on
browser or terminal rendering. Keep Wurst sources UTF-8, especially when a build or editor
may transcode non-ASCII text.

## Common examples

| Symbol | Constant | Code point |
| --- | --- | --- |
| `★` | `FontIcons.BLACK_STAR` | U+2605 |
| `✓` | `FontIcons.CHECK_MARK` | U+2713 |
| `♻` | `FontIcons.BLACK_UNIVERSAL_RECYCLING_SYMBOL` | U+267B |
| `→` | `FontIcons.RIGHTWARDS_ARROW` | U+2192 |
| `•` | `FontIcons.BULLET` | U+2022 |
| `▲` | `FontIcons.BLACK_UP_POINTING_TRIANGLE` | U+25B2 |
| `◆` | `FontIcons.BLACK_DIAMOND` | U+25C6 |
| `─` | `FontIcons.BOX_DRAWINGS_LIGHT_HORIZONTAL` | U+2500 |
| `—` | `FontIcons.EM_DASH` | U+2014 |

See [`wurst/TableUiIcons.wurst`](wurst/TableUiIcons.wurst) for the complete verified
catalog and [`README.md`](README.md) for package usage.
