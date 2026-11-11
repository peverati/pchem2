# Style checklist: P-Chem 2

The reference style, from the preface and P-Chem 1:

- **Voice:** colloquial and guided ("we", "let's", "notice that"). Walk the student through each step instead of dropping results on them.
- **Rigor:** precise, even when that means breaking misleading conventions. Electrons are *described by* orbitals and are not *in* them; orbitals have no definite 3D "shape"; no classical orbits.
- **Math:** for a math-shy audience. Give every equation a sentence of meaning, avoid "it can be shown", and never present a polynomial family without saying what to take away from it.

Line numbers refer to the `.qmd` files as of 11 November 2026. Priority: **H** = clashes with the style or the content rules, **M** = dense or dry, but correct.

| Chapter | Verdict |
|---|---|
| 1 Classical | OK (Coulomb's law rewritten) |
| 2 Motivation | OK |
| 3 Schrödinger | OK |
| 4 Models | OK (box, ring, sphere, oscillator rewritten) |
| 5 Hydrogen | OK (rewritten) |
| 6 Operators | mostly OK |
| 7 Spin | OK (last section rewritten, kept in Ch. 7) |
| 8 Weirdness | OK (tunneling rewritten) |
| 9 Atoms | OK |
| 10 Molecules | OK |
| 11 Bonds | OK |
| 12 Polyatomic | OK (one heading) |
| 13 Spectroscopy | OK |
| Appendices | OK |

## Items

- [x] **H — Ch. 5, intro (`05_Hydrogen.qmd` 7–46).** Opens with "a proton … orbited by an electron", which is a classical orbit in the first sentence. It then gives the Laplacian as "the divergence of the gradient", and the radial solutions with associated Laguerre polynomials, with no guidance. Rewrite as a guided setup: what the equation is, why it separates, and what the solutions look like. Move the formulas to the "Radial Wave Functions" section.
- [x] **H — Ch. 5, quantum numbers (155–161).** "ℓ … determines orbital shape", "the 'shape of the orbital'", "m_ℓ specifies the orientation of the orbital in space". Replace with angular momentum language: ℓ fixes the magnitude of the angular momentum and the number of angular nodes; m_ℓ fixes its z-component.
- [x] **H — Ch. 5, "Building the Complete Orbital" (166–217).** AI-flavored: bold "crucial point", "familiar dumbbell shapes", "electron density probability clouds", "stochastic 'electron cloud' model". The key message, that orbital pictures are not physical objects, is buried in caveats. Rewrite it shorter, in your voice, stating the message plainly up front, and keep the three plot types as short examples.
- [x] **H — Ch. 5, "Experimental Access to Orbitals" (219–227).** It overclaims, for example "electron microscopy" measuring |ψ|², and attosecond experiments "confirming" phases, with bullet-list hype. Either trim it to two careful sentences (orbitals are not observables; what experiments see are densities and ionization energies, see Koopmans in Ch. 12) or cut it.
- [x] **H — Ch. 4, particle on a sphere (`04_Models.qmd` 329–436).** "After a little effort, the eigenfunctions can be shown to be…" plus Legendre polynomials, then a wall of nine Y_ℓ^m formulas as plain lines. The visualization text is AI-flavored: "presents the same challenges … amplified by dimensionality", "Crucially", "each ℓ manifold", "it's clearly shown", plus repeated "the lobes are not…" disclaimers. Cut it to: what Y_ℓ^m depends on, two or three examples, one figure explanation, one clear caveat.
- [x] **M — Ch. 4, particle on a ring, visualization (282–325).** Same AI tone: "intrinsically 1D", bullet lists of axes, "excellent for identifying nodal positions". Shorten.
- [x] **M — Ch. 4, harmonic oscillator (439–489).** "After some effort, the eigenfunctions are…" with Hermite polynomials and no guidance. It also uses μ in ω = √(k/μ) where the TISEq uses m. Add a sentence on why the solution has the Gaussian-times-polynomial form, and make the notation consistent.
- [x] **M — Ch. 4, PIB analysis (142–163).** Dense bold bullets with a closing paragraph ("The connection … is fundamental … reflecting their increased kinetic energy") that reads generated. Light trim.
- [x] **H — Ch. 8, tunneling (`08_Weirdness.qmd` 135–176).** A rigor problem: it imposes only continuity of ψ, not of ψ′, then "derives" A = 0. It names a coefficient E, which clashes with the energy, and says "potentially intractable problem". Rewrite as a qualitative and honest treatment: decay inside the barrier ∝ e^(−αx), transmission ≈ e^(−2αl), with no fake derivation.
- [x] **H — Ch. 7, "Operators Commuting with the Hamiltonian" (`07_Spin.qmd` 142–260).** Formal, encyclopedic, and off-topic for a spin chapter, with "good quantum number", "Coulomb symmetry", and non-breaking hyphens (a sign of pasted text). Either condense it into a one-page "where quantum numbers come from" summary, or move it to Ch. 6 next to commuting operators.
- [x] **M — Ch. 7, Pauli spin commutators and proof.** Proof moved to a collapsible box (as are the proofs in Ch. 9, 10, 11, 13).
- [x] **M — Ch. 1, Coulomb's law (`01_Classical.qmd` 144–199).** Wikipedia-derived: `\textstyle` everywhere, the vector form, and "vector field that associates to each point…". Trim it to the scalar law, the potential energy (the one used later), and one sentence on the field.
- [x] **M — Ch. 6, Hermitian operators.** Rewritten: definition, two consequences, and proofs in collapsible boxes.
- [x] **M — Ch. 6, angular momentum operator (`06_Operators.qmd`, "Angular Momentum Operator").** Correct but proof-heavy; add a "why we care" sentence.
- [x] **M — Ch. 12, heading "Shapes and Energies of Molecular Orbitals" (`12_Polyatomic.qmd` 191).** Rename it, for example "Molecular Orbitals of Water", to avoid "shapes".
- [x] **M — Whole book: "A few important considerations can be made by analyzing…"** appears 16 times. It's a recognizable tic; vary it ("Notice three things in @fig-…", "What do these plots tell us?").
- [x] **M — Study questions (Ch. 7–13).** They contain non-breaking hyphens (‑), a sign of pasted text, and a few stiff stems. A quick pass: replace ‑ with -, and read the stems aloud.
