# AI Usage Cookbook

This file is for AI agents and contributors who need to build Warcraft III UI in this repo.
The goal is to make the boring choice the correct choice: use the existing layout and component helpers first, and only drop to raw frame code when a reusable helper is missing.

## Decision Tree

Before creating any UI, follow this order:

1. Need to position several things?
   Use `TableLayout`. Do not manually calculate frame points for ordinary rows, labels, buttons, icons, forms, or panels.

2. Need text, images, buttons, checkboxes, or bars?
   Use `TableLayout` helpers: `p`, `p2`, `p3`, `h1`-`h5`, `img`, `btn`, `imgBtn`, `checkbox`, `UIBar`, `UICheckbox`.

3. Need a common component such as a panel, card, tooltip, input, text area, or select?
   Use `TableUi`: `panel`, `card`, `textButton`, `iconButton`, `withTooltip`, `boxedTooltip`, `textInput`, `textArea`, `select`.

4. Need default Warcraft III UI integration?
   Use the documented stdlib helpers and this repo's wrappers. For multiboards, use `attachToMultiboard`.

5. Need FDF-only behavior?
   Add a minimal reusable template to `imports/TableLayout.fdf`, then expose it through a Wurst helper in `TableUi.wurst` or `TableLayout.wurst`.

6. Still need custom frame code?
   Add a small reusable helper instead of inline one-off frame construction.

Raw `BlzCreateFrame*` / `createFrameByType` code should be the last step, not the first draft.

## Prefer This

Use these helpers instead of custom frame construction:

- Text: `p`, `p2`, `p3`, `h1`, `h2`, `h3`, `h4`, `h5`
- Images: `img`
- Buttons: `btn`, `imgBtn`, `textButton`, `iconButton`
- Layout roots: `defaultFrame`, `panel`, `card`, `layoutFrame`, `spacer`
- Dividers: `separator`, `vSeparator`
- Common rows: `iconLabel`, `labelValue`
- Forms: `textInput`, `select`, `checkbox`, `UICheckbox`
- Feedback: `UIBar`, `statBar`, `textArea`
- Tooltips: `withTooltip`, `boxedTooltip`
- Dialogs: `confirmDialog`, `closeButton` for the EscMenu-styled X close control
- Multiboard UI: `attachToMultiboard`

Do not hand-roll these unless you are improving the helper itself.

## Escape Hatch

Raw frame creation is acceptable when:

- you are adding a new reusable component helper,
- the component needs native/FDF behavior that is not wrapped yet,
- you are adapting a Blizzard default frame by name,
- you are documenting native semantics in `WC3_FRAMEHANDLE_GUIDE.md`.

When using the escape hatch, keep the raw code inside one helper function or class. Callers should still get a clean API.

## Standard Imports

Most UI code should look like this:

```wurst
import TableLayout
import TableUi
```

Add `ClosureTimers` only when creation must be delayed in the current package:

```wurst
import ClosureTimers

init
    doAfter(0.) ->
        createUi()
```

## Recipes

### Basic Panel

```wurst
import TableLayout
import TableUi

let root = panel(0.24, 0.12)

new TableLayout(0.24, 0.12, "BasicPanel")
..gap(0.004, 0.004)
..row()..add(h2("Status"))..growX()..add(closeButton(root))
..row()..add(separator(0.21))
..row()..add(labelValue("State", "Ready", 0.20))
..row()..add(textButton("Close", 0.08, 0.024))
..applyTo(root)
```

### Settings Form

```wurst
import TableLayout
import TableUi

let root = card(0.26, 0.16)
let difficulty = select("Difficulty", 0.12)
..addOption("Easy")
..addOption("Normal")
..addOption("Hard")

new TableLayout(0.26, 0.16, "SettingsForm")
..gap(0.004, 0.004)
..row()..add(h2("Settings"))
..row()..add(p("Select"))..add(difficulty.create())..growX()
..row()..add(p("Name"))..add(textInput("", 0.12).create())..growX()
..row()..add(textButton("Apply", 0.08, 0.024).withTooltip("Apply these settings."))
..applyTo(root)
```

### Icon Button Row

```wurst
import TableLayout
import TableUi

new TableLayout(0.18, 0.04, "IconButtons")
..gap(0.003, 0.)
..row()
..add(iconButton("ReplaceableTextures\\CommandButtons\\BTNHumanBuild.blp", 0.026).withTooltip("Build"))
..add(iconButton("ReplaceableTextures\\CommandButtons\\BTNMove.blp", 0.026).withTooltip("Move"))
..add(iconButton("ReplaceableTextures\\CommandButtons\\BTNStop.blp", 0.026).withTooltip("Stop"))
..createFrame()
```

### Icon Label

```wurst
import TableUi

let row = iconLabel("ReplaceableTextures\\CommandButtons\\BTNHeroPaladin.blp", "Paladin", 0.14)
```

### Tooltip

```wurst
import TableUi

let start = textButton("Start", 0.08, 0.024)
start.withTooltip("Starts the selected mode.")
```

Use `withTooltip` instead of repeatedly calling `setTooltip`. Reusing the same owner/tooltip pair directly can crash on hover in Warcraft III.

### Dynamic Select

```wurst
import TableLayout
import TableUi

let difficulty = select("Difficulty", 0.12)
..addOption("Story")
..addOption("Normal")
..addOption("Nightmare")

new TableLayout(0.22, 0.08, "SelectExample")
..gap(0.004, 0.004)
..row()..add(p("Difficulty"))..add(difficulty.create())..growX()
..createFrame()
```

Use this custom select for dynamic options. Native `POPUPMENU` options are FDF-defined and are better for fixed menus.

### Confirm Dialog

```wurst
import TableUi

let dialog = confirmDialog("Leave?", "Unsaved progress will be lost.")
..setButtons("Leave", "Stay")

dialog.show()
```

Use `confirmDialog` for ordinary yes/no UI. Native `DIALOG` is FDF-rigid and is usually unnecessary for map UI.

### Stat Bar

```wurst
import TableUi

let hp = statBar("Health", 0.16)
..setValue(0.75)
..setValueText("75 / 100")

let frame = hp.create()
```

### Multiboard Attachment

```wurst
import MultiboardAttach
import TableLayout

attachToMultiboard(mb, "ScoreMb", 0.22, 0.08, true, (uiParent, anchor) -> begin
    let layout = new TableLayout(0.22, 0.08, "ScoreLayout")
    layout.padding = padding(0.006, 0.012, 0.006, 0.012)
    layout
    ..row()..add(h3("Score"))
    ..row()..add(p("Player"))..add(p("10"))..growX()
    layout.applyTo(anchor)
    return anchor
end)
```

After changing multiboard behavior, manually verify minimize/maximize.

## Layout Defaults

Do not change old layout behavior by default.

Safe opt-in layout tools:

- `gap(x, y)` for spacing between cells/rows
- `growX()` for horizontal expansion of the latest cell
- `growY()` for vertical expansion of the latest cell
- `grow()` for both axes
- `minWidth`, `minHeight`
- `fixedWidth`, `fixedHeight`, `fixedSize`

If a requested layout needs new behavior, add it behind an explicit method. Existing layouts should render the same after upgrading the dependency.

## Component Rules

- Components should return either a `framehandle` or a small wrapper with `create()` / `getFrame()`.
- Keep APIs cascade-friendly.
- Keep frame creation cached. Calling `create()` twice should return the same frame when practical.
- Use `onClickReleaseFocus()` or release focus manually for clickable controls.
- Hide and reuse UI frames instead of destroying them in multiplayer UI.
- Put FDF templates in `imports/TableLayout.fdf`.
- Expose FDF names through helpers; do not make map code know template strings.

## Checklist Before Finishing

- Does the code use `TableLayout` for ordinary layout?
- Did it reuse `TableLayout`/`TableUi` helpers before raw frame code?
- Are any new raw frames wrapped in a reusable helper?
- Are new layout behaviors opt-in?
- Are tooltips created through `withTooltip` or `boxedTooltip`?
- Are buttons releasing keyboard focus?
- If multiboard code changed, was minimize/maximize considered?
- Did `grill build` pass?
