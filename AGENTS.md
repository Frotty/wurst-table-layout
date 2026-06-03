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
- Text presets (`p`/`p2`/`p3`/`h1`-`h5`) are FIXEDSIZE and measure `0` until sized. Size every non-grow cell (`setSize`/`prefSize`/`fixedWidth`/`minWidth`) or use `growX`/`growY`, or it collapses and siblings overlap.
- Validate before shipping: `layout.checkFits()` returns a boolean; `layout.inspect()` returns a detailed `LayoutReport`. Both are frame-independent and run headless in `@Test`/`grill test` (build cells with `addSized(w, h)`). At runtime, `Log.warn`s fire for zero-size cells and horizontal/vertical overflow (gated by `tableWarnings`).
- `growX()` only affects the most recently added cell.
- `gap(x, y)` is now reserved correctly in grow distribution, row width, and alignment. Set `legacyGapMath = true` to restore the old (overflowing) behaviour.
- Vertical alignment within a row: `valign(Align)` per cell, `top()`/`middle()`/`bottom()` per row, `defaultValign(Align)` per table.
- Column alignment: `columns()` / `uniformColumns()` makes cells line up into columns across rows (opt-in; `growX` ignored in grid mode); `colspan(n)` spans columns. Use it for forms/rosters instead of manual offsets. Otherwise nest tables (the default composition tool).
- Spacing scale: use `SPACE_XS`/`SPACE_S`/`SPACE_M`/`SPACE_L`/`SPACE_XL` in `gap`/`padding`/`spacer` instead of magic numbers. `gap(all)` and `spacer(size)` take one value.
- Minimum sizes: `textButton`/`iconButton`/`checkbox` clamp to `MIN_BUTTON_WIDTH`/`MIN_BUTTON_HEIGHT`/`MIN_ICON_SIZE` so controls can't render broken.
- Container hierarchy: `panel` (window) > `card` (section, sparingly) > `container`/`section` (no backdrop, default nesting). Never nest backdrops more than one level — box with `container`/`section`, not `card`.
- Safe placement: use `frame.placeSafe(vec2, w, h)` (clamps into `SAFE_AREA_MIN`..`SAFE_AREA_MAX`) instead of raw `setAbsPoint`, to avoid the melee HUD.
- Keyboard focus: library clickables auto-release focus on click (`autoReleaseFocus`, default true) so Enter still opens chat and can't re-fire a button; no manual `unfocus()` needed. For foreign frames call `onClickReleaseFocus()`; for decorative frames `disable()`. There is no FDF "unfocusable" flag and no `GetFocus`/focus event, so focus is handled at creation/click, not globally.
- Flatter setup: `panelTable`/`cardTable` + `.build()` (no duplicated dimensions); `label(text,w)`/`value(text,w)` for sized text.
- If content size changes later, call `layout()` again to recompute positions.
- Free transient layouts with `destroy layout` (frees Row/Cell wrappers and lists; does not destroy the shared framehandles).
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
