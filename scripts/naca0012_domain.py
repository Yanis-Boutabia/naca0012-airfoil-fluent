"""
C-domain boundary for the NACA 0012 case (SpaceClaim point-curve file)
======================================================================
Writes domain.txt: front half-circle (radius 20c) + 3 straight lines
(wake region up to 20c behind the trailing edge). Units: mm, chord = 1000 mm.
Column order "0 x y": SpaceClaim maps the columns so that the curves
land in the global XY plane (same convention as naca0012_points.py).
Import: drag & drop domain.txt into the SpaceClaim design window.
"""
import numpy as np
from pathlib import Path

C = 1000.0            # chord [mm]
R = 20 * C            # far-field radius [mm]
L_WAKE = 21 * C       # downstream boundary at x = 21c (20c behind the TE)

curves = []

# Front half-circle centred on the leading edge: (0, R) -> (-R, 0) -> (0, -R)
theta = np.linspace(np.pi / 2, 3 * np.pi / 2, 181)
curves.append(list(zip(R * np.cos(theta), R * np.sin(theta))))
curves[0][0] = (0.0, R)          # exact end points (no round-off gap)
curves[0][-1] = (0.0, -R)

# Wake box: top, outlet, bottom
curves.append([(0.0, R), (L_WAKE, R)])
curves.append([(L_WAKE, R), (L_WAKE, -R)])
curves.append([(L_WAKE, -R), (0.0, -R)])

out = Path(__file__).resolve().parent / "domain.txt"
with open(out, "w") as f:
    f.write("3d=true\npolyline=false\n")
    for pts in curves:
        f.write("\n")
        for x, y in pts:
            f.write(f"0.0 {x:.6f} {y:.6f}\n")

print(f"{len(curves)} curves written to {out}")
