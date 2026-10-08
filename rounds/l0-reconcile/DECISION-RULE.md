# Reconciliation rule

## Scope and status

This is a descriptive audit of historical receipts. It launches no cells and creates no new performance claim. `STATUS: VALID` applies only to the completeness of this reconciliation. Historical cohort labels are recorded in `RESULTS.md`.

For each row, use the sanitized cell level extract. `PASS` counts as success; `FAIL` and `INVALID` remain visible and are not converted into passes. Preserve each source ITT rule: R69 includes timeout and runner failures and excludes only four documented infrastructure rows; R57 does not treat its missing slot as a failure; R74 missing slots remain unreconstructed. No outcome is inferred for a cell without a grade or terminal receipt.

No new fairness comparison is estimated for R74 because its retained observations span differing times, venues, and configurations. R72 P3 is reported as a partial cohort. R57 pooled results remain interim while one planned slot is missing.

## Calculations

- R72: count official outcomes by arm. The invalid Kogen control row remains in the 84-cell denominator and is not a pass.
- R74: count the 167 internal scored rows and compare the sanitized grade matches with the public scored export. Report the 231 retained slots without scored grades separately; do not infer their terminal outcomes.
- R69: reproduce pooled pass counts and 95% Wilson rate intervals. For the pairwise intervals, use Newcombe’s independent-proportions construction from Wilson limits. For the decision test, condition on pairwise total successes in each task, use each pair’s retained arm counts as fixed margins, convolve exact hypergeometric distributions, and sum the upper tail including the observed treatment successes. Use exact rational arithmetic; no correction is added.
- R57: strata are task × actual host. Use fixed planned per-arm cell weights US 4/156, EU 8/156, and Studio 16/156. Compute each stratum’s shell-only minus default pass proportion using the observed arm denominator. For the one-sided 95% lower bound, use Wilson limits with z=1.644853627 and the stratified Newcombe/MOVER formula `Δ − sqrt(Σ w²[(p_shell − L_shell)² + (U_default − p_default)²])`. Keep the missing shell slot out of the observed denominator while retaining the design weight. Also report equal-stratum sensitivity.

The R57 declaration specifies stratification but not an estimator. The MOVER calculation above reproduces the method selected in the published pooled snapshot; it is not a predeclared estimator.

## Accounting and reproduction

No token or cost totals are recomputed here. If a token total is referenced, use one definition: uncached input + cached input + output; total is their sum.

`reproduce/reconcile_l0.py` uses only the sanitized CSVs in `data/` and Python’s standard library. Run `python3 reproduce/reconcile_l0.py` from the repository root. It does not read source ledgers or other round pages.
