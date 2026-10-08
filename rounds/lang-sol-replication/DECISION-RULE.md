# Sol-medium language replication decision rule

The operator reports that the design was frozen at 2026-10-07T10:01:53Z, before the first scored cell. The public bundle does not independently establish that ordering. [DESIGN.md](DESIGN.md) is a sanitized presentation; it preserves the reported SHA-256 of the original source bytes, not a hash of the edited presentation.

## Question and cohort

The question is whether the Round 70 language result is specific to Luna max. The replication uses direct Codex with gpt-6.1-sol at MEDIUM on three stacks: Rust, Go, and TS-Bun.

The new cohort is tasks t1, t2, and t4-fe2 on fixed skeletons, crossed with the three stacks at three reps each (27 cells). Rep 1 is the rule-L smoke for each task-by-stack pair. Reps 2 and 3 are released after the host smoke gates. Rust is assigned to kogen-bench-eu; Go and TS-Bun are assigned to kogen-bench-us.

The existing Sol-medium t5–t7 cells are reused without reruns. The frozen source text states 36 existing cells, but the latest official exact IDs for these stacks resolve to 31: Rust 11, Go 11, and TS-Bun 9. The results preserve that exact-ID count.

## Outcome and accounting

The primary outcome is the latest official hidden-suite full-pass outcome per exact cell ID. The per-cell table also records hidden tests passed/total and official grade-window time. INVALID remains a named outcome and is retained as a non-pass in the reuse denominator.

Token units are fixed: uncached = usage.input; cached = usage.cached_input; output = usage.output; total = uncached + cached + output. No token total is inferred where one of those fields is absent.

## Decision rule

Reconsider the Rust pick only if either:

1. Rust passes at least 3 fewer of the 9 new cells than the better of Go and TS-Bun; or
2. Rust passes at least 4 fewer across the combined Sol-medium set (new plus reused, “equalized per task”). The original design and cited lane files do not record a formula or a scale for this four-pass threshold, so this branch is under-specified and cannot be executed as written.

The combined branch's calculation below is a post-hoc sensitivity summary, not a replacement decision rule: take each task's official pass fraction for a stack, then average the six task fractions with equal weight. It is shown alongside raw totals so readers can see the effect of this explicit weighting choice. It does not repair the missing registered formula or define a new four-pass threshold. The new-cell branch remains executable; it does not trigger here. The combined registered decision is UNRESOLVED. Do not generalize this result beyond the selected cohort.

## Fairness and interpretation

- The smoke receipts record official grading through the sandbox before reps 2–3. Both host smoke gates passed. The TS-Bun t4-fe2 rep-1 scored 17/18, so it remains a FAIL outcome despite the gate passing.
- The lane receipts say the pre-run smoke gate accepted a declared emitter-gap exception and deferred full Standard-record validation until analysis. The referenced exception receipt is not present in this public bundle; the timing of the exact design freeze is operator-reported rather than independently verified.
- New Rust cells ran in the EU host; new Go and TS-Bun cells ran in the US host. Wall comparisons are only within a host.
- The sample is small and has one model per arm. Report observations descriptively; do not infer broad language effects or use significance tests.
