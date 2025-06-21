# Technical Documentation: warp-convergence-analysis

## Overview

The `warp-convergence-analysis` repository provides a systematic tool for performing convergence analysis on warp solver implementations. It runs validation tests at multiple grid spacings to compute observed convergence orders and generates structured convergence reports in NDJSON format.

## Mathematical Foundation

### Convergence Order Analysis

The convergence analysis computes the observed convergence order using Richardson extrapolation principles:

For successive grid refinements with spacings h₁ and h₂ where h₂ = h₁/2, and corresponding errors E₁ and E₂:

```
Observed Order = log₂(E₁/E₂)
```

This provides a quantitative measure of how the numerical error decreases with grid refinement.

### Error Metrics

The analysis computes two types of errors:
- **L₂ norm**: Root mean square error across the computational domain
- **L∞ norm**: Maximum absolute error at any grid point

## Dependencies and Integration

### Required Components

1. **run_validation.py** (from warp-solver-validation)
   - Validation script that accepts `--h` parameter for grid spacing
   - Must output L₂ and L∞ errors in parseable format

2. **solver.py** (from warp-solver-validation)
   - Solver implementation with `integrate_step()` function
   - Provides the numerical integration methods being tested

3. **solver_update.tex** (from warp-solver-equations)
   - Contains solver equation definitions and finite difference stencils
   - Documents the mathematical basis for the solver implementation

### Integration Points

- **warp-solver-validation**: Provides the validation framework and test cases
- **warp-solver-equations**: Defines the mathematical equations and discretization schemes
- **warp-discretization**: May provide additional discretization methods

## Algorithm Description

### Grid Refinement Study

```python
# Default grid spacings for convergence study
hs = [0.1, 0.05, 0.025, 0.0125]  # Each h is half the previous
```

### Analysis Workflow

1. **Validation Execution**: Run validation script for each grid spacing
2. **Error Extraction**: Parse stdout to extract L₂ and L∞ errors
3. **Order Calculation**: Compute convergence orders between successive refinements
4. **Report Generation**: Output structured NDJSON convergence report

### Output Format

The analysis generates `convergence.ndjson` with:
- **Header record**: Study metadata and configuration
- **Test records**: Error data at each grid spacing
- **Order records**: Computed convergence rates

## Implementation Details

### Error Parsing

The script uses regular expressions to extract error values from validation output:

```python
# Example error pattern matching
l2_pattern = r"L₂.*?(\d+\.\d+e[+-]?\d+)"
linf_pattern = r"L∞.*?(\d+\.\d+e[+-]?\d+)"
```

### Convergence Order Computation

```python
def compute_order(h1, h2, e1, e2):
    """Compute observed convergence order"""
    ratio = e1 / e2
    h_ratio = h1 / h2
    return np.log(ratio) / np.log(h_ratio)
```

## Configuration and Usage

### Grid Spacing Configuration

Modify the `hs` array in `convergence_analysis.py` to adjust grid spacings:

```python
# Example: More aggressive refinement
hs = [0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625]
```

### Running the Analysis

```bash
python convergence_analysis.py
```

The script automatically:
1. Runs validation for each grid spacing
2. Parses output for error values
3. Computes convergence orders
4. Generates NDJSON report

## Analysis Interpretation

### Expected Results

For a well-implemented finite difference scheme:
- **Second-order schemes**: Convergence order ≈ 2.0
- **Fourth-order schemes**: Convergence order ≈ 4.0

### Diagnostic Information

- **Orders significantly less than expected**: May indicate implementation errors
- **Inconsistent orders**: May suggest numerical instabilities
- **Orders higher than expected**: May indicate error cancellation or insufficient resolution

## Related Work

### Theoretical Background

- Richardson extrapolation theory
- Finite difference method analysis
- Numerical convergence testing methodologies

### Related Repositories

- **warp-solver-validation**: Provides validation framework
- **warp-solver-equations**: Mathematical foundation
- **warp-discretization**: Discretization methods
- **warp-curvature-analysis**: Related analysis tools

## Future Enhancements

### Potential Improvements

1. **Adaptive grid spacing**: Automatic selection of optimal spacing ratios
2. **Multiple test cases**: Parallel analysis of different validation scenarios
3. **Visualization**: Graphical convergence plots and trend analysis
4. **Statistical analysis**: Confidence intervals and error estimation

### Integration Opportunities

- Integration with continuous integration for automated convergence testing
- Connection to optimization frameworks for solver parameter tuning
- Extension to time-dependent convergence analysis

## References

### Numerical Methods

- LeVeque, R.J. "Finite Difference Methods for Ordinary and Partial Differential Equations"
- Roache, P.J. "Verification and Validation in Computational Science and Engineering"

### Convergence Analysis

- Richardson extrapolation methodology
- Grid convergence index (GCI) standards
- ASME verification and validation guidelines
