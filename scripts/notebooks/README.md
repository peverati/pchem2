# Figure notebooks

These Jupyter notebooks draw the hydrogen-atom, spherical-harmonic, and model figures (Ch. 4–5). They were written in Google Colab. The copies here have their outputs stripped.

To regenerate the figures, run each notebook from the top, with the book's folder as the working directory (in Colab, upload the notebook and download the `img/` folder at the end). The first cell defines `save_for_print`, which every figure cell calls before showing the figure. It:

- enlarges any text that would be smaller than 7 pt once the figure is printed at its width in the book (4.05 in for a figure at 90% of the 4.5 in text width);
- removes the tick numbers of 3D axes, which would be unreadable in print;
- saves `img/<name>.png` at 400 dpi for the printed size, which is also sharp on the website.

If you change a figure's width in the book, change the width in its `save_for_print` call too.

| Image | Notebook | Cell | Width in print |
|---|---|---|---|
| `H_Re.png` | `hydrogen_orbitals.ipynb` | 2 (real part) | 4.05 in |
| `H_Im.png` | `hydrogen_orbitals.ipynb` | 4 (imaginary part) | 4.05 in |
| `H_levels.png` | `hydrogen_orbitals.ipynb` | 7 | 4.05 in |
| `H_r.png` | `hydrogen_orbitals.ipynb` | 9 | 4.05 in |
| `H_rpf.png` | `hydrogen_orbitals.ipynb` | 10 | 4.05 in |
| `H_dens1.png` | `hydrogen_densities.ipynb` | 38 (80% surfaces, colored by phase) | 4.05 in |
| `H_dens2.png` | `hydrogen_densities.ipynb` | 28 (volumetric clouds) | 4.05 in |
| `H_dens3.png` | `hydrogen_densities.ipynb` | 27 (dot densities) | 4.05 in |
| `SH_Re.png` | `spherical_harmonics.ipynb` | 1 | 4.05 in |
| `SH_Im.png` | `spherical_harmonics.ipynb` | 2 | 4.05 in |
| `SH_abs.png` | `spherical_harmonics.ipynb` | 3 | 4.05 in |
| `SH_Re_def.png` | `spherical_harmonics.ipynb` | 6 | 4.05 in |
| `SH_Im_def.png` | `spherical_harmonics.ipynb` | 8 | 4.05 in |
| `SH_levels.png` | `spherical_harmonics.ipynb` | 9 | 4.05 in |
| `PIR_3d.png` | `particle_in_a_ring.ipynb` | 5 | 2.25 in |
| `PIR_top.png` | `particle_in_a_ring.ipynb` | 7 | 2.25 in |
| `PIR_polar.png` | `particle_in_a_ring.ipynb` | 9 | 2.25 in |
| `PIR_levels.png` | `particle_in_a_ring.ipynb` | 11 | 4.05 in |
| `PIB.png` | `particle_in_a_box.ipynb` | 6 | 3.6 in |
| `HarmOsc.png` | `harmonic_oscillator.ipynb` | 10 | 4.05 in |

Cells are counted from 0, including text cells, as in Jupyter's cell order.

Requirements: `numpy`, `scipy` (1.15 or newer, for `sph_harm_y`), `matplotlib`, and `scikit-image` (for the isosurfaces). Checked with SciPy 1.18 and Matplotlib 3.11 in November 2026.

Notes:

- The notebooks ask for Times New Roman, which Colab does not have (it falls back to DejaVu Serif), so the lettering differs slightly between Colab and a computer that has the font.
- The 3D point plots use `depthshade=False`: Matplotlib 3.10 and later fade distant points much more than older versions, which made the pictures paler.
- `hydrogen_orbitals.ipynb`, cell 1, has a small shim because SciPy 1.17 removed `sph_harm`.
- November 2026, for print: text enlarged to at least 7 pt; 3D tick numbers removed; in the level diagrams, the $m_\ell$ labels show the values only; in `PIR_levels`, "Re" and "Im" beside the small plots instead of above them; in `H_Re` and `H_Im`, transparent plot backgrounds so the row below does not cover the labels; in `H_Im` and `SH_Im`, empty boxes (axes, grid, background) for the functions with no imaginary part; in `PIR_top` and `PIR_polar`, no tick labels.
