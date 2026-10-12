# Shape1 registration — fix 1, before measurement

One replicate per task/language: c4-4, c4-1, c4-2, c4b-2, c4b-3, c4b-4,
c4b-5, c4b-6 × rust/go/ts-bun (24). C4b-1 is excluded because author
validation is pending; c4-3 is outside the explicitly ordered eight-task scope.
Core4b-2 through -6 passed plain author validation; loaded validation is pending.
The shaper is gpt-6.1-sol high. No measured specification has launched.

## Primary

Validity means uniquely numbered INTENT criteria, native acceptance tests in
acceptance/, compilation on base/reference, at least one native assertion
failure on the base, and executed tests passing on the reference. Rust native
assertion panics count; custom panics, unwrap errors, Go panics, Bun throws,
crashes, compile errors, timeouts and zero-test runs do not establish a failure.
Tests cannot change the application: bin/app and public scaffolding are mounted
read-only, with only acceptance/ and ephemeral /tmp writable. Neither reference
source nor grading material is mounted for submitted tests. Only new INTENT.md
and acceptance/ files may change during shaping; Quint is optional and unscored.

Report validity rates and 95% Wilson intervals. Complete task triplets enter
exact two-sided paired sign tests, Rust versus Go and Rust versus TS/Bun, dropping
binary ties. Holm-adjust the two primary p-values at family alpha .05. Report
wins/losses/ties and denominators; a winner needs rejection in its direction.
No confirmatory Go versus TS comparison. This eight-task set is not a random
sample of all programming tasks, and one replicate does not measure variance.

Structural/output failures and incomplete specification attempts (deadline,
stall or agent failure after actual model work) enter the registered denominator
as validity zero, kills zero out of five, and administrative coverage zero.
These kill zeros are registered even before mutant validation; zero evaluated
mutants is recorded separately from the fixed denominator. Native-invalid tests
also receive zero kills; their readable Intent may still receive judged coverage.
Host/toolchain/isolation/preparation and provider/account-limit launch failures
are infrastructure, with missing outcomes, excluded from inference. Missing
trusted receipts are infrastructure, not failed specifications. Preserve and
reconcile every attempt; never automatically rerun a specification.

## Secondary

Each task has one neutral five-mutant list, translated with identical meanings
into each language. C4-4 validation precedes the other tasks. A reference must
complete its unchanged official hidden grader with process exit zero, no timeout
or leftovers, tests_ran true, stage suite, the frozen full inventory count,
pass_ true and zero failures/errors/skips. Only then validate mutants: build
and make check pass; the same complete grader reports pass_ false and at least
one behavioural failure, with zero errors/skips. Record source, hidden-suite,
patch hashes and detailed receipts. All 120 candidates currently await Linux
full validation. Previous Mac subsets never establish full validation.

For valid specifications, kill rate is assertion kills / 5. Runtime failures and
crashes are separately classified and never kills. Missing/stale full validation
or mutant infrastructure failure makes this secondary missing. Use exact paired
Wilcoxon signed-rank tests for the two registered pairs, remove zero differences,
average tied absolute ranks, enumerate sign assignments. Differences/ranks use
fractions derived from integer kill counts and denominator; no float ties or
tolerances. Secondary p-values are exploratory.

Coverage is descriptive. Freeze a private inventory of every test method under
hidden/suite/**/*.py, including run.py and suite.py. A method is one behaviour;
names/docstrings describe it, not every subcase. Counts by task sequence: 30, 29,
29, 29, 29, 28, 29, 28. Strip standalone language/framework markers where possible.
Exactly one gpt-6-astra medium rubric pass per attempted measured cell, including
empty Intents; known administrative zeros remain zero. Missing infrastructure
launches receive no judge pass. The judge receives only rubric, blinded criteria
and behaviours, not code or language metadata. Its reserved ledger key is the
experiment's task/language, independent of filename, Intent hash and host.
Reserve BEFORE any model invocation; persist response evidence; consume before
parsing. A malformed pass remains missing, with no retry/adjudication. It cannot
change primary validity. Private judge workspaces/history must never enter the
bench user's Codex home or any shaper mount.

## Earlier execution configuration

The first wave used an earlier execution configuration and provides descriptive evidence only. Its records are labelled `lane="pre-RC old-descriptive", strict_eligible=false`. The analyzer reports this group separately and excludes it from strict comparisons and stopping rules.

First wave: c4-4, c4b-2, c4b-4, c4b-5 × rust/go/ts-bun, one attempt each.
EU receives c4-4 + c4b-2; US receives c4b-4 + c4b-5. Seed 20261022 shuffles the
12 cells from the stated task/language order; REGISTRATION-FIX-3.json records
the resulting global order and each host follows its filtered order. At most
one cell per host. This wave is a subset of the original 24-cell budget, not
extra replicates; the attempt latch is shared between strict and descriptive
modes. No automatic retries or later reclassification as strict evidence.

All per-task Linux reference/mutant validation and real-Linux bwrap isolation/
integrity gates remain mandatory before shaping. So do benchmark-only Codex
history, targeted recheck acceptance, harness audit controls, quiet window,
disk admission, STOP, and exact registration/overlay/source fingerprints.
The old mode replaces RC strict_standard_dry, lane_watchdog_1800_600 and the
official audit_cell dependency with controls enforced by this harness: poll
the host codex.jsonl, stop systemd unit bench-<run_id> at 1800 seconds wall time
or at 600 seconds with no new complete event and no open command, honor STOP
while running, fence the launcher, and run audit_events on every transcript.
Open commands exempt the idle stop, never the wall deadline. Missing/malformed
transcripts and audit failures block further admission. Scores remain deferred
to quiet Linux gaps; no overlap with measured cells.

No host was touched by the authoring step. <SERVER_ID> remains installation
of the four task overlays into each assigned host's current kit, full validator
reference/mutant evidence, and a real-Linux isolation/integrity check of that
old profile. This authoring revision does not attest that any such gate passed.

## Linux sequencing, budget and stops (strict mode)

The revised setup uses Linux for shaping and scoring.
Run shape tasks through the existing <HOST> bench-run-lane AFTER core4b rep 1
and ksub complete. One measured cell per host, pinned Linux toolchains, proven
bwrap whitelist isolation, benchmark-only bench Codex history, quiet windows
and disk admission. The existing lane owns agent execution, egress, process
fencing, watchdog, audit and strict Standard capture; no separate Mac execution
path remains. Its current implementation uses the outer bwrap boundary and
bypasses the inner Codex sandbox; this replaces the original nested Mac
workspace-write mechanism. No host change is made or implied by this fix.

Score validity/mutants/coverage LATER on Linux <HOST> hosts, in gaps or after
build reps, NEVER overlapping a measured cell. Scoring/validation acquire the
existing /benchmark-root/launch.lock and check running benchmark services. Judge
reservation/import is gap-locked; the external judge invocation must also hold
that lock for its entire duration. Full Linux reference/mutant validation must
PASS BEFORE shaping, per task, together with the real-Linux isolation/integrity
check. LINUX-GATES.json must bind that exact task to the launched overlay SHA
and current registration; missing, malformed, partial or stale evidence refuses
every measured launch. All registered mutants must be validated or explicitly
excluded with a reason in the validator's hash-bound receipt, never by hand in
the gate. Never put hidden-derived material in a shaper.

Maximum 24 specifications × 1800 seconds (12 aggregate hours) and 24 judge
passes; no token cap. Lane variables set BENCH_CELL_SECONDS=1800 and
BENCH_STALL_SECONDS=600. The lane stops idle agents only with no open command;
the hard deadline has no command exemption. Seed 20261022 and the resulting
cell order are recorded in plan.json. Run IDs s1-<host>-<task>-<lang>; attempts
are single-use across hosts. Preserve /benchmark-root/work/<run_id>/repo and all
lane receipts; the non-scoring shape grader returns shape-not-scored, never
a validity result. Collect/freeze Intent after the lane's cgroup is fenced.

At scoring completion of the first four registered task triplets (c4-4,c4-1,
c4-2,c4b-2), stop further measurement/scoring if all 12 primary values equal
zero (floor) or one (ceiling). No partial triplet triggers it. With deferred
scores, all shaping may already have finished; disclose that fact and retain
those outputs without moving the checkpoint. A common-extreme stop supports
descriptive reporting only. Otherwise complete all eight triplets. STOP persists
and the adapter checks it before launch; the manager stops an active lane unit
if a round stop is issued. Stop admission on isolation/capture failures or two
consecutive infrastructure failures; reconcile without automatic retry.

## Revision and disclosures

Original design + full Astra-medium review are preserved in revisions/design-v1.
This is the sole fix round. A targeted different-model recheck and host/arm dry
evidence remain required before measured launches. LINUX-GATES.json is empty.
The official shape stub deliberately never passes a feature grader: shape dry
evidence must verify its exact expected non-scoring receipt; scorer dry controls
must separately prove official grading/validity, audit, analyzer and strict
Standard capture. Manager must reconcile this expected-stub exception to RULES 7
before admitting measured shape cells. No self-test here satisfies a Linux gate.
REGISTRATION-FIX-3.json freezes the explicit old-descriptive opt-in and its
first wave before any launch; REGISTRATION-FIX-2.json and the older registrations
remain preserved, and
attempts are retained. No launched registered plan is changed. No commit,
publication, network/model call or cloud infrastructure command is authorized.

Disclosure: gpt-6.1-sol, the shaper model, also authored the tasks. Model/task
overlap may advantage latent familiarity. Reference unit tests, differing
language prompts/frameworks/toolchains, task difficulty and one sample per cell
are confounds. C4-4 mutants cover workflow guards/revision/error/threshold;
other tasks' five mutants cover only CLI envelope faults, limiting conclusions
about storage/concurrency. An earlier 21-second Mac isolation pilot was stopped,
yielded no measured Intent, and does not count. Account usage-limit interruptions
of this writer are infrastructure, not shaper results. Local native controls and
Mac portable diagnostics are pilots; Linux validation/scoring/recheck are pending.
