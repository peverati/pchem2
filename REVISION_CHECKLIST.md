# Revision Checklist — Live Textbook of P-Chem 2

Status of the improvements identified in the November 2026 review. Effort: **S** = under an hour, **M** = a few hours, **L** = a day or more. This file is not part of the Quarto build.

Chapter numbers below refer to the **current** structure of the book:

| Ch. | File | Title |
|---|---|---|
| 1 | `01_Classical.qmd` | Brief Summary of Classical Physics |
| 2 | `02_Motivation.qmd` | The Failure of Classical Physics |
| 3 | `03_Schrodinger.qmd` | The Schrödinger Equation |
| 4 | `04_Models.qmd` | Analytically Solvable Models |
| 5 | `05_Hydrogen.qmd` | The Hydrogen Atom |
| 6 | `06_Operators.qmd` | Operators and Mathematical Background |
| 7 | `07_Spin.qmd` | Spin |
| 8 | `08_Weirdness.qmd` | Quantum Weirdness |
| 9 | `09_Atoms.qmd` | Many-Electron Atoms |
| 10 | `10_Molecules.qmd` | Introduction to Molecules |
| 11 | `11_Bonds.qmd` | The Chemical Bond in Diatomic Molecules |
| 12 | `12_Polyatomic.qmd` | The Chemical Bond in Polyatomic Molecules |
| 13 | `13_Spectroscopy.qmd` | Spectroscopy |

(The former Postulates chapter was removed; its content was moved to Ch. 4, 6, 8, and 9.)

---

## Open items

- [ ] **Perturbation theory** (M), next to the variational method in Ch. 9: first-order energy correction, with helium's electron repulsion as the example (the $-7{,}220$ kJ/mol value is exactly this).
- [ ] **Ch. 9 extras** (M): helium excited states (singlet vs. triplet, exchange) and the periodic table / ionization-energy trends.
- [ ] **Anharmonicity and the Morse potential; centrifugal distortion** (M), in Ch. 13.
- [ ] **Molecular symmetry and group theory** (L), if the course covers it.
- [ ] **Use the bibliography** (M). `book.bib` exists but no citations are used. Add citations and a short "Further reading" list per chapter.
- [ ] **Accessibility of the PDF** (M–L). The HTML version is done; the PDF is not tagged (PDF/UA fails with the Quarto Typst book template). Also check the site with WAVE or axe on the live site.
- [ ] **Runnable code** (L, optional). Candidates: plot particle-in-a-box and harmonic-oscillator states for any $n$; interactive hydrogen radial probability; a minimal SCF loop for water (Ch. 12); a simulated CO rovibrational spectrum (Ch. 13). The figure scripts in `scripts/` are a starting point.
- [ ] **Practice problems** — not in the book by design: they will be on the companion website.

---

## Done (November 2026)

**Structure**
- [x] Chapters 1 and 2 swapped; Postulates chapter removed and redistributed; `12b_Polyatomic` renumbered as Ch. 12 and Spectroscopy as Ch. 13; `_bookdown.yml` key fixed (`rmd_files`).

**Consistency**
- [x] Review questions aligned with their chapters in every chapter (and several replaced, e.g., Ch. 11 Q10, Ch. 8 Q4).
- [x] Particle-in-a-box normalization derived (Ch. 4); Born's interpretation and the normalization condition introduced in Ch. 3.
- [x] 2s–2p splitting explained by penetration (Ch. 9), as promised in Ch. 5.
- [x] Atomic units introduced once in Ch. 5 and referenced from Ch. 9 and 11.
- [x] Commutators: $[\hat{x},\hat{p}]=i\hbar$ and the common-eigenfunction theorem in Ch. 6; Ch. 7 points back to them; general uncertainty relation $\sigma_A\sigma_B\geq\frac{1}{2}|\langle[\hat{A},\hat{B}]\rangle|$ and a correct energy–time note in Ch. 8.
- [x] No Dirac notation (kets removed; Slater determinants written as $|\chi_1\,\chi_2\cdots|$).
- [x] Notation: $\alpha/\beta$ spin functions, $g$ for gravity, $m_\ell$ for the quantum number, `\text{Å}`, energies in kJ/mol alongside $E_h$, eV, or cm$^{-1}$.
- [x] Orbitals "describe" electrons (no "placing electrons in orbitals").
- [x] Preface updated (by the author).

**New content**
- [x] Ch. 1: classical waves; rewritten Hamiltonian section (Lagrangian reduced to a mention).
- [x] Ch. 2: computed black-body and photoelectric figures, Bohr model and line spectra, summary table.
- [x] Ch. 3: meaning of the wave function, plane waves, wave packets.
- [x] Ch. 4: 3D box (separation of variables, degeneracy).
- [x] Ch. 6: expectation values explained; commuting operators; time evolution of superpositions.
- [x] Ch. 7: Stern–Gerlach, sequential experiments, spin-cone, and parity figures.
- [x] Ch. 8: measurement and collapse; interpretations; new slit, which-way, uncertainty, and tunneling figures.
- [x] Ch. 9: identical particles, variational helium, shielding and penetration, term symbols, Hund's rules, spin–orbit coupling, correlation.
- [x] Ch. 10: potential energy surfaces and reaction coordinate; Fock operator; SCF.
- [x] Ch. 11: H$_2^+$ orbital analysis, beyond Hartree–Fock (CI), second-row and heteronuclear diatomics (HF, CO).
- [x] Ch. 12: symmetry, water MO diagram, Koopmans, localized orbitals, Hückel theory.
- [x] Ch. 13: selection rules, polyatomic vibrations, Jablonski diagram, NMR and ESR.

**Figures, voice, and accessibility**
- [x] Over 70 computed figures (scripts in `scripts/`); no Wikipedia images left.
- [x] Borrowed passages (ChatGPT, Sherrill, Cramer, Wikipedia) rewritten in the author's voice.
- [x] HTML accessibility: alt text on all images, `lang: en`, keyboard-accessible answers, descriptive links, caption contrast, scrollable wide equations, no line breaks before punctuation after inline math.
