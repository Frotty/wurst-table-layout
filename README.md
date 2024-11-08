# wurst-table-layout

![chrome_EkMQO3cJuA](https://user-images.githubusercontent.com/1486037/142081152-42348ece-7cfb-47db-a4e2-c9d552537f02.png)

This library allows you to easily create and align framehandles in a table-ish layout inspired by flex-box.
Table-ish because there are no columns. A table simply consists of rows, which themselves consist of cells which contain a framehandle as content.
After setting up the layout you can apply it to any framehandle.

> Note: The table layout cannot be used with scaling

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

- Headings `h1`, `h2`, `h3`, `h4`
- Paragraph `p`, `p2`, `p3`
- Image `img`
- Button `btn`
- ImageButton `imgBtn`
- Custom (Progress-)Bar `UIBar`
- Custom Checkbox `UICheckbox`

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
