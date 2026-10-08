# L1-EU selection and control registration

**Recorded:** 7 October 2026, before the first L1-EU grade.

This sanitized receipt preserves the dated selection and staged-control design. The source records were dated 7 October 2026 and had SHA-256 `9eb4a5756ae0cd94c6dc1be6e994ff7bda5e1feabfdb4039d1c0fd64bacc4ffc` (`SELECTION.md`) and `d50633984728a6e075713fe063fcd6507f2d58a501875c533de6f2f247a673a4` (`STAGED.md`). Their recorded modification times were 20:29:13Z and 20:33:25Z, respectively.

The selection used the latest official baseline row per exact cell ID for direct Luna-max task cells, excluded X-controls from baseline counts, and excluded task 8 and the withdrawn Rust variant. It selected `r70-6-elixir` at 3/6 and `r70-7-elixir` at 5/6. Task 6 still needed reference/no-op admission controls; task 7's reference/no-op controls were already covered. Six mutant/alternative X-controls (reps 730–735) were staged, with no scored model cells in scope.

The operator record at 2026-10-07T20:34:59Z states the selection and staging were complete and that no L1-EU grades had launched. The first grade window in the published control data is 2026-10-07T20:37:00Z. The source lane records are not included verbatim in the public tree; this sanitized receipt preserves the selection facts and their recorded chronology. Published control outcomes are in [data/controls.csv](../data/controls.csv); the later `NOT-RUN` disposition for `l4b-confirm-eu` is recorded in the L1-EU addendum in [README.md](../README.md).
