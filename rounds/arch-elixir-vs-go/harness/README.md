# ARCH overlay handoff

Run `python3 -B arch_selftest.py` to reproduce the offline self-checks. They use
synthetic token/model receipts, synthetic process tables and fixture kits;
they launch no model or harness arms, implement no kogen semantics and make no
passability claim. One mise regression check runs `go version` with a five-second
limit. SELF-CHECK.json is the machine-readable result.

Installation is selective: arch_install.py reads the frozen lever helper
metadata and race 5 kit pins, then creates a fresh harness. It does not copy
old arm workspaces, sessions, hidden L2/L3 suites or run markers. It refuses an
existing target, and never removes or edits the frozen source. Scratch Git
repositories are initialized without commits. Never invoke lever start.sh,
wave_driver.py or score-wave.sh for ARCH.

Use the Studio sequence after A/B/E/F and the cross-model review are complete.
Only Studio needs a dry cell. A MacBook installation is optional and descriptive;
it can be run separately and is never awaited for the Studio decision. The dry
harness and production harness must be distinct installations; copying a prepared
harness would leave cache/environment paths pointing to the original.

Job F must supply `passability/case-passability.json` in the reviewed-ledger
format documented in ARCH-PLAN.md. The production gate requires the passing
Studio `ARCH-DRY.json` receipt only. Reporting can run with the Studio summary
alone; if the optional MacBook summary is absent, its four cells are marked
`interrupted: optional host unavailable`. Preserve receipt bytes; the gate
verifies hashes. Any transports belong to the integration operator; these
scripts send no messages or SSH commands.

The seal manifest hashes `AMENDMENT-1-STUDIO-DECIDES.md` and its pinned
`AMENDMENT-1-STUDIO-DECIDES.sha256`. The nine commands below are the Studio-only
path, including the one-wave E/G dry receipt. A MacBook dry check or optional
descriptive four-arm wave may be run separately; neither is required or awaited,
and neither can block the Studio launch or verdict.

```sh
export ARCH_HOST=<host> ARCH_AUTH=<codex-home> ARCH_MAP=<harness-map-dir>
python3 -B "$ARCH_MAP/arch_selftest.py"
python3 -B "$ARCH_MAP/arch_install.py" --target "<scratch-dir>/arch-dry/arch-harness" --host "$ARCH_HOST" --codex-home "$ARCH_AUTH" --freeze
python3 -B "$ARCH_MAP/arch_evidence.py" --root "<scratch-dir>/arch-dry/arch-harness" --analysis "<scratch-dir>/arch/passability" --reviewed-ledger "<scratch-dir>/arch/passability/case-passability.json" --out "<scratch-dir>/arch-dry/arch-harness/gates.json"
python3 -B "<scratch-dir>/arch-dry/arch-harness/arch_run.py" --root "<scratch-dir>/arch-dry/arch-harness" --evidence "<scratch-dir>/arch-dry/arch-harness/gates.json" --dry --reference-snapshot "<scratch-dir>/arch-r2/arch-harness/snapshots/build/FINAL/arch-e1"
python3 -B "$ARCH_MAP/arch_install.py" --host "$ARCH_HOST" --codex-home "$ARCH_AUTH" --freeze
python3 -B "$ARCH_MAP/arch_evidence.py" --root "<scratch-dir>/arch-harness" --analysis "<scratch-dir>/arch/passability" --reviewed-ledger "<scratch-dir>/arch/passability/case-passability.json" --dry-studio "<scratch-dir>/arch-dry/arch-harness/out/ARCH-DRY.json" --production --out "<scratch-dir>/arch-harness/gates.json"
python3 -B "<scratch-dir>/arch-harness/arch_run.py" --evidence "<scratch-dir>/arch-harness/gates.json"
python3 -B "$ARCH_MAP/arch_report.py" "<scratch-dir>/arch-harness/out/ARCH-SUMMARY.json" --out "<scratch-dir>/arch-harness/ARCH-RESULTS.json" --markdown "<scratch-dir>/arch-harness/ARCH-RESULTS.md"
```

The Studio production runner executes Wave A, finishes its maintenance and
reserved scoring slot, then starts Wave B. For an optional MacBook run, install
with `ARCH_HOST=macbook`, use the same sealed Studio passability and dry evidence
(the MacBook dry receipt is optional), then report its `out/ARCH-SUMMARY.json`
beside the Studio summary when available. MacBook passability and dry receipts
are descriptive only.

The dry runner uses `--reference-snapshot` only if a dry arm FINAL lacks a
candidate. Reference FINALs are accepted only below the read-only
`<scratch-dir>/arch-r2/arch-harness/snapshots` tree, copied into the dry
harness's `out/` tree with escaping symlinks rejected, and scored by the same
sandboxed scorer. Their numeric receipt is separate from arm results; it can
satisfy the Rules 7 scoring-mechanics gate but is never a scored experiment row.

The installer also accepts explicit --kit, --source-harness, --arch-input,
--go, --elixir and --erlang paths. Defaults match the Studio kit layout.
The physical kit is named race3-kit but its pinned contents are the race 5
Elixir/Go kit. Do not silently replace versions or use a regenerated kit pin.

Build and maintenance run for 90 and 30 minutes respectively. Each phase has a
fresh CODEX_HOME and a recorded deadline. Successful early turns resume the
same phase thread under the original deadline. Hidden tests stay in the parent
harness, never in an arm. Each Studio wave has four arms at 2.5 soft cores each.
Scoring for a wave is reserved after its maintenance phase and before the next
wave. The driver emits eight deciding rows; optional MacBook rows are reported
separately and never enter the decision.
Individual artifacts are under `out/<arm>/phase-{build,maintenance}/`,
`snapshots/<phase>/FINAL/<arm>/`, `tests/results/<phase>/` and
`out/<arm>/ARCH-RUN.json`. Tokens may be re-extracted with arch_tokens.py --run;
this does not require copying raw rollouts. Protect the private output/session
stores and transfer sanitized summaries and proof receipts for reporting.

Self-checks passed; launch gates have not been executed. The handoff still
needs final A/B/E hashes, the job F reviewed case ledger, the Studio scored dry
receipt, and confirmation of MacBook toolchain/auth paths if the optional host
will run. Job F's current
environment blocks for localhost/ps must be resolved on the actual hosts.
The gate schema handoff requires F's proof files to expose a passing status
and input hashes; an absent or blocked status is deliberately rejected.

All overlay source files, the integration sequence and these open integration
questions are listed in OVERLAY-FILES.md and ARCH-PLAN.md. No commits were made,
and the frozen harness was only read.


## Public export boundary

This archive contains only top-level orchestration, briefs, frozen configuration, public specification prose, and the permitted public runner and fakes. Left out: `out/`, evidence directories, ARMS workspaces, transcripts, rollouts, session files, and any source file over 1 MB. The hidden fault suite and its case bodies or expected outputs remain withheld; see the parent round's INPUTS-SHA256.txt commitment.


## Public export boundary

This archive contains only top-level orchestration, briefs, frozen configuration, public specification prose, and the permitted public runner and fakes. Left out: `out/`, evidence directories, ARMS workspaces, transcripts, rollouts, session files, and any source file over 1 MB. The hidden fault suite and its case bodies or expected outputs remain withheld; see the parent round's INPUTS-SHA256.txt commitment.


## Public export boundary

This archive contains only top-level orchestration, briefs, frozen configuration, public specification prose, and the permitted public runner and fakes. Left out: `out/`, evidence directories, ARMS workspaces, transcripts, rollouts, session files, and any source file over 1 MB. The hidden fault suite and its case bodies or expected outputs remain withheld; see the parent round's INPUTS-SHA256.txt commitment.


## Public export boundary

This archive contains only top-level orchestration, briefs, frozen configuration, public specification prose, and the permitted public runner and fakes. Left out: `out/`, evidence directories, ARMS workspaces, transcripts, rollouts, session files, and any source file over 1 MB. The hidden fault suite and its case bodies or expected outputs remain withheld; see the parent round's INPUTS-SHA256.txt commitment.


## Public export boundary

This archive contains only top-level orchestration, briefs, frozen configuration, public specification prose, and the permitted public runner and fakes. Left out: `out/`, evidence directories, ARMS workspaces, transcripts, rollouts, session files, and any source file over 1 MB. The hidden fault suite and its case bodies or expected outputs remain withheld; see the parent round's INPUTS-SHA256.txt commitment.
