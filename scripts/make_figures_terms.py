"""Figure for the atomic states section of chapter 9: the 1s2 2s2 2p2 configuration
of carbon split into terms and levels (experimental energies, NIST ASD).

Usage (from the project root):  python3 scripts/make_figures_terms.py img
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 18, "figure.dpi": 100})
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# experimental energies in cm^-1
levels = {"3P0": 0.0, "3P1": 16.4, "3P2": 43.4, "1D2": 10192.6, "1S0": 21648.0}
avg3P = (1 * 0.0 + 3 * 16.4 + 5 * 43.4) / 9
conf = (9 * avg3P + 5 * levels["1D2"] + 1 * levels["1S0"]) / 15

fig, ax = plt.subplots(figsize=(12, 8))
ax.hlines(conf, 0.2, 2.0, color="k", lw=3)
ax.text(1.1, conf + 500, r"$1s^2 2s^2 2p^2$", ha="center", fontsize=18)
ax.text(1.1, conf - 600, "configuration\n(15 microstates)", ha="center", va="top", fontsize=14)
terms = [("$^3P$", avg3P, C[0], 9), ("$^1D$", levels["1D2"], C[2], 5), ("$^1S$", levels["1S0"], C[3], 1)]
for lab, E, col, deg in terms:
    ax.hlines(E, 4.0, 5.8, color=col, lw=3)
    ax.plot([2.0, 4.0], [conf, E], ls="--", color="0.6", lw=1)
    ax.text(4.9, E + 450, f"{lab}  ({deg} state{'s' if deg > 1 else ''})", ha="center", fontsize=16, color=col)
ax.text(1.1, -2600, "orbitals only\n(average repulsion)", ha="center", fontsize=14, style="italic")
ax.text(4.9, -2600, "terms\n(Coulomb and exchange)", ha="center", fontsize=14, style="italic")
ax.text(8.6, -2600, "levels\n(spin–orbit coupling)", ha="center", fontsize=14, style="italic")
# J levels: 1D2 and 1S0 unsplit; 3P split (magnified in an inset)
for lab, key, col in (("$^1D_2$", "1D2", C[2]), ("$^1S_0$", "1S0", C[3])):
    E = levels[key]
    ax.hlines(E, 7.7, 9.5, color=col, lw=3)
    ax.plot([5.8, 7.7], [E, E], ls="--", color="0.6", lw=1)
    ax.text(9.65, E, f"{lab}  {E:,.0f} cm$^{{-1}}$", va="center", fontsize=15, color=col)
ax.hlines(avg3P, 7.7, 9.5, color=C[0], lw=6, alpha=0.35)
ax.plot([5.8, 7.7], [avg3P, avg3P], ls="--", color="0.6", lw=1)
ax.set_xlim(0, 13.5)
ax.set_ylim(-3600, 24000)
ax.set_xticks([])
ax.set_ylabel(r"Energy (cm$^{-1}$)")
for sp in ("top", "right", "bottom"):
    ax.spines[sp].set_visible(False)
# inset for the fine structure of 3P
axi = fig.add_axes([0.70, 0.19, 0.24, 0.2])
for J, key in ((0, "3P0"), (1, "3P1"), (2, "3P2")):
    axi.hlines(levels[key], 0, 1, color=C[0], lw=3)
    axi.text(1.08, levels[key], f"$^3P_{J}$  ({levels[key]:.1f} cm$^{{-1}}$)", va="center", fontsize=13, color=C[0])
axi.set_xlim(-0.1, 2.6); axi.set_ylim(-6, 52)
axi.set_xticks([]); axi.set_yticks([])
axi.set_title("ground term $^3P$, magnified", fontsize=13)
fig.savefig(f"{OUT}/Carbon_terms.png", dpi=100, bbox_inches="tight")
plt.close(fig)
print("done")

# ---------------------------------------------------------------- microstates of p2
from itertools import combinations
spinorb = [(ml, ms) for ml in (1, 0, -1) for ms in (0.5, -0.5)]
micro = list(combinations(spinorb, 2))
cells = {}
for a, b in micro:
    ML, MS = a[0] + b[0], int(a[1] + b[1])
    cells.setdefault((ML, MS), []).append((a, b))
def lab(so):
    ml, ms = so
    return f"{ml:+d}".replace("+0", "0").replace("-", "−") + ("↑" if ms > 0 else "↓")
MLs, MSs = [2, 1, 0, -1, -2], [1, 0, -1]

# (a) the microstates sorted by ML and MS
W = 1.7  # cell width
fig, ax = plt.subplots(figsize=(14, 8.5))
for i, ML in enumerate(MLs):
    for j, MS in enumerate(MSs):
        ax.add_patch(plt.Rectangle((j * W, -i), W, 1, fc="white", ec="0.3", lw=1.2))
        lst = cells.get((ML, MS), [])
        for k, (a, b) in enumerate(lst):
            ax.text(j * W + W / 2, -i + 0.78 - 0.24 * k, f"({lab(a)}, {lab(b)})", ha="center", va="center", fontsize=15)
        if not lst:
            ax.text(j * W + W / 2, -i + 0.5, "—", ha="center", va="center", fontsize=15, color="0.6")
for i, ML in enumerate(MLs):
    ax.text(-0.12, -i + 0.5, f"$M_L={ML:+d}$".replace("+0", "0"), ha="right", va="center", fontsize=17)
for j, MS in enumerate(MSs):
    ax.text(j * W + W / 2, 1.12, f"$M_S={MS:+d}$".replace("+0", "0"), ha="center", va="center", fontsize=17)
ax.set_xlim(-1.1, 3 * W + 0.05); ax.set_ylim(-4.05, 1.35)
ax.set_aspect("equal"); ax.axis("off")
fig.savefig(f"{OUT}/Carbon_microstates.png", dpi=100, bbox_inches="tight")
plt.close(fig)

# (b) peeling off the terms
counts = {k: len(v) for k, v in cells.items()}
steps = [("1D", C[2], [(ML, 0) for ML in MLs]),
         ("3P", C[0], [(ML, MS) for ML in (1, 0, -1) for MS in MSs]),
         ("1S", C[3], [(0, 0)])]
fig, axs = plt.subplots(1, 4, figsize=(17, 6.6))
titles = ["(a) all 15 microstates", r"(b) remove $^1D$: $L=2$, $S=0$", r"(c) remove $^3P$: $L=1$, $S=1$", r"(d) remove $^1S$: $L=0$, $S=0$"]
removed = {(ML, MS): [] for ML in MLs for MS in MSs}
for p, ax in enumerate(axs):
    if p > 0:
        name, col, blk = steps[p - 1]
        for key in blk:
            removed[key].append(col)
    for i, ML in enumerate(MLs):
        for j, MS in enumerate(MSs):
            ax.add_patch(plt.Rectangle((j, -i), 1, 1, fc="white", ec="0.4", lw=1))
            n = counts.get((ML, MS), 0)
            cols = removed[(ML, MS)]
            for k in range(n):
                xk = j + 0.5 + (k - (n - 1) / 2) * 0.25
                if k < len(cols):
                    filled = cols[k]
                    newest = p > 0 and filled == steps[p - 1][1] and k == len(cols) - 1
                    ax.plot(xk, -i + 0.5, "o", ms=15, mfc=filled, mec="k", alpha=1 if newest else 0.25)
                else:
                    ax.plot(xk, -i + 0.5, "o", ms=15, mfc="0.75", mec="k")
    if p > 0:
        name, col, blk = steps[p - 1]
        js = [MSs.index(MS) for ML, MS in blk]; is_ = [MLs.index(ML) for ML, MS in blk]
        ax.add_patch(plt.Rectangle((min(js) + 0.04, -max(is_) + 0.04), max(js) - min(js) + 0.92, max(is_) - min(is_) + 0.92,
                                   fill=False, ec=col, lw=3.5))
    for i, ML in enumerate(MLs):
        ax.text(-0.1, -i + 0.5, f"{ML:+d}".replace("+0", "0"), ha="right", va="center", fontsize=15)
    for j, MS in enumerate(MSs):
        ax.text(j + 0.5, 1.12, f"{MS:+d}".replace("+0", "0"), ha="center", va="center", fontsize=15)
    ax.text(-0.55, 1.12, r"$M_L \backslash M_S$", ha="center", va="center", fontsize=13)
    ax.set_title(titles[p], fontsize=16, pad=26)
    ax.set_xlim(-0.9, 3.05); ax.set_ylim(-4.05, 1.35)
    ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/Carbon_peeloff.png", dpi=100, bbox_inches="tight")
plt.close(fig)
print("microstates:", len(micro))
