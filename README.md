# Physical chemistry Quarto book template

Copy this folder when you want to start a new Quarto book with the same layout as `physchem_book`. It contains the theme, fonts, callouts, and example content needed to render on its own; nothing elsewhere in the original repository is required.

## What is included

- Responsive book navigation and a table of contents
- Flatly and Darkly themes for light and dark mode
- STIX Two Text for body copy and Roboto Condensed for headings
- STIX Two Math for native MathML and STIX 2 output from MathJax
- Local fonts embedded in both the HTML and EPUB editions
- The  `custom-callout` extension used by the source book ([source here](https://github.com/simenkva/custom-callout))
- `fact`, `visualization`, `learning-goals`, and `preparations` callouts are provided for reference, but custom callouts can be customized in `_quarto.yml`
- Figure lightboxes, margin content, cross-references, citations, and code blocks
- A cover image and EPUB download link

The project files are self-contained, including the extension, icons, artwork, stylesheets, and fonts. There is one network dependency: the HTML edition loads MathJax 4 from jsDelivr. If the book must work entirely offline, point the MathJax URL in `_quarto.yml` to a local installation.

## Requirements

- [Quarto](https://quarto.org/) 1.9.38 or newer. This template was last tested with Quarto 1.9.38.
- A modern browser for the HTML edition
- An EPUB reader for the ebook edition

The example has no executable code cells, so it does not need Python, R, or Jupyter. Install an engine only when you add content that uses it.

## Build the book

From this folder, start a live preview with:

```sh
quarto preview
```

Quarto watches the source files and rebuilds pages as you edit. For a complete build without the preview server, run:

```sh
quarto render
```

Both commands write to `_book/`. Open `_book/index.html` for the HTML edition; the EPUB file is in the same directory.

To build one format at a time:

```sh
quarto render --to html
quarto render --to epub
```

## Start a new book

1. Set the title, subtitle, author, and date in `_quarto.yml`.
2. Replace `figures/cover.png`, or change both `cover-image` entries in `_quarto.yml`.
3. Replace the sample text in `index.qmd` and `chapter.qmd`.
4. Add new chapters to `book.chapters` in `_quarto.yml`.
5. Put BibTeX records in `references.bib` and cite them as `@citation-key`.
6. Keep `references.qmd` as the final chapter if you want Quarto to generate a bibliography page.

A short chapter list looks like this:

```yaml
book:
  chapters:
    - index.qmd
    - chapter.qmd
    - your-new-chapter.qmd
    - references.qmd
```

## Fonts

The active font setup in `_brand.yml` uses the `.woff2` files in `fonts/`. Quarto builds the font declarations for HTML, while the `epub-fonts` list in `_quarto.yml` and the rules in `epub_styles.css` embed and apply the same families in EPUB.

There is also a commented Bunny Fonts setup in `_brand.yml`. To use it, comment out the local `fonts:` block and uncomment the Bunny block. This gives the HTML edition a network dependency; the EPUB configuration remains local.

## Custom callouts

The callouts are configured in `_quarto.yml` and rendered by the vendored extension in `_extensions/simenkva/custom-callout/`.

```markdown
:::learning-goals
- First learning goal
- Second learning goal
:::

:::preparations
List prerequisite ideas or reading here.
:::

:::fact
## Optional custom heading

Place an important result here.
:::

:::visualization
Link to an interactive app or another teaching resource.
:::
```

Callout colors and icon paths live under `custom-callout` in `_quarto.yml`. If you share the project, keep the matching files in `icons/` with it.

## Figures, margin notes, and dark mode

SVG files are inverted automatically in dark mode. Add `.dark-invert` to apply the same treatment to a container or another kind of visual:

```markdown
![Caption](figures/example.svg){.dark-invert}
```

For a margin note, use `.column-margin`:

```markdown
:::{.column-margin}
This note appears in the margin on wide screens.
:::
```

On narrow screens, margin content moves into the main reading flow.

## Project structure

```text
book_template/
├── _extensions/       Vendored custom-callout extension
├── figures/           Cover and example artwork
├── fonts/             Local font files and license texts
├── icons/             Custom-callout icons
├── _brand.yml         HTML typography and font sources
├── _quarto.yml        Book structure and output settings
├── styles.css         Shared HTML behavior
├── math_spacing.css   Display-math spacing
├── mathjax-config.html
├── epub_styles.css    EPUB typography and dark-mode rules
├── LICENSE            MIT license for the template
├── index.qmd
├── chapter.qmd
├── references.qmd
└── references.bib
```

Do not remove `_extensions`, `icons`, or the style files unless you also remove their references from `_quarto.yml`.
