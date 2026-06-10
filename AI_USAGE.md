# AI Usage Cookbook

This file is for AI agents and contributors who need to build Warcraft III UI in this repo.
The goal is to make the boring choice the correct choice: use the existing layout and component helpers first, and only drop to raw frame code when a reusable helper is missing.

## Decision Tree

Before creating any UI, follow this order:

0. Size every non-grow cell. Text presets (`p`, `p2`, `p3`, `h1`-`h5`) are FIXEDSIZE and report a measured size of `0` until sized, so an unsized text cell collapses to nothing and neighbouring cells overlap at the same point. Give each non-grow cell a size via `setSize`, `prefSize`/`prefWidth`/`prefHeight`, `fixedWidth`/`minWidth`, or make it `growX()`/`growY()`. Then confirm with `layout.checkFits()` (see "Validation" below) before you ship.

1. Need to position several things?
   Use `TableLayout`. Do not manually calculate frame points for ordinary rows, labels, buttons, icons, forms, or panels. Aligning siblings with `setPoint`/`setAbsPoint` is the wrong tool: nest a `TableLayout` instead. (`setAbsPoint` on a root container is fine.)

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
- Selectable / state: `interactive(frame)` for whole-frame click/selected/disabled/tooltip state on display-only frames; `selectable(frame)`, `UISelectableGroup` (radio); low-level `clickableOverlay`/`selectionHighlight`/`disabledOverlay` for escape hatches
- Colour / type: `muted`, `accent`, `success`/`warning`/`danger`, `gold`/`lumber`/`mana`/`health`, `colored(text, COLOR_*)`; `underline(text)`
- Layout roots: `defaultFrame`, `panel`, `card`, `layoutFrame`, `spacer`
- Dividers: `separator`, `vSeparator`
- Common rows: `iconLabel`, `labelValue`
- Cards: `statCard(label, value, w)` (stat tile), `iconCard(icon, title, subtitle, w)` (media/list row)
- Forms: `textInput`, `select`, `checkbox`, `UICheckbox`, `slider(label, w, min, max)`
- Navigation: `tabs(w, contentHeight)` (`addTab(title)` returns a content frame to build into, then `build()`)
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

## Art Direction (aim for *nice*, not just functional)

The helpers encode sensible defaults; follow these so a quick UI also looks designed.

**Colour hierarchy.** Don't leave everything pure white. Use the palette (re-theme the whole library by reassigning the `COLOR_*` vars):
- `muted(text)` for captions, labels, subtitles, secondary text (grey).
- `accent(text)` for the values / numbers that matter (gold).
- plain white for body and titles.
- `success(text)` / `warning(text)` / `danger(text)` for state.

Presets already apply this: `labelValue` mutes the label, `statCard` mutes the caption and accents the value, `iconCard`/`statBar` mute the secondary text. So `labelValue("Kills", "12", w)` reads as a designed caption/value pair with no extra work. Accent the key number, mute the caption.

**Typography.** WC3 frame text has no bold / italic / underline attribute, so vary emphasis with the size scale (`h1`-`h5` for headings, `p`/`p2`/`p3` for body/captions; don't invent sizes) and colour (`accent()` an important value instead of bolding it). Do NOT try to fake bold (a heavier shadow just looks muddy at UI sizes). `underline(text)` draws a thin rule beneath the text (the only way to underline in WC3).

**Structure.** One `panel` per window; `card` sparingly and never nested; `section(title, w)` or `container` for grouping; `SPACE_*` tokens for gaps. Let the spacing scale and colour hierarchy carry the design rather than reaching for more chrome.

## Recipes

### Basic Panel

```wurst
import TableLayout
import TableUi

let root = panel(0.24, 0.12)

new TableLayout(0.24, 0.12, "BasicPanel")
..gap(0.004, 0.004)
..row()..add(h2("Status")..setSize(0.16, 0.022))..growX()..add(closeButton(root))
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
..row()..add(h2("Settings")..setSize(0.22, 0.022))..growX()
..row()..add(p("Select")..setSize(0.06, 0.024))..add(difficulty.create())..growX()
..row()..add(p("Name")..setSize(0.06, 0.024))..add(textInput("", 0.12).create())..growX()
..row()..add(textButton("Apply", 0.08, 0.024).withTooltip("Apply these settings."))
..applyTo(root)
// label cells are sized (0.06 wide); the controls take the rest via growX
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

### Whole-Frame Interaction

Use `interactive(target)` when a display-only frame (card, row, panel, icon tile) should be clickable
across its full visual area or needs selected/disabled state. Build all display children first, then add
the directive:

```wurst
let row = card(0.16, 0.05)
// build display-only text/images/bars into row
let hit = interactive(row)
    ..setSelected(false)
    ..setDisabled(false)
    ..withTooltip("Select this row.", 0.18)

hit.getClickFrame().onClick() ->
    hit.setSelected(true)
```

The directive disables display descendants so text/images/bars do not swallow mouse input. If display
children are added or relaid out later, call `hit.refresh()`. Do not use it on a frame containing inner
buttons that must remain independently clickable.

### Building nested content under its parent (`withParent`)

When you build a sub-panel's *content* (e.g. a stats panel holding bars), create it UNDER its eventual
parent so `applyTo`'s re-parent is a no-op and no hit area desyncs. Wrap the build in `withParent`:

```wurst
import TableLayout
import TableUi

let stats = card(0.18, 0.08)
withParent(stats) ->
    new TableLayout(0.18, 0.08, "Stats")
    ..row()..add(statBar("Health", 0.16).getFrame())..growX()
    ..applyTo(stats)
```

`withParent(parent) -> ...` scopes `defaultFrameParent` (a nestable push/pop that auto-restores), so
everything created inside is born under `parent` instead of being created globally and re-parented in
(a post-creation `setParent` can desync a frame's clickable area - the cause of a real overlay click-steal
bug). Use `inLayer(Layer.DIALOG)` / `inLayer(Layer.OVERLAY) -> ...` the same way for floating UI.

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
..row()..add(label("Difficulty", 0.08))..add(difficulty.create())..growX()
..createFrame()
// the label is sized (0.08); the select takes the rest via growX. A bare unsized p("Difficulty") here
// would collapse to 0 and overlap the select (and fail checkFits()).
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
    ..row()..add(h3("Score")..setSize(0.20, 0.02))..growX()
    ..row()..add(p("Player")..setSize(0.12, 0.012))..add(p("10")..setSize(0.04, 0.012))..growX()
    layout.applyTo(anchor)
    return anchor
end)
```

After changing multiboard behavior, manually verify minimize/maximize.

## Layout Defaults

Do not change old layout behavior by default.

Safe opt-in layout tools:

- `gap(x, y)` for spacing between cells/rows (now correctly reserved in grow/width/alignment maths)
- `growX()` for horizontal expansion of the latest cell
- `growY()` for vertical expansion of the latest cell
- `grow()` for both axes
- `minWidth`, `minHeight`
- `fixedWidth`, `fixedHeight`, `fixedSize`
- `prefWidth`, `prefHeight`, `prefSize` for a fallback size used when the frame measures 0 (e.g. text)
- `valign(Align)`, and per-row `top()` / `middle()` / `bottom()` for vertical alignment within a row
- `defaultValign(Align)` to set the vertical alignment of every new row
- `columns()` / `uniformColumns()` for grid alignment (cells line up into columns across rows), with `colspan(n)` for spanning cells. Prefer this over computing per-column offsets by hand. `growX()` is ignored in grid mode: size cells instead.

### Composition: nest by default, columns only for alignment

Nested `TableLayout`s are the default way to build any non-trivial layout: compose small tables inside cells. Only reach for `columns()` when cells in *different rows* must line up into the *same* columns (forms, stat tables, rosters). For everything else, nest.

### Spacing scale

Use the spacing tokens instead of magic numbers, in `gap`, `padding`/`pad` and `spacer`:
`SPACE_XS` 0.004 · `SPACE_S` 0.008 · `SPACE_M` 0.014 · `SPACE_L` 0.022 · `SPACE_XL` 0.034.
e.g. `..gap(SPACE_S, SPACE_S)`, `layout.padding = padding(SPACE_M, SPACE_M, SPACE_M, SPACE_M)`, `add(spacer(SPACE_M))`.

### Minimum sizes

`textButton`, `iconButton` and `checkbox` clamp to `MIN_BUTTON_WIDTH` / `MIN_BUTTON_HEIGHT` / `MIN_ICON_SIZE`, so a control can't be created too small to render. Don't hand-size buttons below ~0.022 height.

### Container hierarchy (consistent visual feel)

Pick the lightest container that does the job, and **never nest backdrops more than one level deep**:
- `panel(w, h)`: the window/dialog surface. One per UI.
- `card(w, h)`: a visually distinct section inside a panel. Use sparingly; never a card inside a card.
- `container(w, h)` / `section(title, w)`: **no backdrop**. The default for structural nesting and grouping (`section` is a heading + separator). Box things with these, not `card`.

### Safe placement

Don't `setAbsPoint` a root at arbitrary coordinates: it can land on the command card, the resource bar, the day/night clock, or the 4:3 edge. There are two bands:

- `frame.placeSafe(vec2(x, y), w, h)` / `clampToSafeArea(w, h)` uses `SAFE_AREA_MIN`..`SAFE_AREA_MAX`: the strict band clear of the bottom HUD, top HUD, 4:3 edge, and the left idle worker / hero button stack.
- `frame.placeVisuallySafe(vec2(x, y), w, h)` / `clampToVisualSafeArea(w, h)` uses `VISUAL_SAFE_AREA_MIN`..`VISUAL_SAFE_AREA_MAX`: the wider visual band clear of the bottom/top HUD and 4:3 edge, but allowed to overlap the left idle-button stack.

Use the strict band for ordinary panels/dialogs. Use the visual band only for UI that intentionally uses the left margin and tolerates possible idle-button overlap, such as custom chat/status sidecars. Both APIs clamp with declared dimensions; do not derive dimensions from local client/frame getters.

For visual debugging, maps can expose `toggleSafeAreaDebugFor(player)` for the strict red outline and `toggleVisualSafeAreaDebugFor(player)` for the wider yellow outline. These helpers create handles for all clients and show/hide owner-scoped.

### Layering (z-order)

WC3 stacking follows the frame tree, with no global z-index; `setLevel` orders siblings within one parent. Verified in-game: of the origin frames `GAME_UI` (the default parent) renders on top — above the HUD console, `WORLD_UI` and `CONSOLE_UI`. So custom UI lives in `GAME_UI`, and "on top of other custom UI" uses two `GAME_UI` child layers raised by `setLevel`:

- `Layer.CONTENT` (`GAME_UI`, default): ordinary panels.
- `Layer.DIALOG` (`GAME_UI` child, above content): modal dialogs.
- `Layer.OVERLAY` (`GAME_UI` child, above dialogs): dropdowns, menus, tooltips.
- `Layer.BACKGROUND` (`WORLD_UI`): behind the melee HUD.

Create frames in their layer with `inLayer(Layer.DIALOG) -> ...` rather than reparenting an existing frame (a post-creation `setParent` can desync the clickable area from the visual). `confirmDialog` uses `DIALOG`, `select` uses `OVERLAY`.

### Flatter setup

- `panelTable(w, h, name)` / `cardTable(w, h, name)` create the backdrop and a bound table in one call; finish the chain with `.build()` (applies the layout and returns the root frame): no duplicated dimensions, no separate root variable.
- `label(text, w)` (left-aligned) / `value(text, w)` (right-aligned): sized text in one call, instead of `p(text)..setSize(w, h)..setTextAlignment(...)`.
- `gap(all)` sets both axes at once.

```wurst
import TableLayout
import TableUi

let panel = panelTable(0.24, 0.12, "Setup")
..gap(SPACE_S)
..row()..add(h2("Setup")..setSize(0.12, 0.02))
..row()..add(label("Name", 0.07))..add(textInput("", 0.12).create())..growX()
..row()..add(textButton("Start", 0.08, 0.024))
..build()

panel.placeSafe(vec2(0.5, 0.5), 0.24, 0.12)
```

If a requested layout needs new behavior, add it behind an explicit method. Existing layouts should render the same after upgrading the dependency.

## Component Rules

- Components should return either a `framehandle` or a small wrapper with `create()` / `getFrame()`.
- Keep APIs cascade-friendly.
- Keep frame creation cached. Calling `create()` twice should return the same frame when practical.
- Keyboard focus is handled automatically: library clickables (`btn`/`imgBtn`/`iconButton`/`textButton`/`checkbox`) release focus on click by default (`autoReleaseFocus`), so Enter still opens chat and a stray Enter can't re-fire a button. Don't add manual `unfocus()` to library buttons. For a frame the library did not create, call `frame.onClickReleaseFocus()`; for a decorative frame, `disable()` it so it never takes focus. Edit boxes keep focus intentionally.
- Hide and reuse UI frames instead of destroying them in multiplayer UI.
- Put FDF templates in `imports/TableLayout.fdf`.
- Expose FDF names through helpers; do not make map code know template strings.

## Validation

The library can sanity-check a layout WITHOUT a running game, so you (and CI) catch overflow and unsized cells before ever launching WC3.

- `layout.checkFits() returns boolean`: true when nothing overflows and every non-grow cell has a size. Leak-free; ideal for assertions.
- `layout.inspect() returns LayoutReport`: the detailed report (`ok`, `zeroSizeCount`, `rowOverflowCount`, `verticalOverflow`, `worstOverflowX`, `summary`, plus soft `textOverflow` / `textOverflowSummary`). Destroy the report when done.
- `layout.validateAndWarn()`: at runtime, logs any problems via `Log.warn` (gated by `tableWarnings`) without aborting layout.
- `..text(text, FONT_*)` after `add(...)` / `addSized(...)` records text metadata for heuristic width validation. Text overflow is soft: it warns through `validateAndWarn()` and appears in `inspect().textOverflow`, but it does not make `checkFits()` fail.
- Use `ellipsizeLines(text, FONT_*, width, maxLines)` for constrained multiline labels; it wraps greedily on spaces and ellipsizes the final visible line.

Self-check pattern: runs headless via `grill test` (no frames needed). Use `addSized(w, h)` to model declared cell sizes:

```wurst
package MyUiTest
import TableLayout
import TableUiTextMetrics

@Test
function setupPanelFits()
    let t = new TableLayout(0.24, 0.16, "SetupPanel")
    t..row()..addSized(0.06, 0.02)..text("Name", FONT_P)..addSized(0.12, 0.02)..growX()
    t.checkFits().assertTrue()
    destroy t
```

At runtime the library also warns automatically: a `Log.warn` fires once per cell that measures `0`, and on horizontal/vertical overflow (all gated by `tableWarnings`). If you see "a cell has 0 measured size", size that cell.

## Checklist Before Finishing

- Does the code use `TableLayout` for ordinary layout?
- Did it reuse `TableLayout`/`TableUi` helpers before raw frame code?
- Are any new raw frames wrapped in a reusable helper?
- Are new layout behaviors opt-in?
- Is every non-grow cell sized (no bare unsized text presets in multi-cell rows)?
- Does `layout.checkFits()` pass (no overflow, no zero-size cells)?
- Is root placement done with `placeSafe(...)` or an explicitly documented safe-band coordinate?
- Is all custom frame creation/manipulation delayed until after map load (`doAfter(0.)` or later), with only TOC loading in `init`?
- Does the layout avoid `BlzGetLocalClientWidth()` / `BlzGetLocalClientHeight()` and other local frame getters for sizing/placement decisions?
- Are tooltips created through `withTooltip` or `boxedTooltip`?
- Library buttons release keyboard focus automatically; for any clickable frame the library did NOT create, did it get `onClickReleaseFocus()` (or `disable()` if decorative)?
- If multiboard code changed, was minimize/maximize considered?
- Did `grill build` pass?
