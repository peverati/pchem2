"""Replacements for the diagrams previously borrowed from Wikipedia:
vector model of orbital angular momentum (ch. 6), rotational levels and spectrum,
rovibrational transitions, and the Franck-Condon principle (ch. 13).

Usage (from the project root):  python3 scripts/make_figures_redraw.py img
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 18, "legend.fontsize": 14, "figure.dpi": 100})
PURPLE = "purple"
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# ---------------------------------------------------------------- vector model, l = 2
l = 2
Lmag = np.sqrt(l * (l + 1))
fig = plt.figure(figsize=(9.5, 10))
ax = fig.add_subplot(projection="3d")
LCOL = {2: C[3], 1: C[1], 0: "k", -1: C[2], -2: C[0]}
phi = np.linspace(0, 2 * np.pi, 90)
for m in range(-l, l + 1):
    col = LCOL[m]
    rho = np.sqrt(Lmag**2 - m**2)
    T, P = np.meshgrid(np.linspace(0, 1, 15), phi)
    if m != 0:
        ax.plot_surface(T * rho * np.cos(P), T * rho * np.sin(P), T * m, color=col, alpha=0.15, lw=0)
    ax.plot(rho * np.cos(phi), rho * np.sin(phi), m * np.ones_like(phi), color=col, lw=1.6)
    ph0 = 0.7
    ax.quiver(0, 0, 0, rho * np.cos(ph0), rho * np.sin(ph0), m, color=col, lw=2.5, arrow_length_ratio=0.07)
    ax.text2D(0.04, 0.5 + 0.105 * m, (f"$m_\\ell={m:+d}$:  $L_z={m:+d}\\hbar$" if abs(m) > 1 else f"$m_\\ell={m:+d}$:  $L_z={'+' if m > 0 else '-'}\\hbar$") if m else r"$m_\ell=0$:  $L_z=0$",
              transform=ax.transAxes, color=col, fontsize=17)
ax.plot([0, 0], [0, 0], [-3, 3], color="k", lw=1)
ax.text(0, 0, 3.15, "$z$", fontsize=20)
ax.text2D(0.04, 0.95, r"$\ell=2$: length of each vector $|\mathbf{L}|=\sqrt{6}\,\hbar\approx2.45\,\hbar$",
          transform=ax.transAxes, fontsize=17)
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.5, 2.5); ax.set_zlim(-3, 3)
ax.set_box_aspect((1, 1, 1.2))
ax.view_init(elev=12, azim=-55)
ax.set_axis_off()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
fig.savefig(f"{OUT}/L_vector_model.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- rotational levels and spectrum
B = 1.0
Jmax = 6
fig = plt.figure(figsize=(10, 9))
ax = fig.add_axes([0.08, 0.3, 0.86, 0.66])
for J in range(Jmax + 1):
    E = B * J * (J + 1)
    ax.hlines(E, 0, 13, color="k", lw=1.5)
    ax.text(13.2, E, f"$J={J}$", va="center", fontsize=15)
    ax.text(-0.2, E, f"${J*(J+1)}B$" if J else "$0$", va="center", ha="right", fontsize=14)
xs = [1.5 + 1.8 * J for J in range(Jmax)]
for J, x in zip(range(Jmax), xs):
    ax.annotate("", xy=(x, B * (J + 1) * (J + 2)), xytext=(x, B * J * (J + 1)),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C[3]))
    ax.text(x + 0.12, B * J * (J + 1) + 1.0 + J * 0.6, f"${J}\\rightarrow{J+1}$", fontsize=13, color=C[3])
ax.set_xlim(-1.5, 14.5); ax.set_ylim(-1.5, 47)
ax.axis("off")
ax.text(-1.4, 47, "energy", fontsize=16, va="top")
ax2 = fig.add_axes([0.08, 0.08, 0.86, 0.15])
pos = [2 * B * (J + 1) for J in range(Jmax)]
ax2.vlines(pos, 0, 1, color=C[3], lw=3)
for J, p in enumerate(pos):
    ax2.text(p, 1.08, f"{2*(J+1)}B", ha="center", fontsize=13)
ax2.set_xlim(0, 14); ax2.set_ylim(0, 1.35); ax2.set_yticks([])
ax2.set_xticks(range(0, 15, 2)); ax2.set_xticklabels(["0"] + [f"{k}B" for k in range(2, 15, 2)])
ax2.set_xlabel(r"Wavenumber of the absorbed light $\tilde{\nu}$")
ax2.annotate("", xy=(4, 0.5), xytext=(2, 0.5), arrowprops=dict(arrowstyle="<->", lw=1.3))
ax2.text(3, 0.6, "$2B$", ha="center", fontsize=14)
fig.savefig(f"{OUT}/Rot_levels.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- rovibrational transitions (P and R branches)
Bv = 1.0
gap = 40.0
fig, ax = plt.subplots(figsize=(11, 9))
for v, base in ((0, 0.0), (1, gap)):
    for J in range(5):
        E = base + Bv * J * (J + 1)
        ax.hlines(E, 0, 16, color="k", lw=1.2)
        ax.text(16.2, E, f"$J={J}$", va="center", fontsize=13)
    ax.text(-0.4, base + 8, f"$v={v}$", ha="right", va="center", fontsize=19)
# R branch: J -> J+1 ; P branch: J -> J-1
for k, J in enumerate(range(0, 4)):
    x = 9.0 + 1.6 * k
    ax.annotate("", xy=(x, gap + (J + 1) * (J + 2)), xytext=(x, J * (J + 1)),
                arrowprops=dict(arrowstyle="-|>", lw=2, color=C[3]))
    ax.text(x, gap + (J + 1) * (J + 2) + 1.2, f"R({J})", ha="center", fontsize=12, color=C[3])
for k, J in enumerate(range(1, 5)):
    x = 1.2 + 1.6 * k
    ax.annotate("", xy=(x, gap + (J - 1) * J), xytext=(x, J * (J + 1)),
                arrowprops=dict(arrowstyle="-|>", lw=2, color=C[0]))
    ax.text(x, gap + (J - 1) * J + 1.2, f"P({J})", ha="center", fontsize=12, color=C[0])
ax.text(3.6, -4.0, r"P-branch, $\Delta J=-1$", color=C[0], ha="center", fontsize=16)
ax.text(11.4, -4.0, r"R-branch, $\Delta J=+1$", color=C[3], ha="center", fontsize=16)
ax.set_xlim(-2.5, 18); ax.set_ylim(-6, gap + 24)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/Rovib_levels.png", dpi=100)
plt.close(fig)

# ---------------------------------------------------------------- Franck-Condon principle
def morse(r, De, a, re):
    return De * (1 - np.exp(-a * (r - re))) ** 2
r = np.linspace(0.6, 4.5, 2500)
dr = r[1] - r[0]
mu = 20.0
def levels(V, n):
    diag = 1 / (mu * dr**2) + V
    off = -0.5 / (mu * dr**2) * np.ones(len(r) - 1)
    E, W = eigh_tridiagonal(diag, off, select="i", select_range=(0, n - 1))
    W = W / np.sqrt(dr)
    return E, W
De0, a0, re0 = 12.0, 1.4, 1.4
De1, a1, re1, T1 = 10.0, 1.0, 1.9, 12.0
V0 = morse(r, De0, a0, re0)
V1 = morse(r, De1, a1, re1) + T1
E0, W0 = levels(V0, 3)
E1, W1 = levels(V1, 9)
fc = (W0[:, 0] @ W1 * dr) ** 2
vbest = int(np.argmax(fc))
fig, ax = plt.subplots(figsize=(10, 9))
ax.plot(r, V0, color=C[0], lw=2.5)
ax.plot(r, V1, color=C[3], lw=2.5)
sc = 0.3
for E, w, col in [(E0[0], W0[:, 0], C[0])] + [(E1[i], W1[:, i], C[3]) for i in range(9)]:
    inside = (morse(r, De0, a0, re0) if col == C[0] else morse(r, De1, a1, re1) + T1) <= E + 0.4
    ax.hlines(E, r[inside][0], r[inside][-1], color=col, lw=1, alpha=0.6)
    ww = w if w[np.argmax(abs(w))] > 0 else -w
    ax.plot(r[inside], E + sc * ww[inside], color=col, lw=1.3)
x_v = re0
ax.annotate("", xy=(x_v, E1[vbest]), xytext=(x_v, E0[0]), arrowprops=dict(arrowstyle="-|>", lw=3, color=PURPLE))
ax.axvline(re0, color="0.6", ls=":", lw=1)
ax.text(x_v + 0.05, (E0[0] + E1[vbest]) / 2, "vertical\ntransition", color=PURPLE, fontsize=15, va="center")
ax.text(4.0, morse(4.0, De0, a0, re0) - 1.0, "ground state", color=C[0], fontsize=16, ha="center")
ax.text(4.0, morse(4.0, De1, a1, re1) + T1 + 0.7, "excited state", color=C[3], fontsize=16, ha="center")
ax.text(1.0, E0[0] + 0.3, "$v''=0$", ha="right", va="center", fontsize=15, color=C[0])
ax.text(1.22, E1[vbest], f"$v'={vbest}$", ha="right", va="center", fontsize=15, color=C[3])
ax.set_xlim(0.6, 4.5); ax.set_ylim(-0.5, 22)
ax.set_xlabel("Internuclear distance $R$")
ax.set_ylabel("Energy")
ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout()
fig.savefig(f"{OUT}/Franck_Condon.png", dpi=100)
plt.close(fig)
print("FC factors from v''=0:", np.round(fc, 3), "strongest v' =", vbest)
