# The Live Textbook of Physical Chemistry 2

GitHub repository of the Live Textbook of Physical Chemistry 2 by Dr. Peverati, Florida Institute of Technology.

The book is written in Markdown (`.qmd` files) and built with [Quarto](https://quarto.org). R and RStudio are **not** needed.
The previous bookdown version is preserved on the branch `bookdown`.

---

## How to update and rebuild the book

### 0. One-time setup (new computer)

1. Install Quarto from <https://quarto.org/docs/get-started/> (it includes everything needed for the website and the Typst PDF).
2. For the LaTeX PDF (`pchem2.pdf`), install TinyTeX once:
   ```bash
   quarto install tinytex
   ```
3. Any text editor works. VS Code or Positron with the Quarto extension gives a preview button.

### 1. Edit

- Chapters are `01_Classical.qmd` … `13_Spectroscopy.qmd`; the preface is `index.qmd`.
- The chapter order is the `chapters:` list in `_quarto.yml`.
- New figures go in `img/`. The computed figures are made by the Python scripts in `scripts/` (run them from this folder, e.g. `python3 scripts/make_figures_ch3.py img`).

### 2. Preview while writing

```bash
quarto preview
```

This opens the book in the browser and reloads it every time you save. Stop it with Ctrl+C.

### 3. Build the website and the PDF

```bash
quarto render
```

Everything goes into `docs/` (the website and `docs/pchem2.pdf`). Check for warnings at the end of the output.

### 4. Publish

```bash
git add -A
```

```bash
git commit -m "Describe the change"
```

```bash
git push
```

GitHub Pages serves the `docs/` folder of the `master` branch; the site updates a minute or two after the push.

---

## Writing cheat sheet

| What | How |
|---|---|
| Numbered equation | `$$ E = h\nu $$ {#eq-planck}` |
| Figure | `![Caption.](img/file.png){#fig-name fig-alt="Description for screen readers" width="80%"}` |
| Table | Markdown table, then a line `: Caption. {#tbl-name}` |
| Section label | `## Title {#sec-name}` |
| Reference | `@eq-planck`, `@fig-name`, `@tbl-name`, `@sec-name` (Quarto adds "eq.", "figure", "table", "section", "chapter"). Use `@Fig-name` at the start of a sentence; `[@fig-name]b` for a panel. |
| Unnumbered heading | `## Title {.unnumbered}` |
| Collapsible answers | `::: {.callout-tip collapse="true" icon="false"}` / `## Answers` / … / `:::` |

Every image needs `fig-alt` (accessibility).

---

## Files

- `_quarto.yml`: book settings (title, chapter list, website theme, PDF layout).
- `quarto.css`, `punctuation.html`, `sidebar-toc.html`, `header-pin.html`: website tweaks (top bar with the group logo in light/dark versions, always visible on wide screens, caption contrast, scrollable equations, no line breaks before punctuation after math, expandable chapter sections in the sidebar; `scripts/sidebar_sections.py` collects the sections after each render).
- `_quarto-typst.yml`: optional Typst PDF, `quarto render --profile typst --to typst` (output in `_book-typst/`, not published).
- `_bookdown-archive/`: the former bookdown sources and the conversion script, for reference only.
- `REVISION_CHECKLIST.md`: open items for future revisions.

Old bookdown page names (e.g. `Models.html`) redirect to the new pages (`04_Models.html`).

---

## License

- **Book text and figures:** [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/), see `LICENSE`. You may share and adapt the book for non-commercial purposes, with attribution, under the same license. Commercial reproduction or resale requires the author's permission.
- **Python scripts in `scripts/`:** MIT License, see `scripts/LICENSE`.

This licensing applies from 10 November 2026 (commit after `3b5f684`). Earlier versions of the book remain under the license they were released with (CC BY 4.0 in `LICENSE`; the preface stated CC BY-SA 4.0).
