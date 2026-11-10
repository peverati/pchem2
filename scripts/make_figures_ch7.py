"""Figures for chapter 7 (spin).

Usage (from the project root):  python3 scripts/make_figures_ch7.py img
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch, Ellipse

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 20, "figure.dpi": 100})
PURPLE = "purple"
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]
UP, DN = C[3], C[0]

# ---------------------------------------------------------------- Stern-Gerlach apparatus
fig = plt.figure(figsize=(15, 6))
ax = fig.add_axes([0.0, 0.0, 0.62, 1.0])
ax.set_xlim(0, 10); ax.set_ylim(-3, 3); ax.axis("off")
# oven
ax.add_patch(FancyBboxPatch((0.2, -0.7), 1.2, 1.4, boxstyle="round,pad=0.05", fc="#f4c27a", ec="k", lw=1.5))
ax.text(0.8, -1.05, "oven\n(Ag atoms)", ha="center", va="top", fontsize=14)
# collimator slits
for xs in (2.0, 2.6):
    ax.add_patch(Rectangle((xs, 0.12), 0.08, 1.0, color="0.3"))
    ax.add_patch(Rectangle((xs, -1.12), 0.08, 1.0, color="0.3"))
# magnet: pointed north pole on top, flat south pole on bottom
ax.add_patch(Polygon([[3.6, 2.4], [6.4, 2.4], [6.4, 1.3], [5.0, 0.55], [3.6, 1.3]], closed=True, fc="#d9534f", ec="k", lw=1.5))
ax.add_patch(Rectangle((3.6, -2.4), 2.8, 1.5, fc="#5b8fd9", ec="k", lw=1.5))
ax.text(5.0, 1.75, "N", ha="center", va="center", fontsize=22, color="w", weight="bold")
ax.text(5.0, -1.65, "S", ha="center", va="center", fontsize=22, color="w", weight="bold")
ax.text(5.0, -2.75, "inhomogeneous magnet", ha="center", fontsize=14)
# beams
ax.plot([1.4, 3.6], [0, 0], color="0.2", lw=3)
xs = np.linspace(3.6, 8.6, 100)
for sgn, col in ((1, UP), (-1, DN)):
    ys = sgn * 0.06 * (xs - 3.6) ** 2
    ax.plot(xs, ys, color=col, lw=3)
# screen
ax.add_patch(Rectangle((8.6, -2.2), 0.15, 4.4, fc="0.85", ec="k"))
ax.text(8.67, -2.5, "screen", ha="center", fontsize=14)
ax.annotate("", xy=(9.6, 1.2), xytext=(9.6, -1.2), arrowprops=dict(arrowstyle="->", lw=1.5))
ax.text(9.7, 0, "$z$", fontsize=18, va="center")
# insets: classical vs observed patterns
for k, (title, pattern) in enumerate((("classical prediction", "smear"), ("observed", "spots"))):
    axi = fig.add_axes([0.63 + k * 0.14, 0.15, 0.11, 0.7])
    axi.set_facecolor("0.15")
    zz = np.linspace(-1, 1, 400)
    if pattern == "smear":
        yy = np.linspace(-1, 1, 200)
        Z = np.tile(np.exp(-(np.linspace(-1, 1, 60)[:, None] ** 2) / 0.05) * 0 + 1, (1, 1))
        img = np.exp(-(np.linspace(-1, 1, 60)[None, :] ** 2) / 0.08) * (np.abs(np.linspace(-1, 1, 200))[:, None] < 0.75)
        axi.imshow(img, extent=[-1, 1, -1, 1], cmap="gray", vmin=0, vmax=1, aspect="auto")
    else:
        img = np.zeros((200, 60))
        Y, X = np.meshgrid(np.linspace(-1, 1, 200), np.linspace(-1, 1, 60), indexing="ij")
        img = np.exp(-((Y - 0.6) ** 2 + X**2 * 0.5) / 0.012) + np.exp(-((Y + 0.6) ** 2 + X**2 * 0.5) / 0.012)
        axi.imshow(img, extent=[-1, 1, -1, 1], cmap="gray", vmin=0, vmax=1, aspect="auto", origin="lower")
        axi.text(1.15, 0.6, r"$m_s=+\frac{1}{2}$", color=UP, fontsize=15, va="center", transform=axi.transData)
        axi.text(1.15, -0.6, r"$m_s=-\frac{1}{2}$", color=DN, fontsize=15, va="center", transform=axi.transData)
    axi.set_xticks([]); axi.set_yticks([])
    axi.set_title(title, fontsize=15)
fig.savefig(f"{OUT}/SG_apparatus.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- sequential Stern-Gerlach experiments
def sg_box(ax, x, y, label):
    ax.add_patch(FancyBboxPatch((x, y - 0.5), 1.4, 1.0, boxstyle="round,pad=0.05", fc="#eeeeee", ec="k", lw=1.8))
    ax.text(x + 0.7, y, label, ha="center", va="center", fontsize=19)
def beam(ax, x1, y1, x2, y2, col, txt=None, tpos=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", lw=2.5, color=col))
    if txt:
        ax.text(*(tpos or ((x1 + x2) / 2, (y1 + y2) / 2 + 0.15)), txt, ha="center", va="bottom", fontsize=15, color=col)
def blocked(ax, x, y, col, txt):
    ax.annotate("", xy=(x + 0.8, y), xytext=(x, y), arrowprops=dict(arrowstyle="-[", lw=2.0, color=col))
    ax.text(x + 1.0, y, txt, fontsize=14, color=col, va="center")

fig, axs = plt.subplots(3, 1, figsize=(13, 10))
for ax in axs:
    ax.set_xlim(-0.3, 13); ax.set_ylim(-1.3, 1.3); ax.axis("off")
# (a) single measurement
ax = axs[0]
ax.text(-0.3, 1.15, "(a)", fontsize=18, weight="bold")
beam(ax, 0.0, 0, 1.4, 0, "0.3", "$N$")
sg_box(ax, 1.5, 0, "SG$_z$")
beam(ax, 3.0, 0.2, 4.6, 0.8, UP, r"$N/2$  $\uparrow_z$", (4.2, 0.85))
beam(ax, 3.0, -0.2, 4.6, -0.8, DN, r"$N/2$  $\downarrow_z$", (4.2, -1.3))
# (b) z then z
ax = axs[1]
ax.text(-0.3, 1.15, "(b)", fontsize=18, weight="bold")
beam(ax, 0.0, 0, 1.4, 0, "0.3", "$N$")
sg_box(ax, 1.5, 0, "SG$_z$")
beam(ax, 3.0, 0.2, 5.1, 0.2, UP, r"$\uparrow_z$  $N/2$")
blocked(ax, 3.0, -0.4, DN, r"$\downarrow_z$ blocked")
sg_box(ax, 5.2, 0.2, "SG$_z$")
beam(ax, 6.7, 0.4, 8.6, 0.9, UP, r"$N/2$  $\uparrow_z$", (8.2, 0.95))
ax.text(10.0, 0.0, "no change:\nthe state was\nalready $\\uparrow_z$", fontsize=15, va="center")
# (c) z then x then z
ax = axs[2]
ax.text(-0.3, 1.15, "(c)", fontsize=18, weight="bold")
beam(ax, 0.0, 0, 1.4, 0, "0.3", "$N$")
sg_box(ax, 1.5, 0, "SG$_z$")
beam(ax, 3.0, 0.2, 5.1, 0.2, UP, r"$\uparrow_z$  $N/2$")
blocked(ax, 3.0, -0.4, DN, r"$\downarrow_z$ blocked")
sg_box(ax, 5.2, 0.2, "SG$_x$")
beam(ax, 6.7, 0.4, 8.8, 0.4, C[2], r"$\rightarrow_x$  $N/4$")
blocked(ax, 6.7, -0.2, C[1], r"$\leftarrow_x$ blocked")
sg_box(ax, 8.9, 0.4, "SG$_z$")
beam(ax, 10.4, 0.6, 12.2, 1.1, UP, r"$N/8$ $\uparrow_z$", (11.9, 1.1))
beam(ax, 10.4, 0.2, 12.2, -0.3, DN, r"$N/8$ $\downarrow_z$", (11.9, -0.85))
fig.tight_layout()
fig.savefig(f"{OUT}/SG_sequential.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- spin vector cones
fig = plt.figure(figsize=(10, 9))
ax = fig.add_subplot(projection="3d")
S = np.sqrt(3) / 2
for mz, col, lab in ((0.5, UP, r"$\alpha$: $m_s=+\frac{1}{2}$"), (-0.5, DN, r"$\beta$: $m_s=-\frac{1}{2}$")):
    rho = np.sqrt(S**2 - mz**2)
    phi = np.linspace(0, 2 * np.pi, 80)
    t = np.linspace(0, 1, 20)
    P, T = np.meshgrid(phi, t)
    ax.plot_surface(T * rho * np.cos(P), T * rho * np.sin(P), T * mz, color=col, alpha=0.18, lw=0)
    ax.plot(rho * np.cos(phi), rho * np.sin(phi), mz * np.ones_like(phi), color=col, lw=1.5)
    for ph0 in (0.6, 2.4, 4.3):
        ax.quiver(0, 0, 0, rho * np.cos(ph0), rho * np.sin(ph0), mz, color=col, lw=2.2, arrow_length_ratio=0.08,
                  alpha=1 if ph0 == 0.6 else 0.35)
    ax.plot([0, 0], [0, 0], [0, mz], color=col, lw=4)
    ax.text2D(0.08, 0.66 if mz > 0 else 0.37, f"$S_z=+\\hbar/2$" if mz > 0 else f"$S_z=-\\hbar/2$", color=col, fontsize=19, transform=ax.transAxes)
    ax.text(rho * 0.9, rho * 0.9, mz * 1.05, lab, color=col, fontsize=17)
ax.plot([0, 0], [0, 0], [-1.05, 1.05], color="k", lw=1)
ax.text(0, 0, 1.12, "$z$", fontsize=20)
ax.text(0.95, 0, 0, "$x$", fontsize=18)
ax.text(0, 0.95, 0, "$y$", fontsize=18)
ax.plot([-0.9, 0.9], [0, 0], [0, 0], color="0.6", lw=0.8)
ax.plot([0, 0], [-0.9, 0.9], [0, 0], color="0.6", lw=0.8)
ax.text2D(0.04, 0.9, r"length of each vector: $|\mathbf{S}|=\frac{\sqrt{3}}{2}\hbar$", transform=ax.transAxes, fontsize=18)
ax.set_xlim(-0.9, 0.9); ax.set_ylim(-0.9, 0.9); ax.set_zlim(-1, 1)
ax.set_box_aspect((1, 1, 1.1))
ax.view_init(elev=14, azim=-60)
ax.set_axis_off()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
fig.savefig(f"{OUT}/Spin_cones.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- parity of particle-in-a-box states
a = 1.0
x = np.linspace(-a / 2, a / 2, 500)
fig, ax = plt.subplots(figsize=(9, 8.5))
for n in range(1, 5):
    E = n**2
    psi = np.sqrt(2 / a) * (np.cos(n * np.pi * x / a) if n % 2 else np.sin(n * np.pi * x / a))
    ax.plot(x, E + 0.9 * psi, color=C[0], lw=2.5)
    ax.hlines(E, -a / 2, a / 2, color="0.6", lw=0.8, ls=":")
    lab = "even, $\\Pi=+1$" if n % 2 else "odd, $\\Pi=-1$"
    ax.text(a / 2 + 0.04, E, f"$n={n}$: {lab}", va="center", fontsize=16, color=C[3] if n % 2 else C[0])
ax.axvline(0, color=PURPLE, ls="--", lw=1.5)
ax.text(0.01, 18.3, r"$x\rightarrow -x$", color=PURPLE, fontsize=16)
ax.vlines([-a / 2, a / 2], 0, 18, color="k", lw=3)
ax.set_xticks([-a / 2, 0, a / 2])
ax.set_xticklabels(["$-a/2$", "$0$", "$+a/2$"])
ax.set_yticks([])
ax.set_ylabel("Energy")
ax.set_xlim(-0.6, 1.15)
ax.set_ylim(0, 19)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/PIB_parity.png", dpi=100)
plt.close(fig)
print("done")
