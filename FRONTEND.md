# Front-end

The pages of Miko. There is no design in them yet, that comes from your Figma. Every file has comments that explain what it does.

## Run it

First time on this computer? Follow [GETTING-STARTED.md](GETTING-STARTED.md) first. You don't need the database for the pages.

1. Open a terminal in this folder (the one with `Program.cs`).
2. Type `dotnet watch` and press Enter.
3. Open **http://localhost:5067** in your browser.

Leave `dotnet watch` running. After you save a `.cshtml` or `.css` file, press F5 in the browser to see the change. Stop it with Ctrl+C.

## Where everything is

```
Views/
  Shared/_Layout.cshtml          the frame around every page: sidebar + main
  Shared/_AccountLayout.cshtml   the frame for Sign in and Sign up, no sidebar
  Home/Index.cshtml              Dashboard   localhost:5067/
  Scan/Index.cshtml              Scan        localhost:5067/Scan
  Label/Index.cshtml             Label       localhost:5067/Label
  Train/Index.cshtml             Train       localhost:5067/Train
  Measure/Index.cshtml           Measure     localhost:5067/Measure
  Account/SignIn.cshtml          Sign in     localhost:5067/Account/SignIn
  Account/SignUp.cshtml          Sign up     localhost:5067/Account/SignUp

wwwroot/css/
  base.css         your Figma colours and sizes, and the basics   (every page)
  layout.css       the frame, row and stack, the phone version    (every page)
  components.css   your Figma components: card, button, ...       (every page)
  pages/           one file per page, only for that page
```

## How a page is made

When you open `/Scan`, `Controllers/ScanController.cs` shows `Views/Scan/Index.cshtml`. That file gets put inside `_Layout.cshtml`, where it says `@RenderBody()`. So the sidebar is written once, and each page file only has what goes in main.

A `.cshtml` file is HTML with a few extra lines that start with `@`. You only need three of them:

| Line | What it does |
|---|---|
| `ViewData["Title"] = "Scan";` | the text in the browser tab |
| `@section Styles { ... }` | links the page's own css file from `css/pages/` |
| `@* ... *@` | a comment, the browser never sees it |

HTML and CSS connect through classes: `class="row"` in a page gets its looks from `.row { ... }` in the CSS.

## Figma to CSS

| In Figma | In the CSS |
|---|---|
| Colours and sizes | the variables at the top of `base.css` |
| Auto layout going down | `.stack` |
| Auto layout going sideways | `.row` |
| The gap number | `gap` |
| Fill container | `.fill` |
| A component (card, button) | a class in `components.css` |

## Build it

1. Put your Figma colours and sizes in the variables in `base.css`.
2. Make a class for each Figma component (card, button) in `components.css`.
3. Open a page. The comment in it lists what to build from that Figma frame. Things next to each other go in a `.row`, things under each other in a `.stack`.
4. Something only one page has goes in that page's file in `css/pages/`.
5. Delete the example boxes on the Dashboard when you start on it.

Stuck on why something looks the way it does? Press F12, click the arrow at the top left of that panel, then click the thing on the page. You see its classes and its CSS.
