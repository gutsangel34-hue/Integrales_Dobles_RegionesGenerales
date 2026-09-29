"""
Simulación — Valor promedio de f(x,y)=xy sobre el triángulo D de vértices (0,0), (1,0), (1,3)
Stewart, Sec. 15.2, ej. 61.  Cálculo Vectorial, Univ. de La Salle.

Genera:
  * simulacion_valor_promedio.html  -> gráfico 3D interactivo (deslizador para el plano z = h)
  * simulacion_valor_promedio.png   -> imagen estática (matplotlib) para las diapositivas

Uso:  pip install numpy matplotlib plotly sympy
      python simulacion_valor_promedio.py
"""
import sys
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---------- 1) Cálculo simbólico (verificación del resultado) ----------
x, y = sp.symbols("x y", real=True)
f = x * y
area  = sp.integrate(sp.integrate(1, (y, 0, 3 * x)), (x, 0, 1))           # A(D)
total = sp.integrate(sp.integrate(f, (y, 0, 3 * x)), (x, 0, 1))           # ∬ xy dA
fprom = sp.simplify(total / area)
print(f"A(D) = {area},  integral doble de xy sobre D = {total},  f_prom = {fprom}")
assert (area, total, fprom) == (sp.Rational(3, 2), sp.Rational(9, 8), sp.Rational(3, 4))
# verificación con el otro orden (tipo II)
otro = sp.integrate(sp.integrate(f, (x, y / 3, 1)), (y, 0, 3))
assert otro == total

F_PROM = float(fprom)

# ---------- 2) Malla sobre D (tipo I: 0<=x<=1, 0<=y<=3x) ----------
n = 40
X, T = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, 1, n))
Y = 3 * X * T                      # y recorre [0, 3x] para cada x
Z = X * Y                          # z = f(x,y) = xy

# ---------- 3) Gráfico interactivo (Plotly) ----------
def plano(h):
    return np.full_like(Z, h)

def lectura(h):
    # ∬_D (xy - h) dA = 9/8 - (3/2) h   (se anula exactamente en h = 3/4)
    dif = 9 / 8 - 1.5 * h
    return (f"h = {h:.2f} &nbsp;|&nbsp; ∬<sub>D</sub>(xy − h) dA = 9/8 − (3/2)h = <b>{dif:+.3f}</b>"
            + ("  ✔ se compensan: h = f<sub>prom</sub> = 3/4" if abs(h - F_PROM) < 1e-9 else ""))

pasos = np.round(np.unique(np.concatenate([np.arange(0, 3.01, 0.25), [F_PROM]])), 4)

fig = go.Figure()
# 0) superficie z = xy sobre D
fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale="Tealgrn", opacity=0.95, showscale=False,
                         name="z = xy", hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=xy=%{z:.2f}<extra></extra>"))
# 1) plano z = h (sobre D)
fig.add_trace(go.Surface(x=X, y=Y, z=plano(F_PROM), colorscale=[[0, "#F2A93B"], [1, "#F2A93B"]],
                         opacity=0.55, showscale=False, name="z = h",
                         hovertemplate="plano z=h<extra></extra>"))
# 2) región D sombreada en el plano xy (z = 0)
fig.add_trace(go.Mesh3d(x=[0, 1, 1], y=[0, 0, 3], z=[0, 0, 0], i=[0], j=[1], k=[2],
                        color="#0B3C3A", opacity=0.35, name="Región D"))
# 3) contorno de D
fig.add_trace(go.Scatter3d(x=[0, 1, 1, 0], y=[0, 0, 3, 0], z=[0, 0, 0, 0], mode="lines",
                           line=dict(color="#0B3C3A", width=6), name="Borde de D", hoverinfo="skip"))
# 4) vértices etiquetados
fig.add_trace(go.Scatter3d(x=[0, 1, 1], y=[0, 0, 3], z=[0, 0, 0], mode="markers+text",
                           text=["(0,0)", "(1,0)", "(1,3)"], textposition="top center",
                           marker=dict(size=4, color="#0B3C3A"), name="Vértices", hoverinfo="skip"))

steps = [dict(method="update",
              args=[{"z": [plano(h)]}, {"title": {"text": lectura(h)}}, [1]],
              label=f"{h:g}") for h in pasos]
i0 = int(np.where(pasos == F_PROM)[0][0])
fig.update_layout(
    title=dict(text=lectura(F_PROM), x=0.5, font=dict(size=16)),
    sliders=[dict(active=i0, currentvalue=dict(prefix="Altura del plano  z = h :  "), pad=dict(t=10), steps=steps)],
    scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z = f(x,y)",
               aspectmode="manual", aspectratio=dict(x=1, y=1.6, z=1),
               camera=dict(eye=dict(x=1.7, y=-1.6, z=1.0))),
    legend=dict(orientation="v", x=0.01, y=0.95), margin=dict(l=0, r=0, t=60, b=10),
    template="plotly_white")
fig.write_html("simulacion_valor_promedio.html", include_plotlyjs=True, full_html=True,
               config={"displaylogo": False})

# ---------- 4) Imagen estática (matplotlib) para las diapositivas ----------
plt.rcParams.update({"font.size": 13, "mathtext.fontset": "cm"})
fg = plt.figure(figsize=(7.8, 5.4), dpi=220)
ax = fg.add_axes([-0.12, -0.10, 1.24, 1.10], projection="3d")
ax.add_collection3d(Poly3DCollection([[(0, 0, 0), (1, 0, 0), (1, 3, 0)]], facecolor="#0B3C3A",
                                     alpha=0.30, edgecolor="#0B3C3A", linewidth=1.8))
ax.plot_surface(X, Y, Z, cmap="YlGnBu", alpha=0.92, linewidth=0, antialiased=True, rstride=1, cstride=1)
ax.plot_surface(X, Y, plano(F_PROM), color="#F2A93B", alpha=0.45, linewidth=0, shade=False)
ax.plot([0, 1, 1, 0], [0, 0, 3, 0], [0, 0, 0, 0], color="#0B3C3A", lw=2)
for (px, py, lab, dx, dy) in [(0, 0, "(0,0)", -0.02, -0.40), (1, 0, "(1,0)", 0.30, -0.50), (1, 3, "(1,3)", 0.0, 0.35)]:
    ax.text(px + dx, py + dy, 0, lab, fontsize=13, color="#0B3C3A", ha="center", va="center", fontweight="bold")
ax.scatter([1], [3], [3], color="#0B3C3A", s=22)
ax.text(1.0, 3.0, 3.35, "$f(1,3)=3$", fontsize=13, color="#0B3C3A", ha="center")
ax.set_xlabel("$x$", fontsize=15); ax.set_ylabel("$y$", fontsize=15); ax.set_zlabel("$z=f(x,y)$", fontsize=14)
ax.set_xlim(0, 1); ax.set_ylim(0, 3); ax.set_zlim(0, 3.3)
ax.set_box_aspect((1, 2.1, 1.05)); ax.view_init(elev=22, azim=-64)
ax.tick_params(labelsize=12); ax.set_xticks([0.5, 1]); ax.set_yticks([1, 2, 3]); ax.set_zticks([1, 2, 3])
ax.set_title(r"$z=xy$ sobre $D$   y   plano $z=f_{\mathrm{prom}}=\frac{3}{4}$", fontsize=15, color="#0B3C3A", y=0.97)
fg.savefig("simulacion_valor_promedio.png", transparent=False, facecolor="white", bbox_inches="tight", pad_inches=0.3)
# recorte de márgenes blancos
from PIL import Image, ImageChops
im = Image.open("simulacion_valor_promedio.png").convert("RGB")
bb = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
im.crop((max(bb[0] - 12, 0), max(bb[1] - 12, 0), min(bb[2] + 12, im.size[0]), min(bb[3] + 12, im.size[1]))).save("simulacion_valor_promedio.png")
print("Listo: simulacion_valor_promedio.html y .png")
