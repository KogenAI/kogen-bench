# Spec review B: Quint models + checks (Opus, read-only, frozen race3 inputs)

I don't think the Quint layer can be trusted to generate race cases yet. All the check logs pass, but most scored cases expect details CORE.md never fixes, several are wrong for any CORE-correct implementation, and some contradict each other. No quint binary was on PATH, so this is a static review, plus a cross-check of the 112 generated case files against the frozen sources.

**Scale:** 83 Quint cases are scored after TARGET.md's exclusions. Only 49 are distinct, and 66 use scripted provider replies.

## BLOCKER

1. **intent.qnt:271-280, 199: every scripted provider request must match Rust's prompts byte for byte.**
   - Each turn requires the exact `/instructions` text ("You are Kogen, an agent for shaping…") and the shaper prompt bytes at `/input/1/content/0/text`.
   - It also requires exactly three tools by name (`read/search/write` for the shaper, `finish/shell/tool_output` for the Builder), `parallel_tool_calls:false`, and an exact request count.
   - The exported manifests carry these as `equals`. CORE fixes only the model and effort.
   - This hits the 66 scored cases that use provider scripts.
   - Fix: keep only `/model` and `/reasoning/effort` as request checks, and put the tool contract in CORE.

2. **status.qnt:468, git.qnt:817: approval hashes are hard-coded.**
   - `intent approve alpha 408a1fa6…` and `fixtureApprovalHash = "7055a12f…"` are literal values.
   - CORE never says what bytes the hash covers, so any other serialization gets a mismatch (exit 1) and every later step fails.
   - Fix: capture the hash from the review card, as intent.qnt:127 already does.

3. **shape.qnt:192-196: the Cargo wrapper runs `${fixtures}/cargo-real`, which nothing installs.**
   - The manifests list `fixtures {}` and `tools: ["git"]`, and the runner has no host-cargo hook.
   - The base check therefore gets no evidence, which CORE §4.2 calls an environment problem (exit 3). The traces expect exit 0 (scored shape 20269011/12/13/15).
   - Fix: install the fixture, or declare and block it.

4. **intent.qnt:44 `rustSource` is not rustfmt-stable.**
   - The expected bytes are `fn acceptance_a1() { assert_eq!(…); }` on one line.
   - CORE §4.2 makes the rustfmt-formatted bytes the source of record, and default rustfmt splits that body onto separate lines. I couldn't run rustfmt here to confirm.
   - It is asserted as exact bytes in 16 scored cases (approve ×6, check ×6, shape ×4), at shape.qnt:263, approve.qnt:129 and check.qnt:341.

5. **Two models expect different exit codes for the same situation.**
   - Deadline expiry: build.qnt:213 expects 1; process.qnt:856 expects 3 (`build_deadline_expired`). Both scored cases (build 20271011, process 20263015) are under deadline expiry.
   - Candidate tampered before the recheck: git.qnt:1378 expects 3; landing.qnt:415 expects 1.
   - No single implementation can pass both sides. Fix: use 1, per CORE §3 ("failed Build").

6. **config.qnt:16-21 accepts a schema CORE doesn't have.**
   - It accepts keys outside CORE: `build.roles`, `domains`, `base`, `sandbox`, `gate_paths`, `setup`, `fix` and others.
   - Scored config cases 20264016/17 expect the exact stdout `environment/project_config_invalid: …` followed by `build.roles.auditor is missing required key \`model\``. A CORE-strict implementation reports an unknown key instead.
   - git.qnt:818-827's landing config uses `base:` and `domains:`, which CORE §4.1 says must be rejected.

7. **status.qnt:517-644: status detail rows must match Rust's full report schema.**
   - `richDetailRow` includes fields such as `routing_headers` (`x-codex-*`), `cache_measurement`, `sandbox` and `approval/schema`.
   - The comparison is complete-shape, so any missing or extra key fails.

## MAJOR

8. **Text and layout CORE leaves OPEN are baked into scored expectations.**
   - The full review card (intent.qnt:126-142), including "Feasibility: not checked" and the "already red on the base:" warning.
   - Shape output lines, including `wall_ms=` usage lines (intent.qnt:159-165).
   - `queue: not running` and `queue: nothing to build` (approve.qnt:145, intent.qnt:183).
   - Package layout: `refs/kogen/intents/<slug>`, `Kogen-Approved-*` trailers and `approval.json` (intent.qnt:168-179).
   - `.kogen/intents/<slug>/intent.md` with front matter, and the two-level workspace path (build.qnt:128-129).
   - `refs/kogen/incoming/*` (git.qnt:1389), the landing subject equal to the Intent title (git.qnt:984), and the exact stash-recovery command (git.qnt:993).
   - CORE §5 says serialization is OPEN. Fix: use patterns or captures, or promote these into CORE.

9. **init.qnt:117, 147-151: hook failure expects behaviour CORE doesn't require.**
   - It expects exit 3 plus a full rollback of `project.yaml`, `.gitignore` and the index. CORE §4.1 says only "exits nonzero".
   - Scored init 20267016/17 test exactly this.

10. **shape.qnt:135-139 never sends inline request text as an argument.**
    - Its comment says inline text "is stdin, never an argv string", and cli.qnt:836 expects a missing file path to fail with exit 2.
    - CORE §3 says such a value is inline text, so the file/inline precedence clause has no witness.

11. **shape.qnt:153, intent.qnt:451: the shaping repair cap is 6 passes.**
    - CORE §4.2 sets `shaping.repair_limit` to default 2.
    - The repair-cap script has min = max = 12 requests, so a CORE-compliant implementation fails it if it is ever generated.

12. **shape.qnt:259-261: shaper questions expect exit 5 and exactly one stdout line.** CORE gives neither.

13. **cli.qnt and status.qnt use different journal paths and recovery schemas.**
    - Journal path: `${repo}/.kogen/local/runs/…` (cli.qnt:1324) versus `${home}/.kogen/workspaces/…/runs/…` (status.qnt:470).
    - Recovery array: cli.qnt:1638 uses 3 keys; recovery.qnt:131-145 uses about 12.

14. **landing.qnt:348-351: an always-failing hook must end with exit 1 within 30 s.** CORE sets no cap on hook repairs, so an implementation that keeps repairing hits an unscripted request.

15. **Duplicate traces skew the scoring.**
    - All 8 intent cases are identical. There are 5 identical landing turn-cap cases, 6 identical empty-queue cases and 4 identical status cases.
    - One bug can therefore cost up to 8 points.
    - Fix: deduplicate, or weight by distinct trace.

16. **Model checks that don't constrain anything.**
    - kogen.qnt:132 sets `lastStep' = []` everywhere, so it produces no replayable steps. `rebasedLandingWitness` was reached in 0/300 runs (kogen-witnesses.log), and there is no park or lost-CAS action.
    - landing.qnt's `st` never changes, so its `safe(st)` checks a constant.
    - process.qnt's supervisor state is never connected to the expected outputs.
    - version.qnt and provider_login.qnt emit no steps at all.

## MINOR

17. **Logs and manifests.**
    - Every typecheck, test and invariant run exits 0, with no warnings or skips.
    - The invariant runs used 20 steps, the traces 30 (config 5), while QUINT-SUITE says 40.
    - All 112 manifests have `clause_ids: ["unassigned"]`.
    - Seeds don't follow QUINT-SUITE's numbering (init should be 12, the files use 7).
    - Config seeds are non-contiguous (10, 13, 14, 16, 17, 20, 47, 51), which looks like cherry-picking.
    - cli-fixtures/manifest.json has `binary_conformance_executed: false`, and the README states no replay was run.
    - Source digests do match the frozen copy.

18. **Defects confined to cases TARGET.md already excludes.**
    - process.qnt:837 waits on a `before-builder` barrier that CORE doesn't define.
    - recovery.qnt:456 uses a `pre-receive` hook to force ref-publication failure, but that hook never runs for a local ref write.
    - recovery.qnt:122 preserves a Landed Build as unverified recovery.
    - cli.qnt:980/992 expect exit 70 ("Kogen bug") for a hook rejection.
    - cli.qnt:646 init output omits CORE's SHA, subject and branch.

## Coverage gaps

These parts of CORE have no generated witness, or only a stub:
- `queue start --detach` and queue stop after the current Build (queue.qnt actions `launchQueue`, `duplicateQueueStart`, `stopAfterCurrent`, `currentBuildFinishes` are never reached).
- A successful `intent remove`.
- `intent shape --json` and `--no-color`.
- Inline and `--` request forms.
- Provider login subject mismatch and its exit 5.
- Label suggestion.
- `version` "(built …)".
- Init check detection (pure tests only).
- Approval invalidation by acceptance presence, and approval with no configured checks.
- Detach on local changes (git.qnt `recoverDetached`).
- Fresh Build after recovery.
- `integrateAndRecheck`.

## Verdict

The model checks pass, but they barely constrain the outputs that actually get replayed.

The generated cases mostly test Rust's own prompts, hashes, layouts and wording, include one uninstalled fixture, and contradict each other on exit codes.

Not trustworthy for deciding the race until findings 1–7 are fixed or the affected cases are excluded and the scoring is deduplicated.