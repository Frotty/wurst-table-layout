# AGENTS.md

## Purpose
This repo is the source for `wurst-table-layout`, a WurstScript Warcraft III UI toolkit: the one-stop shop for programmatic WC3 UI. It provides `TableLayout`, `TableUi` components, SimpleFrame helpers (`TableUiSimple`), named default-HUD control (`TableUiDefaultUi`), frame-safe helpers, validation tests, and documentation. Keep this file short and operational; detailed recipes live in `AI_USAGE.md`, native frame rules in `WC3_FRAMEHANDLE_GUIDE.md`, and public examples in `README.md`.

## Context Refresh
Before editing this repo, and again after any context compaction/resume, re-read this file first. Then open only the task-relevant deeper doc:

- New UI/component/API work: `AI_USAGE.md`
- Frame/desync/native behavior: `WC3_FRAMEHANDLE_GUIDE.md`
- Public-facing docs/examples: `README.md`
- Layout validation behavior: `wurst/TableLayoutValidationTest.wurst`

If you are modifying a downstream map's `_build/dependencies/wurst-table-layout`, stop. Patch this source repo instead, then update the dependency normally.

## Hard Rules
- Do not edit generated dependency copies. `_build/dependencies` in consuming maps is ephemeral, like `node_modules`.
- Prefer `TableLayout` / `TableUi` helpers over raw `BlzCreateFrame*` or one-off frame math.
- Create UI at elapsed time `0.00` or later; only TOC loading belongs in blocking `init`.
- Create/get frame handles for all clients, cache them, and use owner-scoped show/hide for per-player UI.
- Do not destroy Warcraft III frames in multiplayer cleanup. Hide and reuse them.
- Do not create first-time frame handles inside `localPlayer` blocks.
- Do not use local UI getters (`getText`, `getValue`, `getWidth`, `getHeight`, `isVisible`, `BlzGetLocalClientWidth/Height`, etc.) as synced game logic or layout authority.
- Build frames under their eventual parent with `withParent(...)` / `inLayer(...)`; avoid post-creation `setParent`, which leaves the frame in both parents' child lists and can misalign hit areas.
- Keep ordinary roots in the strict safe band with `placeSafe(...)`; use `placeVisuallySafe(...)` only for deliberate sidecars/status UI where left idle-button overlap is acceptable.
- Do not move Blizzard chat/message frames with arbitrary coordinates. Create map-owned UI in a safe band instead.
- Size every non-grow cell. Text presets measure `0` until sized; use `setSize`, `prefSize`, `fixedWidth`, `minWidth`, or `growX/growY`.
- SimpleFrame components (`simpleBar`/`simpleTexture`, `TableUiSimple`) never go inside `TableLayout` cells or under Frame-group parents; they render below all Frame-group UI and are placed absolutely with `placeAt`. Use them only for boss/HUD bars, tinted textures, and off-4:3 band art.
- Validate layout math with `checkFits()` / `inspect()` and headless tests before calling WC3 "done".

## Core Files
- `wurst/TableLayout.wurst`: core layout engine, rows/cells, validation report, basic helpers.
- `wurst/TableUi.wurst`: public facade exporting components.
- `wurst/components/`: component implementations (`TableUiSafeArea`, dialogs, layers, panels, inputs, tooltips, etc.).
- `wurst/MultiboardAttach.wurst`: custom content inside default multiboard shells.
- `wurst/TableLayoutValidationTest.wurst`: headless layout/safe-area validation tests.
- `wurst/TableLayoutTest.wurst`: manual visual demo; requires a real WC3 map run.

## Safe Areas
There are two safe-area concepts:

- Strict: `SAFE_AREA_MIN`..`SAFE_AREA_MAX`, `placeSafe(...)`, `clampToSafeArea(...)`. Use for ordinary panels/dialogs. Clears bottom/top HUD, 4:3 edge, and left idle worker / hero buttons.
- Visual: `VISUAL_SAFE_AREA_MIN`..`VISUAL_SAFE_AREA_MAX`, `placeVisuallySafe(...)`, `clampToVisualSafeArea(...)`. Use only for deliberate sidecars/status areas that may overlap the left idle-button stack but must stay inside the visual 4:3/HUD-safe band.

Debug helpers create handles globally and show/hide owner-scoped:

- `toggleSafeAreaDebugFor(player)`: red strict outline.
- `toggleVisualSafeAreaDebugFor(player)`: yellow visual outline.

## Design/API Guidance
- Keep APIs cascade-friendly and small.
- Add reusable helpers instead of inline raw frame code.
- Components should return a `framehandle` or a small wrapper with `create()` / `getFrame()`.
- New widgets should create frames lazily in `create()`/`build()` under their own root.
- Preserve backward compatibility. New layout behavior should be opt-in.
- Use spacing tokens (`SPACE_XS`..`SPACE_XL`) and existing components before adding new styling primitives.
- Container hierarchy: `panel` for windows/dialogs, `card` sparingly for one nested visual section, `container`/`section` for structure. Do not nest backdrop cards deeply.
- Library clickables release keyboard focus automatically; for foreign clickables use `onClickReleaseFocus()`, and disable decorative frames.

## Validation
After code changes run:

```bash
grill typecheck --quiet
```

Run focused tests for touched behavior, e.g.:

```bash
grill test safeArea
grill test TableLayoutValidationTest
```

Run broader `grill test` when layout core, shared components, or validation behavior changed. For visual/manual behavior, update `wurst/TableLayoutTest.wurst` and mention that a WC3 run is still needed.