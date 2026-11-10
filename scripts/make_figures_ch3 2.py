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
x = np.linspace(0, 6 * np.pi, 1000)
k = 2.0
psi = np.exp(1j * k * x)
fig, axs = plt.subplots(2, 1, figsize=(11, 6.5), sharex=True)
axs[0].plot(x, psi.real, color=C[0], lw=2.2, label=r"real part, $\cos(kx)$")
axs[0].plot(x, psi.imag, color=C[1], lw=2.2, ls="--", label=r"imaginary part, $\sin(kx)$")
axs[0].axhline(0, color="k", lw=0.8)
axs[0].set_ylabel(r"$\psi(x)$")
axs[0].set_ylim(-1.5, 1.9)
axs[0].legend(loc="upper right", ncol=2)
axs[1].fill_between(x, np.abs(psi) ** 2, color="cyan", alpha=0.5)
axs[1].plot(x, np.abs(psi) ** 2, color="teal", lw=2.2)
axs[1].set_ylabel(r"$|\psi(x)|^2$")
axs[1].set_ylim(0, 1.6)
axs[1].set_xlabel(r"Position $x$ (the wave continues forever in both directions)")
axs[1].set_xticks([])
for ax in axs:
    ax.grid(alpha=0.3)
fig.tight_layout()
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
    ax.plot(x, np.abs(s), color=C[3], lw=2, label=r"envelope $|\Psi|$")
    ax.plot(x, -np.abs(s), color=C[3], lw=2)
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
    axs[row, 0].plot(xx, np.abs(psi), color=C[3], lw=2)
    axs[row, 0].plot(xx, -np.abs(psi), color=C[3], lw=2)
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
