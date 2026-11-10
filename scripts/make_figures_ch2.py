"""Figures for chapter 2: black-body radiation, photoelectric effect, hydrogen spectrum.

Usage (from the project root):  python3 scripts/make_figures_ch2.py img
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 20, "legend.fontsize": 15, "figure.dpi": 100})
PURPLE = "purple"
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]
h, c, kB = 6.62607e-34, 2.99792e8, 1.380649e-23


def wl_to_rgb(wl):
    """Approximate RGB color of a visible wavelength in nm."""
    if 380 <= wl < 440: r, g, b = -(wl - 440) / 60, 0, 1
    elif wl < 490: r, g, b = 0, (wl - 440) / 50, 1
    elif wl < 510: r, g, b = 0, 1, -(wl - 510) / 20
    elif wl < 580: r, g, b = (wl - 510) / 70, 1, 0
    elif wl < 645: r, g, b = 1, -(wl - 645) / 65, 0
    elif wl <= 780: r, g, b = 1, 0, 0
    else: r, g, b = 0, 0, 0
    f = 0.3 + 0.7 * (wl - 380) / 40 if wl < 420 else (0.3 + 0.7 * (780 - wl) / 80 if wl > 700 else 1)
    return (r * f, g * f, b * f)


# ---------------------------------------------------------------- black body
lam = np.linspace(50e-9, 3000e-9, 1500)
def planck(l, T):
    return 2 * h * c**2 / l**5 / np.expm1(h * c / (l * kB * T))
def rj(l, T):
    return 2 * c * kB * T / l**4
fig, ax = plt.subplots(figsize=(11, 6.5))
for i, wl in enumerate(np.arange(380, 750, 2)):
    ax.add_patch(Rectangle((wl, 0), 2, 1e3, color=wl_to_rgb(wl), alpha=0.25, lw=0))
scale = 1e-9 * 1e-3  # W m^-3 sr^-1 -> kW m^-2 sr^-1 nm^-1
for T, col in ((5800, C[0]), (4500, C[1]), (3000, C[3])):
    ax.plot(lam * 1e9, planck(lam, T) * scale, color=col, lw=2.5, label=f"Planck, $T={T}$ K")
    lmax = 2.898e-3 / T
    ax.plot(lmax * 1e9, planck(lmax, T) * scale, "o", color=PURPLE, ms=8, zorder=5)
ax.plot(lam * 1e9, rj(lam, 5800) * scale, color="k", ls="--", lw=2, label="Rayleigh–Jeans, $T=5800$ K")
ax.text(565, 31, "visible", ha="center", fontsize=15)
ax.set_xlabel(r"Wavelength $\lambda$ (nm)")
ax.set_ylabel(r"Intensity (kW m$^{-2}$ sr$^{-1}$ nm$^{-1}$)")
ax.set_xlim(50, 3000)
ax.set_ylim(0, 33)
ax.grid(alpha=0.3)
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig(f"{OUT}/Blackbody.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- photoelectric effect
heV = 4.135668e-15
nu = np.linspace(0, 1.6e15, 400)
fig, ax = plt.subplots(figsize=(11, 6.5))
for f in np.arange(4.0e14, 7.9e14, 0.5e13):
    ax.add_patch(Rectangle((f / 1e14, 0), 0.05, 10, color=wl_to_rgb(c / f * 1e9), alpha=0.25, lw=0))
for name, phi, col in (("cesium", 2.1, C[0]), ("sodium", 2.3, C[1]), ("zinc", 4.3, C[2])):
    nu0 = phi / heV
    nn = nu[nu >= nu0]
    ax.plot(nn / 1e14, heV * nn - phi, color=col, lw=2.5, label=f"{name} ($\\phi={phi}$ eV)")
    ax.plot(nn / 1e14, heV * nn - phi, color=col, lw=2.5)
    ax.plot(nu0 / 1e14, 0, "o", color=PURPLE, ms=9, zorder=5)
ax.text(5.9, 3.6, "visible", ha="center", fontsize=15)
ax.annotate(r"slope $=h$", xy=(13.0, heV * 13e14 - 4.3), xytext=(13.6, 0.7), fontsize=16,
            arrowprops=dict(arrowstyle="->", lw=1.3))
ax.set_xlabel(r"Frequency of the light $\nu$ ($10^{14}$ Hz)")
ax.set_ylabel(r"$K_\mathrm{max}$ of the electrons (eV)")
ax.set_xlim(0, 16)
ax.set_ylim(0, 4)
ax.grid(alpha=0.3)
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(f"{OUT}/Photoelectric.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- hydrogen spectrum
fig = plt.figure(figsize=(12, 9.5))
ax = fig.add_axes([0.1, 0.27, 0.86, 0.7])
E = lambda n: -13.6057 / n**2
for n in range(1, 8):
    ax.hlines(E(n), 0, 10, color="k", lw=1.5)
    if n <= 4:
        ax.text(10.15, E(n), f"$n={n}$", va="center", fontsize=15)
ax.hlines(0, 0, 10, color="k", lw=1, ls="--")
ax.text(10.15, 0.3, r"$n=5,6,\ldots,\infty$", va="center", fontsize=15)
series = [("Lyman (UV)", 1, 0.6, "0.4"), ("Balmer (visible)", 2, 4.0, None), ("Paschen (IR)", 3, 7.6, "0.4")]
for name, nlow, x0, col in series:
    for j, nup in enumerate(range(nlow + 1, nlow + 6)):
        wl = 1 / (1.09678e7 * (1 / nlow**2 - 1 / nup**2)) * 1e9
        cc = wl_to_rgb(wl) if col is None and wl < 700 else (col or "0.4")
        if col is None and wl < 380:
            cc = "0.4"
        ax.annotate("", xy=(x0 + 0.45 * j, E(nlow)), xytext=(x0 + 0.45 * j, E(nup)),
                    arrowprops=dict(arrowstyle="-|>", lw=2.2, color=cc))
    ax.text(x0 + 0.9, E(nlow) - 0.5, name, ha="center", va="top", fontsize=15)
ax.set_xlim(0, 11.2)
ax.set_ylim(-14.5, 1.0)
ax.set_xticks([])
ax.set_ylabel("Energy (eV)")
for sp in ("top", "right", "bottom"):
    ax.spines[sp].set_visible(False)
# Balmer line strip
ax2 = fig.add_axes([0.1, 0.07, 0.86, 0.1])
ax2.set_facecolor("black")
for nup in range(3, 8):
    wl = 1 / (1.09678e7 * (1 / 4 - 1 / nup**2)) * 1e9
    ax2.axvline(wl, color=wl_to_rgb(wl), lw=4)
    ax2.text(wl, 1.08, f"{wl:.0f}", ha="center", va="bottom", fontsize=13, transform=ax2.get_xaxis_transform())
ax2.set_xlim(380, 700)
ax2.set_yticks([])
ax2.set_xlabel("Balmer lines: wavelength (nm)", fontsize=16)
fig.savefig(f"{OUT}/H_spectrum.png", dpi=100)
plt.close(fig)
print("done")
