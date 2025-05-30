#!/usr/bin/env python3
"""
Convergence analysis for the warp-solver.

This script performs convergence analysis by:
1. Running run_validation.py with different grid spacings (h values)
2. Parsing the stdout output to extract L₂ and L∞ errors for each test case
3. Computing observed convergence orders between successive grid refinements
4. Outputting structured convergence data in NDJSON format

Dependencies:
  • run_validation.py (from warp-solver-validation)
    Validation script that accepts --h parameter for grid spacing
  • solver.py (from warp-solver-validation)
    Solver implementation with integrate_step() function
  • solver_update.tex (copied from warp-solver-equations)
    Contains solver equation definitions and finite difference stencil information

Output:
  • convergence.ndjson - Newline-delimited JSON convergence report
"""

import subprocess
import re
import json
import numpy as np
from math import log

# --- user settings ---
hs = [0.1, 0.05, 0.025, 0.0125]         # grid spacings Δr
tests = ["Minkowski", "Schwarzschild"]  # test cases to tabulate
# ----------------------

def run_validation_with_h(h):
    """Run run_validation.py with specified grid spacing and parse output."""
    try:
        result = subprocess.run(
            ["python", "run_validation.py", f"--h={h}"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to run validation with h={h}: {e}")

def parse_validation_output(output):
    """Parse stdout from run_validation.py to extract errors."""
    results = {}
    
    for test in tests:
        # Pattern: RESULTS: TestName L2=1.234e-05 Linf=5.678e-04
        pattern = rf"RESULTS: {test} L2=([0-9.eE+-]+) Linf=([0-9.eE+-]+)"
        match = re.search(pattern, output)
        if not match:
            raise RuntimeError(f"Could not find results for {test} in validation output")
        
        L2 = float(match.group(1))
        Linf = float(match.group(2))
        results[test] = (L2, Linf)
    
    return results

# Collect errors by running validation for each grid spacing
print("Running convergence analysis...")
results = {t: {"h": [], "L2": [], "Linf": []} for t in tests}

for h in hs:
    print(f"  Running validation with h={h}...")
    output = run_validation_with_h(h)
    parsed_results = parse_validation_output(output)
    
    for test in tests:
        L2, Linf = parsed_results[test]
        results[test]["h"].append(h)
        results[test]["L2"].append(L2)
        results[test]["Linf"].append(Linf)

# estimate observed orders
orders = {t: {"L2": [], "Linf": []} for t in tests}
for t in tests:
    hs_t = results[t]["h"]
    e2   = results[t]["L2"]
    einf = results[t]["Linf"]
    for i in range(1, len(hs_t)):
        # Handle case where errors might be exactly zero
        if e2[i] == 0 and e2[i-1] == 0:
            p2 = float('inf')  # Perfect convergence
        elif e2[i] == 0 or e2[i-1] == 0:
            p2 = float('nan')  # Cannot compute order
        else:
            p2 = log(e2[i] / e2[i-1]) / log(hs_t[i] / hs_t[i-1])
            
        if einf[i] == 0 and einf[i-1] == 0:
            pinf = float('inf')  # Perfect convergence
        elif einf[i] == 0 or einf[i-1] == 0:
            pinf = float('nan')  # Cannot compute order
        else:
            pinf = log(einf[i] / einf[i-1]) / log(hs_t[i] / hs_t[i-1])
            
        orders[t]["L2"].append(p2)
        orders[t]["Linf"].append(pinf)

# write NDJSON report
print("Writing convergence report...")
with open("convergence.ndjson", "w") as f:
    # Write header record
    header = {
        "type": "header",
        "title": "Convergence Study",
        "date": np.datetime_as_string(np.datetime64('now'), unit='D')
    }
    f.write(json.dumps(header) + "\n")
    
    # Write results for each test
    for t in tests:
        # Write test record
        test_record = {
            "type": "test",
            "name": t,
            "results": []
        }
        
        # Add detailed results for each h
        for h, e2, einf in zip(results[t]["h"], results[t]["L2"], results[t]["Linf"]):
            test_record["results"].append({
                "h": float(h),
                "L2": float(e2),
                "Linf": float(einf)
            })
        
        f.write(json.dumps(test_record) + "\n")
        
        # Write order records
        for i in range(1, len(hs)):
            order_record = {
                "type": "order",
                "test": t,
                "h1": float(hs[i-1]),
                "h2": float(hs[i]),
                "L2_order": orders[t]["L2"][i-1] if not (np.isnan(orders[t]["L2"][i-1]) or np.isinf(orders[t]["L2"][i-1])) else None,
                "Linf_order": orders[t]["Linf"][i-1] if not (np.isnan(orders[t]["Linf"][i-1]) or np.isinf(orders[t]["Linf"][i-1])) else None
            }
            f.write(json.dumps(order_record) + "\n")

print("NDJSON convergence report written to convergence.ndjson")