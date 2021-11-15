# wurst-table-layout

This library allows you to easily create and align framehandles in a table-ish layout inspired by flex-box.
Table-ish because there are no columns. A table simply consists of rows, which themselves consist of cells which contain a framehandle as content.
After setting up the layout you can apply it to any framehandle.

> The table layout can not be used with scaling

table diagram here

## Basics

The API makes heavy use of the cascade operator to apply changes to the root element.
First create a table layout, passing width and height of relative screen space.
Then start adding rows and cells via `.row()` and `.add()`.
The functions will always work on the most recently added row/cell.

```
new TableLayout(0.3, 0.35)
..row()
..add(p("1"))
..add(p("2"))
..add(p("3"))
.row()
..add(p("4"))
..add(p("5"))
..add(p("6"))
```

## Alignment

By default the alignment in a table is top left. You can adjust horizontal alignment on a per row basis.

```
new TableLayout(0.3, 0.35)
..row()..center()
..add(p("1"))
..add(p("2"))
..add(p("3"))
.row()..end_()
..add(p("4"))
..add(p("5"))
..add(p("6"))
```

## Presets

As you should have noticed from the previous examples we were using the `p()` function, which analagous to html represents a paragraph text element.
Because you cannot use scaling with the table layout, several presets are provided for common types, similar to html tags:

- Headings `h1`, `h2`, `h3`, `h4`
- Paragraph `p`
- Image `img`
- Button `btn`
- ImageButton `imgBtn`
