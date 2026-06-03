# Wurst Framehandle Guide for AI Agents

This guide adapts Warcraft III 1.31+ frame API rules for this Wurst library.
Prefer Wurst standard-library helpers and `TableLayout` over raw `Blz*` calls, but keep the native frame/desync rules in mind. Warcraft III UI is fragile, patch-dependent, and multiplayer-sensitive.

## Default Approach

When adding UI in this repo:

0. Check `AI_USAGE.md` for the component decision tree and recipes.
1. Use `TableLayout` for layout instead of manual point math.
2. Create UI at elapsed time `0.00` or later with `ClosureTimers.doAfter`.
3. Create/get frame handles for all players, cache them, and update/show/hide them.
4. Do not destroy UI frames in multiplayer code; hide and reuse them.
5. Use `ClosureFrames` frame events for input.
6. Use stdlib framehandle methods (`setPoint`, `setSize`, `setText`, `setTexture`, `show`, `hide`) rather than raw `BlzFrame*` calls.
7. Use raw `Blz*` names only when documenting native semantics or when no stdlib wrapper exists.

Safe setup pattern:

```wurst
package MyUi
import ClosureTimers
import TableLayout

framehandle root = null

function createMyUi()
    if root != null
        root.show()
        return

    let layout = new TableLayout(0.18, 0.08, "MyUi")
    layout.padding = padding(0.006, 0.008, 0.006, 0.008)
    layout
    ..row()..add(h3("Status"))
    ..row()..add(p("Ready"))
    ..row()..add(btn("Close")..setSize(0.08, 0.024))

    root = layout.createFrame()

init
    doAfter(0.) ->
        createMyUi()
```

## Core Model

WC3 UI elements are `framehandle`s. They include default UI parts, custom frames, multiboards, timer dialogs, command buttons, inventory buttons, tooltips, chat, and resource UI.

There are two main UI families:

- Frame group: created by `createFrame(...)` / `BlzCreateFrame` / `BlzCreateFrameByType`; supports many events; usually lives in the 4:3 virtual screen.
- SimpleFrame group: created by `createSimpleFrame(...)`; used heavily by the default in-game UI; often needs FDF; has fewer events.

Do not freely mix Frame parents and SimpleFrame children. Keep Frame children under Frame parents, and SimpleFrame children under SimpleFrame parents.

`String` and `Texture` SimpleFrame children are special. Do not treat them like generic frames. Avoid calling visibility, alpha, level, enable, scale, parent, or destroy APIs on those children. `setFont` is for String-SimpleFrames and can crash on generic SimpleFrames.

## Coordinates and Positioning

Most UI uses WC3's fixed 4:3 virtual screen:

- bottom-left: `(0.0, 0.0)`
- center: `(0.4, 0.3)`
- top-right: `(0.8, 0.6)`

Prefer stdlib wrappers:

```wurst
frame.clearAllPoints()
frame.setAbsPoint(FRAMEPOINT_CENTER, vec2(0.4, 0.3))
frame.setPoint(FRAMEPOINT_TOPLEFT, parent, FRAMEPOINT_TOPLEFT, vec2(0.01, -0.01))
backdrop.setAllPoints(frame)
frame.setSize(0.12, 0.04)
```

Rules:

- Call `clearAllPoints()` before moving existing/default frames unless intentionally using multiple anchors.
- `setAbsPoint` places one point at absolute screen coordinates.
- `setPoint` anchors one frame point to another frame point.
- `setAllPoints(a)` copies another frame's size/position and follows later changes.
- `+x` moves right, `+y` moves up.
- `setScale` affects relative offsets and children; this library's table layout does not support scaling.

Relative placement examples:

```wurst
// A left of B
frameA.setPoint(FRAMEPOINT_RIGHT, frameB, FRAMEPOINT_LEFT, vec2(0, 0))

// A right of B
frameA.setPoint(FRAMEPOINT_LEFT, frameB, FRAMEPOINT_RIGHT, vec2(0, 0))

// A below B
frameA.setPoint(FRAMEPOINT_TOP, frameB, FRAMEPOINT_BOTTOM, vec2(0, 0))

// A above B
frameA.setPoint(FRAMEPOINT_BOTTOM, frameB, FRAMEPOINT_TOP, vec2(0, 0))
```

## TableLayout Patterns

`TableLayout` is the preferred abstraction here. It lays out rows and cells by reading each child frame's size at layout time.

```wurst
let layout = new TableLayout(0.22, 0.10, "Panel")
layout.padding = padding(0.006, 0.012, 0.006, 0.012)
layout
..row()..center()..add(h2("Inventory"))
..row()
..add(img("ReplaceableTextures\\CommandButtons\\BTNFootman.blp", 0.024, 0.024))
..add(p("Footman"))..growX()
..row()
..add(btn("Select")..setSize(0.08, 0.024))
let panel = layout.createFrame()
```

Important behavior:

- `add(...)` uses the latest row. If no row exists, `TableLayout` creates one.
- Set widths/heights before `applyTo`, `createFrame`, or `createContainer`.
- `growX()` applies only to the most recently added cell.
- If child sizes change later, call `layout.layout()` again.
- Use `defaultFrameParent` when helpers must be created under an existing parent from the start.

Temporary parent override:

```wurst
let oldParent = defaultFrameParent
defaultFrameParent = someExistingFrame

let nested = new TableLayout(0.12, 0.05, "Nested")
nested..row()..add(p("Inside"))
nested.applyTo(someExistingFrame)

defaultFrameParent = oldParent
```

For reusable widgets, follow existing helper style in `wurst/TableLayout.wurst`: return a sized `framehandle` and let the table position it.

Use opt-in layout conveniences for new code:

```wurst
let layout = new TableLayout(0.24, 0.12, "Options")
layout
..gap(0.004, 0.003)
..row()..add(p("Name"))..add(textInput("", 0.12).create())..growX()
..row()..add(p("Select"))..add(select("Difficulty", 0.12)..addOption("Easy")..addOption("Hard").create())
```

Do not change defaults that would make old layouts render differently. Add new behavior behind explicit calls such as `gap`, `growY`, `minWidth`, `minHeight`, `fixedWidth`, `fixedHeight`, or `fixedSize`.

## TableUi Components

`TableUi` is the higher-level component layer for common, safer WC3 UI. Prefer it when an AI would otherwise need to hand-roll fragile frame code.

```wurst
import TableUi

let root = panel(0.24, 0.16)

let difficulty = select("Difficulty", 0.12)
..addOption("Practice")
..addOption("Normal")
..addOption("Hard")

new TableLayout(0.24, 0.16, "UiDemo")
..gap(0.004, 0.004)
..row()..add(h2("Setup"))
..row()..add(p("Select"))..add(difficulty.create())..growX()
..row()..add(textButton("Start", 0.08, 0.024).withTooltip("Begin the selected mode."))
..applyTo(root)
```

Current component helpers:

- `panel(width, height)` and `card(width, height)` create decorated layout roots.
- `spacer(width, height)`, `separator(width)`, and `vSeparator(height)` avoid ad hoc invisible frames and divider backdrops.
- `iconLabel(path, text, width)` and `labelValue(label, value, width)` cover common WC3 information rows.
- `closeButton(target)` creates an EscMenu-styled X button with the native purple hover effect and hides a target frame.
- `textButton(text, width, height)` and `iconButton(path, size)` create EscMenu-styled buttons; release focus inside custom click handlers when the button also needs behavior.
- `withTooltip(text)` / `boxedTooltip(owner, text)` create reusable boxed tooltips and avoid repeated `setTooltip` calls for the same owner.
- `textInput(initialText, width)` creates an edit box wrapper whose submit listener uses synced frame-event text.
- `textArea(text, width, height)` creates a styled scrollable text area.
- `select(placeholder, width)` creates a dynamic TableLayout-backed select menu. This is preferred over native `POPUPMENU` when options need to be generated from code.
- `confirmDialog(title, message)` creates a simple code-driven yes/no dialog.
- `statBar(label, width)` wraps `UIBar` with label/value text.

Native `POPUPMENU` options are FDF-defined, so they are useful for fixed menus but not good for dynamic code-generated selects.

## Creating Frames

Prefer these helpers from stdlib / this repo:

```wurst
let text = p("Hello")
let title = h2("Title")
let icon = img("ReplaceableTextures\\CommandButtons\\BTNFootman.blp", 0.026, 0.026)
let button = btn("Click")..setSize(0.08, 0.024)
let checkboxFrame = checkbox(0.018, 0.018)
let rawBackdrop = createFrame(FramehandleTypeNames.backdrop, "MyBackdrop", GAME_UI, "", 0)
```

Use `loadTOCFile("TableLayout.toc")` once before creating FDF-backed frames. This repo already does that in `TableLayout` init.

Use `createContext` intentionally for repeated instances or per-player copies. Created frames and named children are stored by `(name, createContext)`.

## Frame Events and Focus

`TableLayout` imports `ClosureFrames` publicly, so packages importing `TableLayout` can use event helpers.

```wurst
let close = btn("Close")..setSize(0.08, 0.024)
close.onClick() ->
    root.hide()
```

Available wrappers include `onClick`, `onMouseEnter`, `onMouseLeave`, `onSliderValueChange`, `onEditboxChange`, and `onEditboxEnter`.

Frame events are synchronized. For game-affecting input, read the event data inside the event and store it in synced/player-indexed state. Do not read local UI getters later and use them for synced game logic.

### Keyboard focus

Clicked frames steal keyboard focus, and a focused frame swallows the **Enter** key. Because Enter normally opens chat, a stray focus means Enter either does nothing (chat won't open) or re-fires the focused control — which can be destructive (an accidental button press). This affects buttons, edit boxes and even clickable backdrops (e.g. Blizzard's chat window).

Why there is no single global cure: WC3 exposes `BlzFrameSetFocus` but **no `GetFocus`** (you can't ask what is focused), there is **no focus-changed frame event**, and player mouse events don't fire reliably over UI frames. So focus must be handled where a frame is created or clicked, not via one global listener.

How this library handles it:

- **Library clickables auto-release focus by default.** `btn`, `imgBtn`, `iconButton`, `textButton`, `checkbox`, and the components built on them attach `onClickReleaseFocus()` automatically (controlled by the `autoReleaseFocus` flag, default true). So after a library button is clicked, focus drops and Enter opens chat normally — no manual `unfocus()` needed. Edit boxes (`textInput`) are intentionally excluded, since typing needs focus.
- **Opt out** project-wide with `autoReleaseFocus = false`, or per-component by creating that component while the flag is false (reset it afterwards, like `defaultFrameParent`).
- **Foreign / Blizzard frames** the library did not create: call `frame.onClickReleaseFocus()` on a clickable you want to behave, or `frame.disable()` on a purely decorative frame so it never grabs focus in the first place (the library already disables its own `panel`/`card` backdrops for this reason). There is **no FDF flag** for "unfocusable" — disabling is the structural equivalent.
- Manual `unfocus()` / `releaseKeyboardFocus(player)` is still available when you need to release focus from a specific frame yourself.

## Multiplayer Safety

WC3 is lockstep. UI visuals may be local, but handle allocation and game-affecting results must remain deterministic.

Safe pattern:

```wurst
let console = getFrame(FramehandleDefaultNames.consoleUI)
if localPlayer == Player(0)
    console.hide()
```

Unsafe pattern:

```wurst
if localPlayer == Player(0)
    let console = getFrame(FramehandleDefaultNames.consoleUI)
    console.hide()
```

Rules:

- Do not create/get first-time UI handles only inside a local-player block.
- Do not destroy UI frames in MP code; use `hide()`.
- Do not use local UI state getters as synced data sources.
- Create all per-player copies for all players, then hide/show locally.
- Cache handles. Do not repeatedly create duplicate UI.

Be careful with these getters in MP because their values can differ locally: `getText`, `getValue`, `isEnabled`, `getAlpha`, `getHeight`, `getWidth`, `getParent`, `isVisible`.

## Default UI and Named Frames

Prefer stdlib constants instead of stringly-typed names:

```wurst
let console = getFrame(FramehandleDefaultNames.consoleUI)
let multiboardBackdrop = getFrame(FramehandleDefaultNames.multiboardBackdrop)
let command0 = getFrame("CommandButton_0")
```

In WC3 1.32+, moving command and inventory buttons through origin frames can glitch. Prefer named frames like `"CommandButton_0"` and `"InventoryButton_0"`.

When moving built-in UI, often disable auto-positioning:

```wurst
enableUIAutoPosition(false)
someDefaultFrame.clearAllPoints()
someDefaultFrame.setAbsPoint(FRAMEPOINT_BOTTOMLEFT, vec2(0.0, 0.0))
```

Do not assume changes to default UI survive selection, resource, minimize/maximize, or resolution refreshes. Reapply geometry after the native UI settles when needed.

## Multiboard Attach

Use `attachToMultiboard` when custom content should live inside the default multiboard shell and reuse its minimize/maximize behavior.

```wurst
attachToMultiboard(mb, "DemoMb", 0.22, 0.08, true, (uiParent, anchor) -> begin
    let layout = new TableLayout(0.22, 0.08, "DemoMbLayout")
    layout.padding = padding(0.006, 0.012, 0.006, 0.012)
    layout
    ..row()..add(h3("Score"))
    ..row()..add(p("Player"))..add(p("10"))..growX()
    layout.applyTo(anchor)
    return anchor
end)
```

Multiboard-specific cautions:

- Make the multiboard large enough for the content height, or let `autoRowsEnabled` fit rows.
- Native minimize/maximize can rewrite default frame geometry after click callbacks.
- Reapply title width/container geometry after a zero-second delay when touching multiboard defaults.
- Verify maximize/minimize manually after changes.

## Tooltips

Tooltips are frames too. Keep tooltip group types compatible: Frame-to-Frame and SimpleFrame-to-SimpleFrame.

```wurst
let tooltip = createFrame(FramehandleTypeNames.text, "MyTooltip", GAME_UI, "", 0)
tooltip
..setText("Tooltip text")
..setPoint(FRAMEPOINT_BOTTOM, button, FRAMEPOINT_TOP, vec2(0, 0.01))
..disable()

button.setTooltip(tooltip)
```

Cautions:

- `setTooltip` cannot really be undone.
- Calling `setTooltip` twice with the same frame/tooltip pair can crash on hover.
- Prefer per-tooltip frames when styled text matters.
- Disable tooltip text/backdrops if they should not capture mouse input.

## FDF and TOC

This repo uses `imports/TableLayout.toc` and `imports/TableLayout.fdf` for text styles, buttons, and backdrops. When adding FDF-backed helpers:

- Put reusable templates in `imports/TableLayout.fdf`.
- Keep `imports/TableLayout.toc` ending with blank lines.
- Load base FDF includes before templates that inherit from them.
- Use `UseActiveContext` when child frames should follow the current `createContext`.
- Prefer helper functions in `TableLayout.wurst` instead of making callers know FDF names.

Only main frames defined outside another `Frame {}` block can be created or inherited directly. Child frames are created as side effects of their parent.

## Save/Load

Custom UI frames are not reliably preserved by Warcraft III save/load in affected versions. After loading, old frame handles can be hidden, broken, or crash-prone.

Library policy:

- If a map supports save/load, provide a rebuild path.
- Re-run static UI creation after `EVENT_GAME_LOADED` with a zero-second delay.
- Do not trust old cached custom frame handles after load.

## Hard Rules

- Do not create/manipulate custom UI at map init; use `doAfter(0.)`.
- Do not create/get first-time frame handles inside `localPlayer` blocks.
- Do not destroy frames in MP UI code; hide and reuse them.
- Do not repeatedly create duplicate UI instead of caching handles.
- Do not use local-only UI getters for synced game logic.
- Do not blindly call frame APIs on SimpleFrame `String` or `Texture` children.
- Do not call `setTooltip` twice for the same frame/tooltip pair.
- Do not let invisible enabled frames block mouse input.
- Do not forget to clear keyboard focus after clickable UI.
- Do not assume default UI changes survive game-driven refreshes.
- Do not use scaling with this table layout.
