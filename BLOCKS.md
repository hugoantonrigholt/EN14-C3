# Building blocks

A page is boxes inside boxes. This file explains how to make them: what a box is, how boxes line up (row and stack), the space around them (padding, margin, gap), components, and which CSS file each rule goes in.

How to run the site is in [FRONTEND.md](FRONTEND.md).

## 1. Everything is a box

Every tag on a page is a box. A `<div>` is an empty box with no look of its own. You use it to group things that belong together.

Boxes go inside boxes. Indent the HTML so you can see which box is inside which:

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

**See all the boxes:** put this at the bottom of `base.css`, save, press F5. Every box gets a red line. Delete it when you're done.

```css
* { outline: 1px solid red; }
```

## 2. Classes connect HTML to CSS

`class="card"` in the HTML gets its looks from `.card { ... }` in a CSS file. The dot means "class".

```html
<div class="card">...</div>
```

```css
.card {
    padding: var(--space);
    background: var(--color-box);
}
```

- A tag can have more than one class, with a space between: `class="card fill"`.
- Name a class after what it is, in lowercase with dashes: `card`, `stat-card`, `upload-button`.
- Upper and lower case count: `class="KPI"` and `.kpi { }` do not match.
- A class with no rule in any CSS file does nothing.

## 3. Row, stack and fill

In Figma you use auto layout. In CSS the same thing is called flexbox, and this project has three classes for it in `layout.css`:

| Figma | Class | What it does |
|---|---|---|
| auto layout going sideways | `.row` | the boxes inside sit next to each other |
| auto layout going down | `.stack` | the boxes inside sit under each other |
| Fill container | `.fill` | this box takes all the space that is left |

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

Rows and stacks go inside each other. A big box on the left with three small boxes under each other on the right is a row with a stack inside:

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

Write it with `.row` and `.stack`, not with `style="display: flex"` and a `margin-top` on each box. It does the same thing, but the space between the boxes is the same on every page, and on a phone `.row` turns into a column by itself (that rule is at the bottom of `layout.css`).

Two more things:

- `main` is already a `.stack` (see `_Layout.cshtml`), so the blocks on a page already sit under each other with space between. A `.row` with one thing in it does nothing, leave it out.
- Width in Figma: **Hug contents** = write nothing, that is what a box does already. **Fill container** = `.fill`. **Fixed** = `width: 240px;` in the box's class.

## 4. Padding, margin, border and gap

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
| `gap` | space between the boxes inside a `.row` or `.stack` | the spacing between items in auto layout |

**The rule:** padding for space inside a box, gap for space between boxes. Figma has no margin, so you almost never need it. This project only uses margin twice: `margin: 0` on the body and `margin: 0 auto` to put the sign-in form in the middle.

**Space you didn't make:** browsers give `h1`, `h2` and `p` their own margin, top and bottom. If a card has more space than in Figma, that is probably it. Remove it in your class:

```css
.card h2 {
    margin: 0;   /* only the h2's inside a .card */
}
```

**Writing the numbers:** Figma often gives different numbers per side.

```css
padding: 16px;                /* all four sides */
padding: 8px 16px;            /* top and bottom 8, left and right 16 */
padding: 8px 16px 24px 32px;  /* top, right, bottom, left: clockwise from the top */
```

Use a variable from `base.css` (`var(--space)`) instead of a number when the same size comes back in many places. Need another size? Add it to the variables in `base.css`, for example `--space-small: 8px;`.

`base.css` has `box-sizing: border-box`, so padding stays inside a box's width, the same as in Figma. A 300px card with 16px padding is 300px wide, not 332px.

## 5. Components

A component is a piece that looks the same everywhere you use it: a card, a button, a stat. In Figma it is the purple diamond. In the code it is two things:

1. **one class in `components.css`**: how it looks, written once.
2. **the same few lines of HTML** on every page that uses it: what is in it.

```css
/* components.css */
/* the white card with round corners from figma */
.card {
    padding: var(--space);
    background: var(--color-box);
    border: 1px solid var(--color-line);
    border-radius: 12px;
}
```

```html
@* Views/Home/Index.cshtml *@
<div class="card">
    <h2>Datasets</h2>
    <p>4 datasets</p>
</div>

@* Views/Train/Index.cshtml: same class, different content *@
<div class="card">
    <h2>Last training</h2>
    <p>92% correct</p>
</div>
```

Parts inside a component get a name that starts with the component's name, so they stay together: `.card-title`, `.card-number`.

A component that looks a little different somewhere (a Figma variant) gets a second class that only changes that bit:

```html
<button class="button button-primary">Train</button>
```

```css
.button {
    padding: 8px 16px;
    border-radius: 8px;
}

/* the filled version, only the colours are different */
.button-primary {
    background: var(--color-primary);  /* add --color-primary to base.css first */
    color: white;
}
```

`.box` in `components.css` is a stand-in. Replace it with your own components.

## 6. Shared or page file: where does the CSS go?

`base.css`, `layout.css` and `components.css` are **shared**: every page loads them. The files in `css/pages/` are loaded by one page only.

| File | Loaded on | What goes in it |
|---|---|---|
| `base.css` | every page | your Figma colours, sizes and fonts, as variables |
| `layout.css` | every page | the frame, `.row`, `.stack`, `.fill`, the phone version |
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

**Why not `style="..."` on the tag:** it can't be reused, you have to hunt for it in seven files to change it, and the phone rules in `layout.css` can't change it. Try things out in F12 (you can edit the CSS live there), then write what works as a class.

## 7. Building one block, step by step

1. In Figma, click the frame and look at its auto layout: which direction, the padding, the gap.
2. On paper, draw the boxes: the outer box first, then what is inside it.
3. Write the HTML from the outside in. Give each box `row` or `stack` for its direction, and a component class for its looks.
4. Is there a class for it already? Use it. Is there none? Make one, in the file from section 6.
5. Copy the numbers from Figma: padding, gap, corner radius, font size, colours. A colour or size you use more than once goes in the variables in `base.css`.
6. Save, press F5. Doesn't look right? F12, click the arrow at the top left of that panel, click the box. You see its classes, its CSS, and its padding and margin in colour.

If Figma shows you CSS (Dev Mode), copy the numbers from it, not the whole thing. It gives every box a fixed width and height, which breaks on other screen sizes. |
