# warp-convergence-analysis

Performs a convergence analysis of your warp-solver by using validation results at multiple Δr values, fits observed orders, and emits an **AsciiMath** convergence report.

## Dependencies

- **validation_results.tex**  
  Copied from warp-solver-validation repository  
  Contains baseline validation results
  
- **solver_update.tex**  
  Copied from warp-solver-equations repository  
  Contains solver equation definitions

- Python 3.7+  
- numpy  

## Inputs

- `validation_results.tex`  
  (copied from **warp-solver-validation**)

- `solver_update.tex`  
  (copied from **warp-solver-equations**)

## Repository Structure
```
warp-convergence-analysis/  
├── convergence_analysis.py ← this script  
├── validation_results.tex ← contains validation results
├── solver_update.tex ← contains solver equations
└── convergence.am ← generated AsciiMath report
```

## Usage

1. **Make sure input files are available**  
   Ensure both `validation_results.tex` and `solver_update.tex` exist in the repository.

2. **Run convergence analysis**
    
```bash
python convergence_analysis.py
```
    
This produces `convergence.am` with AsciiMath-formatted tables.
    
3. **View the report**  
   Open `convergence.am` in any AsciiMath-aware renderer (or read as plain text).
    

## Customization

- Adjust `hs = [ … ]` in `convergence_analysis.py` to change grid spacings.
    
- Extend `tests = [ … ]` to add new test cases; the script will parse and tabulate their errors.