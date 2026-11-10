"""Figures for chapter 13 (polyatomic molecules): water MO diagram, localized
orbitals of water, and Hückel theory.

The water orbitals are rebuilt from the STO-3G basis set at the geometry used in
the text (R(OH) = 0.95 Å, angle = 104.5°), using the MO coefficients reported in
eq. (eigenvalMO). The script first checks that the rebuilt basis reproduces the
overlap matrix of eq. (smatrix).

Usage (from the project root):  python3 scripts/make_figures_polyatomic.py img
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
EV = 27.2114

# ------------------------------------------------------------------ geometry and basis
R = 0.95 / 0.529177
th = np.radians(104.5 / 2)
O = np.array([0.0, 0.0, 0.0])
Ha = np.array([0.0, R * np.sin(th), -R * np.cos(th)])
Hb = np.array([0.0, -R * np.sin(th), -R * np.cos(th)])

h_a = np.array([3.42525091, 0.62391373, 0.16885540]); h_c = np.array([0.15432897, 0.53532814, 0.44463454])
o1_a = np.array([130.7093200, 23.8088610, 6.4436083]); o1_c = h_c
o2_a = np.array([5.0331513, 1.1695961, 0.3803890])
o2s_c = np.array([-0.09996723, 0.39951283, 0.70011547])
o2p_c = np.array([0.15591627, 0.60768372, 0.39195739])

# basis: (center, exponents, coefficients, angular part: None, 0=x, 1=y, 2=z)
basis = [(O, o1_a, o1_c, None), (O, o2_a, o2s_c, None), (O, o2_a, o2p_c, 0),
         (O, o2_a, o2p_c, 1), (O, o2_a, o2p_c, 2), (Ha, h_a, h_c, None), (Hb, h_a, h_c, None)]


def evaluate(bf, X, Y, Z):
    cen, a, c, ang = bf
    dx, dy, dz = X - cen[0], Y - cen[1], Z - cen[2]
    r2 = dx**2 + dy**2 + dz**2
    out = 0
    for ai, ci in zip(a, c):
        if ang is None:
            N = (2 * ai / np.pi) ** 0.75
            out = out + ci * N * np.exp(-ai * r2)
        else:
            N = (2 * ai / np.pi) ** 0.75 * 2 * np.sqrt(ai)
            out = out + ci * N * np.exp(-ai * r2)
    if ang is not None:
        out = out * (dx, dy, dz)[ang]
    return out


# 3D grid for numerical integrals
g = np.linspace(-6, 6, 121)
X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
dV = (g[1] - g[0]) ** 3
F = np.array([evaluate(bf, X, Y, Z) for bf in basis])
S_num = np.einsum("ixyz,jxyz->ij", F, F) * dV

S_text = np.array([
    [1.000, 0.237, 0, 0, 0, 0.055, 0.055],
    [0.237, 1.000, 0, 0, 0, 0.479, 0.479],
    [0, 0, 1.000, 0, 0, 0, 0],
    [0, 0, 0, 1.000, 0, 0.313, -0.313],
    [0, 0, 0, 0, 1.000, -0.242, -0.242],
    [0.055, 0.479, 0, 0.313, -0.242, 1.000, 0.256],
    [0.055, 0.479, 0, -0.313, -0.242, 0.256, 1.000]])
print("max |S_num - S_text| (core 1s excluded):", np.abs(S_num - S_text)[1:, 1:].max())

E = np.array([-20.24094, -1.27218, -0.62173, -0.45392, -0.39176, 0.61293, 0.75095])
Cmo = np.array([
    [.99411, -.23251, .00000, -.10356, .00000, -.13340, .00000],
    [.02672, .83085, .00000, .53920, .00000, .89746, .00000],
    [.00000, .00000, .00000, .00000, 1.0000, .00000, .00000],
    [.00000, .00000, .60677, .00000, .00000, .00000, .99474],
    [-.00442, -.13216, .00000, .77828, .00000, -.74288, .00000],
    [-.00605, .15919, .44453, -.27494, .00000, -.80246, -.84542],
    [-.00605, .15919, -.44453, -.27494, .00000, -.80246, .84542]])
print("diag of C^T S C:", np.round(np.diag(Cmo.T @ S_text @ Cmo), 3))
print("Koopmans IEs (eV):", np.round(-E[:5] * EV, 2))

# ------------------------------------------------------------------ Foster-Boys localization of the 4 valence MOs
Cv = Cmo[:, 1:5].copy()
def centroids(Cv):
    phi = np.einsum("mi,mxyz->ixyz", Cv, F)
    dens = phi**2 * dV
    n = dens.sum(axis=(1, 2, 3))
    return np.array([(dens * X).sum(axis=(1, 2, 3)), (dens * Y).sum(axis=(1, 2, 3)), (dens * Z).sum(axis=(1, 2, 3))]).T / n[:, None]
def boys(Cv):
    return (centroids(Cv) ** 2).sum()
for sweep in range(30):
    changed = False
    for i in range(4):
        for j in range(i + 1, 4):
            best, bestg = boys(Cv), 0.0
            for gam in np.linspace(-np.pi / 4, np.pi / 4, 91):
                T = Cv.copy()
                ci, cj = Cv[:, i], Cv[:, j]
                T[:, i] = np.cos(gam) * ci + np.sin(gam) * cj
                T[:, j] = -np.sin(gam) * ci + np.cos(gam) * cj
                b = boys(T)
                if b > best + 1e-7:
                    best, bestg = b, gam
            if bestg != 0.0:
                ci, cj = Cv[:, i].copy(), Cv[:, j].copy()
                Cv[:, i] = np.cos(bestg) * ci + np.sin(bestg) * cj
                Cv[:, j] = -np.sin(bestg) * ci + np.cos(bestg) * cj
                changed = True
    if not changed:
        break
cen = centroids(Cv)
print("LMO centroids (a0):\n", np.round(cen, 3))
lp = [k for k in range(4) if abs(cen[k, 0]) > 0.1]
bd = [k for k in range(4) if k not in lp]
v1, v2 = cen[lp[0]], cen[lp[1]]
ang_lp = np.degrees(np.arccos(v1 @ v2 / np.linalg.norm(v1) / np.linalg.norm(v2)))
w1, w2 = cen[bd[0]], cen[bd[1]]
ang_bd = np.degrees(np.arccos(w1 @ w2 / np.linalg.norm(w1) / np.linalg.norm(w2)))
print(f"angle between lone-pair centroids: {ang_lp:.1f} deg; between bond centroids: {ang_bd:.1f} deg")
np.savetxt(f"{OUT}/../scripts/water_LMO_coefficients.txt" if OUT == "img" else f"{OUT}/water_LMO_coefficients.txt",
           Cv, fmt="%9.5f", header="Boys-localized valence MOs of water (columns), basis order as in eq. eigenvalMO")

# ------------------------------------------------------------------ plots of localized orbitals
def plane_map(coeffs, plane):
    s = np.linspace(-3.2, 3.2, 300)
    A, B = np.meshgrid(s, s)
    if plane == "yz":
        XX, YY, ZZ = 0 * A, A, B
    else:
        XX, YY, ZZ = A, 0 * A, B
    f = sum(c * evaluate(bf, XX, YY, ZZ) for c, bf in zip(coeffs, basis))
    return A, B, f

fig, axs = plt.subplots(2, 2, figsize=(11, 11))
panels = [(bd[0], "yz", "O–H bond (molecular plane)"), (bd[1], "yz", "O–H bond (molecular plane)"),
          (lp[0], "xz", "lone pair (perpendicular plane)"), (lp[1], "xz", "lone pair (perpendicular plane)")]
for ax, (k, plane, title) in zip(axs.flat, panels):
    v = Cv[:, k]
    c0 = cen[k]
    val = sum(c * evaluate(bf, np.array(c0[0]), np.array(c0[1]), np.array(c0[2])) for c, bf in zip(v, basis))
    if val < 0:
        v = -v
    A, B, f = plane_map(v, plane)
    m = np.abs(f).max() * 0.6
    ax.contourf(A, B, np.clip(f, -m, m), levels=np.linspace(-m, m, 41), cmap="RdBu_r")
    ax.plot(0, 0, "o", color="k", ms=8)
    if plane == "yz":
        for H in (Ha, Hb):
            ax.plot(H[1], H[2], "o", color="w", ms=8, mec="k")
        ax.set_xlabel(r"$y/a_0$")
    else:
        ax.set_xlabel(r"$x/a_0$")
        # the two H atoms lie out of this plane (y = +/-1.42 a0); both project onto (x=0, z=z_H)
        ax.plot([0, 0], [0, Ha[2]], ls="--", color="0.3", lw=1.2)
        ax.plot(0, Ha[2], "o", mfc="white", mec="k", ms=8)
        ax.text(0.15, Ha[2] - 0.35, "2 H (projected)", fontsize=13)
    ax.set_ylabel(r"$z/a_0$")
    ax.set_title(title, fontsize=17)
    ax.set_aspect("equal")
fig.tight_layout()
fig.savefig(f"{OUT}/H2O_LMO.png", dpi=100)
plt.close(fig)

# ------------------------------------------------------------------ MO diagram of water
fig, ax = plt.subplots(figsize=(11, 9))
names = [r"$1a_1$", r"$2a_1$", r"$1b_2$", r"$3a_1$", r"$1b_1$", r"$4a_1$", r"$2b_2$"]
for k in range(1, 7):
    col = C[0] if k < 5 else C[3]
    ax.hlines(E[k], 2.6, 3.4, color=col, lw=3)
    if k < 5:
        ax.text(3.0, E[k] + 0.004, r"$\uparrow\!\downarrow$", ha="center", va="center", fontsize=19)
    dy = {4: 0.03, 3: -0.03}.get(k, 0)
    ax.text(3.5, E[k] + dy, f"MO{k + 1}: {names[k]}  ({E[k]:+.3f})", va="center", fontsize=16)
# oxygen atomic levels (qualitative positions)
ao_O = {"$2s$": -1.05, "$2p$": -0.39}
ax.hlines(ao_O["$2s$"], 0.3, 0.9, color="0.3", lw=3)
for dx in (-0.25, 0, 0.25):
    ax.hlines(ao_O["$2p$"], 0.6 + dx - 0.1, 0.6 + dx + 0.1, color="0.3", lw=3)
ax.text(0.6, ao_O["$2s$"] - 0.1, "O $2s$", ha="center", va="top")
ax.text(0.6, ao_O["$2p$"] - 0.1, "O $2p$", ha="center", va="top")
ax.hlines(-0.47, 5.4, 6.0, color="0.3", lw=3)
ax.text(5.7, -0.57, r"H $1s$ $\times 2$", ha="center", va="top")
links = {1: ["s", "H"], 2: ["p", "H"], 3: ["s", "p", "H"], 4: ["p"], 5: ["s", "p", "H"], 6: ["p", "H"]}
for k, srcs in links.items():
    for s_ in srcs:
        if s_ == "s":
            ax.plot([0.9, 2.6], [ao_O["$2s$"], E[k]], ls="--", color="0.65", lw=1)
        elif s_ == "p":
            ax.plot([0.95, 2.6], [ao_O["$2p$"], E[k]], ls="--", color="0.65", lw=1)
        else:
            ax.plot([5.4, 3.4], [-0.47, E[k]], ls=":", color="0.65", lw=1)
ax.text(3.0, -1.47, r"MO1: $1a_1$ (O $1s$ core) at $-20.24$, not shown", ha="center", fontsize=14, style="italic")
ax.set_xlim(0, 6.6)
ax.set_ylim(-1.55, 0.95)
ax.set_xticks([])
ax.set_ylabel(r"Orbital energy ($E_h$)")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/H2O_MOdiagram.png", dpi=100)
plt.close(fig)

# ------------------------------------------------------------------ Hückel theory
def huckel_chain(N):
    M = np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1)
    return M
def huckel_ring(N):
    M = huckel_chain(N)
    M[0, -1] = M[-1, 0] = 1
    return M
systems = [("ethylene", huckel_chain(2), 2), ("butadiene", huckel_chain(4), 4),
           ("hexatriene", huckel_chain(6), 6), ("benzene", huckel_ring(6), 6)]
fig, ax = plt.subplots(figsize=(12, 7.5))
for i, (name, M, ne) in enumerate(systems):
    x = np.sort(np.linalg.eigvalsh(M))[::-1]   # E = alpha + x beta, beta < 0: larger x is lower
    xs, counts = np.unique(np.round(x, 6), return_counts=True)
    xs, counts = xs[::-1], counts[::-1]
    filled = ne
    for xv, cnt in zip(xs, counts):
        y = -xv
        for c_ in range(cnt):
            off = (c_ - (cnt - 1) / 2) * 0.42
            ax.hlines(y, 2 * i + off - 0.17, 2 * i + off + 0.17, color=C[0] if xv > 0 else (C[3] if xv < 0 else "k"), lw=3)
            if filled > 0:
                ax.annotate("", xy=(2 * i + off - 0.06, y + 0.12), xytext=(2 * i + off - 0.06, y - 0.12), arrowprops=dict(arrowstyle="-|>", lw=1.4))
                ax.annotate("", xy=(2 * i + off + 0.06, y - 0.12), xytext=(2 * i + off + 0.06, y + 0.12), arrowprops=dict(arrowstyle="-|>", lw=1.4))
                filled -= 2
        ax.text(2 * i + 0.55 + 0.21 * (cnt - 1), y, (f"$\\alpha{'+' if xv >= 0 else '-'}{'' if abs(abs(xv)-1)<1e-6 else format(abs(xv), '.3g')}\\beta$" if abs(xv) > 1e-6 else r"$\alpha$"), va="center", fontsize=13)
    ax.text(2 * i, -2.55, name, ha="center", fontsize=17)
ax.axhline(0, color="0.6", ls=":", lw=1)
ax.set_xlim(-0.7, 7.4)
ax.set_ylim(-2.7, 2.3)
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylabel(r"Energy  ($\beta<0$)")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/Huckel_levels.png", dpi=100)
plt.close(fig)

# butadiene Hückel coefficients compared with particle-in-a-box standing waves
N = 4
w, V = np.linalg.eigh(huckel_chain(N))
order = np.argsort(-w)
fig, axs = plt.subplots(1, 4, figsize=(15, 4.2), sharey=True)
xx = np.linspace(0, N + 1, 300)
for k, ax in enumerate(axs):
    v = V[:, order[k]]
    n = k + 1
    pib = np.sqrt(2 / (N + 1)) * np.sin(n * np.pi * xx / (N + 1))
    if v[0] * pib[np.argmin(abs(xx - 1))] < 0:
        v = -v
    ax.plot(xx, pib, color="0.6", ls="--", lw=1.5)
    ax.vlines(np.arange(1, N + 1), 0, v, color=C[0] if k < 2 else C[3], lw=4)
    ax.plot(np.arange(1, N + 1), v, "o", color=C[0] if k < 2 else C[3], ms=8)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_title(f"$\\psi_{n}$: $E=\\alpha{'+' if w[order[k]] > 0 else '-'}{abs(w[order[k]]):.3f}\\beta$", fontsize=16)
    ax.set_xticks(range(1, N + 1))
    ax.set_xlabel("carbon atom")
    ax.grid(alpha=0.3)
axs[0].set_ylabel("coefficient $c_j$")
fig.tight_layout()
fig.savefig(f"{OUT}/Huckel_butadiene.png", dpi=100)
plt.close(fig)
print("done")
