This is the GitHub repository for the Live Textbook of Physical Chemistry 2 by Dr. Peverati, Florida Institute of Technology.

The book is written in Markdown (`.qmd` files) and built with [Quarto](https://quarto.org). R and RStudio are not needed.

## Build

From this folder:

```bash
quarto preview      # live preview while writing
quarto render       # website and PDF (pchem2.pdf) into docs/
```

Then commit and push: GitHub Pages serves the `docs/` folder.

Optional PDF built with Typst (into `_book-typst/`, not published):

```bash
quarto render --profile typst --to typst
```

## Layout

- `index.qmd`, `01_Classical.qmd` … `13_Spectroscopy.qmd`: the chapters, in the order listed in `_quarto.yml`.
- `img/`: figures; `scripts/`: Python scripts that generate the computed figures.
- `quarto.css`, `punctuation.html`: accessibility tweaks (caption contrast, scrollable equations, no line breaks before punctuation after math).
- `_bookdown-archive/`: the former bookdown sources (`.Rmd`) and the script that converted them; kept for reference only.

Old bookdown page names (e.g. `Models.html`) redirect to the new pages (`04_Models.html`).
