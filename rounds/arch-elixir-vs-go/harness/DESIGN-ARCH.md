# ARCH-20261011 design: Elixir core + Go CLI (E) vs Go only (G)

Opus-written (build-research). Needs one cross-model review (Astra) before freeze. Source: research/benchmarks/proposals/architecture-elixir-go-vs-go-2026-10-11.md.

## 1. The slice both arms build ("kogen-mini")
One external contract, identical for both arms. The hidden tests drive only this contract.
- **Processes (simulated two-node on one host):**
  - one coordinator;
  - two workers, `w1` and `w2`, which are separate OS processes and connect to the coordinator over localhost TCP;
  - a CLI.
  Commands:
  - `kogen coordinator --data DIR --port P`
  - `kogen worker --id ID --coordinator [IP omitted]:P --work DIR`
  - `kogen submit --coordinator … JOB.json`
  - `kogen status --coordinator … --json`
  - `kogen wait --coordinator … JOB_ID --timeout S`
  - `kogen cancel …`
- **Jobs:**
  - A job = `{id, repo, base, patch, build_cmd, timeout_s}`. A worker clones the repo at its base into a private workspace, applies the patch, and runs `build_cmd` with child containment.
  - On success, the job enters the **landing lane** for its repo. Landing is serialized per repo: rebase onto the current head, rerun `build_cmd`, then fast-forward the repo. If the rebase or the rerun fails, the outcome is `rejected`.
- **Durability:** queue and landing state live under `--data` and survive a coordinator SIGKILL. After restart:
  - no accepted job is lost;
  - no job lands twice;
  - in-flight jobs from a dead worker are re-queued after a stated lease (≤10 s);
  - landing order follows the documented order.
- **Containment:**
  - `cancel`, a timeout or worker shutdown kills the job's whole descendant tree, including double-fork/setsid children. Descendants are tracked explicitly (the race 6/process-control lesson: process groups alone don't suffice);
  - a worker SIGKILL must not leave the job's descendants running past the lease. A reaper on restart or a supervisor is acceptable.
- **E-only constraint:** application-owned coordinator and worker logic is Elixir/OTP. The `kogen` CLI is Go and uses PROTOCOL.md for client requests. Go may parse flags, encode/decode protocol messages, display results and launch the Elixir processes; it must not implement queueing, scheduling, leases, recovery, landing or containment. Both required language components and their integration must be delivered within the shared time budget.
- **G-only constraint:** application-owned CLI, coordinator and worker logic is Go. It implements the same externally observable protocol. Standard tools such as Git and the jobs' own build commands are allowed in both arms. Source inspection checks these constraints at each phase snapshot; noncompliance is an implementation outcome handled by DECISION-RULE-ARCH.md.

## 2. Spec given to both arms
- Prose: SPEC.md and PROTOCOL.md.
- Quint models: queue/lease/landing state machine with invariants: no loss, no double-land, serialized landing.
- Gherkin: FEATURES/*.feature with STEPS.md.
- No language hints beyond the E/G constraint sentence. The hidden tests are NOT given; arms write their own tests.

## 3. Hidden tests (black-box, written before scored runs)
- **Groups:** B covers submit/status/wait, documented landing order and rejects. F covers coordinator SIGKILL mid-build and mid-landing; worker SIGKILL mid-build and lease re-queue; double-fork/setsid containment on cancel, timeout and after worker kill; and restart idempotence. M covers the frozen maintenance extension.
- **Counts and coverage:** target approximately 12 B, 12 F and 6 M. Before freeze, record the actual N_B, N_F and N_M, stable test IDs, assertions, deadlines and a mapping to the listed behaviours/faults. N_F must be at least 3 and every listed fault scenario must remain covered. Record per-family counts, including closely related variants: the raw count gives each test one vote, so suite composition is part of the decision policy. Do not select, drop, reweight or alter tests after scored runs start.
- **Non-vacuous fault passes:** each F test must establish its specified accepted job and fault trigger, then verify the required job/repository outcome and applicable containment/recovery invariants through the public contract. An idle program, missing process, missing acceptance, untriggered fault or expired deadline fails the test. Mere survival or absence of descendants is insufficient.
- **Passability gate:** RULES 32: no witness implementation unless the operator orders one. Default passability gate = implementation-free analysis (job F: every oracle traces to a numbered clause, literals are stated decisions, no contradictions, Quint typecheck/invariants/trace consistency, and fault/cleanup mechanics proven against a semantics-free stub on both Macs). If the operator orders witnesses: TWO (Elixir/OTP and Go), a test is passable only if BOTH pass it 3/3 clean repetitions on each Mac; neither is ever visible to builders. Fix or drop unprovable or unreliable tests before freeze, recording why; retain the required coverage. Freeze the gate evidence. Review assertions and deadlines for accidental dependence on any language's internals, output not specified in the contract, or particular scheduling choices.
- **Scoring:** run each snapshot's applicable suite twice. Use a pristine repository fixture, fresh data/work directories and ports, and complete process cleanup for each test/repetition. Start both repetitions from the same immutable artifact, not the state left by the first. A test passes only if both repetitions pass. Score artifacts under the same per-host resource setting without concurrent agent builds or maintenance; use a frozen interleaved E/G scoring order.
- **Isolation:** builders receive only the visible frozen base specification and allowed kits. Keep hidden suites, witness sources/binaries, scorer commands/output, other runs' directories/transcripts and maintenance materials outside their accessible working material. The harness scores separate snapshot copies; hidden results and diagnostics must not enter builder or maintenance sessions. Withhold every run's hidden scores until all eight maintenance snapshots are sealed. Maintenance receives its own build workspace and fixed maintenance prompt, with a fresh session and no hidden feedback.
- **Audit boundary:** use separate workspaces and protected paths plus the existing access audit; audit hidden artifacts, copies, logs and cross-arm access in both phases. No OS-level broker is required. This is audit-based isolation, not proof against every possible covert read; disclose that limit. Dry-cell artifacts, sessions and diagnostics must not be reused by scored agents.

## 4. Arms, runs, time
- **Assignment:** each Mac runs E1, E2, G1 and G2, giving four runs per architecture in total. Before launch, assign the within-host pairs E1/G1 and E2/G2. Use these pair IDs for exclusions and the decision; never rematch based on results.
- **Resources:** the requested aggregate soft CPU budget per run is 3 cores on the MacBook and 2.5 on the Studio. It covers the agent's commands and all application, BEAM, CLI, compiler, worker, supervisor and reaper processes together. It is not a separate allowance per executable or language runtime. Freeze launcher settings, concurrency, sampling method and scoring order; report sampled aggregate CPU and deviations rather than treating a soft cap as hard isolation.
- **Toolchains and kits:** record macOS, host and toolchain versions, exact Race 5 kit hashes, starting dependency caches and allowed install policy. Both architectures receive the same Go kit; E additionally receives the frozen Elixir/OTP kit. Kits must not contain a solution to this slice. Preflight both toolchains and offline kit availability before timing; restore the same per-language starting kit/cache for every run. Any additional permitted dependency installation, compilation and integration during a phase consumes that phase's budget. Record install/network failures and shared-host contention.
- **Build:** 90-minute cap, gpt-6.1-sol high, one builder per run, no reviewers or subagents. REAL-WORKFLOW, permitted Hex/Go installs, Kogen denylist and voiding audit apply. At completion or the cap, stop the phase and seal an immutable build FINAL before maintenance begins. The agent may run its own visible tests; it receives no hidden tests or hidden scores.
- **Maintenance:** a fresh gpt-6.1-sol high session in its own run's existing workspace, 30-minute cap, with the same resource and audit rules. Freeze the full prompt and protocol/spec extension before launch, but disclose them to the agent only after build FINAL. The prompt is: “Add an optional per-job priority field, high or normal, defaulting to normal. Dispatch queued high-priority jobs before normal-priority jobs, without preempting running jobs. Within each priority, preserve original acceptance order; lease re-queue preserves priority and original acceptance order. Persist priority across coordinator restart. Preserve the existing landing-order, serialization, recovery and containment requirements.” The extension must specify its exact JSON field and acceptance/error behaviour consistently with PROTOCOL.md.
- **Completion:** seal maintenance FINAL at completion or the cap. A failed or incomplete build still gets its maintenance opportunity. Model early completion is allowed and recorded; unused time is not transferred to another phase or run.
- **Runner:** freeze the lever harness, launch checks, snapshots, CPU collector, audit, scoring and token/LOC collectors with the maintenance driver before scored launch.

## 5. Measures
- **Primary F:** B/F tests run against the immutable build FINAL. Per-run F is the count out of frozen N_F passing both scoring repetitions. Report F/N_F and the architecture median; do not substitute maintenance FINAL for build FINAL.
- **Cost T:** total provider-reported input plus output tokens for every builder and maintenance session, including continuations, tool-result input and retries that incurred usage, through each phase's stop point. Input includes cached input once; output includes reasoning tokens once under the documented provider semantics. Do not add those subsets a second time. Take one final cumulative usage total per session at its phase stop and sum across the complete session lineage; do not sum overlapping cumulative rollout events. Freeze the collector/schema and token categories in the manifest; report phase totals and the combined total. Missing usage tails or unknown sessions make T incomplete; complete recorded zero usage is distinct from absent telemetry. Exclude preparation, witness, hidden scoring and orchestration costs. Local tool CPU is reported separately and is not converted into tokens.
- **Maintenance:** score B/F/M on maintenance FINAL with the same clean two-repetition rule. Report M/N_M and B/F changes from build FINAL per run, including unresolved baseline failures and regressions. This measures the ability to change the delivered artifact in 30 minutes; unequal starting quality limits claims about maintainability. Maintenance scores do not affect F, but maintenance tokens are included in T by policy.
- **LOC:** report build and maintenance source counts per language with a frozen counter/version, invocation and inclusion/exclusion manifest. Count nonblank, noncomment application source, including handwritten CLI/core/support scripts; report authored tests separately. Exclude dependencies, build artifacts and genuinely generated output, but count authored generator/template source. Apply the same rules to both architectures and disclose exclusions.
- **Repair turns:** report separately per phase the number of subsequent agent continuation prompts after the first explicit agent statement that all its own tests pass. Record that statement and timestamp. Count each continuation prompt once, excluding tool replies and the initial phase prompt; if no such statement occurs, report “not applicable”, not zero. This self-report-dependent diagnostic is not a reliable standalone measure of repair difficulty and does not decide the verdict.
- **Other reports:** B/N_B, per-fault-family results, phase elapsed wall time, sampled CPU, and measured build/test command durations. Define wall time from phase launch to early completion or forced stop, including waits/installations; it is not inferred from token usage. Report missing nondeciding measurements as unavailable with reasons.

## 6. Decision rule (frozen and hashed before launch)
DECISION-RULE-ARCH.md is authoritative. Use the preassigned within-host E/G pairs and retain only complete valid pairs. At least three pairs are required; otherwise the verdict is inconclusive and the recorded direction stands. A valid partner of an invalid run remains reported but is not used in deciding medians.

For the retained pairs, E wins if and only if median F(E) − median F(G) ≥ 3 and median T(E) ≤ 1.5 × median T(G). Otherwise G wins by the simplicity prior. With four values take the mean of the middle two; with three take the middle value. Keep half values and do not round before comparison. Equality at either threshold qualifies.

The manifest freezes actual N_F and reports the 3-test threshold as 3/N_F of the suite. It is a policy threshold, not a significance test. Missing decision data and experimental invalidity are resolved before applying “otherwise G”; agent implementation failures are scored outcomes, not exclusions. B, maintenance, maintenance regressions, LOC, wall time, per-fault-family and per-host results are reported but do not change this rule.

## 7. Build and launch gates
Preparation jobs may run in parallel with distinct files (Sol high, planned ≤45 minutes each): A writes the base and maintenance specifications/models/features; B writes the black-box tests and coverage manifest; C (witnesses) is NOT built unless the operator orders it (RULES 32), and then as two witnesses, Elixir/OTP and Go; F proves passability by analysis; D implements the harness, phases, resource settings and collectors; E incorporates this review and synchronizes the rule and design. These preparation budgets do not weaken the launch gates.

Before scored launch:
1. Review the external contract and tests for language-specific assumptions, vacuous passes, specified deadlines and coverage. Resolve ambiguities in the spec before builders see it.
2. Obtain the passability evidence (job F analysis + stub mechanics on both Macs; or, if the operator orders witnesses, both witnesses 3/3 on both Macs) for baseline B/F and maintenance B/F/M. Record all drops/changes and retain the required coverage.
3. Run sacrificial E and G dry cells on each host, with shortened build and maintenance phases, to verify both toolchains, receipts, aggregate CPU collection, phase stop/snapshot behaviour, token accounting, access audit and separate scoring. A dry-cell product need not pass the suite. Do not feed its code, transcript or hidden diagnostics into scored sessions.
4. Resolve any infrastructure/spec/test changes and repeat the affected validation; a test change requires fresh passability evidence. Freeze the final spec bundles, prompts, kits/cache manifests, harness/scorer/collectors, test counts/coverage/deadlines, passability evidence, dry-cell evidence, pair assignments and rules in a hash manifest. Record status and hashes only now.
5. Start all scored runs with fresh sessions, workspaces and the frozen initial state. Changes to deciding materials after this point require a new registered comparison, not a quiet rule or suite amendment.

## 8. Disclosures
- Two worker processes simulate nodes on one host per run; neither inter-Mac networking nor independent-host failures are tested.
- Results concern macOS containment/recovery on these two hosts; Linux and production operations remain unmeasured.
- E must deliver an Elixir core, Go CLI and their integration inside the same budget as G. This intentional end-to-end architecture comparison does not isolate a language/runtime effect or mature-system performance.
- Passability is proven by implementation-free analysis (RULES 32), not by a running implementation; if the operator orders witnesses they are one Elixir/OTP and one Go. Neither route proves equal implementation difficulty in the two languages.
- Report exact starting kits/toolchains/caches, timed installation costs, soft CPU settings, measured deviations and shared-host contention. More processes do not confer more aggregate CPU allowance.
- Isolation uses separated workspaces, embargoed artifacts/results and access audits; no OS-level broker is used, and isolation is not absolute proof against covert access.
- One model/effort and four runs per architecture make this a pilot. Two suite repetitions do not increase the independent sample size. Complete-pair exclusions preserve equal host representation but may reduce it to three pairs; report the excluded partner runs too.
- F comes from build FINAL, while T includes build plus maintenance. Maintenance outcomes and regressions are reported but do not decide; different starting artifacts confound claims about maintainability. LOC and self-reported repair turns are descriptive, not productivity or quality measures.
- The actual fault count, family weighting and three-test/1.5-token thresholds are policy choices. Report 3/N_F and any ceiling that makes an E win impossible. No statistical significance is claimed.
- Ties and other valid failures to meet E's thresholds default to G by the simplicity prior, even if both implementations perform poorly. Such a verdict is a policy recommendation within this pilot, not proof of production readiness. Fewer than three complete valid pairs is inconclusive and leaves the recorded direction standing.
