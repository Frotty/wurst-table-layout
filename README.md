<img width="582" height="113" alt="Screenshot 2026-06-03 125518" src="https://github.com/user-attachments/assets/2b004018-4283-41ad-a65e-f1100978d1be" />


[![CI](https://github.com/Frotty/wurst-table-layout/actions/workflows/ci.yml/badge.svg)](https://github.com/Frotty/wurst-table-layout/actions/workflows/ci.yml)

# wurst-table-layout

**The one-stop shop for quick, consistent, programmatic Warcraft III UI in WurstScript**: a flexbox-style layout engine, a library of ready-made EscMenu-styled components, SimpleFrame helpers (boss bars, tinted art), named control of the default WC3 HUD, sane defaults, built-in validation, and first-class agent support so an LLM can build correct UI on the first try. Add elegant frame UI to your map in minutes, without hand-rolling frame maths.

<img width="820" alt="The demo map (wurst/TableLayoutTest.wurst): component, display, typography and showcase panels, multiboard attachment, an animated SimpleFrame HUD bar, and the day/night clock hidden via TableUiDefaultUi" src="https://github.com/user-attachments/assets/0edc2743-2f3a-4f10-862d-3f20f3263d41" />

*The demo map ([`wurst/TableLayoutTest.wurst`](wurst/TableLayoutTest.wurst)): interactive components, display rows, the type scale, nested-table/grid/tabs showcase and multiboard attachment - plus an animated SimpleFrame bar in the HUD band and the day/night clock removed with one call.*

It began as a table/flexbox layout (rows → cells → framehandles, with optional column alignment) and now covers the whole WC3 UI surface: custom Frame-group UI through layouts and components, the SimpleFrame band for what Frames cannot do, and named access to the default HUD - so most UIs are a few cascade lines instead of raw `BlzCreateFrame` calls. Build a layout, drop in components, apply it to any framehandle.

> Note: The table layout cannot be used with scaling.

### What you get

- **Ready-made components**: panels & cards, buttons, icon buttons, checkboxes, select menus, sliders, tabs, edit boxes, text areas, tooltips, confirm dialogs, progress & stat bars, stat/icon cards, icon-label and label-value rows, separators and spacers, and whole-frame interaction (`interactive` / `selectable` / radio groups).
- **A layout engine**: flexbox-style rows and cells with padding, gaps, horizontal & vertical alignment and `grow`, plus opt-in column/grid alignment (`columns()`, `colspan`).
- **Text presets**: `h1`-`h5`, `p`-`p3`, and sized `label` / `value` helpers.
- **SimpleFrame helpers**: `simpleBar` (boss/HUD bars with native fill + runtime tinting) and `simpleTexture` (tintable, full-width band art) for what Frame-group UI cannot do.
- **Default-HUD control**: hide or modify the day/night clock, resource bar, menu buttons, minimap, portrait, hero bar and command card by name (`TableUiDefaultUi`), or go fully custom-UI with `hideDefaultUi()`.
- **Sane defaults**: a spacing scale (`SPACE_*`), automatic component minimums, automatic keyboard-focus release, a container hierarchy, and safe-area placement that keeps panels clear of the melee HUD.
- **Built-in validation**: `checkFits()` / `inspect()` catch overflow and unsized cells, at runtime and headless in `grill test`.
- **Agent support**: ships agent instruction files (decision tree, recipes, verified WC3 frame rules) and a headless feedback loop, so an LLM can generate correct UI on the first try (see [AI readiness](#ai-readiness)).

![Diagram](https://user-images.githubusercontent.com/1486037/141851102-390b7136-41b1-4b8f-9197-be286a7a4ba5.png)

# Quick start

A complete, styled settings panel (layout, components, spacing and safe placement) in a handful of lines:

```wurst
package MyUi
import ClosureTimers
import TableLayout
import TableUi

init
    doAfter(0.) ->
        let difficulty = select("Difficulty", 0.12)
            ..addOption("Easy")..addOption("Normal")..addOption("Hard")

        let setup = panelTable(0.26, 0.15, "Setup")
        setup
        ..gap(SPACE_S)
        ..row()..add(h2("New Game")..setSize(0.16, 0.022))
        ..row()..add(label("Difficulty", 0.08))..add(difficulty.create())..growX()
        ..row()..add(label("Name", 0.08))..add(textInput("", 0.12).create())..growX()
        ..row()..add(textButton("Start", 0.10, 0.026))

        setup.build().placeSafe(vec2(0.5, 0.5), 0.26, 0.15)
```

No frame maths, no manual point anchoring, no focus boilerplate: `panelTable` makes the backdrop, the components size themselves, buttons release focus on click automatically, and `placeSafe` keeps the panel clear of the melee HUD.

# Documentation

## Install

Install as dependency via grill:

`grill install https://github.com/Frotty/wurst-table-layout`

Ensure you have the latest version of WurstScript with transitive dependencies support.

## Basics

The layout is applied to a framehandle, which becomes the base frame to which all other framehandles are attached as children. You can either provide your own base frame or use the default escape menu border, which varies in appearance depending on the player's race.

```
// Default base frame
new TableLayout(0.3, 0.35)
..createFrame()
```

![Photoshop_oXmHmp3h1B](https://user-images.githubusercontent.com/1486037/142065401-1f754d8d-5bf8-4376-baec-e608eef57f83.png)

```
// Provide base frame
new TableLayout(0.3, 0.35)
..applyTo(yourCustomFrame)
```

### Rows and Cells

The API extensively uses the cascade operator (`..`) to apply changes to the root element. To get started, create a `TableLayout` by specifying the width and height in relative screen space units. Then, add rows and cells using the `.row()` and `.add()` methods. These methods always operate on the most recently added row or cell.

```
new TableLayout(0.2, 0.15)
..row()
..add(p("1"))
..add(p("2"))
..add(p("3"))
..row()
..add(p("4"))
..add(p("5"))
..add(p("6"))
..createFrame()
```

![Warcraft_III_ZMlsVQqqxX](https://user-images.githubusercontent.com/1486037/142065460-35d1eb89-ecb9-4573-9f4e-5438e947d8ec.png)

### Padding

By default, cells have no padding, making them appear right next to each other. You can introduce space between cells by adding padding to each of the four sides: left, right, top, and bottom.

```
new TableLayout(0.2, 0.15)
..row()
..add(p("1"))..padRight(0.01)..padTop(0.01)
..add(p("2"))..padRight(0.01)..padTop(0.01)
..add(p("3"))..padRight(0.01)..padTop(0.01)
..row()
..add(p("4"))..padRight(0.01)..padTop(0.01)
..add(p("5"))..padRight(0.01)..padTop(0.01)
..add(p("6"))..padRight(0.01)..padTop(0.01)
..createFrame()
```

![Warcraft_III_MzBrGAza4Q](https://user-images.githubusercontent.com/1486037/142065482-3c9d8b72-6acf-4925-bb07-8378ffdde546.png)

### Alignment

By default, the alignment in a table is top-left. You can adjust horizontal alignment on a per-row basis.

```
new TableLayout(0.2, 0.15)
..row()..center()
..add(p("1"))..padRight(0.01)..padTop(0.01)
..add(p("2"))..padRight(0.01)..padTop(0.01)
..add(p("3"))..padRight(0.01)..padTop(0.01)
..row()..end_()
..add(p("4"))..padRight(0.01)..padTop(0.01)
..add(p("5"))..padRight(0.01)..padTop(0.01)
..add(p("6"))..padRight(0.01)..padTop(0.01)
..createFrame()
```

![Warcraft_III_1R8F91NBJl](https://user-images.githubusercontent.com/1486037/142065499-73aabd15-1da1-4173-b081-ed1c6130ecfb.png)

You can also make certain cells grow horizontally to distribute them evenly.

```
new TableLayout(0.2, 0.15)
..row()
..add(p("1"))..growX()..padBot(0.01)
..add(p("2"))..growX()
..add(p("3"))..growX()
..row()
..add(p("4"))
..add(p("5"))..growX()
..add(p("6"))
..createFrame()
```

![Warcraft_III_GEeA1xkx1e](https://user-images.githubusercontent.com/1486037/142065518-b15fe6dd-579f-4616-a7bc-28d243a986eb.png)

## Presets

As you should have noticed from the previous examples we were using the `p()` function, which analagous to html represents a paragraph text element.
Because you cannot use scaling with the table layout, several presets are provided for common types, similar to html tags:

- Headings `h1`-`h5` and paragraphs `p`, `p2`, `p3`; sized text in one call with `label` (left-aligned) / `value` (right-aligned)
- Image `img`, Button `btn`, ImageButton `imgBtn`, Checkbox `checkbox` / `UICheckbox`
- Custom (Progress-)Bar `UIBar`
- Containers: `panel` (window), `card` (section), `container` / `section` (no backdrop), plus `panelTable` / `cardTable` + `.build()`
- Higher-level components in `TableUi` such as spacers, separators, icon/label rows, label/value rows, close/X buttons, boxed tooltips, edit boxes, text areas, dynamic selects, sliders, tabs, stat/icon cards, confirm dialogs, and stat bars
- Spacing scale `SPACE_XS`-`SPACE_XL` for use in `gap` / `padding` / `spacer`

```
let baseFrame = defaultFrame()

let bar1 = new UIBar(0.075, 0.01)

let nestedTable1 = new TableLayout(0.1, 0.05)
..row()..center()
..add(img(Icons.bTNAcolyte))
..row()..center()
..add(p("Acolyte"))..padTop(0.01)

let nestedTable2 = new TableLayout(0.1, 0.05)
..row()..center()
..add(img(Icons.bTNAbomination))
..row()..center()
..add(p("Abomination"))..padTop(0.01)

new TableLayout(0.25, 0.35)
..row()
..add(h1("h1"))
..row()
..add(h2("h2"))
..row()
..add(h3("h3"))
..row()
..add(h4("h4"))
..row()
..add(h5("h5"))
..row()
..add(p("p1"))
..row()
..add(p2("p2"))
..row()
..add(p3("p3"))
..row()
..add(img(Icons.bTNAcorn1))
..row()
..add(btn("button")..setWidth(0.125)..setHeight(0.02))
..row()
..add(imgBtn(Icons.bTNHumanBuild))
..row()
..add(bar1.create())
..row()
..add(nestedTable1.createContainer(baseFrame))..padRight(0.0025)
..add(nestedTable2.createContainer(baseFrame))
..applyTo(baseFrame)
```

![image](https://user-images.githubusercontent.com/1486037/182793113-a73c3fe7-5856-4061-a897-311b7164551b.png)


## Events and Framehandles

Since the table is just a layout container, you can modify the contained framehandles as you like.
You can use the cascade operator for inline notation or simply save the framehandle in a variable.

```
let titleHandle = h1("Hello")..setSize(0.18, 0.03)
new TableLayout(0.2, 0.25)
..row()..center()
..add(titleHandle)
..row()
..add(btn("button")..setSize(0.125, 0.024))
..createFrame()
```

You can combine this with the `ClosureFrames` package to add event listeners.

```
new TableLayout(0.5, 0.25)
..row()..center()
..add(btn("button")..setSize(0.125, 0.024)..onClick(() -> print("clicked")))
..createFrame()
```

## Higher-level UI helpers

For common UI, import `TableUi` and use its small component helpers on top of `TableLayout`.
See [`AI_USAGE.md`](AI_USAGE.md) for a decision tree and cookbook-style examples that help agents choose existing components instead of hand-rolling frames.

```
import TableUi

let root = panel(0.24, 0.16)

let difficulty = select("Difficulty", 0.12)
..addOption("Practice")
..addOption("Normal")
..addOption("Hard")

new TableLayout(0.24, 0.16, "SetupPanel")
..gap(0.004, 0.004)
..row()..add(h2("Setup")..setSize(0.16, 0.022))..growX()..add(closeButton(root))
..row()..add(separator(0.21))
..row()..add(label("Select", 0.06))..add(difficulty.create())..growX()
..row()..add(labelValue("Status", "Ready", 0.18))
..row()..add(textButton("Start", 0.08, 0.024).withTooltip("Begin the selected mode."))
..applyTo(root)
```

`select` is implemented as a custom code-driven list of buttons so options can be generated in code. Native `POPUPMENU` is still useful for fixed FDF-defined menus, but its options are not dynamic.

Library buttons release keyboard focus automatically after a click, so Enter keeps opening chat instead of re-firing the last clicked button. This is controlled by the `autoReleaseFocus` flag (default `true`); set it to `false` to opt out, and call `onClickReleaseFocus()` on foreign or Blizzard frames you want to behave the same way.

## SimpleFrame helpers (boss bars, tinted and full-width art)

WC3's second frame family, SimpleFrames, can do three things ordinary frames cannot: leave the 4:3 band without malforming, be tinted at runtime with `setVertexColor`, and drive a native fill via `SIMPLESTATUSBAR`. `TableUiSimple` wraps them as `simpleBar` and `simpleTexture`:

```
let boss = simpleBar(0.30, 0.012)
..setValue(0.65)
..setColor(color(220, 60, 60))
..placeAt(vec2(0.4, 0.575))
```

The trade-off: SimpleFrames render **below** all ordinary frames and cannot be parented under them, so these helpers can never go inside a `TableLayout` cell or panel; they are free-floating HUD furniture placed absolutely with `placeAt`. For bars and images inside layouts, keep using `UIBar`/`statBar` and `img`. See [`WC3_FRAMEHANDLE_GUIDE.md`](WC3_FRAMEHANDLE_GUIDE.md) ("SimpleFrames") for the full rules.

## Taming the default WC3 UI

`TableUiDefaultUi` gives named, cached access to the default game UI so you can hide or move pieces without memorising frame names, child indices and patch quirks:

```
hideDayNightClock()                  // the clock has no frame name; this knows the child path
setResourceBarVisible(false)
setMinimapVisible(false)

// or go fully custom-UI (one-way on recent patches):
hideDefaultUi()
```

Individual elements: `dayNightClock()`, `resourceBar()`, `upperButtonBar()`, `minimapFrame()`, `portraitFrame()`, `heroBar()`, `commandButton(0..11)`, `inventoryButton(0..5)`, each with a `setXVisible` helper. Call `reserveDefaultUiHandles()` once at elapsed `0.` before any per-player (local) show/hide. The quirks (command buttons reappearing on selection, menu hotkeys surviving a hide, Reforged 2.0 console changes) are documented in [`WC3_FRAMEHANDLE_GUIDE.md`](WC3_FRAMEHANDLE_GUIDE.md).

Layout additions such as `gap`, `growY`, `minWidth`, `minHeight`, `fixedWidth`, `fixedHeight`, and `fixedSize` are opt-in and do not alter existing layouts unless called.

## Columns (grid mode)

By default a table has no columns: each row is laid out independently, so cells in different rows do not line up. Call `columns()` to opt into grid alignment: every cell lines up into a column sized to the widest cell in that column index, which is what you want for forms, rosters and stat tables. `uniformColumns()` makes every column take the single widest column width, and `colspan(n)` lets a cell (e.g. a header) span several columns.

```
let roster = panel(0.2, 0.13)
new TableLayout(0.2, 0.13, "Roster")
..columns()
..gap(0.006, 0.004)
..row()..add(h4("Roster")..setSize(0.12, 0.016))..colspan(2)
..row()..add(iconLabel(Icons.bTNAcolyte, "Acolyte", 0.11))..add(p("x12")..setSize(0.03, 0.014))
..row()..add(iconLabel(Icons.bTNAbomination, "Abomination", 0.11))..add(p("x3")..setSize(0.03, 0.014))
..applyTo(roster)
```

Grid mode is opt-in and back-compatible (tables render exactly as before unless you call `columns()`). `growX()` is ignored in grid mode: size cells, and the columns do the aligning. A `colspan` cell only widens the columns it spans when it is wider than their combined width (so a spanning header that overruns its columns is caught by `checkFits()` and laid out to fit); otherwise the other rows define those columns. (Note: don't shadow the `p()` text helper with a local named `p` as in older snippets - name the root `roster`/`root` instead.)

## Spacing, containers and safe placement

Use the spacing scale (`SPACE_XS`, `SPACE_S`, `SPACE_M`, `SPACE_L`, `SPACE_XL`) in `gap`, `padding` and `spacer` instead of magic numbers. Buttons, icon buttons and checkboxes clamp to sane minimums (`MIN_BUTTON_WIDTH`/`MIN_BUTTON_HEIGHT`/`MIN_ICON_SIZE`) so they cannot be created too small to render.

Pick the lightest container and never nest backdrops more than one level: a `panel` (window) holds `card`s (distinct sections, used sparingly), and everything else nests in `container`/`section` (no border).

Position ordinary roots with `placeSafe` to keep them inside the strict band that is clear of the melee HUD (command card, resource bar, day/night clock, hero bar, minimap, and left idle buttons) rather than raw `setAbsPoint`. For deliberate sidecars that may use the left idle-button margin but must stay inside the 4:3 visual/HUD-safe band, use `placeVisuallySafe`. Debug outlines are available via `toggleSafeAreaDebugFor(player)` (red strict band) and `toggleVisualSafeAreaDebugFor(player)` (yellow visual band). `panelTable`/`cardTable` + `.build()` create a backdrop and its table in one chain, and `label`/`value` size text in one call:

```
let p = panelTable(0.24, 0.12, "Setup")
..gap(SPACE_S)
..row()..add(h2("Setup")..setSize(0.12, 0.02))
..row()..add(label("Name", 0.07))..add(textInput("", 0.12).create())..growX()
..build()
p.placeSafe(vec2(0.5, 0.5), 0.24, 0.12)
```

For z-order, parent into the right layer rather than fighting `setLevel` (which only orders siblings within one parent). WC3 has no global z-index, and of the origin frames `GAME_UI` (the default parent) renders on top, above the HUD console and the other bands. So on-top UI uses two `GAME_UI` child layers raised with `setLevel`: `Layer.DIALOG` for modal dialogs and `Layer.OVERLAY` (above it) for dropdowns, menus and tooltips; ordinary panels stay in `Layer.CONTENT` (`GAME_UI`). Create frames in their layer with `inLayer(Layer.DIALOG) -> ...` rather than reparenting later, since a post-creation `setParent` leaves the frame in both parents' child lists and can misalign its hit area. `confirmDialog` uses `DIALOG` and `select` uses `OVERLAY`.

## Nested Tables

A table can be applied to any framehandle and thus easily inserted into another table. Ensure that the parent frame already exists when creating the child frame.

The `#createContainer` function can be used to create a container framehandle without any visuals, which can be added to other tables.

```
let baseFrame = defaultFrame()

let nestedTable1 = new TableLayout(0.1, 0.05)

let nestedTable2 = new TableLayout(0.1, 0.05)

new TableLayout(0.25, 0.35)
..row()
..add(nestedTable1.createContainer(baseFrame))..padRight(0.0025)
..add(nestedTable2.createContainer(baseFrame))
..applyTo(baseFrame)
```

## Validation

Because Warcraft III cannot measure text and the text presets (`p`, `h1`-`h5`) are FIXEDSIZE, a cell with no size measures `0` and collapses: the most common cause of overlapping/overflowing UI. Size every non-grow cell (`setSize`, `prefSize`/`prefWidth`/`prefHeight`, `fixedWidth`/`minWidth`) or make it `growX()`/`growY()`.

You can sanity-check a layout without launching the game:

```
let layout = new TableLayout(0.24, 0.16, "SetupPanel")
..row()..add(p("Name")..setSize(0.06, 0.02))..add(textInput("", 0.12).create())..growX()

if not layout.checkFits()
    let report = layout.inspect()
    Log.warn(report.summary)   // e.g. "[row 0 cell 0] zero width; [row 1] width overflow by 0.0040; "
    destroy report
```

`checkFits()`/`inspect()` are frame-independent, so they also run headless in unit tests (`grill test`): build cells with `addSized(w, h)` to model declared sizes. At runtime the library additionally logs a warning (gated by `tableWarnings`) for any zero-size cell and for horizontal/vertical overflow.

## AI readiness

This library is built to be driven by LLM coding agents: the goal is that an agent can produce correct, aligned, non-overflowing Warcraft III UI without hand-rolling frame math.

It ships agent instruction files. Point your agent at these first:

- [`AGENTS.md`](AGENTS.md): project map, key behaviours, and the rules for changing UI.
- [`AI_USAGE.md`](AI_USAGE.md): a decision tree and cookbook: which helper to use, copy-pasteable recipes, anti-patterns, and a self-check the agent runs before finishing.
- [`WC3_FRAMEHANDLE_GUIDE.md`](WC3_FRAMEHANDLE_GUIDE.md): Warcraft III framehandle, focus and desync rules adapted for this library.

What makes it agent-friendly:

- **A real feedback loop.** `layout.checkFits()` / `inspect()` validate a layout (overflow, zero-size cells) *without a running game*, so the agent can verify its own output: at runtime and headless via `grill test`. Runtime `Log.warn`s flag the common mistakes (unsized text, gap+grow overflow, vertical overflow).
- **Guard rails and sane defaults.** Zero-size/overflow warnings, component minimums, a consistent spacing scale, a container hierarchy, and opt-in safe-area placement keep generated UI inside the lines. APIs that desync or crash in multiplayer (frame destruction, post-creation reparenting, fragile SimpleFrame children) are simply not exposed.
- **A streamlined, cascade-friendly API** where the boring choice is the correct choice: nest tables and reuse helpers instead of computing frame points.
- **The whole UI surface, with the quirks encoded.** Custom panels (Frame group), boss bars and band art (SimpleFrames), and the default HUD (`TableUiDefaultUi`) are all reachable through named helpers whose documentation carries the verified WC3 facts (what reappears on selection, what is one-way, what crashes), so the agent does not have to know Warcraft III folklore.

When working with an agent, tell it to read `AGENTS.md` and `AI_USAGE.md`, then run `grill test` (or call `checkFits()`) after building UI and fix anything the report flags.

## Dynamic changes

There currently is no change detection. If you changed the contained frames and want the table to recognize the change, you have to call `table.layout()` to update the table and its contents.

## Changing the default frame parent

Due to quirks in Warcraft III's handling of frames, frames created by the presets are created as children of `GAME_UI` by default. The parent is then changed to the table's base frame after layouting. However, this can cause problems if you're trying to use a table layout inside an existing frame. The clean way is `withParent(parent) -> ...`, a scoped, nestable push/pop of `defaultFrameParent` that creates everything inside under `parent` and restores the previous value automatically (use `inLayer(Layer.DIALOG/OVERLAY) -> ...` for floating UI):

```
withParent(getFrame("SimpleInfoPanelUnitDetail", 0)) ->
    new TableLayout(...)
    ..applyTo(getFrame("SimpleInfoPanelUnitDetail", 0))
```

If you set `defaultFrameParent` manually instead, restore the **previous** value rather than hardcoding `GAME_UI`, so you don't clobber an intentional baseline parent:

```
let prev = defaultFrameParent
defaultFrameParent = getFrame("SimpleInfoPanelUnitDetail", 0)

new TableLayout(...)
..applyTo(defaultFrameParent)

defaultFrameParent = prev
```
