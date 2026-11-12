# Figure notebooks

These Jupyter notebooks draw the hydrogen-atom, spherical-harmonic, and model figures (Ch. 4–5). They were written in Google Colab. The copies here have their outputs stripped; the images are in `img/`.

To regenerate a figure, open the notebook in Colab or Jupyter, run the cells from the top, and save the image of the cell listed below as `img/<name>.png`. The notebooks show their figures inline and do not save files.

| Image | Notebook | Cell |
|---|---|---|
| `H_Re.png` | `hydrogen_orbitals.ipynb` | 1 (real part) |
| `H_Im.png` | `hydrogen_orbitals.ipynb` | 3 (imaginary part) |
| `H_levels.png` | `hydrogen_orbitals.ipynb` | 6 |
| `H_r.png` | `hydrogen_orbitals.ipynb` | 8 |
| `H_rpf.png` | `hydrogen_orbitals.ipynb` | 9 |
| `H_dens1.png` | `hydrogen_densities.ipynb` | 37 (80% isosurfaces, colored by phase) |
| `H_dens2.png` | `hydrogen_densities.ipynb` | 27 |
| `H_dens3.png` | `hydrogen_densities.ipynb` | 26 (dot densities) |
| `SH_Re.png` | `spherical_harmonics.ipynb` | 0 |
| `SH_Im.png` | `spherical_harmonics.ipynb` | 1 |
| `SH_abs.png` | `spherical_harmonics.ipynb` | 2 |
| `SH_Re_def.png` | `spherical_harmonics.ipynb` | 5 |
| `SH_Im_def.png` | `spherical_harmonics.ipynb` | 7 |
| `SH_levels.png` | `spherical_harmonics.ipynb` | 8 |
| `PIR_3d.png` | `particle_in_a_ring.ipynb` | 4 |
| `PIR_top.png` | `particle_in_a_ring.ipynb` | 6 |
| `PIR_polar.png` | `particle_in_a_ring.ipynb` | 8 |
| `PIR_levels.png` | `particle_in_a_ring.ipynb` | 10 |
| `PIB.png` | `particle_in_a_box.ipynb` | 5 |
| `HarmOsc.png` | `harmonic_oscillator.ipynb` | 9 |

Cells are counted from 0, including text cells, as in Jupyter's cell order.

Requirements: `numpy`, `scipy` (1.15 or newer, for `sph_harm_y`), `matplotlib`, and `scikit-image` (for the isosurfaces). All six notebooks were checked with SciPy 1.18 and Matplotlib 3.11 in November 2026 and reproduce the book images.

Notes:

- Small differences in size come from the fonts: the notebooks ask for Times New Roman, which Colab does not have (it falls back to DejaVu Serif).
- `hydrogen_orbitals.ipynb`:
  - Cell 0 has a small shim because SciPy 1.17 removed `sph_harm`.
  - The book's `H_Re.png` has stronger colors than what cell 1 gives now; it was made with an earlier version of that cell.
