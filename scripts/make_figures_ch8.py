"""Figures for chapter 8 (Quantum Weirdness): slits, electron build-up, which-way
experiment, position/momentum uncertainty, and tunneling through a barrier.

Usage (from the project root):  python3 scripts/make_figures_ch8.py img
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 18, "legend.fontsize": 14, "figure.dpi": 100})
PURPLE = "purple"
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]
rng = np.random.default_rng(7)

# screen coordinate (arbitrary units); slit width a, separation d
y = np.linspace(-1, 1, 2000)
a, d, lam_over_L = 0.12, 0.6, 1.0 / 40
def single(y, shift=0.0):
    """Single-slit diffraction pattern (first zeros at +/-0.45)."""
    return np.sinc((y - shift) / 0.45) ** 2
def double(y):
    """Two-slit pattern: single-slit envelope times interference fringes."""
    return single(y) * np.cos(np.pi * y / 0.12) ** 2

def screen_strip(ax, I, title=None):
    ax.imshow(np.tile(I / I.max(), (60, 1)), extent=[-1, 1, 0, 1], cmap="gray", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks([]); ax.set_yticks([])
    if title:
        ax.set_title(title, fontsize=16)

def slit_schematic(ax, n_slits, detectors=False):
    ax.set_xlim(0, 10); ax.set_ylim(-3, 3); ax.axis("off")
    ax.annotate("", xy=(3.2, 0), xytext=(0.4, 0), arrowprops=dict(arrowstyle="-|>", lw=2.5, color="0.3"))
    ax.text(1.6, 0.35, "source", ha="center", fontsize=14)
    gaps = [(-0.25, 0.25)] if n_slits == 1 else [(-1.2, -0.7), (0.7, 1.2)]
    edges = [-3] + [g for gap in gaps for g in gap] + [3]
    for lo, hi in zip(edges[::2], edges[1::2]):
        ax.add_patch(Rectangle((3.4, lo), 0.25, hi - lo, color="0.25"))
    if detectors:
        for lo, hi in gaps[-1:]:  # a single detector on the upper slit is enough
            ax.add_patch(FancyBboxPatch((3.85, (lo + hi) / 2 - 0.3), 0.9, 0.6, boxstyle="round,pad=0.05", fc="#ffd966", ec="k"))
            ax.text(4.3, (lo + hi) / 2, "D", ha="center", va="center", fontsize=14, weight="bold")
    ax.add_patch(Rectangle((9.3, -2.8), 0.25, 5.6, fc="0.85", ec="k"))
    ax.text(9.42, -2.95, "screen", ha="center", va="top", fontsize=13)
    for lo, hi in gaps:
        yc = (lo + hi) / 2
        for ang in np.linspace(-0.5, 0.5, 5):
            ax.plot([3.7, 9.2], [yc, yc + ang * 5.5], color=C[0], lw=0.8, alpha=0.5)

# ---------------------------------------------------------------- single vs double slit
fig = plt.figure(figsize=(13, 7.5))
for row, (n, I, lab) in enumerate(((1, single(y), "one slit"), (2, double(y), "two slits"))):
    ax0 = fig.add_axes([0.0, 0.53 - row * 0.5, 0.38, 0.42]); slit_schematic(ax0, n)
    ax0.set_title(lab, fontsize=17)
    ax1 = fig.add_axes([0.42, 0.6 - row * 0.5, 0.55, 0.3])
    ax1.fill_between(y, I, color="cyan", alpha=0.4); ax1.plot(y, I, color="teal", lw=2)
    ax1.set_yticks([]); ax1.set_xticks([]); ax1.set_ylabel("intensity")
    ax2 = fig.add_axes([0.42, 0.53 - row * 0.5, 0.55, 0.06]); screen_strip(ax2, I)
ax2.set_xlabel("position on the screen")
fig.savefig(f"{OUT}/Slits_patterns.png", dpi=100, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- electrons one at a time
P = double(y); P = P / P.sum()
fig, axs = plt.subplots(1, 4, figsize=(14, 4.6))
for ax, N in zip(axs, (20, 200, 2000, 20000)):
    ys = rng.choice(y, size=N, p=P) + rng.normal(0, 0.002, N)
    zs = rng.uniform(0, 1, N)
    ax.set_facecolor("black")
    ax.scatter(ys, zs, s=6 if N < 2000 else (1.5 if N == 2000 else 0.3), color="white", lw=0)
    ax.set_xlim(-1, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"{N:,} electrons", fontsize=16)
fig.tight_layout()
fig.savefig(f"{OUT}/Slits_buildup.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- which-way experiment
shift = 0.03
I_off = double(y)
I_on = 0.5 * (single(y, shift=-shift) + single(y, shift=shift))
fig = plt.figure(figsize=(13, 8))
for col, (det, I, title) in enumerate(((False, I_off, "detector off: interference"),
                                       (True, I_on, "detector on: no interference"))):
    ax0 = fig.add_axes([0.02 + col * 0.5, 0.45, 0.46, 0.48]); slit_schematic(ax0, 2, detectors=det)
    ax0.set_title(title, fontsize=17)
    ax1 = fig.add_axes([0.04 + col * 0.5, 0.15, 0.42, 0.25])
    ax1.fill_between(y, I / I_off.max(), color="cyan", alpha=0.4); ax1.plot(y, I / I_off.max(), color="teal", lw=2)
    if det:
        for s_, c_ in ((-shift, C[1]), (shift, C[2])):
            ax1.plot(y, 0.5 * single(y, shift=s_) / I_off.max(), color=c_, lw=1.3, ls="--")
    ax1.set_ylim(0, 1.05); ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_ylabel("intensity")
    ax2 = fig.add_axes([0.04 + col * 0.5, 0.06, 0.42, 0.07]); screen_strip(ax2, I)
    ax2.set_xlabel("position on the screen")
fig.savefig(f"{OUT}/Slits_whichway.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- position and momentum space
x = np.linspace(-8, 8, 2000)
p = np.linspace(-8, 8, 2000)
fig, axs = plt.subplots(3, 2, figsize=(12, 9), sharex="col")
for row, sx in enumerate((2.0, 1.0, 0.4)):
    sp = 1 / (2 * sx)  # hbar = 1
    rx = np.exp(-x**2 / (2 * sx**2)) / np.sqrt(2 * np.pi * sx**2)
    rp = np.exp(-p**2 / (2 * sp**2)) / np.sqrt(2 * np.pi * sp**2)
    for ax, r, s, var, col in ((axs[row, 0], rx, sx, "x", C[0]), (axs[row, 1], rp, sp, "p", C[3])):
        ax.fill_between(x if var == "x" else p, r, color=col, alpha=0.3)
        ax.plot(x if var == "x" else p, r, color=col, lw=2)
        h = r.max() * np.exp(-0.5)
        ax.annotate("", xy=(s, h), xytext=(-s, h), arrowprops=dict(arrowstyle="<->", lw=1.6, color=PURPLE))
        ax.text(s + 0.3, h, f"$2\\sigma_{var}$", color=PURPLE, va="center", fontsize=16)
        ax.set_yticks([]); ax.set_ylim(0, r.max() * 1.15)
        ax.grid(alpha=0.3)
    axs[row, 1].text(1.02, 0.5, f"$\\sigma_x={sx}$\n$\\sigma_p={sp:.2f}$\n$\\sigma_x\\sigma_p=\\hbar/2$",
                     transform=axs[row, 1].transAxes, fontsize=15, va="center")
axs[0, 0].set_title(r"position space: $|\psi(x)|^2$", fontsize=17)
axs[0, 1].set_title(r"momentum space: $|\varphi(p)|^2$", fontsize=17)
axs[2, 0].set_xlabel("position $x$"); axs[2, 1].set_xlabel("momentum $p$")
fig.tight_layout(rect=(0, 0, 0.88, 1))
fig.savefig(f"{OUT}/Uncertainty_xp.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- tunneling through a rectangular barrier
E, V0, l = 1.0, 2.0, 1.2           # hbar = m = 1
k = np.sqrt(2 * E); kap = np.sqrt(2 * (V0 - E))
# unknowns: r, Cp, Cm, t ; psi_I = e^{ikx}+r e^{-ikx}; psi_II = Cp e^{kap x}+Cm e^{-kap x}; psi_III = t e^{ikx}
M = np.array([[-1, 1, 1, 0],
              [1j * k, kap, -kap, 0],
              [0, np.exp(kap * l), np.exp(-kap * l), -np.exp(1j * k * l)],
              [0, kap * np.exp(kap * l), -kap * np.exp(-kap * l), -1j * k * np.exp(1j * k * l)]], dtype=complex)
rhs = np.array([1, 1j * k, 0, 0], dtype=complex)
r, Cp, Cm, t = np.linalg.solve(M, rhs)
xx = np.linspace(-12, 12, 3000)
psi = np.where(xx < 0, np.exp(1j * k * xx) + r * np.exp(-1j * k * xx),
               np.where(xx < l, Cp * np.exp(kap * xx) + Cm * np.exp(-kap * xx), t * np.exp(1j * k * xx)))
fig, ax = plt.subplots(figsize=(12, 5.5))
ax.add_patch(Rectangle((0, -2.2), l, 4.6, color="0.85", zorder=0))
ax.text(l / 2, 2.15, "barrier\n$V_0>E$", ha="center", va="top", fontsize=15)
ax.plot(xx, psi.real, color=C[0], lw=2, label=r"$\mathrm{Re}\,\psi(x)$")
ax.axhline(0, color="k", lw=0.8)
ax.text(-11.5, -1.95, "incoming and reflected waves", fontsize=14)
ax.text(3.0, -1.95, f"transmitted wave ($|t|^2={abs(t)**2:.2f}$)", fontsize=14)
ax.set_xlim(-12, 12); ax.set_ylim(-2.2, 2.4)
ax.set_xticks([0, l]); ax.set_xticklabels(["$0$", "$l$"])
ax.set_yticks([])
ax.set_xlabel("Position $x$")
ax.grid(alpha=0.3)
ax.set_ylabel(r"$\mathrm{Re}\,\psi(x)$")
fig.tight_layout()
fig.savefig(f"{OUT}/Tunneling.png", dpi=100)
plt.close(fig)
print("transmission", abs(t) ** 2, "reflection", abs(r) ** 2)
