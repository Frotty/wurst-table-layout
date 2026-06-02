# AGENTS.md

## Project Summary
This repo provides a flexbox-inspired table layout library for WurstScript UI frames.
Core concepts: a TableLayout has rows, rows contain cells, cells contain framehandles.

## Key Files
- `wurst/TableLayout.wurst` Core layout engine and UI helpers (text, image, button, checkbox, bar).
- `wurst/TableUi.wurst` Small higher-level UI helpers (panel/card, tooltip, edit box, textarea, dynamic select).
- `wurst/MultiboardAttach.wurst` Helpers to attach layout content to the default multiboard UI.
- `wurst/TableLayoutTest.wurst` Example usage and manual test harness.
- `README.md` High-level overview and examples.
- `AI_USAGE.md` Decision tree and cookbook for choosing TableLayout/TableUi helpers before raw frames.
- `WC3_FRAMEHANDLE_GUIDE.md` Wurst/TableLayout-specific framehandle guidance for AI agents.

## How To Use
Minimal usage pattern:
```wurst
let layout = new TableLayout(0.22, 0.1, "Demo")
layout.padding = padding(0.006, 0.012, 0.006, 0.012)
layout
..row()
..add(p("Hello"))
..row()
..add(btn("Click")..setWidth(0.1))..growX()
layout.applyTo(someFrame)
```

Multiboard attach pattern:
```wurst
attachToMultiboard(mb, "DemoMb", 0.22, 0.08, true, (uiParent, anchor) -> begin
    let layout = new TableLayout(0.22, 0.1, "DemoMbLayout")
    layout..row()..add(p("Hello"))
    layout.applyTo(anchor)
    return anchor
end)
```

## Important Behaviors
- Call `row()` before the first `add(...)`. `add` uses the last row.
- Cell sizes come from the frame size at layout time. Set widths/heights before `applyTo`.
- `growX()` only affects the most recently added cell.
- If content size changes later, call `layout()` again to recompute positions.
- `defaultFrameParent` controls the parent for new frames created by helpers.

## Agent Guidance
- Read `AI_USAGE.md` before creating new UI. Follow its decision tree and recipes.
- Read `WC3_FRAMEHANDLE_GUIDE.md` before adding or changing Warcraft III UI/framehandle behavior.
- Prefer editing or extending `wurst/TableLayout.wurst` for new layout features.
- Prefer adding common components to `wurst/TableUi.wurst` unless they are core layout primitives.
- Keep API changes small and chain-friendly (`..row()..add(...)` style).
- If you add new helpers (e.g., new widget types), follow the existing `p`, `img`, `btn` helpers.
- If you touch multiboard behavior, verify maximize/minimize still restores layout sizing.
- Prefer stdlib framehandle methods and `TableLayout` helpers over raw `Blz*` calls unless native semantics matter.
- Before any raw `BlzCreateFrame*` / `createFrameByType` use, check `TableLayout`, `TableUi`, and `imports/TableLayout.fdf`; if nothing fits, add a reusable helper.
- Create UI at elapsed time `0.00` or later, cache handles, and hide/reuse frames instead of destroying them.
- Keep layout behavior backward-compatible. New spacing/sizing behavior should be opt-in.

## Tests and Demos
- `wurst/TableLayoutTest.wurst` is the current demo and manual test. Keep it updated when you add features.
