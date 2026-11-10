"""Generate figures for chapters 10-13 in the style of chapters 4-5."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy.special import erf
from scipy.optimize import minimize

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({
    "font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
    "axes.labelsize": 20, "legend.fontsize": 17, "axes.grid": True,
    "grid.alpha": 0.3, "figure.dpi": 100,
})
PURPLE = "purple"
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]
KJ = 2625.5  # kJ/mol per hartree


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}", dpi=100)
    plt.close(fig)


# ---------------------------------------------------------------- Ch. 10
# Variational energy of helium as a function of the orbital exponent zeta
z = np.linspace(1.2, 2.4, 400)
E = z**2 - 2 * 2 * z + 5 / 8 * z          # hartree
zmin = 2 - 5 / 16
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.plot(z, E * KJ, color=C[0], lw=2.5, label=r"$E(\zeta)=\zeta^2-2Z\zeta+\frac{5}{8}\zeta$")
ax.axhline(-2.90372 * KJ, color="k", ls=":", lw=2, label="exact energy")
ax.plot([2.0], [(4 - 8 + 5 / 4) * KJ], "o", color=C[1], ms=10,
        label=r"$\zeta=Z=2$ (no shielding)")
ax.plot([zmin], [(zmin**2 - 4 * zmin + 5 / 8 * zmin) * KJ], "o", color=PURPLE, ms=10,
        label=r"minimum, $\zeta=Z-\frac{5}{16}=1.6875$")
ax.set_xlabel(r"Orbital exponent $\zeta$")
ax.set_ylabel(r"Energy (kJ/mol)")
ax.set_xlim(1.2, 2.4)
ax.legend(loc="upper center")
save(fig, "He_var.png")

# Ladder of approximations for helium
levels = [("no repulsion", -4.0, C[3]),
          ("average repulsion added", -2.75, C[1]),
          ("variational, $\\zeta=1.6875$", -(27 / 16) ** 2, C[0]),
          ("Hartree–Fock limit", -2.86168, C[2]),
          ("exact", -2.90372, "k")]
fig, ax = plt.subplots(figsize=(10, 7))
for i, (lab, e, col) in enumerate(levels):
    ax.hlines(e * KJ, i - 0.35, i + 0.35, color=col, lw=4)
    ax.text(i, e * KJ - 260, f"{e * KJ:,.0f}", ha="center", va="top", fontsize=15, color=col)
ax.set_xticks(range(len(levels)))
ax.set_xticklabels([l[0] for l in levels], rotation=20, ha="right", fontsize=15)
ax.set_ylabel("Energy of He (kJ/mol)")
ax.set_ylim(-11000, -7000)
ax.grid(axis="x", visible=False)
save(fig, "He_ladder.png")

# Penetration: 2s vs 2p radial probability compared with the 1s core of Li
r = np.linspace(0, 12, 1200)
def P(n, l, Zeff):
    rho = Zeff * r
    if (n, l) == (1, 0):
        R = 2 * Zeff**1.5 * np.exp(-rho)
    elif (n, l) == (2, 0):
        R = Zeff**1.5 / (2 * np.sqrt(2)) * (2 - rho) * np.exp(-rho / 2)
    else:
        R = Zeff**1.5 / (2 * np.sqrt(6)) * rho * np.exp(-rho / 2)
    return r**2 * R**2
fig, ax = plt.subplots(figsize=(10, 6.5))
core = P(1, 0, 2.69)
ax.fill_between(r, 0, core, color="0.85", label=r"Li $1s^2$ core")
ax.plot(r, P(2, 0, 1.28), color=C[1], lw=2.5, label=r"$2s$")
ax.plot(r, P(2, 1, 1.28), color=C[2], lw=2.5, label=r"$2p$")
ax.plot([2 / 1.28], [0], "o", color=PURPLE, ms=8, zorder=5)
ax.annotate("inner lobe of $2s$\npenetrates the core", xy=(0.45, 0.05), xytext=(1.6, 0.42),
            fontsize=16, arrowprops=dict(arrowstyle="->", lw=1.5))
ax.set_xlabel(r"Radius $r/a_0$")
ax.set_ylabel(r"Probability Density $r^2|R_{n\ell}(r)|^2$")
ax.set_xlim(0, 12)
ax.set_ylim(0, None)
ax.legend()
save(fig, "Li_penetration.png")

# ---------------------------------------------------------------- Ch. 11
# Potential energy curve of H2 (Morse) with harmonic approximation and levels
De, Re, a = 0.1745, 1.401, 1.0288
w = 4401.2 / 219474.6
wx = w**2 / (4 * De)
R = np.linspace(0.6, 6, 600)
U = De * (1 - np.exp(-a * (R - Re)))**2 - De
k = 2 * De * a**2
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.plot(R, U * KJ, color=C[0], lw=2.5, label="potential energy curve $U(R)$")
ax.plot(R, (0.5 * k * (R - Re)**2 - De) * KJ, color=C[1], ls="--", lw=2,
        label="harmonic approximation")
for v in range(0, 14):
    Ev = w * (v + 0.5) - wx * (v + 0.5)**2 - De
    if Ev > 0:
        break
    # classical turning points of the Morse potential
    s = np.sqrt((Ev + De) / De)
    r1 = Re - np.log(1 + s) / a
    r2 = Re - np.log(1 - s) / a if s < 1 else 6
    ax.hlines(Ev * KJ, r1, min(r2, 6), color="0.4", lw=1)
ax.axhline(0, color="k", lw=1)
E0 = w * 0.5 - wx * 0.25 - De
ax.annotate("", xy=(4.6, -De * KJ), xytext=(4.6, 0), arrowprops=dict(arrowstyle="<->", lw=1.5))
ax.text(4.7, -De * KJ / 2, r"$D_e$", fontsize=20)
ax.annotate("", xy=(5.4, E0 * KJ), xytext=(5.4, 0), arrowprops=dict(arrowstyle="<->", lw=1.5, color=C[2]))
ax.text(5.5, E0 * KJ / 2, r"$D_0$", fontsize=20, color=C[2])
ax.plot([Re], [-De * KJ], "o", color=PURPLE, ms=9)
ax.text(Re + 0.1, -De * KJ - 40, r"$R_e$", fontsize=20)
ax.set_xlabel(r"Internuclear distance $R/a_0$")
ax.set_ylabel(r"Energy (kJ/mol)")
ax.set_xlim(0.6, 6)
ax.set_ylim(-520, 300)
ax.legend(loc="upper right")
save(fig, "H2_PEC.png")

# Two-dimensional model surface (Mueller-Brown) with minima and saddle points
A = [-200, -100, -170, 15]; aa = [-1, -1, -6.5, 0.7]; bb = [0, 0, 11, 0.6]
cc = [-10, -10, -6.5, 0.7]; x0 = [1, 0, -0.5, -1]; y0 = [0, 0.5, 1.5, 1]
def mb(p):
    x, y = p
    return sum(A[i] * np.exp(aa[i] * (x - x0[i])**2 + bb[i] * (x - x0[i]) * (y - y0[i])
                             + cc[i] * (y - y0[i])**2) for i in range(4))
def grad2(p, h=1e-5):
    gx = (mb((p[0] + h, p[1])) - mb((p[0] - h, p[1]))) / (2 * h)
    gy = (mb((p[0], p[1] + h)) - mb((p[0], p[1] - h))) / (2 * h)
    return gx**2 + gy**2
mins = [minimize(mb, g).x for g in [(-0.55, 1.45), (0.6, 0.03), (-0.05, 0.47)]]
saddles = [minimize(grad2, g, method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-10)).x
           for g in [(-0.82, 0.62), (0.21, 0.29)]]
X, Y = np.meshgrid(np.linspace(-1.5, 1.2, 400), np.linspace(-0.4, 2.0, 400))
Z = mb((X, Y))
fig, ax = plt.subplots(figsize=(10, 8))
cs = ax.contourf(X, Y, np.minimum(Z, 100), levels=40, cmap="viridis")
ax.contour(X, Y, np.minimum(Z, 100), levels=40, colors="k", linewidths=0.3)
cb = fig.colorbar(cs, ax=ax)
cb.set_label("Energy (arbitrary units)")
for i, m in enumerate(mins):
    ax.plot(*m, "o", color="white", mec="k", ms=12)
ax.text(mins[0][0] + 0.06, mins[0][1] + 0.05, "A (global min.)", color="white", fontsize=15)
ax.text(mins[1][0] + 0.05, mins[1][1] + 0.06, "C", color="white", fontsize=15)
ax.text(mins[2][0] + 0.06, mins[2][1] + 0.03, "B", color="white", fontsize=15)
for s in saddles:
    ax.plot(*s, "X", color="red", mec="k", ms=14)
ax.text(saddles[0][0] - 0.45, saddles[0][1] - 0.05, "TS$_1$", color="white", fontsize=15)
ax.text(saddles[1][0] + 0.07, saddles[1][1] + 0.02, "TS$_2$", color="white", fontsize=15)
ax.set_xlabel(r"Nuclear coordinate $q_1$")
ax.set_ylabel(r"Nuclear coordinate $q_2$")
ax.grid(False)
save(fig, "PES_2D.png")

# SCF flowchart
fig, ax = plt.subplots(figsize=(8, 9))
ax.axis("off")
boxes = [
    (0.5, 0.92, "Choose basis functions $f_i$ and\nnuclear geometry $\\mathbf{R}_a$"),
    (0.5, 0.76, "Calculate integrals $S_{ij}$, $K_{ij}$, $V_{ij}$, $V_{ijkl}$"),
    (0.5, 0.60, "Guess the coefficients $c_i$\n(i.e., the occupied orbitals)"),
    (0.5, 0.44, "Build the Fock operator from\nthe current orbitals"),
    (0.5, 0.28, "Solve the secular determinant\n$\\rightarrow$ new orbitals and energies"),
    (0.5, 0.10, "Converged?  Yes $\\rightarrow$ final energy"),
]
for x, y, t in boxes:
    ax.add_patch(FancyBboxPatch((x - 0.36, y - 0.055), 0.72, 0.11, boxstyle="round,pad=0.01",
                                fc="#e8f0fa", ec=C[0], lw=2))
    ax.text(x, y, t, ha="center", va="center", fontsize=16)
for (x1, y1, _), (x2, y2, _) in zip(boxes[:-1], boxes[1:]):
    ax.annotate("", xy=(x2, y2 + 0.06), xytext=(x1, y1 - 0.06), arrowprops=dict(arrowstyle="->", lw=2))
ax.annotate("", xy=(0.88, 0.44), xytext=(0.88, 0.10),
            arrowprops=dict(arrowstyle="->", lw=2, color=C[3], connectionstyle="arc3,rad=0"))
ax.plot([0.86, 0.88], [0.10, 0.10], color=C[3], lw=2)
ax.plot([0.86, 0.88], [0.44, 0.44], color=C[3], lw=2)
ax.text(0.90, 0.27, "No: update\norbitals and\nrepeat", color=C[3], fontsize=15, va="center")
ax.set_xlim(0, 1.15)
ax.set_ylim(0, 1)
save(fig, "SCF_cycle.png")

# ---------------------------------------------------------------- Ch. 12
# H2+ LCAO energy curves from the analytic integrals (zeta = 1)
def h2p(R):
    S = np.exp(-R) * (1 + R + R**2 / 3)
    J = -1 / R + np.exp(-2 * R) * (1 + 1 / R)
    K = -np.exp(-R) * (1 + R)
    Haa = -0.5 + J
    Hab = -0.5 * S + K
    Ep = (Haa + Hab) / (1 + S) + 1 / R + 0.5
    Em = (Haa - Hab) / (1 - S) + 1 / R + 0.5
    return S, Ep, Em
R = np.linspace(0.8, 8, 500)
S, Ep, Em = h2p(R)
i0 = np.argmin(Ep)
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.plot(R, Ep * KJ, color=C[0], lw=2.5, label=r"$E_+$ (bonding, $\varphi_+$)")
ax.plot(R, Em * KJ, color=C[3], lw=2.5, label=r"$E_-$ (antibonding, $\varphi_-$)")
ax.axhline(0, color="k", lw=1)
ax.plot([R[i0]], [Ep[i0] * KJ], "o", color=PURPLE, ms=9)
ax.plot([2.00], [-0.1026 * KJ], "*", color="k", ms=15, label="exact minimum")
ax.text(R[i0] + 0.15, Ep[i0] * KJ - 45, f"$R={R[i0]:.2f}\\,a_0$", fontsize=16)
ax.text(6.6, -55, r"H + H$^+$", fontsize=17)
ax.set_xlabel(r"Internuclear distance $R/a_0$")
ax.set_ylabel(r"$E-E(\mathrm{H}+\mathrm{H}^+)$ (kJ/mol)")
ax.set_xlim(0.8, 8)
ax.set_ylim(-320, 500)
ax.legend()
save(fig, "H2p_PEC.png")
print("H2+ LCAO minimum:", R[i0], Ep[i0], Ep[i0] * KJ, "S=", S[i0])

# H2+ molecular orbitals: contour maps and line profiles at R = 2 a0
Rb = 2.0
Sb = np.exp(-Rb) * (1 + Rb + Rb**2 / 3)
xs = np.linspace(-3, 3, 400)
zs = np.linspace(-3.5, 3.5, 450)
Xg, Zg = np.meshgrid(xs, zs)
ra = np.sqrt(Xg**2 + (Zg + Rb / 2)**2)
rb = np.sqrt(Xg**2 + (Zg - Rb / 2)**2)
ag, bg = np.exp(-ra) / np.sqrt(np.pi), np.exp(-rb) / np.sqrt(np.pi)
phip = (ag + bg) / np.sqrt(2 + 2 * Sb)
phim = (ag - bg) / np.sqrt(2 - 2 * Sb)
fig, axs = plt.subplots(1, 2, figsize=(11, 5.2))
for ax, f, t in zip(axs, [phip, phim], [r"$\varphi_+$ (bonding, $\sigma_g$)", r"$\varphi_-$ (antibonding, $\sigma_u$)"]):
    m = np.abs(f).max()
    ax.contourf(Zg, Xg, f, levels=np.linspace(-m, m, 41), cmap="RdBu_r")
    ax.contour(Zg, Xg, f, levels=[0], colors=PURPLE, linewidths=2)
    ax.plot([-Rb / 2, Rb / 2], [0, 0], "ko", ms=7)
    ax.set_title(t, fontsize=19)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$z/a_0$")
    ax.grid(False)
axs[0].set_ylabel(r"$x/a_0$")
save(fig, "H2p_MO_maps.png")

zl = np.linspace(-4, 4, 800)
al = np.exp(-np.abs(zl + Rb / 2)) / np.sqrt(np.pi)
bl = np.exp(-np.abs(zl - Rb / 2)) / np.sqrt(np.pi)
pp = (al + bl) / np.sqrt(2 + 2 * Sb)
pm = (al - bl) / np.sqrt(2 - 2 * Sb)
fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))
axs[0].plot(zl, al, "--", color="0.5", lw=1.5, label="$a$, $b$")
axs[0].plot(zl, bl, "--", color="0.5", lw=1.5)
axs[0].plot(zl, pp, color=C[0], lw=2.5, label=r"$\varphi_+$")
axs[0].plot(zl, pm, color=C[3], lw=2.5, label=r"$\varphi_-$")
axs[0].plot([0], [0], "o", color=PURPLE, ms=9)
axs[0].set_xlabel(r"Position along the bond axis $z/a_0$")
axs[0].set_ylabel("Amplitude")
axs[0].legend(fontsize=15)
ref = (al**2 + bl**2) / 2
axs[1].plot(zl, ref, "--", color="0.4", lw=2, label=r"$\frac{1}{2}(a^2+b^2)$")
axs[1].plot(zl, pp**2, color=C[0], lw=2.5, label=r"$|\varphi_+|^2$")
axs[1].plot(zl, pm**2, color=C[3], lw=2.5, label=r"$|\varphi_-|^2$")
axs[1].set_xlabel(r"Position along the bond axis $z/a_0$")
axs[1].set_ylabel("Probability density")
axs[1].legend(fontsize=15)
for ax in axs:
    for zn in (-Rb / 2, Rb / 2):
        ax.axvline(zn, color="k", lw=0.8, ls=":")
save(fig, "H2p_MO_lines.png")

# H2 in a minimal STO-3G basis: RHF versus full CI (Szabo-Ostlund style)
cST = np.array([0.444635, 0.535328, 0.154329])
aST0 = np.array([0.109818, 0.405771, 2.22766])
aST = aST0 * 1.24**2
def F0(t):
    return np.where(t < 1e-8, 1 - t / 3, 0.5 * np.sqrt(np.pi / np.maximum(t, 1e-12)) * erf(np.sqrt(np.maximum(t, 1e-12))))
def ints(R):
    norm = (2 * aST / np.pi) ** 0.75
    cen = [0.0, R]
    S = np.zeros((2, 2)); T = np.zeros((2, 2)); V = np.zeros((2, 2)); G = np.zeros((2, 2, 2, 2))
    for i in range(2):
        for j in range(2):
            for p in range(3):
                for q in range(3):
                    a, b = aST[p], aST[q]
                    d = cen[i] - cen[j]
                    pre = cST[p] * cST[q] * norm[p] * norm[q]
                    s = (np.pi / (a + b))**1.5 * np.exp(-a * b / (a + b) * d**2)
                    S[i, j] += pre * s
                    T[i, j] += pre * a * b / (a + b) * (3 - 2 * a * b / (a + b) * d**2) * s
                    P = (a * cen[i] + b * cen[j]) / (a + b)
                    for Cn in cen:
                        V[i, j] += -pre * 2 * np.pi / (a + b) * np.exp(-a * b / (a + b) * d**2) * F0((a + b) * (P - Cn)**2)
    for i in range(2):
        for j in range(2):
            for k_ in range(2):
                for l in range(2):
                    val = 0
                    for p in range(3):
                        for q in range(3):
                            for r_ in range(3):
                                for s_ in range(3):
                                    a, b, c, d = aST[p], aST[q], aST[r_], aST[s_]
                                    pre = cST[p] * cST[q] * cST[r_] * cST[s_] * norm[p] * norm[q] * norm[r_] * norm[s_]
                                    P = (a * cen[i] + b * cen[j]) / (a + b)
                                    Q = (c * cen[k_] + d * cen[l]) / (c + d)
                                    val += pre * 2 * np.pi**2.5 / ((a + b) * (c + d) * np.sqrt(a + b + c + d)) * \
                                        np.exp(-a * b / (a + b) * (cen[i] - cen[j])**2 - c * d / (c + d) * (cen[k_] - cen[l])**2) * \
                                        F0((a + b) * (c + d) / (a + b + c + d) * (P - Q)**2)
                    G[i, j, k_, l] = val
    return S, T + V, G
def h2(R):
    S, h, G = ints(R)
    s = S[0, 1]
    Cg = np.array([1, 1]) / np.sqrt(2 + 2 * s)
    Cu = np.array([1, -1]) / np.sqrt(2 - 2 * s)
    def mo2(C1, C2, C3, C4):
        return np.einsum("i,j,k,l,ijkl->", C1, C2, C3, C4, G)
    hg, hu = Cg @ h @ Cg, Cu @ h @ Cu
    Jgg, Juu, Kgu = mo2(Cg, Cg, Cg, Cg), mo2(Cu, Cu, Cu, Cu), mo2(Cg, Cu, Cu, Cg)
    E1 = 2 * hg + Jgg + 1 / R
    E2 = 2 * hu + Juu + 1 / R
    Hci = np.array([[E1, Kgu], [Kgu, E2]])
    return E1, np.linalg.eigvalsh(Hci)[0]
from scipy.optimize import minimize_scalar
def h2opt(R):
    global aST
    out = []
    for k_ in (0, 1):
        def f(zeta):
            global aST
            aST = aST0 * zeta**2
            return h2(R)[k_]
        r_ = minimize_scalar(f, bounds=(0.8, 1.6), method="bounded", options=dict(xatol=1e-5))
        out.append((r_.fun, r_.x))
    return out[0][0], out[1][0], out[0][1], out[1][1]
Rs = np.linspace(0.7, 7, 110)
full = np.array([h2opt(x) for x in Rs])
res = full[:, :2]
Einf = res[-1, 1]   # CI correctly goes to two H atoms
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.plot(Rs, (res[:, 0] - Einf) * KJ, color=C[3], lw=2.5, label="Hartree–Fock (RHF)")
ax.plot(Rs, (res[:, 1] - Einf) * KJ, color=C[0], lw=2.5, label="with configuration interaction")
ax.axhline(0, color="k", lw=1)
ax.text(5.6, 20, "H + H", fontsize=17)
ax.set_xlabel(r"Internuclear distance $R/a_0$")
ax.set_ylabel(r"$E-E(\mathrm{H}+\mathrm{H})$ (kJ/mol)")
ax.set_xlim(0.7, 7)
ax.set_ylim(-450, 600)
ax.legend()
save(fig, "H2_HF_CI.png")
im = np.argmin(res[:, 0])
print("H2 STO-3G RHF min", Rs[im], res[im] - Einf, (res[im] - Einf) * KJ, "zeta", full[im,2:], "E(R=7)-Einf RHF", (res[-1, 0] - Einf) * KJ, "Einf", Einf)

# ---------------------------------------------------------------- Ch. 13
# CO: rotational populations and pure-rotation spectrum at 298 K
B, T = 1.9313, 298.15
kT = 0.695035 * T  # cm-1
J = np.arange(0, 41)
pop = (2 * J + 1) * np.exp(-B * J * (J + 1) / kT)
pop /= pop.sum()
Jmax = np.sqrt(kT / (2 * B)) - 0.5
fig, axs = plt.subplots(1, 2, figsize=(14, 5.5))
axs[0].bar(J, pop, color=C[0], width=0.7)
axs[0].axvline(Jmax, color=PURPLE, ls="--", lw=2, label=f"$J_{{max}}\\approx{Jmax:.1f}$")
axs[0].set_xlabel("Rotational quantum number $J$")
axs[0].set_ylabel("Fraction of molecules")
axs[0].set_xlim(-1, 35)
axs[0].legend()
nu = 2 * B * (J + 1)
inten = pop * (J + 1) / (2 * J + 1) * nu
inten /= inten.max()
axs[1].vlines(nu, 0, inten, color=C[3], lw=2)
axs[1].set_xlabel(r"Wavenumber $\tilde{\nu}$ (cm$^{-1}$)")
axs[1].set_ylabel("Relative intensity")
axs[1].set_xlim(0, 140)
axs[1].set_ylim(0, 1.08)
save(fig, "CO_rot.png")
print("CO Jmax", Jmax)

# CO: rovibrational fundamental band (P and R branches)
nu0, B1, B0 = 2143.27, 1.9050, 1.9225
lines, ints_ = [], []
for Jl in range(0, 40):
    w_ = (2 * Jl + 1) * np.exp(-B0 * Jl * (Jl + 1) / kT)
    # R branch: J -> J+1
    lines.append(nu0 + B1 * (Jl + 1) * (Jl + 2) - B0 * Jl * (Jl + 1)); ints_.append(w_ * (Jl + 1) / (2 * Jl + 1))
    if Jl > 0:  # P branch: J -> J-1
        lines.append(nu0 + B1 * (Jl - 1) * Jl - B0 * Jl * (Jl + 1)); ints_.append(w_ * Jl / (2 * Jl + 1))
lines, ints_ = np.array(lines), np.array(ints_)
ints_ /= ints_.max()
fig, ax = plt.subplots(figsize=(12, 5.5))
ax.vlines(lines, 0, ints_, color=C[0], lw=1.8)
ax.axvline(nu0, color=PURPLE, ls="--", lw=1.5)
ax.text(nu0 + 2, 1.02, r"$\tilde{\nu}_0$ (no Q-branch)", color=PURPLE, fontsize=16)
ax.text(2060, 0.85, "P-branch\n($\\Delta J=-1$)", fontsize=17, ha="center")
ax.text(2225, 0.85, "R-branch\n($\\Delta J=+1$)", fontsize=17, ha="center")
ax.set_xlabel(r"Wavenumber $\tilde{\nu}$ (cm$^{-1}$)")
ax.set_ylabel("Relative intensity")
ax.set_xlim(2000, 2290)
ax.set_ylim(0, 1.15)
save(fig, "CO_rovib.png")
print("done")
