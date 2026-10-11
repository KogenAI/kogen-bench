# DECISION-RULE-v5: Race 5, Almir/main night run

Frozen inputs SHA: 1e01ae32828e9eca. N=106 scored cases and TARGET=106 come
from COUNTS.txt. TARGET = N: all scored cases (100%). The installed inventory,
not an expected count, owns N; excluded IDs remain published separately.
This rule, MODE, briefs, kit and harness are frozen before either wave.

## Hosts and waves

Rust, Go, TypeScript (Bun), Elixir and Python run on both Macs. Two waves
on each Mac give four Mac runs per language. All five run simultaneously with
soft two-core build/test caps per arm, gpt-6.1-sol / high, three-hour waves,
five-minute snapshots and stop-on-target at 106/106 = 100%.

Linux hosts have 2 vCPU / 7 GB and run Rust and Go only, one language per wave,
counterbalanced: wave 1 EU Rust / US Go; wave 2 EU Go / US Rust. These are
robustness checks: reported, not deciding. Python runs on Macs only and has a
second independently pinned kit hash, PY-KIT-SHA256. The main kit is unchanged.

Wave A is planned around 19:00Z and B around 22:10Z with explicit shared epochs.
B must be at least A + three hours + the declared gap (default ten minutes).
Score A between waves. If scoring or setup overruns B's epoch, abort B and
disclose it; never overlap scoring with a live wave on that host.

If a Mac host drops, continue on the other Mac, add a make-up wave if time
allows, and disclose the drop and any missing or make-up runs. Four Mac runs
per language are the intended deciding sample. Report an incomplete sample
as such; do not silently replace missing Mac runs with Linux robustness runs.

Disk admission on Macs uses PHYSICAL growth estimates for APFS cp -c clones,
not the logical sum of copied directory sizes. If historical df deltas are
unavailable, use the documented APFS clone-aware estimate in DISK-DEFAULTS.json
plus 30% margin. Never let a logical-size overestimate block launch. Sizing
is overridable and logged. Linux uses physical allocation for non-clone copies
with its shorter retention; no Python kit is needed there.

On Macs keep every five-minute source snapshot. During the wave a background
pruner deletes target/, _build/, node_modules/, .venv/, build/, dist/ and build
artifacts within deps/ from periodic snapshots older than thirty minutes.
Keep dependency source. Never prune FINAL, TARGET-<arm>, incomplete snapshots
or snapshots thirty minutes old or younger. Only FINAL and target crossings
need executables; recent periodic snapshots retain them too. Mark older
snapshots as source-only and exclude them from executable scoring. Their
sources and hash receipts remain available; do not manufacture failure scores
for missing pruned executables. Python .venv is kept in all executable snapshots.
On Linux keep only the last three completed periodic snapshots, plus FINAL
and TARGET-<arm>; remove older periodic snapshots. Linux is not deciding.
The results disclose retention and its limit on reconstructing earlier scores.

Every 10 seconds, each watcher reads its own brief-command result file. Only a
complete inventory of every scored case, with 106/106 passes, triggers a
TARGET-arm snapshot, STOP-arm and timestamp/pass-count/result-SHA/token receipt.
Partial runs never trigger. Official scores come from later offline scoring.

## Main measure and decision order

PRIMARY: the median official FINAL score /106 across the four Mac runs per
language. If any arm reaches 100%, time to 100% ranks first: earlier is better,
and a reached time beats any unreached arm. Use the earliest officially verified
100% time for a language when comparing reached languages, and report every
Mac run's reached time and reach count. Linux runs do not enter this decision.

TIE ZONE: if the top two medians are within three cases, compare median
build/test time per change from the run data, then spread. State the measurement
method in the results. Spread is max minus min of official FINAL counts across
the four Mac runs; smaller wins. A reached time still beats any unreached arm.

Name the winner mechanically by this rule. If the top two are still within
the tie zone after both tie breakers, report "no clear winner". Equal or
unavailable build/test timing does not manufacture a winner; proceed to spread
and disclose missing observations. If both tie breakers leave the leaders
indistinguishable, report "no clear winner".

Reported, not deciding: Linux robustness runs, tokens, blind code review,
binary size and startup. After wave 2, if time allows, run a change round on
the top two and a blind review; both are reported only. Raw/stall-adjusted
run times, CPU, sampled scores and audit observations are also disclosed.

Operations: three-hour waves; 100% target with stop-on-target; REAL-WORKFLOW
with live web search, the Kogen denylist and voiding audit; scoring at most
three concurrent arm-snapshots per host, with double scoring in the band below.

## Scoring

Score only after a wave is DONE: at most THREE concurrent arm-snapshots per
host, --jobs 2 each. SCORE_CONCURRENCY defaults to 3 (allowed 1, 2, 3), with the
existing shared host slot pool. Keep 60-second invocation limits, kg-wrap process
groups/cwd sweeps and one untimed version warm-up (<=900 seconds) per raw score.
Score all FINALs over all cases first, report /N_total and scored /106, then
search exact scored IDs from runner list minus SPEC-BUG-CASES for time-to-target.
Search the executable snapshots only (recent periodic, TARGET crossings and FINAL),
check the preceding retained checkpoint and verify earlier executable checkpoints
on regressions. Source-only or removed snapshots cannot supply official scores.

Every snapshot whose FIRST scored count is within TARGET ±3 (inclusive),
including FINAL, is scored a SECOND time. A case officially passes only if it
passes BOTH raw scorings for that arm and snapshot. Outside the band use the
first result. Preserve raw, combined and flip receipts. A flip affects only
that snapshot/arm. No live scoring; watcher inspection is not scoring.

## Invalidation and disclosures

Invalidates the whole round: changes to the frozen rule, suite, briefs, kit or
harness; lock/isolation failure allowing other runs' code, implementations or
hidden suites; wrong model/effort in more than one arm; different harness
versions between waves. A Mac power/host drop follows the continuation and
make-up policy above; disclose it rather than invalidating the whole round.

Invalidates one arm in one run (counts as not reached): any receipt using a
model/effort other than gpt-6.1-sol / high; missing model/effort receipts; an audit
flag for a real model-provider call or protected outside read ($HOME/.codex*,
$HOME/Library, iCloud, $HOME/Areas, other implementations/races/arms); changes to spec/,
conformance/ or TARGET.md (hash checked); FINAL unscorable for a harness reason.
Every Kogen denylist access, including a blocked attempt or native web query,
returned result URL or page open, VOIDS that arm. Installs/search follow MODE.
Locks and the voiding audit remain required.

Disclose quota/rate-limit stalls, soft CPU bursts, flaky cases, warm-up time,
clean-copy regrade differences, Studio efficiency cores, Linux resources,
mode/network limitations and scheduling failures. No agent dry cell, Astra
pre-review or reference/witness implementation. Satisfiability rests on suite
checks and published exclusions; this race shows what is reachable.

## MODE: real-workflow

REAL-WORKFLOW: you may install packages with your ecosystem's package manager, read documentation on the web, and use live Codex web search as a developer normally would. Never call real model providers; the suite uses a local fake.

Every benchmark declares exactly one MODE in the `MODE` file before freeze.
`sealed` is the controlled, offline, kit-libraries-only comparison: no downloads,
package installs, remote repository fetches, web reads or web search. Offline
Cargo, Go, Hex, npm and Bun switches are enabled, and the Codex workspace shell
has network access disabled. `real-workflow` is the normal developer setup:
package installs, internet documentation and live Codex web search are allowed,
with only the anti-cheating restrictions below. Its offline switches are removed;
Go uses its normal proxy/checksum service and Codex shell networking is enabled.
Both the initial `codex exec` and every `codex exec resume` pass
`-c 'web_search="live"'` in real-workflow or `-c 'web_search="disabled"'` in sealed.
No cached-search fallback is allowed in sealed. The agent's Codex model transport
is permitted in both modes and is not an agent-issued provider call.

### Anti-cheating restrictions in both modes

Do not access any existing Kogen repository, kogen.dev or bench.kogen.dev.
Commands, URLs, web search queries, returned result URLs and page opens touching
`KogenAI`, `github.com/.../kogen*`, `kogen.dev`, `www.kogen.dev` or
`bench.kogen.dev` are VOIDING for that arm. The suite's own local
`conformance/bin/kogen-conformance` remains allowed. Calls executed by agent
commands to real model providers, including `api.openai.com`,
`chatgpt.com/backend-api` and `auth.openai.com`, are VOIDING. Provider endpoint
URLs merely written into source (heredocs or file writes) are not provider calls;
executing an HTTP client to those endpoints is a call. The suite uses a local fake.
Read-only kit aids and the fixed Python interpreter in race5-py-kit are allowed,
as with race3-kit; writable caches remain private inside the arm.
Reads outside the arm of `$HOME/.codex*`, `$HOME/Library`, iCloud, `$HOME/Areas`, other arms,
other races and other implementations remain forbidden and voiding. Frozen
specification, suite, target and model/effort integrity checks remain in force.

Each arm has both repository-local git rewrites and its own `GIT_CONFIG_GLOBAL`
file inside the arm. These redirect `https://github.com/KogenAI/`,
`http://github.com/KogenAI/`, `git@github.com:KogenAI/` and
`ssh://git@github.com/KogenAI/` to `https://invalid.invalid/blocked/`, including
clones started outside the repository while using the arm environment.

The Macs have no DNS-level block: no sudo is available, and HOSTALIASES does not
work on macOS. Kogen blocking there is the brief plus git `insteadOf` plus the
voiding event audit. Linux hosts additionally have an `/etc/hosts` sinkhole for
`kogen.dev`, `www.kogen.dev` and `bench.kogen.dev`, applied by the host owner.
This harness does not apply privileged host changes. Locks include all existing
race3-* and race4-* candidates and race5-* candidates except the current wave's
own directory; inherited kit/harness and publishing exceptions still apply, including the
separate race5-py-kit (and a declared RACE5_PY_KIT_DIR) used by Python.

### Caches, scoring and audit limits

Each arm receives private, writable repository-local caches copied from the kit:
Cargo, Go, Mix/Hex, Bun, XDG and npm. In sealed these are the only available
libraries; in real-workflow they may be extended with package installs.

Scoring and warm-up are offline in BOTH modes, using dead HTTP/HTTPS/ALL proxies
at `http://127.0.0.1:9`, `NO_PROXY=127.0.0.1,localhost` for the local fake and
Cargo, Go, Hex and npm offline switches. The exec wrapper reapplies these after
runner environment filtering. GOFLAGS and build-cache variables are removed
from the implementation environment; the deliverable must be prebuilt.
Every runtime dependency must be vendored, bundled or cached inside repository
content retained in snapshots, which include build output but exclude
`.kitcache/`. Runtime paths must not point back to the original arm or kit.

The audit records observed commands and web search events in
`out/network-<arm>.log`. Permitted real-workflow downloads/searches are logged;
sealed network/download/search actions and anti-cheating violations are voiding.
This is a static event-log audit, not packet capture. It cannot observe hidden
traffic inside arbitrary programs, reconstruct destinations reached by unknown
scripts or inspect the agent's own Codex model transport. On macOS scoring uses
proxies, UV_OFFLINE=1 and offline flags, not a kernel network deny.

The mode/brief/environment gates must pass before launch. Changing MODE requires
rerendering briefs and the decision rule and preparing fresh arms before freeze.
The supervisor package smoke `./smoke-race4.sh` is only applicable in real-workflow.
