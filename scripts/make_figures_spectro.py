"""Figures for heteronuclear diatomics (ch. 11) and for the new spectroscopy
sections (ch. 13): transition dipole, normal modes, Jablonski diagram, NMR and ESR.

Usage (from the project root):  python3 scripts/make_figures_spectro.py img
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from numpy.polynomial.hermite import hermval
from math import factorial, pi

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 18, "legend.fontsize": 14, "figure.dpi": 100})
PURPLE = "purple"
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]


# ================================================================ heteronuclear MO diagrams
def level(ax, x, y, w=0.7, color="k", lw=3):
    ax.hlines(y, x - w / 2, x + w / 2, color=color, lw=lw)


def electrons(ax, x, y, n):
    if n:
        ax.text(x, y + 0.05, r"$\uparrow\!\downarrow$" if n == 2 else r"$\uparrow$", ha="center", va="center", fontsize=17)


def mo_diagram(ax, title, left, right, mos, ylim, notes=()):
    """left/right: dict label -> (energy, n_orbitals, electrons_per_orbital list)."""
    xl, xr, xm = 0.9, 7.6, 3.4
    for (lab, (E, n, els)), x0, side in [(kv, xl, "L") for kv in left.items()] + [(kv, xr, "R") for kv in right.items()]:
        offs = [0] if n == 1 else [-0.42, 0, 0.42]
        w = 0.7 if n == 1 else 0.36
        for o, e in zip(offs, els):
            level(ax, x0 + o, E, w=w, color="0.3")
            electrons(ax, x0 + o, E, e)
        ax.text(x0, E - 0.9, lab, ha="center", va="top", fontsize=15)
    for name, (E, n, els, col, links, desc) in mos.items():
        offs = [0] if n == 1 else [-0.42, 0.42]
        w = 0.7 if n == 1 else 0.62
        for o, e in zip(offs, els):
            level(ax, xm + o, E, w=w, color=col)
            electrons(ax, xm + o, E, e)
        ax.text(xm + 0.85, E, f"{name}  {desc}", va="center", fontsize=13)
        for side, Eat in links:
            xa = xl + 0.38 if side == "L" else xr - 0.38
            xb = xm - 0.45 if side == "L" else xm + 0.45
            ax.plot([xa, xb], [Eat, E], ls="--", color="0.6", lw=1)
    for x, y, t in notes:
        ax.text(x, y, t, ha="center", fontsize=15, style="italic")
    ax.set_title(title, fontsize=20)
    ax.set_xlim(0, 8.4); ax.set_ylim(*ylim)
    ax.set_xticks([]); ax.set_ylabel("Energy (eV)")
    for sp in ("top", "right", "bottom"):
        ax.spines[sp].set_visible(False)


fig, axs = plt.subplots(1, 2, figsize=(17, 9))
mo_diagram(axs[0], "HF",
           {"H $1s$": (-13.6, 1, [1])},
           {"F $2s$": (-40.2, 1, [2]), "F $2p$": (-18.6, 3, [2, 2, 1])},
           {r"$4\sigma^*$": (-4.0, 1, [0], C[3], [("L", -13.6), ("R", -18.6)], "antibonding"),
            r"$1\pi$": (-16.0, 2, [2, 2], "k", [("R", -18.6)], "nonbonding (F lone pairs)"),
            r"$3\sigma$": (-19.9, 1, [2], C[0], [("L", -13.6), ("R", -18.6)], "bonding (mostly F)"),
            r"$2\sigma$": (-39.0, 1, [2], "k", [("R", -40.2)], "nonbonding (F $2s$)")},
           (-43, 0), notes=[(0.9, -42.5, "hydrogen"), (7.6, -42.5, "fluorine")])
mo_diagram(axs[1], "CO",
           {"C $2s$": (-19.4, 1, [2]), "C $2p$": (-10.7, 3, [1, 1, 0])},
           {"O $2s$": (-32.4, 1, [2]), "O $2p$": (-15.9, 3, [2, 1, 1])},
           {r"$6\sigma^*$": (-2.0, 1, [0], C[3], [("L", -10.7), ("R", -15.9)], "antibonding"),
            r"$2\pi^*$": (-7.0, 2, [0, 0], C[3], [("L", -10.7), ("R", -15.9)], "LUMO (mostly C)"),
            r"$5\sigma$": (-14.0, 1, [2], "k", [("L", -19.4), ("L", -10.7)], "HOMO (C lone pair)"),
            r"$1\pi$": (-16.9, 2, [2, 2], C[0], [("L", -10.7), ("R", -15.9)], "bonding (mostly O)"),
            r"$4\sigma$": (-19.7, 1, [2], C[0], [("R", -15.9), ("L", -19.4)], "mostly O"),
            r"$3\sigma$": (-38.3, 1, [2], C[0], [("R", -32.4)], "mostly O $2s$")},
           (-41.5, 0), notes=[(0.9, -41.0, "carbon"), (7.6, -41.0, "oxygen")])
fig.tight_layout()
fig.savefig(f"{OUT}/MO_HF_CO.png", dpi=100)
plt.close(fig)

# CO frontier orbitals: schematic LCAO of Slater-type functions (illustrative coefficients)
R = 2.13  # a0
zC, zO = 1.57, 2.23
X, Z = np.meshgrid(np.linspace(-3.5, 3.5, 400), np.linspace(-4.5, 4.5, 500))
def s2(zc, zeta): r = np.sqrt(X**2 + (Z - zc)**2); return r * np.exp(-zeta * r)
def pz(zc, zeta): r = np.sqrt(X**2 + (Z - zc)**2); return (Z - zc) * np.exp(-zeta * r)
def px(zc, zeta): r = np.sqrt(X**2 + (Z - zc)**2); return X * np.exp(-zeta * r)
zc_C, zc_O = -R / 2, R / 2
homo = 0.65 * s2(zc_C, zC) - 0.75 * pz(zc_C, zC) - 0.25 * s2(zc_O, zO) - 0.25 * pz(zc_O, zO)
lumo = 0.8 * px(zc_C, zC) - 0.55 * px(zc_O, zO)
fig, axs = plt.subplots(1, 2, figsize=(12, 6.5))
for ax, f, t in zip(axs, [homo, lumo], [r"$5\sigma$ (HOMO)", r"$2\pi^*$ (LUMO)"]):
    m = np.abs(f).max()
    ax.contourf(Z, X, f, levels=np.linspace(-m, m, 41), cmap="RdBu_r")
    ax.plot([zc_C], [0], "o", color="0.2", ms=11); ax.plot([zc_O], [0], "o", color="red", ms=11, mec="k")
    ax.text(zc_C, -0.55, "C", ha="center", fontsize=16, weight="bold")
    ax.text(zc_O, -0.55, "O", ha="center", fontsize=16, weight="bold")
    ax.set_title(t, fontsize=19); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout()
fig.savefig(f"{OUT}/CO_frontier.png", dpi=100)
plt.close(fig)

# ================================================================ transition dipole integrand (harmonic oscillator)
x = np.linspace(-5, 5, 1000)
def ho(n):
    c = np.zeros(n + 1); c[n] = 1
    return hermval(x, c) * np.exp(-x**2 / 2) / np.sqrt(2**n * factorial(n) * np.sqrt(pi))
fig, axs = plt.subplots(1, 2, figsize=(14, 5.2), sharey=True)
for ax, n, t in zip(axs, (1, 2), (r"$v=0\rightarrow v=1$: allowed", r"$v=0\rightarrow v=2$: forbidden")):
    f = ho(n) * x * ho(0)
    ax.fill_between(x, f, where=f > 0, color=C[3], alpha=0.35)
    ax.fill_between(x, f, where=f < 0, color=C[0], alpha=0.35)
    ax.plot(x, f, color="k", lw=2, label=rf"$\psi_{n}\,x\,\psi_0$")
    ax.plot(x, ho(0), color="0.5", ls="--", lw=1.3, label=r"$\psi_0$")
    ax.plot(x, ho(n), color="0.5", ls=":", lw=1.6, label=rf"$\psi_{n}$")
    area = np.trapz(f, x) if hasattr(np, "trapz") else np.trapezoid(f, x)
    ax.text(0.03, 0.06, f"integral = {area:.2f}", transform=ax.transAxes, fontsize=16, color=PURPLE)
    ax.axhline(0, color="k", lw=0.7)
    ax.set_title(t, fontsize=18); ax.set_xlabel("displacement $x$"); ax.legend(loc="upper right"); ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(f"{OUT}/Transition_dipole.png", dpi=100)
plt.close(fig)

# ================================================================ normal modes of H2O and CO2
def atom(ax, xy, r, col, lab):
    ax.add_patch(plt.Circle(xy, r, fc=col, ec="k", lw=1.5, zorder=3))
    ax.text(*xy, lab, ha="center", va="center", fontsize=13, zorder=4, color="w" if col != "w" else "k")
def arrow(ax, xy, d):
    ax.annotate("", xy=(xy[0] + d[0], xy[1] + d[1]), xytext=xy, arrowprops=dict(arrowstyle="-|>", lw=2.5, color=PURPLE), zorder=5)
th = np.radians(104.5 / 2)
O = np.array([0, 0.25]); H1 = O + 1.0 * np.array([-np.sin(th), -np.cos(th)]); H2 = O + 1.0 * np.array([np.sin(th), -np.cos(th)])
u1 = (H1 - O) / np.linalg.norm(H1 - O); u2 = (H2 - O) / np.linalg.norm(H2 - O)
p1 = np.array([u1[1], -u1[0]]); p2 = np.array([-u2[1], u2[0]])
modes_h2o = [("symmetric stretch", "3657", "IR and Raman", [(O, (0, 0.12)), (H1, 0.45 * u1), (H2, 0.45 * u2)]),
             ("bend", "1595", "IR and Raman", [(O, (0, -0.12)), (H1, -0.45 * p1), (H2, -0.45 * p2)]),
             ("antisymmetric stretch", "3756", "IR and Raman", [(O, (0.12, 0)), (H1, -0.45 * u1), (H2, 0.45 * u2)])]
Cc = np.array([0, 0]); O1 = np.array([-1.16, 0]); O2 = np.array([1.16, 0])
modes_co2 = [("symmetric stretch", "≈1330", "Raman only", [(O1, (-0.45, 0)), (O2, (0.45, 0))]),
             ("bend (×2)", "667", "IR only", [(Cc, (0, 0.4)), (O1, (0, -0.25)), (O2, (0, -0.25))]),
             ("antisymmetric stretch", "2349", "IR only", [(Cc, (0.4, 0)), (O1, (-0.25, 0)), (O2, (-0.25, 0))])]
fig, axs = plt.subplots(2, 3, figsize=(15, 9))
for j, (name, wn, act, arrs) in enumerate(modes_h2o):
    ax = axs[0, j]
    ax.plot(*zip(O, H1), color="0.4", lw=4, zorder=1); ax.plot(*zip(O, H2), color="0.4", lw=4, zorder=1)
    atom(ax, O, 0.22, "red", "O"); atom(ax, H1, 0.15, "w", "H"); atom(ax, H2, 0.15, "w", "H")
    for xy, d in arrs: arrow(ax, xy, d)
    ax.set_title(f"H$_2$O {name}\n{wn} cm$^{{-1}}$, {act}", fontsize=15)
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.3, 0.9); ax.set_aspect("equal"); ax.axis("off")
for j, (name, wn, act, arrs) in enumerate(modes_co2):
    ax = axs[1, j]
    ax.plot([-1.16, 1.16], [0, 0], color="0.4", lw=4, zorder=1)
    atom(ax, O1, 0.22, "red", "O"); atom(ax, Cc, 0.2, "0.25", "C"); atom(ax, O2, 0.22, "red", "O")
    for xy, d in arrs: arrow(ax, np.array(xy, dtype=float), d)
    ax.set_title(f"CO$_2$ {name}\n{wn} cm$^{{-1}}$, {act}", fontsize=15)
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-0.8, 0.8); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/Normal_modes.png", dpi=100)
plt.close(fig)

# ================================================================ Jablonski diagram
fig, ax = plt.subplots(figsize=(12, 9))
states = {"S$_0$": (0.0, 1.0), "S$_1$": (6.0, 1.0), "S$_2$": (9.5, 1.0), "T$_1$": (4.6, 6.0)}
for lab, (E, x0) in states.items():
    w = 9.2 if lab == "S$_0$" else 3.2
    ax.hlines(E, x0, x0 + w, color="k", lw=3)
    for k in range(1, 4):
        ax.hlines(E + 0.35 * k, x0, x0 + w, color="0.6", lw=1)
    ax.text(x0 - 0.15 if lab != "T$_1$" else x0 + 3.35, E, lab, ha="right" if lab != "T$_1$" else "left", va="center", fontsize=20)
ax.text(2.6, 11.4, "singlets", ha="center", fontsize=17, style="italic")
ax.text(7.6, 11.4, "triplets", ha="center", fontsize=17, style="italic")
def straight(x, y1, y2, col, lab, lx):
    ax.annotate("", xy=(x, y2), xytext=(x, y1), arrowprops=dict(arrowstyle="-|>", lw=3, color=col))
    ax.text(lx, (y1 + y2) / 2, lab, color=col, fontsize=15, ha="center", va="center", rotation=90)
def wavy(x1, y1, x2, y2, col):
    t = np.linspace(0, 1, 200)
    xs, ys = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
    L = np.hypot(x2 - x1, y2 - y1); nx, ny = -(y2 - y1) / L, (x2 - x1) / L
    amp = 0.12 * np.sin(2 * pi * 8 * t)
    ax.plot(xs + nx * amp, ys + ny * amp, color=col, lw=2)
    ax.annotate("", xy=(x2, y2), xytext=(xs[-8] + nx * amp[-8], ys[-8] + ny * amp[-8]), arrowprops=dict(arrowstyle="-|>", lw=2, color=col))
straight(1.4, 0.0, 6.0 + 1.05, C[4], "absorption", 1.15)
straight(1.9, 0.0, 9.5 + 0.7, C[4], "absorption", 1.65)
wavy(2.6, 9.5 + 0.7, 2.6, 9.5, C[7]); ax.text(2.8, 10.1, "vibrational\nrelaxation", fontsize=12, color=C[7])
wavy(2.6, 9.5, 2.6, 6.0 + 1.05, C[7]); ax.text(2.8, 8.2, "internal\nconversion", fontsize=12, color=C[7])
wavy(2.4, 6.0 + 1.05, 2.4, 6.0, C[7])
straight(3.3, 6.0, 0.0 + 0.7, C[2], "fluorescence (ns)", 3.05)
wavy(4.2, 6.0, 5.2, 4.6 + 0.7, C[1]); ax.text(4.4, 6.25, "intersystem\ncrossing", fontsize=12, color=C[1])
wavy(5.6, 4.6 + 0.7, 5.6, 4.6, C[7])
straight(7.0, 4.6, 0.0 + 1.05, C[3], "phosphorescence (μs–s)", 6.75)
ax.set_xlim(-0.3, 11.5); ax.set_ylim(-0.6, 12)
ax.set_ylabel("Energy"); ax.set_xticks([]); ax.set_yticks([])
for sp in ("top", "right", "bottom"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/Jablonski.png", dpi=100)
plt.close(fig)

# ================================================================ magnetic resonance
# Zeeman splitting of a spin-1/2 in a magnetic field
fig, axs = plt.subplots(1, 3, figsize=(18, 5.5), gridspec_kw=dict(width_ratios=[1, 1.4, 1.4]))
ax = axs[0]
B = np.linspace(0, 1, 100)
ax.plot(B, 0.5 * B, color=C[3], lw=2.5); ax.plot(B, -0.5 * B, color=C[0], lw=2.5)
ax.text(1.02, 0.5, r"$m=-\frac{1}{2}$ ($\beta$)", color=C[3], va="center", fontsize=14)
ax.text(1.02, -0.5, r"$m=+\frac{1}{2}$ ($\alpha$)", color=C[0], va="center", fontsize=14)
ax.annotate("", xy=(0.75, 0.375), xytext=(0.75, -0.375), arrowprops=dict(arrowstyle="<->", lw=2, color=PURPLE))
ax.text(0.71, 0, r"$\Delta E=h\nu$", color=PURPLE, ha="right", va="center", fontsize=15)
ax.axvline(0.75, color="0.6", ls=":", lw=1)
ax.set_xlabel("magnetic field $B_0$"); ax.set_ylabel("energy"); ax.set_xticks([0.75]); ax.set_xticklabels(["$B_0$"]); ax.set_yticks([])
ax.set_xlim(0, 1.45); ax.set_title("(a) spin-1/2 in a field (for $\\gamma>0$)", fontsize=16)
# 1H NMR spectrum of ethanol (400 MHz, first-order, J = 7 Hz)
ax = axs[1]
d = np.linspace(0.5, 4.5, 20000)
spec = np.zeros_like(d)
def lor(x0, w=0.006): return 1 / (1 + ((d - x0) / w) ** 2)
J = 7.0 / 400.0  # ppm
for k, rel in zip((-1, 0, 1), (1, 2, 1)):            # CH3 triplet, 3H
    spec += 3 * rel / 4 * lor(1.18 + k * J)
for k, rel in zip((-1.5, -0.5, 0.5, 1.5), (1, 3, 3, 1)):  # CH2 quartet, 2H
    spec += 2 * rel / 8 * lor(3.69 + k * J)
spec += 1 * lor(2.61)                                   # OH singlet, 1H
ax.plot(d, spec, color="k", lw=1.2)
for x0, lab in ((1.18, "CH$_3$\ntriplet"), (3.69, "CH$_2$\nquartet"), (2.61, "OH")):
    ax.text(x0, spec[np.argmin(abs(d - x0))] + 0.1 if x0 != 3.69 else 0.95, lab, ha="center", fontsize=13)
ax.set_xlim(4.3, 0.7); ax.set_ylim(0, 1.8); ax.set_yticks([])
ax.set_xlabel(r"chemical shift $\delta$ (ppm)"); ax.set_title(r"(b) $^1$H NMR spectrum of ethanol (simulated)", fontsize=16)
# ESR spectrum of the methyl radical (first derivative, a = 2.3 mT)
ax = axs[2]
Bf = np.linspace(334, 346, 4000)
sig = np.zeros_like(Bf)
w = 0.12
for k, rel in zip((-1.5, -0.5, 0.5, 1.5), (1, 3, 3, 1)):
    x0 = 340 + k * 2.3
    sig += rel * (-2 * (Bf - x0) / w**2) / (1 + ((Bf - x0) / w) ** 2) ** 2
ax.plot(Bf, sig / np.abs(sig).max(), color="k", lw=1.3)
ax.annotate("", xy=(340 + 0.5 * 2.3, -1.12), xytext=(340 - 0.5 * 2.3, -1.12), arrowprops=dict(arrowstyle="<->", lw=1.5, color=PURPLE))
ax.text(340, -1.08, "$a=2.3$ mT", ha="center", va="bottom", color=PURPLE, fontsize=14)
ax.set_xlabel("magnetic field (mT)"); ax.set_yticks([]); ax.set_ylim(-1.3, 1.15)
ax.set_title(r"(c) ESR spectrum of $\cdot$CH$_3$ (simulated)", fontsize=16)
fig.tight_layout()
fig.savefig(f"{OUT}/Magnetic_resonance.png", dpi=100)
plt.close(fig)
print("done")
