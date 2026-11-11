"""Figures for the H2+ and H2 sections of chapter 11: geometries and MO diagrams.

Usage (from the project root):  python3 scripts/make_figures_h2.py img
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 18, "figure.dpi": 100})
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]


def geometry(two_electrons, name, title):
    fig, ax = plt.subplots(figsize=(8, 5))
    A, B = (0.0, 0.0), (6.0, 0.0)
    ax.plot([A[0], B[0]], [A[1], B[1]], color="k", lw=2)
    ax.text(3.0, -0.45, "$R$", ha="center", fontsize=20)
    for (x, y), lab in ((A, "A"), (B, "B")):
        ax.plot(x, y, "o", ms=16, color=C[3])
        ax.text(x, y - 0.75, lab, ha="center", fontsize=20)
    if not two_electrons:
        P = (2.6, 2.6)
        ax.plot(*P, "o", ms=10, color=C[0])
        ax.text(P[0] + 0.2, P[1] + 0.25, "electron", fontsize=16, color=C[0])
        for (x, y), lab, dx in ((A, "$r_A$", -0.75), (B, "$r_B$", 0.25)):
            ax.plot([x, P[0]], [y, P[1]], ls="--", color="0.4", lw=1.5)
            ax.text((x + P[0]) / 2 + dx, (y + P[1]) / 2, lab, fontsize=20)
    else:
        e1, e2 = (1.6, 2.4), (4.0, 3.0)
        for (x, y), lab in ((e1, "1"), (e2, "2")):
            ax.plot(x, y, "o", ms=10, color=C[0])
            ax.text(x - 0.15, y + 0.3, lab, fontsize=18, color=C[0])
        ax.plot([e1[0], e2[0]], [e1[1], e2[1]], ls="-", color=C[0], lw=1.5)
        ax.text(2.7, 2.95, "$r_{12}$", fontsize=18, color=C[0])
        for (ex, ey), (nx, ny), lab, off in ((e1, A, "$r_{1A}$", (-0.75, 0)), (e1, B, "$r_{1B}$", (0.3, -0.35)),
                                              (e2, A, "$r_{2A}$", (-0.2, 0.35)), (e2, B, "$r_{2B}$", (0.25, 0))):
            ax.plot([ex, nx], [ey, ny], ls="--", color="0.55", lw=1.2)
            ax.text((ex + nx) / 2 + off[0], (ey + ny) / 2 + off[1], lab, fontsize=16)
    ax.set_title(title, fontsize=20)
    ax.set_xlim(-1.2, 7.2); ax.set_ylim(-1.3, 3.8); ax.set_aspect("equal"); ax.axis("off")
    fig.savefig(f"{OUT}/{name}", dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrows(ax, x, y, n):
    if n == 1:
        ax.annotate("", xy=(x, y + 0.32), xytext=(x, y - 0.32), arrowprops=dict(arrowstyle="-|>", lw=2))
    elif n == 2:
        ax.annotate("", xy=(x - 0.12, y + 0.32), xytext=(x - 0.12, y - 0.32), arrowprops=dict(arrowstyle="-|>", lw=2))
        ax.annotate("", xy=(x + 0.12, y - 0.32), xytext=(x + 0.12, y + 0.32), arrowprops=dict(arrowstyle="-|>", lw=2))


def mo_diagram(n_el, name, title, lab_b, lab_a):
    fig, ax = plt.subplots(figsize=(8, 6))
    E_at, E_b, E_a = 0.0, -1.6, 2.2   # antibonding pushed up more than bonding is pushed down (S > 0)
    xl, xm, xr, w = 0.0, 3.0, 6.0, 1.1
    for x in (xl, xr):
        ax.hlines(E_at, x - w / 2, x + w / 2, color="k", lw=3)
    ax.text(xl, E_at - 0.55, "$1s$ (A)", ha="center", fontsize=17)
    ax.text(xr, E_at - 0.55, "$1s$ (B)", ha="center", fontsize=17)
    ax.hlines(E_b, xm - w / 2, xm + w / 2, color=C[0], lw=3)
    ax.hlines(E_a, xm - w / 2, xm + w / 2, color=C[3], lw=3)
    for x0, sgn in ((xl + w / 2, 1), (xr - w / 2, -1)):
        for E in (E_b, E_a):
            ax.plot([x0, xm - sgn * w / 2], [E_at, E], ls="--", color="0.6", lw=1.2)
    ax.text(xm, E_b - 0.65, "bonding, " + lab_b, ha="center", fontsize=17, color=C[0])
    ax.text(xm, E_a + 0.3, "antibonding, " + lab_a, ha="center", fontsize=17, color=C[3])
    arrows(ax, xm, E_b, n_el)
    ax.set_ylabel("Energy")
    ax.set_title(title, fontsize=20)
    ax.set_xlim(-1.0, 7.0); ax.set_ylim(-2.6, 3.0)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ("top", "right", "bottom"):
        ax.spines[sp].set_visible(False)
    fig.savefig(f"{OUT}/{name}", dpi=150, bbox_inches="tight")
    plt.close(fig)


geometry(False, "H2p_geometry.png", r"$\mathrm{H}_2^+$")
geometry(True, "H2_geometry.png", r"$\mathrm{H}_2$")
mo_diagram(1, "H2p_MO.png", r"$\mathrm{H}_2^+$", r"$\varphi_+$", r"$\varphi_-$")
mo_diagram(2, "H2_MO.png", r"$\mathrm{H}_2$", r"$\sigma_g$", r"$\sigma_u^*$")
print("done")
