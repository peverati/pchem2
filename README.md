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
| Proof or derivation box (blue, closed) | `::: {.callout-note collapse="true" icon="false"}` / `## Proof: …` (or `## Derivation: …`, `## Details: …`) / … / `:::` |
| Worked example (numbered, green, collapsible; open in the PDF) | `::: {#tip-label .callout-tip collapse="true" icon="false"}` / `## Title` / … / `:::` (appears as "Example 4.1: Title"; reference it with `@tip-label`) |
| Key Ideas | `### Key Ideas` with 5–6 bullets, right after `## Chapter Review {#sec-revN}` |
| Study questions | 10 per chapter, 5 options (`a.`–`e.`, each line ending with two spaces), `---` between questions, answers in the collapsible box |
| Website-only content | `::: {.content-visible when-format="html"}` / … / `:::` (used for the interactive figures) |
| Interactive figure | an `{ojs}` cell with `//| echo: false`; plots use `Plot.plot({style: {fontSize: "14px", color: "var(--bs-body-color)", background: "transparent"}, …})` so they work in light and dark mode |
| PDF-only small table | wrap the table in `` ```{=latex} `` blocks with `\begingroup\footnotesize\hyphenpenalty=10000` … `\endgroup`, and add `tbl-colwidths="[…]"` to the caption |

Every image needs `fig-alt` (accessibility). The writing style and content rules are summarized in `STYLE_CHECKLIST.md`.

---

## Files

- `_quarto.yml`: book settings (title, chapter list, website theme, PDF layout).
- `quarto.css`, `punctuation.html`, `sidebar-toc.html`, `header-pin.html`: website tweaks (top bar with the title, a "Report an issue" link, and the group logo in light/dark versions, always visible on wide screens, caption contrast, scrollable equations, no line breaks before punctuation after math, expandable chapter sections in the sidebar; `scripts/sidebar_sections.py` collects the sections after each render).
- **Interactive figures** (website only, Observable JS inside the chapters): building a wave packet and its spreading (Ch. 3), hydrogen radial probabilities (Ch. 5), a particle-in-a-box superposition (Ch. 6), the uncertainty principle and a tunneling simulation (Ch. 8), Hückel π levels (Ch. 12), rotational populations and spectra (Ch. 13). They are hidden in the PDF, which keeps the static figures.
- `scripts/`: Python scripts for the computed figures (e.g., `make_figures_h2.py` for the Ch. 11 diagrams); `scripts/notebooks/` holds the Jupyter notebooks for the hydrogen orbitals, spherical harmonics, and model figures (its README says which cell makes which image).
- `_quarto-typst.yml`: optional Typst PDF, `quarto render --profile typst --to typst` (output in `_book-typst/`, not published).
- `_bookdown-archive/`: the former bookdown sources and the conversion script, for reference only.
- `REVISION_CHECKLIST.md`: open items and parked ideas; `STYLE_CHECKLIST.md`: the completed style audit and the style rules.

Old bookdown page names (e.g. `Models.html`) redirect to the new pages (`04_Models.html`).

---

## License

- **Book text and figures:** [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/), see `LICENSE`. You may share and adapt the book for non-commercial purposes, with attribution, under the same license. Commercial reproduction or resale requires the author's permission.
- **Python scripts in `scripts/`:** MIT License, see `scripts/LICENSE`.

This licensing applies from 10 November 2026 (commit after `3b5f684`). Earlier versions of the book remain under the license they were released with (CC BY 4.0 in `LICENSE`; the preface stated CC BY-SA 4.0).
