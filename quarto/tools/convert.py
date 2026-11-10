"""Convert the bookdown chapters of the Live Textbook of P-Chem 2 to Quarto (.qmd).

Usage (from the project root):  python3 quarto/tools/convert.py
Reads the .Rmd files listed in _bookdown.yml and writes .qmd files into quarto/.
The original bookdown sources are not modified.
"""
import re
import os
import subprocess
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "quarto"
CHAPTERS = ["01_Classical", "02_Motivation", "03_Schrodinger", "04_Models", "05_Hydrogen",
            "06_Operators", "07_Spin", "08_Weirdness", "09_Atoms", "10_Molecules", "11_Bonds",
            "12_Polyatomic", "13_Spectroscopy"]

warnings = []


def r_unescape(s):
    """Undo R string escaping inside fig.cap / fig.alt."""
    return s.replace("\\'", "'").replace("\\\\", "\\")


def opt(header, name):
    m = re.search(name + r"\s*=\s*'((?:[^'\\]|\\.)*)'", header)
    return r_unescape(m.group(1)) if m else None


def convert_figure(m):
    header, path = m.group(1), m.group(2)
    label = re.match(r"\{r\s+([A-Za-z0-9_]+)", header)
    cap, alt, width = opt(header, "fig.cap"), opt(header, "fig.alt"), opt(header, "out.width")
    path = path.replace("./", "")
    attrs = []
    if label and cap is not None:
        attrs.append(f"#fig-{label.group(1)}")
    if alt:
        attrs.append('fig-alt="' + alt.replace('"', "&quot;") + '"')
    if width:
        attrs.append(f'width="{width}"')
    return f"\n![{cap or ''}]({path}){{{' '.join(attrs)}}}\n"


def convert_table(m):
    """Evaluate the knitr::kable call once with R and write a plain Markdown (pipe) table,
    so the converted book no longer needs R."""
    label, body = m.group(1), m.group(2)
    cap = re.search(r',\s*caption\s*=\s*"((?:[^"\\]|\\.)*)"', body)
    body = re.sub(r',\s*caption\s*=\s*"((?:[^"\\]|\\.)*)"', "", body)
    code = "cat(" + body.replace("knitr::kable(", "knitr::kable(format = 'pipe', ", 1) + ', sep = "\\n")'
    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False) as f:   # Rscript -e mangles backslashes
        f.write(code)
    res = subprocess.run(["Rscript", f.name], capture_output=True, text=True)
    os.unlink(f.name)
    if res.returncode != 0:
        warnings.append(f"table {label}: {res.stderr.strip()}")
        return m.group(0)
    caption = r_unescape(cap.group(1)) if cap else ""
    return res.stdout.strip() + f"\n\n: {caption} {{#tbl-{label}}}"


def convert_answers(m):
    ans = m.group(1).strip()
    return ('::: {.callout-tip collapse="true" icon="false"}\n## Answers\n\n' + ans + "\n:::")


def convert_example(m):
    label, body = m.group(1), m.group(2)
    body = re.sub(r"(?m)^> ?", "", body)
    return f"::: {{#exm-{label}}}\n{body.strip()}\n:::"


PREFIX_WORDS = {
    "eq": r"(?:[Ee]qs?\.|[Ee]quations?)\s+",
    "fig": r"(?:[Ff]igures?)\s+",
    "tab": r"(?:[Tt]ables?)\s+",
    "sec": r"(?:[Cc]hapters?|[Ss]ections?)\s+",
}


def convert_refs(text):
    # typed references with a preceding word ("eq. \@ref(eq:x)" -> "@eq-x"; capitalized if the word was)
    for kind, qkind in (("eq", "eq"), ("fig", "fig"), ("tab", "tbl")):
        def repl(m, qkind=qkind):
            cap = m.group(1)[0].isupper() if m.group(1) else False
            pre = qkind[0].upper() + qkind[1:] if cap else qkind
            ref = f"@{pre}-{m.group(2)}"
            nxt = m.string[m.end():m.end() + 1]
            return f"[{ref}]" if nxt.isalnum() else ref
        text = re.sub(r"(" + PREFIX_WORDS[kind] + r")?\\@ref\(" + kind + r":([A-Za-z0-9_\-]+)\)", repl, text)
    # section / chapter references
    def srepl(m):
        cap = m.group(1)[0].isupper() if m.group(1) else False
        ref = f"@{'Sec' if cap else 'sec'}-{m.group(2)}"
        nxt = m.string[m.end():m.end() + 1]
        return f"[{ref}]" if nxt.isalnum() else ref
    text = re.sub(r"(" + PREFIX_WORDS["sec"] + r")?\\@ref\(([A-Za-z0-9_\-]+)\)", srepl, text)
    return text


def modernize_math(s):
    """Replace old LaTeX idioms that newer engines (e.g., Typst via Pandoc) cannot convert."""
    s = re.sub(r"\{\\bf\s*([^{}]+?)\}", r"\\mathbf{\1}", s)
    s = re.sub(r"\{\\cal\s*([^{}]+?)\}", r"\\mathcal{\1}", s)
    s = re.sub(r"\\hat\\mathbf\{([^{}]+)\}", r"\\hat{\\mathbf{\1}}", s)
    s = s.replace("\\begin{vmatrix}", "\\left|\\begin{matrix}").replace("\\end{vmatrix}", "\\end{matrix}\\right|")
    s = re.sub(r"(?m)^\$\\\\\$\s*$", "", s)        # lines containing only $\\$ (spacing hack)
    return s


def convert(src):
    s = modernize_math(src)
    # figure chunks
    s = re.sub(r"```(\{r[^\n]*\})\nknitr::include_graphics\('([^']+)'\)\n```", convert_figure, s)
    # kable tables
    s = re.sub(r"```\{r ([A-Za-z0-9_]+), echo=FALSE\}\n(knitr::kable\(.*?\n\))\n```", convert_table, s, flags=re.S)
    # answer reveal blocks
    s = re.sub(r"`r if \(knitr::is_html_output\(\)\) \{\n  '\n  <details><summary>Answers \(select to reveal\)</summary>\n(.*?)\n  </details>\n  '\n\} else if \(knitr::is_latex_output\(\)\) \{\n  '[^']*'\n\}`",
               convert_answers, s, flags=re.S)
    # example blocks
    s = re.sub(r"> ```\{example, ([A-Za-z0-9_]+)\}\n(.*?)\n> ```", convert_example, s, flags=re.S)
    # equations: \begin{equation} body (\#eq:label) \end{equation}  ->  $$ body $$ {#eq-label}
    def eq(m):
        body = m.group(1).rstrip()
        lab = re.search(r"\(\\#eq:([A-Za-z0-9_\-]+)\)", body)
        body = re.sub(r"\s*\(\\#eq:[A-Za-z0-9_\-]+\)\s*", "\n", body).strip()
        return "$$\n" + body + "\n$$" + (f" {{#eq-{lab.group(1)}}}" if lab else "")
    s = re.sub(r"\\begin\{equation\}\s*\n?(.*?)\\end\{equation\}", eq, s, flags=re.S)
    # headers: {#Label} -> {#sec-Label}; {-} -> {.unnumbered}
    s = re.sub(r"(?m)^(#+ .*?)\s*\{#([A-Za-z0-9_\-]+)\}\s*\{-\}\s*$", r"\1 {#sec-\2 .unnumbered}", s)
    s = re.sub(r"(?m)^(#+ .*?)\s*\{-\}\s*$", r"\1 {.unnumbered}", s)
    s = re.sub(r"(?m)^(#+ .*?)\s*\{#([A-Za-z0-9_\-]+)\}\s*$", r"\1 {#sec-\2}", s)
    s = convert_refs(s)
    for left in re.findall(r"\\@ref\([^)]*\)", s):
        warnings.append(left)
    if "knitr::" in s.replace("knitr::kable", ""):
        warnings.append("leftover knitr call")
    return s


def main():
    for ch in CHAPTERS:
        src = (ROOT / f"{ch}.Rmd").read_text()
        (OUT / f"{ch}.qmd").write_text(convert(src))
    idx = (ROOT / "index.Rmd").read_text()
    idx = idx.split("---", 2)[2]  # drop YAML (moved to _quarto.yml)
    idx = idx.replace("\\renewcommand{\\arraystretch}{1.8}\n", "")
    (OUT / "index.qmd").write_text(convert(idx))
    print("converted", len(CHAPTERS), "chapters;", len(warnings), "warnings")
    for w in sorted(set(warnings)):
        print("  ", w)


if __name__ == "__main__":
    sys.exit(main())
