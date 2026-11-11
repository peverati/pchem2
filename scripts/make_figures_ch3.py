"""Figures for chapter 3: free-particle plane waves and wave packets.

Units: hbar = m = 1. Usage (from the project root):  python3 scripts/make_figures_ch3.py img
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

# ---------------------------------------------------------------- plane wave
# Front view: real part in the vertical plane, imaginary part on a horizontal
# plane drawn in oblique perspective (a depiction, not an exact projection).
from matplotlib.patches import Polygon
x = np.linspace(0, 4 * np.pi, 800); k = 2.0
re, im = np.cos(k * x), np.sin(k * x)
# oblique ("cabinet") projection of the horizontal plane: depth goes up-right
dx, dy = 0.55, 0.32
X_im, Y_im = x + dx * im, dy * im
fig = plt.figure(figsize=(12, 7.6))
L = x[-1]
PAD = 1.6
sc = 0.82 / L  # figure fraction per unit of x, matching the bottom panel
ax = fig.add_axes([0.1 - PAD * sc, 0.44, (L + 2 * PAD) * sc, 0.465])
# faint planes
ax.add_patch(Polygon([(0, -1.25), (L, -1.25), (L, 1.25), (0, 1.25)], closed=True, fc="0.97", ec="0.8", lw=1, zorder=0))
ax.add_patch(Polygon([(-dx, -dy), (L - dx, -dy), (L + dx, dy), (dx, dy)], closed=True, fc="0.92", ec="0.75", lw=1, zorder=0.5))
# imaginary part (horizontal plane, drawn behind)
ax.fill(np.r_[X_im, L, 0], np.r_[Y_im, 0, 0], color=C[3], alpha=0.25, lw=0, zorder=1)
ax.plot(X_im, Y_im, color=C[3], lw=2.5, zorder=2, label=r"imaginary part, $\sin(kx)$ (horizontal plane)")
# real part (vertical plane, in front)
ax.fill_between(x, re, color=C[0], alpha=0.25, lw=0, zorder=3)
ax.plot(x, re, color=C[0], lw=2.5, zorder=4, label=r"real part, $\cos(kx)$ (vertical plane)")
ax.plot([0, L], [0, 0], color="k", lw=1, zorder=5)
ax.annotate("", xy=(L + 0.9, 0), xytext=(L, 0), arrowprops=dict(arrowstyle="-|>", lw=1.2))
ax.text(L + 1.0, 0, "$x$", va="center", fontsize=18)
ax.annotate("", xy=(-0.3, 1.35), xytext=(-0.3, 0), arrowprops=dict(arrowstyle="-|>", lw=1.2, color=C[0]))
ax.text(-0.45, 1.25, r"Re $\psi$", ha="right", color=C[0], fontsize=16)
ax.annotate("", xy=(-0.3 + 1.6 * dx, 1.6 * dy), xytext=(-0.3, 0), arrowprops=dict(arrowstyle="-|>", lw=1.2, color=C[3]))
ax.text(-0.3 + 1.7 * dx, 1.7 * dy + 0.05, r"Im $\psi$", color=C[3], fontsize=16)
ax.set_xlim(-PAD, L + PAD); ax.set_ylim(-1.4, 1.75); ax.axis("off")
h, l = ax.get_legend_handles_labels()
ax.legend(h[::-1], l[::-1], loc="upper center", ncol=2, fontsize=13, frameon=False, bbox_to_anchor=(0.5, 1.13))
ax2 = fig.add_axes([0.1, 0.09, 0.82, 0.29])
ax2.fill_between(x, np.ones_like(x), color="cyan", alpha=0.5); ax2.plot(x, np.ones_like(x), color="teal", lw=2.2)
ax2.set_ylabel(r"$|\psi(x)|^2$"); ax2.set_ylim(0, 1.6); ax2.set_xlim(0, L); ax2.set_xticks([]); ax2.grid(alpha=0.3)
ax2.set_xlabel(r"Position $x$ (the wave continues forever in both directions)")
fig.savefig(f"{OUT}/FP_planewave.png", dpi=100)
plt.close(fig)


# ---------------------------------------------------------------- building a wave packet
x = np.linspace(-20, 20, 3000)
k0, sk = 5.0, 0.5
fig, axs = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
for ax, N in zip(axs, (2, 5, 41)):
    ks = np.linspace(k0 - 2.5 * sk, k0 + 2.5 * sk, N) if N > 2 else np.array([k0 - 0.3, k0 + 0.3])
    w = np.exp(-(ks - k0) ** 2 / (2 * sk**2))
    s = (w[:, None] * np.exp(1j * ks[:, None] * x[None, :])).sum(axis=0)
    s = s / np.abs(s).max()
    ax.plot(x, s.real, color=C[0], lw=1.3, label=r"$\mathrm{Re}\,\Psi$")
    ax.plot(x, np.abs(s), color=C[1], lw=2, label=r"envelope $|\Psi|$")
    ax.plot(x, -np.abs(s), color=C[1], lw=2)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_title(f"sum of {N} plane waves" if N > 2 else "sum of 2 plane waves (beats)", fontsize=16)
    ax.set_yticks([])
    ax.set_ylim(-1.15, 1.15)
    ax.grid(alpha=0.3)
axs[0].legend(loc="upper right", ncol=2)
axs[-1].set_xlabel("Position $x$")
axs[-1].set_xticks([])
fig.tight_layout()
fig.savefig(f"{OUT}/FP_buildpacket.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- Gaussian packet: motion and spreading
L, Ngrid = 160.0, 8192
x = np.linspace(-L / 2, L / 2, Ngrid, endpoint=False)
kgrid = 2 * np.pi * np.fft.fftfreq(Ngrid, d=x[1] - x[0])
s0, k0, x0 = 1.0, 3.0, -25.0
psi0 = (2 * np.pi * s0**2) ** -0.25 * np.exp(-(x - x0) ** 2 / (4 * s0**2) + 1j * k0 * x)
phik = np.fft.fft(psi0)
def evolve(t):
    return np.fft.ifft(phik * np.exp(-1j * kgrid**2 * t / 2))
fig, ax = plt.subplots(figsize=(12, 5.5))
times = [0, 5, 10, 15]
cols = [C[0], C[2], C[1], C[3]]
for t, col in zip(times, cols):
    p = evolve(t)
    rho = np.abs(p) ** 2
    ax.fill_between(x, rho, color=col, alpha=0.25)
    ax.plot(x, rho, color=col, lw=2.2, label=f"$t={t}$")
    xm = np.sum(x * rho) / np.sum(rho)
    ax.plot(xm, rho.max() + 0.015, "v", color=PURPLE, ms=9)
ax.annotate("", xy=(22, 0.43), xytext=(-25, 0.43), arrowprops=dict(arrowstyle="->", lw=1.8, color=PURPLE))
ax.text(-1.5, 0.445, r"moves with $v=p/m$", color=PURPLE, ha="center", fontsize=16)
ax.set_xlim(-35, 30)
ax.set_ylim(0, 0.5)
ax.set_xlabel("Position $x$")
ax.set_ylabel(r"$|\Psi(x,t)|^2$")
ax.legend(loc="upper right")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(f"{OUT}/FP_packet_motion.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- narrow vs wide packet: position and momentum
fig, axs = plt.subplots(2, 2, figsize=(12, 7))
xx = np.linspace(-12, 12, 2000)
kk = np.linspace(0, 10, 1000)
for row, (s0, name) in enumerate(((0.6, "narrow packet"), (2.5, "wide packet"))):
    sk = 1 / (2 * s0)
    psi = np.exp(-xx**2 / (4 * s0**2) + 1j * 5 * xx)
    axs[row, 0].plot(xx, psi.real, color=C[0], lw=1.2)
    axs[row, 0].plot(xx, np.abs(psi), color=C[1], lw=2)
    axs[row, 0].plot(xx, -np.abs(psi), color=C[1], lw=2)
    axs[row, 0].set_title(f"{name}: position", fontsize=16)
    phi = np.exp(-(kk - 5) ** 2 / (2 * sk**2))
    axs[row, 1].fill_between(kk, phi, color="cyan", alpha=0.5)
    axs[row, 1].plot(kk, phi, color="teal", lw=2)
    axs[row, 1].set_title(f"{name}: spread of $k$ (momentum)", fontsize=16)
    for ax in axs[row]:
        ax.set_yticks([])
        ax.grid(alpha=0.3)
axs[1, 0].set_xlabel("Position $x$")
axs[1, 1].set_xlabel("Wave vector $k=p/\\hbar$")
for ax in axs[:, 0]:
    ax.set_xticks([])
for ax in axs[:, 1]:
    ax.set_xticks([5]); ax.set_xticklabels(["$k_0$"])
fig.tight_layout()
fig.savefig(f"{OUT}/FP_uncertainty.png", dpi=100)
plt.close(fig)
print("done")
