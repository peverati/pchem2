# Quarto trial

An experimental Quarto version of the book. The bookdown sources in the project root are untouched and remain the master copy.

## Rebuild

From the project root:

```bash
python3 quarto/tools/convert.py
```

(regenerates `quarto/*.qmd` from the `.Rmd` chapters), then from `quarto/`:

```bash
quarto render
```

(HTML and LaTeX PDF in `_book/`), and optionally:

```bash
quarto render --profile typst --to typst
```

(Typst PDF in `_book-typst/`).

## What the converter changes

- Cross-references: `\@ref(eq:x)` → `@eq-x`, `\@ref(fig:x)` → `@fig-x`, `\@ref(tab:x)` → `@tbl-x`, `\@ref(Label)` → `@sec-Label`. Quarto adds the words "eq.", "figure", "chapter", so the preceding word is dropped.
- Figure chunks become Markdown images with `fig-alt`; kable chunks get `tbl-` labels.
- The `<details>` answer blocks become collapsible callouts; examples become `exm-` blocks.
- Old LaTeX idioms are modernized for Typst: `{\bf x}` → `\mathbf{x}`, `{\cal X}` → `\mathcal{X}`, `vmatrix` → `\left|…\right|`, and `$\\$` spacing lines are dropped.

## Known limitations

- **PDF/UA (tagged PDF):** `pdf-standard: ua-1` fails with Quarto's Typst book template (orange-book's outline). Revisit when the template is fixed, or use a custom Typst template.
- Typst PDF and LaTeX PDF use the same filename, so the Typst build uses its own profile and output folder.
