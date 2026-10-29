"""
NACA 0012 coordinates for SpaceClaim (chord = 1000 mm, sharp trailing edge)
==========================================================================
Writes naca0012.txt: one smooth spline TE (upper) -> LE -> TE (lower).
Thickness law with modified last coefficient (-0.1036) -> closed trailing edge.
Column order "0 x y" and values in mm: this is how SpaceClaim's point-curve
import places the profile in the global XY plane at the right scale.
Import: drag & drop naca0012.txt into the SpaceClaim design window.
"""
import numpy as np
from pathlib import Path

N = 200          # points per surface (cosine spacing)
T = 0.12         # max thickness / chord
C = 1000.0       # chord [mm]

beta = np.linspace(0, np.pi, N)
x = 0.5 * (1 - np.cos(beta))
yt = 5 * T * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2
              + 0.2843 * x**3 - 0.1036 * x**4)
yt[-1] = 0.0

xs = np.concatenate([x[::-1], x[1:]]) * C
ys = np.concatenate([yt[::-1], -yt[1:]]) * C

out = Path(__file__).resolve().parent / "naca0012.txt"
with open(out, "w") as f:
    f.write("3d=true\npolyline=false\n\n")
    for xi, yi in zip(xs, ys):
        f.write(f"0.0 {xi:.8f} {yi:.8f}\n")

print(f"{len(xs)} points written to {out}")
print(f"Max thickness: {2 * yt.max():.5f} c at x = {x[yt.argmax()]:.3f} c")
