# warp-convergence-analysis

Performs a convergence analysis of your warp-solver by parsing baseline validation results, generating synthetic error data at multiple grid spacings (Δr), computing observed convergence orders, and emitting a **NDJSON** convergence report.

## Dependencies

- **validation_results.tex**  
  Copied from warp-solver-validation repository  
  Contains baseline validation results that are scaled to simulate convergence behavior
  
- **solver_update.tex**  
  Copied from warp-solver-equations repository  
  Contains solver equation definitions and stencil information

- Python 3.7+  
- numpy  

## Inputs

- `validation_results.tex`  
  Contains baseline L₂ and L∞ errors for test cases (copied from **warp-solver-validation**)

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
├── validation_results.tex ← baseline validation results
├── solver_update.tex ← solver equations and stencils
└── convergence.ndjson ← generated NDJSON convergence report
```

## Usage

1. **Make sure input files are available**  
   Ensure both `validation_results.tex` and `solver_update.tex` exist in the repository.

2. **Run convergence analysis**
    
```bash
python convergence_analysis.py
```
    
This produces `convergence.ndjson` with newline-delimited JSON records containing convergence data.
    
3. **View the report**  
   Parse `convergence.ndjson` with any NDJSON-compatible tool, or process it line by line as JSON objects.

## How It Works

The script:
1. Parses baseline L₂ and L∞ errors from `validation_results.tex`
2. Generates synthetic error data at multiple grid spacings using theoretical scaling (h²)
3. Computes observed convergence orders between successive grid refinements
4. Outputs structured convergence data in NDJSON format

## Customization

- Adjust `hs = [ … ]` in `convergence_analysis.py` to change grid spacings Δr
- Extend `tests = [ … ]` to add new test cases; the script will parse and tabulate their errors from `validation_results.tex`