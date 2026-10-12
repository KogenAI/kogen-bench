# BM-SHAPE1-FIX-2 — sole fix round

All eight full-review blocking findings have code fixes and offline controls.
No measured shaper, scoring cell, hidden suite, judge, network or cloud command
ran in this fix round. Local native/unit controls are unmeasured self-tests.

| Review item | Fix and evidence |
| --- | --- |
| Isolation | run_shaper.sh/py delegate solely to the existing Linux lane; 8 shape tasks and 24 overlay definitions contain only public inputs and a non-scoring stub. collect_intent.py freezes lane output and audits hidden-path commands. Bench history must contain only public benchmark cells; private judge history is separate. |
| Validity/kills | score_cell.py identifies native assertions separately from panics, throws, crashes, timeouts and unclassified failures. Real pinned Rust/Go/Bun assertion, runtime and pass controls succeed. |
| Implementation integrity | Submitted tests get a bwrap whitelist with the whole public tree and bin directory read-only, acceptance/ writable, ephemeral /tmp, no task/reference/results mounts. All binary sidecars are preserved and hashed before/after. Local mount-plan controls pass; actual Linux enforcement remains to prove there. |
| Denominators | Structural/incomplete submissions receive validity 0 and kills 0/5 even with no evaluated mutants. Missing receipts, provider/account-limit/preparation/<SERVER_ID> remain infrastructure with missing scores, excluded by analyze.py. Empty/incomplete/infra controls pass. |
| Statistics | Kill counts/denominators and all Wilcoxon differences/ranks use Fraction; fifths ties now return p=1, with exact exhaustive sign assignments and no equality tolerance. |
| Coverage | Frozen inventories cover all eight tasks, including 29 behaviours from c4b-5/run.py and 28 from c4b-6/suite.py. The single pass is keyed by registered task/language across filenames/Intent hashes/hosts. Reserve before invocation; consume before parsing; malformed and aliased passes cannot retry. No judge call ran. |
| Validation | validate_linux.sh uses existing grade wrappers and lane lock. Reference completion requires rc=0, no timeout/leftovers, full count, suite stage, tests_ran, true pass and zero failures/errors/skips before any mutant. Mutants then need build/check and complete hidden behavioural failure with no skips/errors. Full Linux validation was not run: all 120 candidates remain pending. |
| Linux sequencing/disclosures | DECISION-RULE.md and plan.json register shaping after core4b rep 1 + ksub on the <HOST> lane, later Linux scoring only in locked quiet gaps, model/task-author overlap, prior stopped isolation pilot, CLI mutant limits, exact one-rep budget/seed and deferred ceiling/floor checkpoint. |

Local regression suite: 15 tests passed (results/fix1-self-tests-final-v2.log).
Real native controls: assertion failure / runtime failure / pass in all three
languages (results/fix1-native-controls.json). C4-4 reference units pass in
Rust/Go/Bun; their test-only base transplant is invalid; unit tests kill 0/5
mutants per language (results/fix1-reference-units/summary.json). Empty Intent
receives invalid validity and 0/5 kills in all three languages. These controls
do not claim any full hidden validation or end-to-end Linux gate.

Overlay files: overlays/overlay-shape-{c4-1,c4-2,c4-4,c4b-2,c4b-3,c4b-4,c4b-5,c4b-6}.tar.
Source shape task directories: tasks/shape-<TASK>/; SHA-256 manifest:
overlays/MANIFEST.json. Offline tests cloned all 24 bundles, proved exactly one
public commit and byte-identical base files/public prompt suffixes, and verified
that no original hidden/reference/mutant files are in any overlay.

Pending: sole targeted Astra-medium recheck; installation into the existing
Linux kit; full reference/mutant validation (c4-4 first); real Linux bwrap
integrity/isolation/audit and host/arm dry/strict Standard capture. The exact
non-scoring stub necessarily has pass_=false; manager reconciliation of its
expected shape-dry receipt with RULES 7 is a launch gate, not fabricated grading.
No launch gates are accepted. REGISTRATION-FIX-1.json is the new immutable
revision; original registration/full-review evidence is retained. No commit or
publication was made.

Provenance check: every archived registered artifact matches the original
fingerprint except REVIEW-LOG.md, which contains a post-freeze administrative
review record. Its original frozen bytes are unavailable; the post-review log
and this discrepancy are retained in revisions/design-v1/PROVENANCE.json.
No measured launch used that changed log. The new registration freezes the
current review record and implementation together.
