# Revision Checklist: Live Textbook of P-Chem 2

The status of the November 2026 revision. This file is not part of the book.

| Ch. | File | Title |
|---|---|---|
| 1 | `01_Classical.qmd` | Brief Summary of Classical Physics |
| 2 | `02_Motivation.qmd` | The Failure of Classical Physics |
| 3 | `03_Schrodinger.qmd` | The Schrödinger Equation |
| 4 | `04_Models.qmd` | Analytically Solvable Models |
| 5 | `05_Hydrogen.qmd` | The Hydrogen Atom |
| 6 | `06_Operators.qmd` | Operators, Observables, and Measurements |
| 7 | `07_Spin.qmd` | Spin |
| 8 | `08_Weirdness.qmd` | Quantum Weirdness |
| 9 | `09_Atoms.qmd` | Many-Electron Atoms |
| 10 | `10_Molecules.qmd` | Introduction to Molecules |
| 11 | `11_Bonds.qmd` | The Chemical Bond in Diatomic Molecules |
| 12 | `12_Polyatomic.qmd` | The Chemical Bond in Polyatomic Molecules |
| 13 | `13_Spectroscopy.qmd` | Spectroscopy |
| A | `A1_Math.qmd` | Mathematical Toolkit |
| B | `A2_Constants.qmd` | Physical Constants and Unit Conversions |
| C | `A3_References.qmd` | Further Reading and References |

---

## Open items

- [ ] **Hidden edit/issue links.** "Edit this page" and "Report an issue" disappeared on wide screens when the right-hand column was hidden; they could go in the footer.
- [ ] **Print edition** (see `SELF_PUBLISHING_GUIDE.md`):
  - a new front cover with the print title;
  - a print PDF profile: two-sided layout, 300-dpi figures, answers at the end of each chapter, a copyright page;
  - KDP and IngramSpark.
- [x] **Worked examples**: one step-by-step example per chapter (Ch. 2–13), in collapsible boxes.
- [x] **Chapter summaries**: "Key Ideas" at the start of each chapter review.
- [x] **Older images**: the four H₂⁺/H₂ diagrams of Ch. 11 redrawn (`scripts/make_figures_h2.py`).
- [x] **Interactive figures** (website only): hydrogen radial probability (Ch. 5) and particle-in-a-box superposition (Ch. 6), with sliders.

## Potential additions (parked: not planned; consider only on request)

- Perturbation theory (first order, with helium as the example).
- Helium excited states (singlet vs. triplet, exchange) and periodic trends.
- Anharmonicity, the Morse potential, centrifugal distortion.
- Molecular symmetry and group theory.
- Runnable code or notebooks.

## Not pursued

- **Tagged/accessible PDF.** Accessibility is handled on the website; the PDF is provided as is.

---

## Done (November 2026)

**Platform and publishing**
- [x] Moved from bookdown to Quarto, with the website and PDF built into `docs/`. Old page names redirect. The bookdown version is kept on the `bookdown` branch, and its sources in `_bookdown-archive/`.
- [x] Website:
  - a top bar with the title, GitHub, PDF, dark mode, and the group logo (light and dark versions);
  - a left sidebar with search and expandable chapter sections;
  - no right-hand column;
  - layout tuned for phones.
- [x] PDF: cover page, floating figures, Table 8.1 layout, and a print title page ("Beyond the Classical World").
- [x] License: CC BY-NC-SA 4.0 for the book and MIT for `scripts/`, from 10 November 2026.
- [x] README with the update and publish procedure.

**Structure and content**
- [x] Chapters reordered; the Postulates chapter redistributed.
- [x] New sections throughout:
  - classical waves (Ch. 1);
  - computed figures, the Bohr model, and line spectra (Ch. 2);
  - the meaning of ψ and wave packets (Ch. 3);
  - the 3D box (Ch. 4);
  - commutators and time evolution (Ch. 6);
  - symmetry and quantum numbers (Ch. 7);
  - measurement, interpretations, and the uncertainty relation (Ch. 8);
  - identical particles, variational helium, shielding, and term symbols (Ch. 9);
  - potential energy surfaces and SCF (Ch. 10);
  - second-row and heteronuclear diatomics (Ch. 11);
  - water MOs, Koopmans' theorem, localized orbitals, and Hückel theory (Ch. 12);
  - selection rules, normal modes, Jablonski diagrams, and NMR/ESR (Ch. 13).
- [x] Appendices: mathematical toolkit, constants and conversions, further reading with references.
- [x] All display equations numbered.

**Style (see `STYLE_CHECKLIST.md`)**
- [x] Colloquial, guided style throughout, including rewrites of:
  - Coulomb's law (Ch. 1);
  - all four models (Ch. 4);
  - the hydrogen atom (Ch. 5);
  - Hermitian operators and angular momentum (Ch. 6);
  - symmetry (Ch. 7);
  - tunneling (Ch. 8).
- [x] Misconceptions removed: no orbits, no orbital "shapes", electrons described by orbitals; no Dirac notation.
- [x] Proofs and derivations in collapsible boxes; formulaic openers varied.
- [x] Study questions rewritten: 10 per chapter, 5 choices each.

**Figures and accessibility (website)**
- [x] Over 70 computed figures (scripts in `scripts/`), with no Wikipedia images.
- [x] Alt text, `lang`, caption contrast, keyboard-accessible answers and proofs, scrollable equations, punctuation glued to math, light and dark modes.
