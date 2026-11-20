# Blocks and components

A small library for the Miko pages. It has two kinds of pieces:

- **Blocks** put things in place: next to each other, under each other, how wide. They are in `wwwroot/css/layout.css`.
- **Components** are the things you see: a card, a button, a bar. They are in `wwwroot/css/components.css`.

You use a piece by copying its HTML into a page. You make it look like your Figma by changing its CSS (section 5). How to run the site is in [FRONTEND.md](FRONTEND.md).

**See them all at localhost:5067/Blocks** (the Blocks link at the bottom of the sidebar). That page shows every piece and a set of row and column layouts, and its file `Views/Blocks/Index.cshtml` has the HTML to copy. It is not part of the app.

## What's in it

| Piece | Class | Kind | Use it for |
|---|---|---|---|
| Row | `row` | block | things next to each other |
| Stack | `stack` | block | things under each other |
| Fill | `fill` | block | a box that takes the space that is left |
| Middle | `middle` | block | a row whose boxes line up in the middle, top to bottom |
| Card | `card` | component | stat cards, dataset cards, sample info, "Where it went wrong" |
| Stat | `stat-number`, `stat-label` | component | cells labelled, accuracy, the percentages |
| Button | `button`, `button-secondary` | component | Take a photo, Start training, Sign in, ... |
| Bar | `bar`, `bar-fill` | component | sharpness, training progress, the bars on Measure |
| Field | `field` | component | Username, Password, choosing a dataset |
| Thumbnails | `thumbnails` | component | the photos on Scan, the cells on Label |
| Box | `box` | component | a dashed stand-in while you build, delete it after |

## 1. The basics: boxes, tags and classes

Every tag on a page is a box. A `<div>` is an empty box with no look of its own, you use it to group things. Boxes go inside boxes, so indent the HTML to see which box is inside which:

```html
<div class="card">          @* the outer box *@
    <h2>Datasets</h2>       @* a box inside it *@
    <p>4 datasets</p>       @* another box inside it *@
</div>                      @* closes the outer box *@
```

The tags you need most:

| Tag | Use it for |
|---|---|
| `<div>` | a box to group things |
| `<h1>` | the page title, once per page |
| `<h2>`, `<h3>` | the title of a part of the page, like a card title |
| `<p>` | text, or a number |
| `<a href="/Scan">` | a link to another page |
| `<button>` | something you click that does something on this page |
| `<img src="..." alt="...">` | a picture, `alt` describes it in words |

Every tag you open you also close: `<div>` ... `</div>`. Only `<img>` and `<input>` have no closing tag.

**Classes connect HTML to CSS.** `class="card"` in the HTML gets its looks from `.card { ... }` in a CSS file. The dot means "class".

- A tag can have more than one class, with a space between: `class="card fill"`.
- Name a class after what it is, in lowercase with dashes: `card`, `dataset-card`, `upload-button`.
- Upper and lower case count: `class="Card"` and `.card { }` do not match.
- A class with no rule in any CSS file does nothing.

**See all the boxes:** put this at the bottom of `base.css`, save, press F5. Every box gets a red line. Delete it when you're done.

```css
* { outline: 1px solid red; }
```

## 2. Space: padding, margin, border and gap

```
              margin: space outside, see-through, pushes other boxes away
        ┌─────────────────────────────────────┐   ← border: the line
        │   padding: space inside the box     │
        │   ┌─────────────────────────────┐   │
        │   │          content            │   │
        │   └─────────────────────────────┘   │
        └─────────────────────────────────────┘
```

| Word | What it is | In Figma |
|---|---|---|
| `padding` | space between the edge of a box and what is inside it. The background colour fills it. | the padding numbers in auto layout |
| `border` | the line around the box | stroke |
| `margin` | space outside the box, pushes other boxes away. It is see-through. | Figma has no margin |
| `gap` | space between the boxes inside a row or stack | the spacing between items in auto layout |

**The rule:** padding for space inside a box, gap for space between boxes. Figma has no margin, so you almost never need it. Browsers do give `h1`, `h2`, `h3` and `p` a margin of their own, so `base.css` removes it. That way all space comes from padding and gap, like in Figma.

**Writing the numbers:** Figma often gives a different number per side.

```css
padding: 16px;                /* all four sides */
padding: 8px 16px;            /* top and bottom 8, left and right 16 */
padding: 8px 16px 24px 32px;  /* top, right, bottom, left: clockwise from the top */
```

`base.css` has `box-sizing: border-box`, so padding stays inside a box's width, the same as in Figma. A 300px card with 16px padding is 300px wide, not 332px.

## 3. Blocks: row, stack and fill

In Figma you use auto layout. In CSS the same thing is called flexbox, and the library has four classes for it:

| Figma | Class | What it does |
|---|---|---|
| auto layout going sideways | `.row` | the boxes inside sit next to each other |
| auto layout going down | `.stack` | the boxes inside sit under each other |
| Fill container | `.fill` | this box takes all the space that is left |
| Alignment: center | `.middle` | goes next to `row`: the boxes line up in the middle, top to bottom. Without it they are all as tall as the tallest one. |

```
.row                                  .stack
┌─────────────────────────────────┐   ┌──────────────┐
│ ┌─────┐ ┌─────┐ ┌─────────────┐ │   │ ┌──────────┐ │
│ │  A  │ │  B  │ │  C  (.fill) │ │   │ │    A     │ │
│ └─────┘ └─────┘ └─────────────┘ │   │ └──────────┘ │
└─────────────────────────────────┘   │ ┌──────────┐ │
                                      │ │    B     │ │
                                      │ └──────────┘ │
                                      └──────────────┘
```

- **Width.** Figma's **Hug contents** = write nothing, a box does that already. **Fill container** = `.fill`. **Fixed** = `width: 240px;` in the box's class.
- **The same width side by side:** give each box `.fill`. Two are half each, three are a third each.
- **`main` is already a stack** (see `_Layout.cshtml`), so the blocks on a page already sit under each other with space between. A `.row` with one thing in it does nothing, leave it out.
- **On a phone** every `.row` turns into a column by itself (the rule at the bottom of `layout.css`).

Use these classes, not `style="display: flex"` and a `margin-top` on each box. That looks the same at first, but the space is different on every page, and the phone rule can't reach it.

### Ready-made layouts

Three ways to put the blocks together that the Miko pages need. Copy one and change what is inside. The Blocks page has more: two and three columns, a fixed column and the rest, columns of stacks, and a title on the left with a button on the right.

**Cards side by side, all the same width** (the stat cards on the Dashboard):

```html
<div class="row">
    <div class="card fill">...</div>
    <div class="card fill">...</div>
    <div class="card fill">...</div>
</div>
```

**A big box with a column of small ones next to it** (the live view with the sample info, the photo with the cell choice):

```html
<div class="row">
    <div class="card fill">the big box</div>

    <div class="stack">
        <div class="card">small 1</div>
        <div class="card">small 2</div>
        <div class="card">small 3</div>
    </div>
</div>
```

**A form** (Sign in, Sign up):

```html
<form method="post" class="stack">
    <label class="field">
        Username
        <input name="Username">
    </label>

    <label class="field">
        Password
        <input type="password" name="Password">
    </label>

    <button class="button">Sign in</button>
</form>
```

## 4. Components

A component is a piece that looks the same everywhere you use it. In Figma it is the purple diamond. In the code it is two things: a class in `components.css` that says how it looks, written once, and a few lines of HTML that you copy onto every page that uses it, with that page's content.

### Card

A white box with round corners. What is inside sits under each other, with a small gap.

```html
<div class="card">
    <h2>Sample A</h2>
    <p>Taken 20 Nov</p>
</div>
```

Things next to each other inside a card: put a `.row` inside it.

### Stat

A big number with a grey label under it. It has no box of its own, put it in a card.

```html
<div class="card">
    <p class="stat-number">92%</p>
    <p class="stat-label">Accuracy</p>
</div>
```

### Button

```html
<button class="button">Take a photo</button>
<button class="button button-secondary">Cancel</button>
<button class="button" disabled>Start training</button>
<a class="button" href="/Label">Label</a>
```

- `button-secondary` is the second kind: white with a coloured line.
- `disabled` fades it and it can't be clicked, like Start training while it trains.
- `<button>` does something on this page. `<a class="button">` goes to another page but looks the same.
- A button is as wide as its text, like Hug contents in Figma.

### Bar

A bar that is partly filled. The width is the only thing you write on the tag with `style`, because it is a number from the data. Later the real number goes there, for example the sharpness.

```html
<div class="bar">
    <div class="bar-fill" style="width: 72%"></div>
</div>
```

### Field

A label with an input or a dropdown under it, for forms.

```html
<label class="field">
    Username
    <input name="Username">
</label>

<label class="field">
    Dataset
    <select name="Dataset">
        <option>Sample A</option>
        <option>Sample B</option>
    </select>
</label>
```

- `name` has to be the same as in the view model, so the controller gets what was typed. The comment in Sign in and Sign up lists the names.
- `type="password"` shows dots instead of the letters.

### Thumbnails

Small square photos next to each other. When the row is full they go to the next line.

```html
<div class="thumbnails">
    <img src="~/images/example.svg" alt="photo 1">
    <img src="~/images/example.svg" alt="photo 2">
</div>
```

`example.svg` in `wwwroot/images/` is a stand-in photo until there are real ones.

### Box

A dashed box so you can see where things sit while you build. Replace it with a card or your own component when you know what goes there.

## 5. Make them look like your Figma

**First the variables** at the top of `base.css`. Every piece uses them, so one change there changes every page.

| Variable | What it changes |
|---|---|
| `--color-background` | the page behind everything |
| `--color-box` | cards, the sidebar, the secondary button |
| `--color-line` | the borders, the empty part of a bar |
| `--color-text` | all text |
| `--color-muted` | grey text, like the stat label |
| `--color-primary` | buttons, the filled part of a bar |
| `--space` | padding in cards, the gap in rows and stacks |
| `--space-small` | the gap inside cards, fields and thumbnails |
| `--radius` | the round corners of everything |

**Then the component itself** in `components.css`: the numbers that belong to one piece, like the font size of `.stat-number`, the height of `.bar` or the size of the thumbnails.

**Your Figma font:** if it is a Google font, copy its `<link>` from fonts.google.com into the `<head>` of both `_Layout.cshtml` and `_AccountLayout.cshtml`, and put its name in `font-family` in `base.css`.

**A variant** (in Figma: the same component, a little different): give it a second class that only changes that bit, the way `button-secondary` does. Write it under the component in `components.css`: when two rules change the same thing, the one further down wins.

```html
<div class="card card-highlight">...</div>
```

```css
/* the card with the coloured line */
.card-highlight {
    border-color: var(--color-primary);
}
```

**Different on one page only:** write the change in that page's file. It loads after `components.css`, so it wins. This makes the buttons full width on Sign in and Sign up, and nowhere else:

```css
/* pages/account.css */
.button {
    width: 100%;
}
```

**A new component:** add it to `components.css` the same way as the others: a comment with what it is and its HTML, then the class. Add it to the table at the top of this file too.

## 6. Shared or page file: where does the CSS go?

`base.css`, `layout.css` and `components.css` are **shared**: every page loads them. The files in `css/pages/` are loaded by one page only.

| File | Loaded on | What goes in it |
|---|---|---|
| `base.css` | every page | your Figma colours, sizes and font, as variables |
| `layout.css` | every page | the frame, the blocks, the phone version |
| `components.css` | every page | anything you use on more than one page |
| `pages/home.css` (and the others) | that one page | things only that page has |

The same goes for HTML: `Views/Shared/_Layout.cshtml` is the frame around every page. Something that is on every page, like the sidebar, goes there once and not into seven page files.

**How to decide:** is it on more than one page in Figma?

- **Yes:** `components.css`.
- **No:** that page's file in `css/pages/`.
- **Not sure yet:** start in the page file. The moment a second page needs it, move it to `components.css`. Cut it, don't copy it.

**Why shared:**

- **Change it once.** The corner of the cards changes in Figma: you change one line and all seven pages follow. With a copy on every page you have to find all of them, and you will miss one.
- **It looks the same everywhere.** One class can't be a little different on one page by accident.
- **The page files stay short.** They only hold what is special about that page, so you find things fast.

**Why not everything shared:** `components.css` becomes one long list where you can't find anything, and a rule meant for one page can change another page that happens to use the same class name.

**Why not `style="..."` on the tag:** it can't be reused, you have to hunt for it in seven files to change it, and the phone rules in `layout.css` can't change it. The bar's width is the one exception. Try things out in F12 (you can edit the CSS live there), then write what works as a class.

## 7. Building a part of a page, step by step

1. In Figma, click the frame and look at its auto layout: which direction, the padding, the gap.
2. On paper, draw the boxes: the outer box first, then what is inside it.
3. Look in the table at the top. Is there a block or component for it? Copy its HTML.
4. Write the HTML from the outside in: `row` or `stack` for the direction, a component class for the looks.
5. Nothing in the library for it? Make a class, in the file from section 6.
6. Copy the numbers from Figma: padding, gap, corner radius, font size, colours. A colour or size you use more than once goes in the variables in `base.css`.
7. Save, press F5. Doesn't look right? F12, click the arrow at the top left of that panel, click the box. You see its classes, its CSS, and its padding and margin in colour.

If Figma shows you CSS (Dev Mode), copy the numbers from it, not the whole thing. It gives every box a fixed width and height, which breaks on other screen sizes.
