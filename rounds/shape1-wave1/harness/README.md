# Shape1

One continuing worker; offline fix round for executable specification. Read
[DECISION-RULE.md](DECISION-RULE.md), [FIX-REPORT.md](FIX-REPORT.md), and
[REVIEW-LOG.md](REVIEW-LOG.md). No measured cell or judge is run by this job.

`tasks/shape-<TASK>/` contains the original public bases, the fixed shaping
instruction followed by each public prompt verbatim, and a non-scoring stub.
Empty reference/<LANG> directories satisfy the existing overlay builder; they
contain no feature implementations. Base Git bundles have one public commit,
verified against registered tracked-file hashes. The stub is the only hidden
file in the overlays. No original hidden suite, reference code or mutant patch
is packaged. Base files are unchanged; no Mac compatibility ports are applied.

Local packaging (already completed; refuses to overwrite tasks):

```sh
python3 build_shape_tasks.py
```

It calls `../core4/tools/build_overlay.py --root "$PWD/tasks" --family shape1`
and writes `overlays/overlay-shape-<TASK>.tar` plus `overlays/MANIFEST.json`.
Installation into the existing host kit is a later manager step; not performed.

On the intended Linux host, after core4b rep 1 + ksub and every launch gate:

```sh
./run_shaper.sh eu c4-4 go
# Default only prints the existing lane invocation; future actual launch:
./run_shaper.sh eu c4-4 go --launch
```

This invokes `bench-run-lane shape-c4-4-go s1-eu-c4-4-go gpt-6.1-sol high`
with 1800/600 second lane deadline/stall variables. One cell per host; no Mac
launch path, nested sandbox or personal Codex history. The lane's bwrap mounts
only its public work directory plus benchmark-only Codex home and pinned tools.
Bench Codex history must contain only public benchmark-cell history. The lane
currently bypasses Codex's inner sandbox; bwrap is the enforced isolation.
The shaped worktree remains `/benchmark-root/work/s1-eu-c4-4-go/repo`.
Lane stub grades are always non-scoring. START/END logs are in logs/launcher.log.

After the lane is fenced, on the host collect the output and hidden-path audit:

```sh
python3 collect_intent.py c4-4 go s1-eu-c4-4-go
```

This freezes the public tree, INTENT.md, acceptance/, codex.jsonl, usage and lane
timing in results/<RUN_ID>/intent/, verifies prompt identity and unchanged base
files, and records audit flags. Zero flags are required. Infrastructure/provider
failures stay distinct from attempted incomplete specifications. Missing trusted
receipts are infrastructure. No output may be overwritten or silently retried.

Later, in Linux scoring gaps, validate c4-4 first, then remaining tasks:

```sh
./validate_linux.sh c4-4 --revision=-linux-fix1
```

Set SHAPE_SOURCE_ROOT to the private directory containing core4/ and core4b/.
SHAPE_SEALED_ROOT defaults to /benchmark-root/shape1-private. The validator uses
the kit's existing `sandbox-profile.sh grade WORK TASK -- COMMAND`, checks the
complete reference verdict before mutants, and holds the lane launch lock.
All full Linux validation is pending. Mac subset evidence cannot promote mutants.
After acceptance, the manager may select an immutable validation file as
mutants/<TASK>/validation-current.json; reference/patch/suite hashes must match.

Then score a collected Intent, in a gap with pinned Linux toolchains:

```sh
python3 score_cell.py c4-4 go results/s1-eu-c4-4-go/intent/repo \
  --output results/s1-eu-c4-4-go/score.json
```

The scorer builds trusted variants before adding submitted tests. Submitted
tests see only identical public base scaffolding, their acceptance files and
the read-only binary, inside a networkless bwrap sandbox. No reference/hidden
source or other workspaces are reachable. Assertion failures, runtime errors,
crashes, no-tests and timeouts are classified separately. Structural/incomplete
rows receive registered zero kills/5; infrastructure receives missing outcomes.

Private coverage packet and ONE external judge pass per attempted cell:

```sh
python3 coverage.py prepare c4-4 go results/s1-eu-c4-4-go/intent/repo/INTENT.md \
  /benchmark-root/shape1-private/coverage/s1-eu-c4-4-go.json --run-id s1-eu-c4-4-go
python3 run_coverage.py /benchmark-root/shape1-private/coverage/s1-eu-c4-4-go.json
# Manager invokes ONE gpt-6-astra medium pass with rubric + criteria + behaviours.
# Keep the judge workspace/history private, outside the bench Codex home.
# Hold /benchmark-root/launch.lock for the entire external judge invocation.
python3 run_coverage.py /benchmark-root/shape1-private/coverage/s1-eu-c4-4-go.json \
  --response /benchmark-root/shape1-private/coverage/s1-eu-c4-4-go-response.json \
  --output results/s1-eu-c4-4-go/coverage.json
```

Reservation precedes the model call. This adapter reserves/imports; it never
calls Codex locally or uses personal authentication/history. A canonical
task/language ledger prevents filename/host/Intent aliases buying another pass.
Malformed responses consume the pass. Pass --coverage-result to score_cell.py
before its immutable output if a judged coverage result exists.

`python3 analyze.py <SCORE_FILES> --output results/analysis.json --apply-stop`
reports paired sign/Holm, exact fraction Wilcoxon, descriptive coverage and the
registered floor/ceiling latch. Analyze checkpoint triplets in registration
order even if all shaping precedes scoring; no new cell is admitted after STOP.

Offline verification (does not launch agents or feature scoring):

```sh
python3 test_fix.py
```

It checks all 24 overlay bundles/public prompts, all eight inventories, real
native assertion/panic/pass controls, empty zeros, infrastructure exclusions,
exact ties, the read-only mount plan, audit positives and one-pass reservations.
Current evidence: results/fix1-self-tests-final-v2.log and native/reference-unit
controls. Linux mount enforcement, full mutants, host dry/strict capture and
the sole targeted recheck remain pending. Current launcher gates are empty.
Original design evidence is archived in revisions/design-v1/; old Mac scripts
are retained only there or as unmeasured unit-control helpers, never shapers.
