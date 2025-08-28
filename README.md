# warp-convergence-analysis

Performs a convergence analysis of your warp-solver by running validation tests at multiple grid spacings (Δr), computing observed convergence orders, and emitting a **NDJSON** convergence report.

## Dependencies

- **run_validation.py**  
  Copied from warp-solver-validation repository  
  Validation script that accepts `--h` parameter for grid spacing
  
- **solver.py**  
  Copied from warp-solver-validation repository  
  Solver implementation with `integrate_step()` function
  
- **solver_update.tex**  
  Copied from warp-solver-equations repository  
  Contains solver equation definitions and stencil information

- Python 3.7+  
- numpy  

## Inputs

- `run_validation.py`  
  Validation script that runs warp solver with specified grid spacing (copied from **warp-solver-validation**)

- `solver.py`  
  Solver implementation (copied from **warp-solver-validation**)

- `solver_update.tex`  
  Contains solver equations and finite difference stencils (copied from **warp-solver-equations**)

## Outputs

- `convergence.ndjson`  
  Newline-delimited JSON file containing:
  - Header record with study metadata
  - Test records with error data at each grid spacing
  - Order records with computed convergence rates between successive grid refinements

## Repository Structure
```
warp-convergence-analysis/  
├── convergence_analysis.py ← main analysis script  
├── run_validation.py ← validation script from warp-solver-validation
├── solver.py ← solver implementation from warp-solver-validation
├── solver_update.tex ← solver equations and stencils
└── convergence.ndjson ← generated NDJSON convergence report
```

## Usage

1. **Make sure input files are available**  
   Ensure `run_validation.py`, `solver.py`, and `solver_update.tex` exist in the repository.

2. **Run convergence analysis**
    
```bash
python convergence_analysis.py
```
    
This:
- Calls `run_validation.py --h=<h>` for each grid spacing in the study
- Parses the stdout output to extract L₂ and L∞ errors
- Computes observed convergence orders between successive grid refinements  
- Produces `convergence.ndjson` with newline-delimited JSON records containing convergence data
    
3. **View the report**  
   Parse `convergence.ndjson` with any NDJSON-compatible tool, or process it line by line as JSON objects.

## How It Works

The script:
1. Runs `run_validation.py --h=<h>` for each grid spacing in `hs = [0.1, 0.05, 0.025, 0.0125]`
2. Parses the stdout output using regex to extract L₂ and L∞ errors for each test case
3. Computes observed convergence orders between successive grid refinements
4. Outputs structured convergence data in NDJSON format

## Customization

- Adjust `hs = [ … ]` in `convergence_analysis.py` to change grid spacings Δr
- Extend `tests = [ … ]` to add new test cases; the script will parse their errors from `run_validation.py` output


## Scope, Validation & Limitations

- Scope: The materials and numeric outputs in this repository are research-stage examples and depend on implementation choices, parameter settings, and numerical tolerances.
- Validation: Reproducibility artifacts (scripts, raw outputs, seeds, and environment details) are provided in `docs/` or `examples/` where available; reproduce analyses with parameter sweeps and independent environments to assess robustness.
- Limitations: Results are sensitive to modeling choices and discretization. Independent verification, sensitivity analyses, and peer review are recommended before using these results for engineering or policy decisions.
