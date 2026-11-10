"""Figures for the classical waves section of chapter 1.

Usage (from the project root):  python3 scripts/make_figures_ch1.py img
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 20, "legend.fontsize": 16, "figure.dpi": 100})
PURPLE = "purple"
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# ---------------------------------------------------------------- traveling wave
lam, A = 2.0, 1.0
k = 2 * np.pi / lam
x = np.linspace(0, 6, 800)
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(x, A * np.sin(k * x), color=C[0], lw=2.5, label=r"$t=0$")
ax.plot(x, A * np.sin(k * (x - 0.4)), color=C[0], lw=2, ls="--", alpha=0.6, label=r"a short time later")
ax.axhline(0, color="k", lw=0.8)
# wavelength arrow between two crests
x1, x2 = lam / 4, lam / 4 + lam
ax.annotate("", xy=(x2, 1.18), xytext=(x1, 1.18), arrowprops=dict(arrowstyle="<->", lw=1.6))
ax.text((x1 + x2) / 2, 1.25, r"wavelength $\lambda$", ha="center", va="bottom")
# amplitude arrow
xa = 2 * lam + lam / 4
ax.annotate("", xy=(xa, A), xytext=(xa, 0), arrowprops=dict(arrowstyle="<->", lw=1.6, color=C[3]))
ax.text(xa + 0.08, A / 2, r"amplitude $A$", color=C[3], va="center")
# direction of motion
ax.annotate("", xy=(5.9, -1.35), xytext=(4.9, -1.35), arrowprops=dict(arrowstyle="->", lw=2, color="0.3"))
ax.text(5.4, -1.25, r"speed $v$", ha="center", va="bottom", color="0.3")
ax.set_xlabel(r"Position $x$")
ax.set_ylabel(r"Displacement $y(x,t)$")
ax.set_xlim(0, 6)
ax.set_ylim(-1.6, 1.7)
ax.set_yticks([-1, 0, 1])
ax.set_xticks([])
ax.grid(alpha=0.3)
ax.legend(loc="lower left")
fig.tight_layout()
fig.savefig(f"{OUT}/Wave_traveling.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- standing waves on a string
L = 1.0
x = np.linspace(0, L, 600)
fig, ax = plt.subplots(figsize=(9, 9))
for n in range(1, 5):
    base = 2.6 * (n - 1)
    psi = np.sin(n * np.pi * x / L)
    for phase in np.linspace(-1, 1, 5):
        ax.plot(x, base + phase * psi, color=C[0], lw=1, alpha=0.25)
    ax.plot(x, base + psi, color=C[0], lw=2.5)
    ax.plot(x, base - psi, color=C[0], lw=2.5, ls="--")
    ax.hlines(base, 0, L, color="k", lw=0.8)
    nodes = [j * L / n for j in range(1, n)]
    ax.plot(nodes, [base] * len(nodes), "o", color=PURPLE, ms=9, zorder=5)
    ax.plot([0, L], [base, base], "s", color="k", ms=9, zorder=5)
    ax.text(1.04, base, f"$n={n}$,  $\\lambda_{n}=" + {1: "2L", 2: "L", 3: "2L/3", 4: "L/2"}[n] + "$", va="center", fontsize=17)
ax.set_xlim(-0.05, 1.45)
ax.set_ylim(-1.5, 2.6 * 3 + 1.5)
ax.set_xticks([0, L])
ax.set_xticklabels(["$0$", "$L$"])
ax.set_yticks([])
ax.set_xlabel("Position along the string $x$")
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/Wave_standing.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- superposition / interference
x = np.linspace(0, 4, 800)
w1 = np.sin(2 * np.pi * x)
fig, axs = plt.subplots(1, 2, figsize=(13, 4.5), sharey=True)
for ax, ph, title in ((axs[0], 0, "constructive (in phase)"), (axs[1], np.pi, "destructive (out of phase)")):
    w2 = np.sin(2 * np.pi * x + ph)
    ax.plot(x, w1, color=C[0], lw=1.5, ls="--", label="wave 1")
    ax.plot(x, w2, color=C[1], lw=1.5, ls=":", label="wave 2")
    ax.plot(x, w1 + w2, color=C[3], lw=2.5, label="sum")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_title(title, fontsize=18)
    ax.set_xticks([])
    ax.set_xlabel("Position $x$")
    ax.grid(alpha=0.3)
axs[0].set_ylabel("Displacement")
axs[0].set_ylim(-2.3, 2.6)
axs[1].legend(loc="upper right", fontsize=14)
fig.tight_layout()
fig.savefig(f"{OUT}/Wave_interference.png", dpi=100)
plt.close(fig)
print("done")
