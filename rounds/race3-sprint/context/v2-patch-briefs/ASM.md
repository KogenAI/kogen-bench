# ASM: assemble race3-v2 (Sol medium, 15-minute hard cap)

You work in `~/Scratch.noindex/race3-v2/`.
- `base/{spec,conformance,harness,reviews}` = the original.
- `jobs/<J>/` = nine patch jobs, each on its own copy. `jobs/<J>.last.md` = each job's report (read them all first). `diffs/<J>.diff` = their diffs vs base.
- Build `final/` = base + all job changes. No network, installs or commits. Read nothing under `~/Areas`, `~/.codex*` or `~/Library`.

1. `final/{spec,conformance,harness}` = clones of base (`cp -c -p -R`). Copy in every file each job changed or created, from `jobs/<J>/...` (files are disjoint by design: if two jobs touched the same file, stop and report). S2's `CORE-OUTCOMES.md` and `CORE-WIRE.md` are appended to `final/spec/CORE.md` as new sections (after S1's wording changes), and also kept as files.
2. **Exclusions:** `final/harness/SPEC-BUG-CASES.txt` = the union of the IDs in `jobs/T3/EXCLUDED-V2.txt` and the dropped duplicate IDs from `jobs/T2/conformance/T2-DEDUPE.md`. Case files stay in place; duplicates are excluded as "duplicate of <kept>".
   - Also write `final/harness/EXCLUDED-V2.txt` (ID TAB reason, duplicates included). Add the cases T1 marked "exclude".
   - Every ID must exist in `final/conformance`. Report unknown IDs and drop them.
3. **Counts:**
   - N_total = the number of cases the runner runs (same method as `base/harness/inputs/NCASES`, which says 144: check how it's counted);
   - N = N_total − |excluded|;
   - TARGET = ceil(0.88 × N).
   Write `final/harness/COUNTS.txt` (`N_total=`, `N_scored=`, `target=`, `excluded=`).
4. **Install the inputs:**
   - `final/harness/inputs/` = `final/spec` → `inputs/spec`, `final/conformance` → `inputs/conformance`, plus `NCASES` = N_total.
   - Compute the inputs sha with the same `tree_hash(…, frozen=True)` that `harness/checks.py` uses, and write it to `final/harness/inputs.sha`.
   - Make `checks.py` read the expected sha from `inputs.sha`, and the N/target/exclusions from COUNTS.txt and SPEC-BUG-CASES.txt (no hard-coded 114, 100 or 30 anywhere).
5. **Remove the hard-coded counts** in `score-arm.sh` (the `excl …/114` column), `metrics.py` (thresholds 86/103/100/114 → ceil(0.75 N), ceil(0.90 N), TARGET, N), `checks.py`, `TARGET.md` (regenerate it: target line `TARGET/N`, then the excluded IDs with reasons), and the briefs (fill H3's `{TARGET}`, `{N}`, `{NEXCL}` placeholders). Also update `DECISION-RULE.md`, `RESULTS-OUTLINE.md` and `RACE3-PLAN.md` wording to TARGET/N with the actual numbers and the new inputs sha.
6. **Add to `DECISION-RULE.md`** a "Disclosures (Almir's speed call)" section:
   - no agent dry cell (a no-model harness smoke per host instead);
   - no Astra pre-review;
   - no reference/witness implementations;
   - satisfiability rests on the spec-lint, the contradiction check and the published exclusion list, and the race itself shows what's reachable;
   - the spec v2 patch was a wording and suite patch of the v1 spec, not a full rewrite;
   - races 1, 2, 2s and 2s2 used the unpatched Rust-worded spec.
   Change the double scoring to every snapshot within TARGET±3 plus FINAL, with flakiness judged per arm.
7. **Write `final/harness/suite-checks.py` and run it on the scored set (non-excluded cases):**
   - (a) **spec-lint**: no request assertion other than `/model` and `/reasoning/effort`; no literal 64-hex approval hash.
   - (b) **contradiction check**: no two scored cases expect different exit codes for the same command + outcome. Derive a coarse key, explain it, and report conflicts.
   Exclude any offending case, with a reason, then recompute the counts.
8. Run `bash -n` on every `.sh` file and `python3 -m py_compile` on every `.py` file in `final/harness`.
   - Run the conformance runner's own unit tests if they exist (`final/conformance/tests`, with `python3 -m unittest` or however its README says), offline.
   - Run `final/harness/checks.py` if it can run without a race directory.
Final message: N_total, N, TARGET, excluded by reason, the inputs sha, the test results, and anything unresolved.

## Addendum (main)
In every brief's **Deliverable** line, after "A wrapper script that runs prebuilt output is fine.", add: "`./kogen` must locate its build output relative to its own location (e.g. `$(dirname "$0")/…`), never through an absolute path: snapshots are copied to another directory and scored there."
The kit's rustup `settings.toml` already exists (H4); the supervisor syncs the kit to the MacBook.
After filling the placeholders, run a mechanical brief-equality check (`final/harness/brief-equality.sh`): for each BRIEF-<arm>.md, substitute that arm's language name, stack paths and `<arm>` back into the template's placeholders and diff it against BRIEF.tmpl rendered for that arm. Any difference beyond template substitution fails. Print the result.

## Rulings from the reviewer (main): these OVERRIDE anything above
**Exclusion scope (T3 was too broad).** OPEN text, layouts and paths are not unfair: every arm can read the expected strings in `conformance/`. Exclude only what is Rust-specific, contradictory or impossible.
- RE-INCLUDE (score) T3's B8, B13 and B9 cases, unless a case is also excluded for a kept reason.
- KEEP excluded: the v1 30; B3 (cargo-real); B4 (rustfmt bytes); B5 (process 20263015 and the other losing side); B6; B7; B14; C3 (`feature.05-state`).
- Also exclude BOTH questions-only cases: Quint shape 20269010 (expects 5) and the Gherkin 04-lifecycle questions scenario (expects 0), with the reason "contradictory expected exit (5 vs 0)". Under OUTCOMES in CORE, add: "The questions-only exit code is unscored in race 3."
- CORE §1 (precedence): add the sentence "Where this contract leaves a detail OPEN, the expected values in the scored conformance cases are normative for this race."
- Make sure T1's hash capture and its request-check removal also cover the re-included cases.

**Order:** apply T1 → set the exclusions → **rerun `t2_dedupe.py` on the T1-applied suite** (dropping request checks can create new duplicates) → for each duplicate pair, assert that the dropped case's manifest equals the kept case's manifest apart from id/seed (fixtures, tools, fakes, limits). **If any of these differ, keep both.** → compute N, TARGET = ceil(0.88 × N), the sha.

**Runner patches** (the suite gets a new sha anyway):
- (a) Locale: the Quint and Gherkin runners force `LC_ALL=C` per case. Change the per-case locale to `en_US.UTF-8` (`LC_ALL` and `LANG`) in both runners.
- (b) C2: in `conformance/kogen_conformance/quint_runner.py` around lines 1799–1800, delete the check that compares the captured PID's executable basename with `Path(self.kogen).name`. Keep the TMPDIR identity and start-time checks. Do the same for the executable-path check in `gherkin_runner.py` around line 1047 (even though `feature.05-state` is excluded).
- (c) H1's kg-wrap is exec-in-place. Check that `score-arm.sh` still points `--kogen` at it correctly.
Run the runner's unit tests after the patches.

**Report:** N_total, N, TARGET, the excluded count by reason, the inputs sha, brief equality, the unit tests, and anything unresolved.
