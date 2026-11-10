"""Figures for the second-row diatomics section of chapter 12.

Usage (from the project root):  python3 scripts/make_figures_diatomics.py img
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 20, "figure.dpi": 100})
PURPLE = "purple"
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]


# ------------------------------------------------------------ MO diagrams
def electrons(ax, x, y, n, w):
    """Draw n (0, 1, or 2) electrons as arrows on a level centered at x."""
    if n == 1:
        ax.annotate("", xy=(x, y + 0.28), xytext=(x, y - 0.28), arrowprops=dict(arrowstyle="-|>", lw=1.8))
    elif n == 2:
        ax.annotate("", xy=(x - w * 0.18, y + 0.28), xytext=(x - w * 0.18, y - 0.28), arrowprops=dict(arrowstyle="-|>", lw=1.8))
        ax.annotate("", xy=(x + w * 0.18, y - 0.28), xytext=(x + w * 0.18, y + 0.28), arrowprops=dict(arrowstyle="-|>", lw=1.8))


def level(ax, x, y, n, w=0.7, color="k", label=None, lx=None):
    ax.hlines(y, x - w / 2, x + w / 2, color=color, lw=3)
    electrons(ax, x, y, n, w)
    if label:
        ax.text(x + w / 2 + 0.12 if lx is None else lx, y, label, va="center", fontsize=17)


def diagram(ax, title, mo, nval_atom, mixed):
    # atomic levels: (energy, number of electrons per atom)
    s_at, p_at = 0.0, 4.0
    ns, np_ = min(2, nval_atom), nval_atom - 2
    for xa, side in ((0.6, "L"), (5.4, "R")):
        level(ax, xa, s_at, ns, w=0.6, color="0.3")
        # three p orbitals
        filled = [0, 0, 0]
        for i in range(np_):
            filled[i % 3] += 1
        for k, dx in enumerate((-0.42, 0, 0.42)):
            level(ax, xa + dx, p_at, filled[k], w=0.36, color="0.3")
    ax.text(0.6, s_at - 0.75, "$2s$", ha="center", fontsize=17)
    ax.text(0.6, p_at - 0.75, "$2p$", ha="center", fontsize=17)
    ax.text(5.4, s_at - 0.75, "$2s$", ha="center", fontsize=17)
    ax.text(5.4, p_at - 0.75, "$2p$", ha="center", fontsize=17)
    xm = 3.0
    for name, (e, n, kind) in mo.items():
        if kind == "pi":
            level(ax, xm - 0.42, e, n[0], w=0.62, color=C[0] if "u" in name[:6] else C[3])
            level(ax, xm + 0.42, e, n[1], w=0.62, color=C[0] if "u" in name[:6] else C[3], label=name, lx=xm + 1.0)
            src = [(xm - 0.75, e), (xm + 0.75, e)]
        else:
            col = C[0] if ("g" in name[:12] and "2s" in name and "*" not in name) else None
            level(ax, xm, e, n, w=0.7, color=C[3] if "*" in name else C[0], label=name, lx=xm + 1.0)
            src = [(xm - 0.37, e), (xm + 0.37, e)]
        at = s_at if "2s" in name else p_at
        ax.plot([0.6 + (0.3 if at == s_at else 0.65), src[0][0]], [at, e], ls="--", color="0.6", lw=1)
        ax.plot([5.4 - (0.3 if at == s_at else 0.65), src[1][0]], [at, e], ls="--", color="0.6", lw=1)
    ax.set_title(title, fontsize=21)
    ax.set_xlim(-0.2, 6.6)
    ax.set_ylim(-3.3, 9.0)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ("top", "right", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.set_ylabel("Energy")
    if mixed:
        ax.text(3.0, -3.0, "with $2s$–$2p$ mixing", ha="center", fontsize=15, style="italic")
    else:
        ax.text(3.0, -3.0, "little $2s$–$2p$ mixing", ha="center", fontsize=15, style="italic")


fig, axs = plt.subplots(1, 2, figsize=(14, 8.5))
N2 = {r"$\sigma_g 2s$": (-1.6, 2, "s"), r"$\sigma_u^* 2s$": (1.2, 2, "s"),
      r"$\pi_u 2p$": (2.6, (2, 2), "pi"), r"$\sigma_g 2p$": (3.5, 2, "s"),
      r"$\pi_g^* 2p$": (6.0, (0, 0), "pi"), r"$\sigma_u^* 2p$": (8.0, 0, "s")}
O2 = {r"$\sigma_g 2s$": (-1.6, 2, "s"), r"$\sigma_u^* 2s$": (1.2, 2, "s"),
      r"$\sigma_g 2p$": (2.2, 2, "s"), r"$\pi_u 2p$": (3.1, (2, 2), "pi"),
      r"$\pi_g^* 2p$": (5.4, (1, 1), "pi"), r"$\sigma_u^* 2p$": (7.9, 0, "s")}
diagram(axs[0], r"N$_2$", N2, 5, True)
diagram(axs[1], r"O$_2$", O2, 6, False)
fig.tight_layout()
fig.savefig(f"{OUT}/MO_N2_O2.png", dpi=100)
plt.close(fig)


# ------------------------------------------------------------ sigma and pi orbitals from 2p
R, zeta = 2.07, 1.95  # N2 bond length (a0) and Slater exponent of N 2p
x = np.linspace(-3.2, 3.2, 360)
z = np.linspace(-4.2, 4.2, 460)
X, Z = np.meshgrid(x, z)
def p2(coord, zc):
    r = np.sqrt(X**2 + (Z - zc)**2)
    return coord * np.exp(-zeta * r)
pzA, pzB = p2(Z + R / 2, -R / 2), p2(Z - R / 2, R / 2)
pxA, pxB = p2(X, -R / 2), p2(X, R / 2)
orbs = [(pzA - pzB, r"$\sigma_g 2p$ (bonding)"), (pzA + pzB, r"$\sigma_u^* 2p$ (antibonding)"),
        (pxA + pxB, r"$\pi_u 2p$ (bonding)"), (pxA - pxB, r"$\pi_g^* 2p$ (antibonding)")]
fig, axs = plt.subplots(2, 2, figsize=(11, 9.5))
for ax, (f, t) in zip(axs.flat, orbs):
    m = np.abs(f).max()
    ax.contourf(Z, X, f, levels=np.linspace(-m, m, 41), cmap="RdBu_r")
    ax.contour(Z, X, f, levels=[0], colors=PURPLE, linewidths=1.8)
    ax.plot([-R / 2, R / 2], [0, 0], "ko", ms=6)
    ax.set_title(t, fontsize=19)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout()
fig.savefig(f"{OUT}/MO_2p_maps.png", dpi=100)
plt.close(fig)
print("done")
