# HC01 exception wording status

Reviewed 2026-10-08 against the frozen HC01 registration. **B** means the specific exception is not defined by the preregistration; the exact reporting sentence is drafted under each item. The release-checklist receipt is unchanged.

## Item 4 — B, genuine exception

Frozen text:

- `DESIGN.md:42`: “After that no-model preflight, complete these gates in order before releasing HC01 scored cells:” Lines 44–46 enumerate the KRS-GATEFAIL build check, packet-capable lane, and Tier 1/SMALL32 order; none designates a formatter-red base as intentional.
- `DESIGN.md:131`: “Follow the release checklist. The first two assigned EU syn06 cells are the two Kogen arm smokes and remain in ITT; bulk release requires official grade/handoff and record validation, not task success.”
- `AMENDMENT-1.md:5`: “This amendment overrides only the registered execution host.”

The frozen text does not say that a pre-existing `mix format --check-formatted` failure is an intended red gate. Arm symmetry and the formatter’s absence from the official outcome do not waive checklist item 4.

**Why not VALID / why DESCRIPTIVE:** “The untouched base’s formatter gate was red, and the frozen registration never declared that red as intentional; this is a genuine release-gate exception, so the result cannot be called VALID for confirmation and should be reported DESCRIPTIVE.”

## Item 5 — B, genuine exception

Frozen text:

- `DESIGN.md:57`: “Both arms use one identical release binary and source commit.”
- `LANE-REQUIREMENTS.md:3`: “Build the dedicated HC01 lane from a copy of levers/kogen-rs-runner, pinned to krs-rc1, built once on EU from a fresh clone.”
- `LANE-REQUIREMENTS.md:5`: “Both arms share one binary and commit; aliases OFF/ON; `build.context_packet` written explicitly (false/true) into the generated .kogen/project.yaml.”
- `DESIGN.md:80`: “Existing read-only dependency caches may be warm, but isolate per-cell worktrees, HOME, conversation IDs and writable caches.”
- `AMENDMENT-1.md:12` also preserves “arms and their single shared binary/commit”.

These lines define a common binary and commit, not a single shared filesystem root. The text is silent on overriding the checklist’s per-arm-root requirement, so the coordinator’s “shared root is mandated” rationale does not satisfy the strict A test.

**Why not VALID / why DESCRIPTIVE:** “The registration requires a common binary and commit but does not authorize one shared Kogen filesystem root where the release checklist requires per-arm roots; this is a genuine execution exception, so the result cannot be called VALID for confirmation and should be reported DESCRIPTIVE.”

## Item 10 — B, genuine exception

Frozen text:

- `DECISION-RULE.md:50`: “Report per-task rates and net differences, all R/L pairs, official `tests_passed/tests_total`, Build reachability and packet exposure, model/effort violations, host/order/load, wall time and complete tokens.” It then says cost and time are secondary; it does not say they may be omitted.
- `DECISION-RULE.md:54`: “Confirmatory execution must satisfy the shared release/record gates before bulk release; undeclared accounting gaps block it.”
- `DESIGN.md:133`: “Publish the entire assigned-cell ledger, strict-validation result, aggregate and task pass rates, rescues/losses, tests passed/total, exposure counts, token vectors, all-stage token/pass and wall/pass, timing/host/order circumstances and every fault.”
- `AMENDMENT-2.md:5`: “This amendment only settles how two existing DECISION-RULE requirements are met.” Amendments 2–4 define official count extraction/retention; none waives strict run-record validation or the required reporting fields.

The preregistration keeps strict record validation and these secondary reporting fields as gates; calling cost/time secondary does not redefine missing emitter fields as part of the measurement.

**Why not VALID / why DESCRIPTIVE:** “The HC01 registration requires the shared record gates and publication of strict-validation, token, timing, host/order and fault fields; while those emitter gaps remain, the result cannot be called VALID for confirmation and should be reported DESCRIPTIVE.”
