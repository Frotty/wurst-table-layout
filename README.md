# wurst-table-layout

This library allows you to easily create and align framehandles in a table-ish layout inspired by flex-box.
Table-ish because there are no columns. A table simply consists of rows, which themselves consist of cells which contain a framehandle as content.
After setting up the layout you can apply it to any framehandle.

> The table layout can not be used with scaling

![Diagram](https://user-images.githubusercontent.com/1486037/141851102-390b7136-41b1-4b8f-9197-be286a7a4ba5.png)

## Basics

The layout is applied to a framehandle which becomes the base frame all other framehandles are children of.
You can either provide your own or use the default escape menu border which is race dependent.

```
// Default parent
new TableLayout(0.3, 0.35)
..createFrame()
```

SCREENSHOT HERE

```
// Provide custom parent
new TableLayout(0.3, 0.35)
..applyTo(yourCustomFrame)
```

## Rows and Cells

The API makes heavy use of the cascade operator to apply changes to the root element.
First create a table layout, passing width and height of relative screen space.
Then start adding rows and cells via `.row()` and `.add()`.
The functions will always work on the most recently added row/cell.

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

SCREENSHOT HERE

## Padding

by default cells have no padding, making them appear right next to each other. We can introduce some space between the cells by adding padding to each of the four sides left, right, top and bottom.

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

SCREENSHOT HERE

## Alignment

By default the alignment in a table is top left. You can adjust horizontal alignment on a per row basis.

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

SCREENSHOT HERE

You can also make certain cells grow horizontally. This can be used to distribute cells evenly.

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

SCREENSHOT HERE

## Presets

As you should have noticed from the previous examples we were using the `p()` function, which analagous to html represents a paragraph text element.
Because you cannot use scaling with the table layout, several presets are provided for common types, similar to html tags:

- Headings `h1`, `h2`, `h3`, `h4`
- Paragraph `p`
- Image `img`
- Button `btn`
- ImageButton `imgBtn`

```
new TableLayout(0.2, 0.25)
..row()
..add(h1("h1"))
..row()
..add(h2("h2"))
..row()
..add(h3("h3"))
..row()
..add(h4("h4"))
..row()
..add(p("paragraph"))
..row()
..add(img(Icons.bTNAcorn1))
..row()
..add(btn("button")..setWidth(0.125))
..row()
..add(imgBtn(Icons.bTNHumanBuild))
..createFrame()
```

SCREENSHOT HERE
