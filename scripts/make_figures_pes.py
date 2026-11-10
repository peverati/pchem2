"""Model two-dimensional potential energy surface (Mueller-Brown) with its minimum
energy path, and the energy profile along the reaction coordinate (ch. 10).

The path is obtained by steepest descent from each saddle point, in both directions
along the eigenvector of the Hessian with negative curvature.

Usage (from the project root):  python3 scripts/make_figures_pes.py img
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16,
                     "axes.labelsize": 18, "legend.fontsize": 14, "figure.dpi": 100})
PURPLE = "purple"

A = [-200, -100, -170, 15]; aa = [-1, -1, -6.5, 0.7]; bb = [0, 0, 11, 0.6]
cc = [-10, -10, -6.5, 0.7]; x0 = [1, 0, -0.5, -1]; y0 = [0, 0.5, 1.5, 1]
def V(p):
    x, y = p
    return sum(A[i] * np.exp(aa[i] * (x - x0[i])**2 + bb[i] * (x - x0[i]) * (y - y0[i])
                             + cc[i] * (y - y0[i])**2) for i in range(4))
def grad(p, h=1e-6):
    return np.array([(V((p[0] + h, p[1])) - V((p[0] - h, p[1]))) / (2 * h),
                     (V((p[0], p[1] + h)) - V((p[0], p[1] - h))) / (2 * h)])
def hess(p, h=1e-4):
    g0 = lambda q: grad(q)
    H = np.zeros((2, 2))
    for i in range(2):
        e = np.zeros(2); e[i] = h
        H[:, i] = (g0(p + e) - g0(p - e)) / (2 * h)
    return 0.5 * (H + H.T)

mins = [minimize(V, g).x for g in [(-0.55, 1.45), (-0.05, 0.47), (0.6, 0.03)]]          # A, B, C
saddles = [minimize(lambda p: np.sum(grad(p)**2), g, method="Nelder-Mead",
                    options=dict(xatol=1e-10, fatol=1e-14, maxiter=4000)).x
           for g in [(-0.82, 0.62), (0.21, 0.29)]]                                       # TS1, TS2

def descend(start, step=2e-3, nmax=20000):
    path = [start.copy()]
    p = start.copy()
    for _ in range(nmax):
        g = grad(p)
        n = np.linalg.norm(g)
        if n < 1e-3 or min(np.linalg.norm(p - m) for m in mins) < 3 * step:
            break
        q = p - step * g / n
        if V(q) > V(p):          # overshooting the bottom of the valley
            break
        p = q
        path.append(p.copy())
    path.append(min(mins, key=lambda m: np.linalg.norm(p - m)).copy())
    return np.array(path)

segments = []
for ts in saddles:
    w, U = np.linalg.eigh(hess(ts))
    v = U[:, 0]
    a = descend(ts + 0.01 * v)
    b = descend(ts - 0.01 * v)
    segments.append((a, b))
# assemble A -> TS1 -> B -> TS2 -> C
def ends_near(seg, target):
    return np.linalg.norm(seg[-1] - target) < 0.05
pieces = []
for (a, b), (start_min, end_min) in zip(segments, [(mins[0], mins[1]), (mins[1], mins[2])]):
    first, second = (a, b) if ends_near(a, start_min) else (b, a)
    pieces.append(np.vstack([first[::-1], second]))
path = np.vstack([pieces[0], pieces[1][1:]])
s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])
s = s / s[-1]
Epath = np.array([V(p) for p in path])

# ---------------------------------------------------------------- figure
fig = plt.figure(figsize=(17, 7))
ax = fig.add_axes([0.05, 0.11, 0.42, 0.83])
X, Y = np.meshgrid(np.linspace(-1.5, 1.2, 400), np.linspace(-0.4, 2.0, 400))
Z = V((X, Y))
cs = ax.contourf(X, Y, np.minimum(Z, 100), levels=40, cmap="viridis")
ax.contour(X, Y, np.minimum(Z, 100), levels=40, colors="k", linewidths=0.3)
ax.plot(path[:, 0], path[:, 1], color="white", lw=3, ls="--")
labels = ["A", "B", "C"]
for m, lab in zip(mins, labels):
    ax.plot(*m, "o", color="white", mec="k", ms=12, zorder=5)
offs = {"A": (0.07, 0.05), "B": (0.06, 0.06), "C": (0.05, 0.07)}
for m, lab in zip(mins, labels):
    ax.text(m[0] + offs[lab][0], m[1] + offs[lab][1], lab, color="white", fontsize=17, weight="bold")
for ts, lab, off in zip(saddles, ["TS$_1$", "TS$_2$"], [(-0.38, -0.02), (0.07, 0.03)]):
    ax.plot(*ts, "X", color="red", mec="k", ms=15, zorder=5)
    ax.text(ts[0] + off[0], ts[1] + off[1], lab, color="white", fontsize=16)
ax.set_xlabel(r"Nuclear coordinate $q_1$")
ax.set_ylabel(r"Nuclear coordinate $q_2$")
ax.set_title("(a) potential energy surface", fontsize=18)
cb = fig.colorbar(cs, ax=ax, fraction=0.045, pad=0.02)
cb.set_label("Energy (arbitrary units)")

ax2 = fig.add_axes([0.66, 0.11, 0.32, 0.83])
ax2.plot(s, Epath, color="k", lw=2.5)
idx_min = [np.argmin(np.linalg.norm(path - m, axis=1)) for m in mins]
idx_ts = [np.argmin(np.linalg.norm(path - t, axis=1)) for t in saddles]
for i, lab in zip(idx_min, labels):
    ax2.plot(s[i], Epath[i], "o", color="white", mec="k", ms=12, zorder=5)
    ax2.text(s[i], Epath[i] - 9, lab, ha="center", va="top", fontsize=17, weight="bold")
for i, lab in zip(idx_ts, ["TS$_1$", "TS$_2$"]):
    ax2.plot(s[i], Epath[i], "X", color="red", mec="k", ms=15, zorder=5)
    ax2.text(s[i], Epath[i] + 7, lab, ha="center", va="bottom", fontsize=16)
# activation energy for A -> B
iA, iT = idx_min[0], idx_ts[0]
xa = s[iT] + 0.04
ax2.annotate("", xy=(xa, Epath[iT]), xytext=(xa, Epath[iA]), arrowprops=dict(arrowstyle="<->", lw=1.6, color=PURPLE))
ax2.hlines(Epath[iA], s[iA], xa, color=PURPLE, ls=":", lw=1.2)
ax2.text(xa + 0.02, (Epath[iA] + Epath[iT]) / 2, r"$E_a$ (A$\rightarrow$B)", color=PURPLE, va="center", fontsize=15)
ax2.set_xlabel("Reaction coordinate")
ax2.set_ylabel("Energy (arbitrary units)")
ax2.set_xticks([])
ax2.set_title("(b) energy along the reaction coordinate", fontsize=18)
ax2.set_ylim(Epath.min() - 25, Epath.max() + 25)
ax2.grid(alpha=0.3)
fig.savefig(f"{OUT}/PES_2D.png", dpi=100)
plt.close(fig)
print("minima energies", [round(V(m), 1) for m in mins], "TS energies", [round(V(t), 1) for t in saddles])
