# wurst-table-layout

[![CI](https://github.com/Frotty/wurst-table-layout/actions/workflows/ci.yml/badge.svg)](https://github.com/Frotty/wurst-table-layout/actions/workflows/ci.yml)

![chrome_EkMQO3cJuA](https://user-images.githubusercontent.com/1486037/142081152-42348ece-7cfb-47db-a4e2-c9d552537f02.png)

This library lets you create and align Warcraft III framehandles in a table-ish layout inspired by flex-box and the libGDX table. A table consists of rows, which consist of cells, which hold a framehandle. Rows are laid out independently by default; opt into cross-row column alignment with `columns()`. After setting up the layout you apply it to any framehandle.

> Note: The table layout cannot be used with scaling.

### Features

- Flexbox-style rows and cells with padding, gaps, horizontal and vertical alignment, and `growX`/`growY`.
- Opt-in column/grid alignment (`columns()`, `uniformColumns()`, `colspan`).
- HTML-like text presets (`h1`-`h5`, `p`-`p3`) plus image, button, bar and checkbox presets.
- Higher-level `TableUi` components: panels, cards, tooltips, edit boxes, text areas, dynamic selects, confirm dialogs, stat bars, and icon/label & label/value rows.
- A consistent spacing scale, sane component minimums, a container hierarchy, and safe-area placement helpers.
- Frame-independent validation (`checkFits()` / `inspect()`) that catches overflow and unsized cells — at runtime and headless in `grill test`.
- Ships LLM / agent instructions for smooth, correct UI generation (see [AI readiness](#ai-readiness)).

![Diagram](https://user-images.githubusercontent.com/1486037/141851102-390b7136-41b1-4b8f-9197-be286a7a4ba5.png)

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
- Higher-level components in `TableUi` such as spacers, separators, icon/label rows, label/value rows, close/X buttons, boxed tooltips, edit boxes, text areas, dynamic selects, confirm dialogs, and stat bars
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
let titleHandle = h1("Hello")
new TableLayout(0.2, 0.25)
..row()..center()
..add(titleHandle)
..row()
..add(btn("button")..setWidth(0.125))
..createFrame()
```

You can combine this with the `ClosureFrames` package to add event listeners.

```
new TableLayout(0.5, 0.25)
..row()..center()
..add(btn("button")..onClick(() -> print("clicked")))
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
..row()..add(h2("Setup"))..growX()..add(closeButton(root))
..row()..add(separator(0.21))
..row()..add(p("Select"))..add(difficulty.create())..growX()
..row()..add(labelValue("Status", "Ready", 0.18))
..row()..add(textButton("Start", 0.08, 0.024).withTooltip("Begin the selected mode."))
..applyTo(root)
```

`select` is implemented as a custom code-driven list of buttons so options can be generated in code. Native `POPUPMENU` is still useful for fixed FDF-defined menus, but its options are not dynamic.

Layout additions such as `gap`, `growY`, `minWidth`, `minHeight`, `fixedWidth`, `fixedHeight`, and `fixedSize` are opt-in and do not alter existing layouts unless called.

## Columns (grid mode)

By default a table has no columns — each row is laid out independently, so cells in different rows do not line up. Call `columns()` to opt into grid alignment: every cell lines up into a column sized to the widest cell in that column index, which is what you want for forms, rosters and stat tables. `uniformColumns()` makes every column take the single widest column width, and `colspan(n)` lets a cell (e.g. a header) span several columns.

```
let p = panel(0.2, 0.13)
new TableLayout(0.2, 0.13, "Roster")
..columns()
..gap(0.006, 0.004)
..row()..add(h4("Roster")..setSize(0.12, 0.016))..colspan(2)
..row()..add(iconLabel(Icons.bTNAcolyte, "Acolyte", 0.11))..add(p("x12")..setSize(0.03, 0.014))
..row()..add(iconLabel(Icons.bTNAbomination, "Abomination", 0.11))..add(p("x3")..setSize(0.03, 0.014))
..applyTo(p)
```

Grid mode is opt-in and back-compatible (tables render exactly as before unless you call `columns()`). `growX()` is ignored in grid mode — size cells, and the columns do the aligning. A `colspan` cell does not size the columns it spans, so make sure other rows define those columns.

## Spacing, containers and safe placement

Use the spacing scale — `SPACE_XS`, `SPACE_S`, `SPACE_M`, `SPACE_L`, `SPACE_XL` — in `gap`, `padding` and `spacer` instead of magic numbers. Buttons, icon buttons and checkboxes clamp to sane minimums (`MIN_BUTTON_WIDTH`/`MIN_BUTTON_HEIGHT`/`MIN_ICON_SIZE`) so they cannot be created too small to render.

Pick the lightest container and never nest backdrops more than one level: a `panel` (window) holds `card`s (distinct sections, used sparingly), and everything else nests in `container`/`section` (no border).

Position roots with `placeSafe` to keep them inside the central band that is clear of the melee HUD (command card, resource bar, hero bar, minimap) rather than raw `setAbsPoint`. `panelTable`/`cardTable` + `.build()` create a backdrop and its table in one chain, and `label`/`value` size text in one call:

```
let p = panelTable(0.24, 0.12, "Setup")
..gap(SPACE_S)
..row()..add(h2("Setup")..setSize(0.12, 0.02))
..row()..add(label("Name", 0.07))..add(textInput("", 0.12).create())..growX()
..build()
p.placeSafe(vec2(0.5, 0.5), 0.24, 0.12)
```

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

Because Warcraft III cannot measure text and the text presets (`p`, `h1`-`h5`) are FIXEDSIZE, a cell with no size measures `0` and collapses — the most common cause of overlapping/overflowing UI. Size every non-grow cell (`setSize`, `prefSize`/`prefWidth`/`prefHeight`, `fixedWidth`/`minWidth`) or make it `growX()`/`growY()`.

You can sanity-check a layout without launching the game:

```
let layout = new TableLayout(0.24, 0.16, "SetupPanel")
..row()..add(p("Name")..setSize(0.06, 0.02))..add(textInput("", 0.12).create())..growX()

if not layout.checkFits()
    let report = layout.inspect()
    Log.warn(report.summary)   // e.g. "[row 0 cell 0] zero width; [row 1] width overflow by 0.0040; "
    destroy report
```

`checkFits()`/`inspect()` are frame-independent, so they also run headless in unit tests (`grill test`) — build cells with `addSized(w, h)` to model declared sizes. At runtime the library additionally logs a warning (gated by `tableWarnings`) for any zero-size cell and for horizontal/vertical overflow.

## AI readiness

This library is built to be driven by LLM coding agents: the goal is that an agent can produce correct, aligned, non-overflowing Warcraft III UI without hand-rolling frame math.

It ships agent instruction files — point your agent at these first:

- [`AGENTS.md`](AGENTS.md) — project map, key behaviours, and the rules for changing UI.
- [`AI_USAGE.md`](AI_USAGE.md) — a decision tree and cookbook: which helper to use, copy-pasteable recipes, anti-patterns, and a self-check the agent runs before finishing.
- [`WC3_FRAMEHANDLE_GUIDE.md`](WC3_FRAMEHANDLE_GUIDE.md) — Warcraft III framehandle, focus and desync rules adapted for this library.

What makes it agent-friendly:

- **A real feedback loop.** `layout.checkFits()` / `inspect()` validate a layout (overflow, zero-size cells) *without a running game*, so the agent can verify its own output — at runtime and headless via `grill test`. Runtime `Log.warn`s flag the common mistakes (unsized text, gap+grow overflow, vertical overflow).
- **Guard rails and sane defaults.** Zero-size/overflow warnings, component minimums, a consistent spacing scale, a container hierarchy, and opt-in safe-area placement keep generated UI inside the lines.
- **A streamlined, cascade-friendly API** where the boring choice is the correct choice: nest tables and reuse helpers instead of computing frame points.

When working with an agent, tell it to read `AGENTS.md` and `AI_USAGE.md`, then run `grill test` (or call `checkFits()`) after building UI and fix anything the report flags.

## Dynamic changes

There currently is no change detection. If you changed the contained frames and want the table to recognize the change, you have to call `table.layout()` to update the table and its contents.

## Changing the default frame parent

Due to quirks in Warcraft III's handling of frames, frames created by the presets are created as children of `GAME_UI` by default. The parent is then changed to the table's base frame after layouting. However, this can cause problems if you're trying to use a table layout inside an existing frame. To work around this, you can set `defaultFrameParent` to your custom frame so that all new framehandles are created with the correct parent from the start. Make sure to reset the variable afterward to prevent side effects.

```
defaultFrameParent = getFrame("SimpleInfoPanelUnitDetail", 0)

new TableLayout(...)
..applyTo(defaultFrameParent)

defaultFrameParent = GAME_UI
```
