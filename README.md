# wurst-table-layout

![chrome_EkMQO3cJuA](https://user-images.githubusercontent.com/1486037/142081152-42348ece-7cfb-47db-a4e2-c9d552537f02.png)


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

![Photoshop_oXmHmp3h1B](https://user-images.githubusercontent.com/1486037/142065401-1f754d8d-5bf8-4376-baec-e608eef57f83.png)


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

![Warcraft_III_ZMlsVQqqxX](https://user-images.githubusercontent.com/1486037/142065460-35d1eb89-ecb9-4573-9f4e-5438e947d8ec.png)


## Padding

By default cells have no padding, making them appear right next to each other. We can introduce some space between the cells by adding padding to each of the four sides left, right, top and bottom.

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

![Warcraft_III_1R8F91NBJl](https://user-images.githubusercontent.com/1486037/142065499-73aabd15-1da1-4173-b081-ed1c6130ecfb.png)


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

![Warcraft_III_GEeA1xkx1e](https://user-images.githubusercontent.com/1486037/142065518-b15fe6dd-579f-4616-a7bc-28d243a986eb.png)


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

![Warcraft_III_iajLsjehEv](https://user-images.githubusercontent.com/1486037/142065527-b0fe678f-078f-4113-90b3-a0236b3cb7cc.png)

