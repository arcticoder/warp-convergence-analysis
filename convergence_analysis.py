#!/usr/bin/env python3
"""
Performs one RK4 time‐step for Minkowski and Schwarzschild profiles
using your solver.integrate_step(), computes error norms,
and writes a LaTeX table to validation_results.tex.
"""

import numpy as np
from solver import integrate_step

# Analytic test profiles
def f_minkowski(r, t):
    return np.zeros_like(r)

def f_schwarzschild(r, t, M=1.0):
    return 2 * M / r

# Error norms: returns (L2, Linf)
def norms(numeric, exact):
    err = numeric - exact
    return np.linalg.norm(err) / np.sqrt(len(err)), np.max(np.abs(err))

if __name__ == "__main__":
    # Grid and timestep
    r_min, r_max, N = 1.0, 10.0, 100
    dt = 1e-3
    tol = 1e-6  # adjust as needed

    grid = np.linspace(r_min, r_max, N)

    # Initial data
    X0_mink = f_minkowski(grid, 0.0)
    X0_schw = f_schwarzschild(grid, 0.0)

    # One RK4 step
    X1_mink   = integrate_step(X0_mink, dt)
    X1_schw   = integrate_step(X0_schw, dt)

    # Analytic exact next state
    X1_mink_ex = f_minkowski(grid, dt)
    X1_schw_ex = f_schwarzschild(grid, dt)

    # Compute norms
    L2_m, Linf_m = norms(X1_mink,   X1_mink_ex)
    L2_s, Linf_s = norms(X1_schw,   X1_schw_ex)

    # Prepare table rows
    table = [
        ("Minkowski",    L2_m,   Linf_m,   L2_m < tol and Linf_m < tol),
        ("Schwarzschild", L2_s,   Linf_s,   L2_s < tol and Linf_s < tol),
    ]
    rows = "\n".join(
        f"{name} & {l2:.2e} & {linf:.2e} & {'Pass' if ok else 'Fail'} \\\\"
        for name, l2, linf, ok in table
    )

    # LaTeX document
    latex = r"""\documentclass{article}
\usepackage{booktabs}
\begin{document}

\section*{Baseline Validation Results}
\begin{tabular}{lrrl}
\toprule
Test           & $L_2$ Error & $L_\infty$ Error & Status \\
\midrule
""" + rows + r"""
\bottomrule
\end{tabular}

\end{document}
"""

    # Write out
    with open("validation_results.tex", "w") as f:
        f.write(latex)

    print("Generated validation_results.tex")