#!/usr/bin/env python3
"""
Convergence analysis for the warp-solver.

Dependencies:
  • warp-solver-validation (https://github.com/arcticoder/warp-solver-validation)
      Provides run_validation.py
  • warp-solver-equations (https://github.com/arcticoder/warp-solver-equations)
      Provides generate_solver_equations.py → solver_update.tex
"""

import numpy as np
import subprocess, re
from math import log

# --- user settings ---
hs = [0.1, 0.05, 0.025, 0.0125]         # grid spacings Δr
tests = ["Minkowski", "Schwarzschild"]  # test cases to tabulate
# ----------------------

# collect errors from run_validation.py
results = {t: {"h": [], "L2": [], "Linf": []} for t in tests}
for h in hs:
    out = subprocess.check_output(
        ["python", "run_validation.py", f"--h={h}"], text=True
    )
    for t in tests:
        m = re.search(rf"{t}\s*&\s*([\d.eE+-]+)\s*&\s*([\d.eE+-]+)", out)
        if not m:
            raise RuntimeError(f"Could not parse {t} at h={h}")
        L2, Linf = float(m.group(1)), float(m.group(2))
        results[t]["h"].append(h)
        results[t]["L2"].append(L2)
        results[t]["Linf"].append(Linf)

# estimate observed orders
orders = {t: {"L2": [], "Linf": []} for t in tests}
for t in tests:
    hs_t = results[t]["h"]
    e2   = results[t]["L2"]
    einf = results[t]["Linf"]
    for i in range(1, len(hs_t)):
        p2   = log(e2[i]   / e2[i-1]  ) / log(hs_t[i]   / hs_t[i-1])
        pinf = log(einf[i]/ einf[i-1]) / log(hs_t[i]   / hs_t[i-1])
        orders[t]["L2"].append(p2)
        orders[t]["Linf"].append(pinf)

# write AsciiMath report
with open("convergence.am", "w") as f:
    f.write("=== Convergence Study ===\n\n")
    for t in tests:
        f.write(f"== {t} ==\n")
        f.write("| h       | L_2 error | L_inf error |\n")
        f.write("|---------|-----------|-------------|\n")
        for h, e2, einf in zip(results[t]["h"], results[t]["L2"], results[t]["Linf"]):
            f.write(f"| {h:.4f}  | {e2:.2e}   | {einf:.2e}    |\n")
        f.write("\n")
        f.write("| Pair           | order_2 | order_inf |\n")
        f.write("|----------------|---------|-----------|\n")
        for i in range(1, len(hs)):
            pair = f"{hs[i-1]:.4f}->{hs[i]:.4f}"
            f.write(
                f"| {pair} | "
                f"{orders[t]['L2'][i-1]:.2f}    | "
                f"{orders[t]['Linf'][i-1]:.2f}      |\n"
            )
        f.write("\n")

print("AsciiMath convergence report written to convergence.am")