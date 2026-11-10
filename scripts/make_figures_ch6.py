"""Figure for chapter 6: time evolution of a particle-in-a-box superposition.

Usage (from the project root):  python3 scripts/make_figures_ch6.py img
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 18, "legend.fontsize": 14, "figure.dpi": 100})
PURPLE = "purple"
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]
trapz = getattr(np, "trapezoid", None) or np.trapz

a = 1.0
x = np.linspace(0, a, 600)
p1 = np.sqrt(2 / a) * np.sin(np.pi * x / a)
p2 = np.sqrt(2 / a) * np.sin(2 * np.pi * x / a)
# time in units of the period T = 2*pi*hbar/(E2-E1); E1 = 1, E2 = 4 (arbitrary units)
def psi(t):
    w1, w2 = 2 * np.pi * (1 / 3) * t, 2 * np.pi * (4 / 3) * t   # phases E_n t / hbar with E2-E1 = 3 -> period 1
    return (p1 * np.exp(-1j * w1) + p2 * np.exp(-1j * w2)) / np.sqrt(2)

fig = plt.figure(figsize=(14, 8))
times = [0, 0.25, 0.5, 0.75]
labels = ["$t=0$", "$t=T/4$", "$t=T/2$", "$t=3T/4$"]
for k, (t, lab) in enumerate(zip(times, labels)):
    ax = fig.add_subplot(2, 4, k + 1)
    rho = np.abs(psi(t)) ** 2
    ax.fill_between(x, rho, color="cyan", alpha=0.5)
    ax.plot(x, rho, color="teal", lw=2)
    xm = trapz(x * rho, x)
    ax.axvline(xm, color=PURPLE, ls="--", lw=1.8)
    ax.set_title(lab, fontsize=17)
    ax.set_xticks([0, a / 2, a]); ax.set_xticklabels(["$0$", "$a/2$", "$a$"])
    ax.set_yticks([])
    ax.set_ylim(0, 3.7)
    if k == 0:
        ax.set_ylabel(r"$|\Psi(x,t)|^2$")
ax = fig.add_subplot(2, 1, 2)
tt = np.linspace(0, 2, 400)
xm = [trapz(x * np.abs(psi(t)) ** 2, x) for t in tt]
ax.plot(tt, xm, color=PURPLE, lw=2.5)
ax.axhline(a / 2, color="0.5", ls=":", lw=1.2)
ax.set_xlabel(r"Time $t/T$")
ax.set_ylabel(r"$\langle x\rangle$")
ax.set_yticks([0.25, 0.5, 0.75]); ax.set_yticklabels(["$a/4$", "$a/2$", "$3a/4$"])
ax.set_ylim(0.2, 0.8)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(f"{OUT}/PIB_superposition.png", dpi=100)
plt.close(fig)
print("amplitude of <x>:", (max(xm) - min(xm)) / 2, "expected 16/(9 pi^2) =", 16 / (9 * np.pi**2))
