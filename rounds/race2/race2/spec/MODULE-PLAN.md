# Full CORE ownership plan

This is the implementation split for the full Quint specification, not a claim that step 0 completes those models.
The existing ten files remain unchanged. New module writers share [kogen_io.qnt](quint/kogen_io.qnt) and the
[trace contract](QUINT-SUITE.md). Only IO is implemented here; all elements named below are work assignments.

Each ID below identifies one source occurrence or a tightly related group of clauses in CORE §§1–9, with a short
quote for lookup. **The Owner column is exclusive.** Repeated statements in CORE get distinct IDs; consumers import
the owner's definitions and do not duplicate its oracle. `cli.qnt` owns every §3 invocation/option/output/exit clause;
its effects delegate to lifecycle modules. `status.qnt` owns projection from durable state, while CLI owns rendering,
JSON key sets and watch behavior specified in §3. Git owns physical publication, landing owns integration policy.

Notation: S=state/type, A=action/setup step, I=invariant/guard, O=pure output/exit function. All CLI effects set
`lastStep'=[Cli({cmd,expect}), ...]`; environment effects emit Setup. Hashes are abstract byte/tree identities with
capture/reuse constraints on concrete hashes, never unconstrained symbols that let two unequal trees compare equal.

## §1 Purpose and scope

| ID / short quote | Owner | Required element |
|---|---|---|
| 1.platform “Rust, single-binary … macOS and Linux” | kogen.qnt | S supported hosts; O distribution metadata and executable-only runner capability obligation. Language/build provenance is external artifact review (R1 below). |
| 1.pipeline “shapes … waits … bounded Build … exact candidate … only verified” | kogen.qnt | A composed pipeline; I approved-before-build, serial, exact receipt before publication. |
| 1.chatgpt “first core uses ChatGPT only” | kogen.qnt | S provider domain; I no fallback. |
| 1.command-status “statuses … §3” | cli.qnt | O implemented/reserved command table referencing 3.tree. |
| 1.recipe “reuse … lifecycle mechanisms … plain-data recipe” | kogen.qnt | S recipe/stages as data; I no experiment eligibility inputs. Reuse provenance is R1, not a runtime oracle. |
| 1.goal “cheap models … quality … not a performance guarantee” | kogen.qnt | I no claimed success/performance guarantee; declared non-guarantee, with qualitative goal R2. |

## §2 Terms

| ID / short quote | Owner | Required element |
|---|---|---|
| 2.intent “verbatim request … requirements and acceptance … one Build” | intent.qnt | S raw request/shaped fields and bounded Build linkage. |
| 2.shaper “own ChatGPT-backed role … cannot approve” | shape.qnt | S role; I actor cannot authorize. |
| 2.approval “exact … bytes … invalidates” | approve.qnt | S bound identities; I exactApproval, including acceptance presence/absence. |
| 2.build “bounded, isolated … one … at a time” | build.qnt | S attempt/private workspace; I isolation and active count ≤1. |
| 2.candidate “exact workspace tree … unverified” | check.qnt | S candidate/receipt tree ids; I unverified until complete green evidence. |
| 2.gate “deterministic command or approved acceptance … recorded” | check.qnt | S check kind, configuration identity, evidence, candidate tree. |
| 2.landing “one ordinary Git commit” | git.qnt | A hooked ordinary commit; O commit observations. |
| 2.reserved “name and behavior do not change” | cli.qnt | O frozen reserved command behavior. |

## §3 CLI (all owned by cli.qnt)

| ID / short quote | Owner | Required element |
|---|---|---|
| 3.tree “command tree … contract” | cli.qnt | S complete grammar and implemented/reserved table; O help; A every route and invalid route, including bare invocation. |
| 3.init “create … ignore … one commit … valid … no-op” | cli.qnt | A argv `[init]`; O success/no-op/config-invalid/environment exits and text; Git/file expectations delegated to init. Outside-Git exact wording remains OPEN. |
| 3.update “reserved” | cli.qnt | A `[update]`; O fixed reserved route status with no project mutation; no fabricated update operation. |
| 3.status.args “status [slug] [--watch] [--json]” | cli.qnt | A combinations/unknown slug/inspection errors; O text default and JSON/watch incompatibility. |
| 3.status.board “every non-Landed … at most five … groups” | cli.qnt | O board group/order/retention, including Building/Queued/Blocked/Failed/Parked/Interrupted/Drafts/Landed. |
| 3.status.row “reason and latest Build … Landed … SHA” | cli.qnt | O wait/failure reason, latest Build ID/status in every category, landed SHA. |
| 3.status.recovery “locations and expiry … detail … stage times … diff … journal” | cli.qnt | O text overview/detail and preserved-unverified locations; named paths/captures. |
| 3.status.queue-json “schema:1,type:queue … state,pid,queued,next” | cli.qnt | O exact queue JSON row and first-row placement. |
| 3.status.intent-json “board order … slug,status,queue_position … recovery” | cli.qnt | O exact intent row keys: slug/status/queue_position/reason/build_id/build_status/stage/elapsed_ms/landed_sha/priority/blocks_on/journal/candidate_diff/recovery; lowercase status domain. |
| 3.status.agent-json “then … type:agent … id,role,build … events” | cli.qnt | O exact agent row keys id/role/build/status/elapsed_ms/activity/events, following Intents. |
| 3.status.nulls “Missing … null … 1-based … recovery array” | cli.qnt | O null vs absence, queue positions, recovery location/expiry/expired arrays. |
| 3.status.stage “latest nonempty … model_stage … rung_started … only Building” | cli.qnt | O event filtering/last recognized stage; no unrelated, terminal or reapproved-queue stage. |
| 3.status.detail-json “one detailed object … intent_detail” | cli.qnt | O schema/type, detail including recovery; one JSON object. Extra detail keys outside the stated contract need a documented schema decision, not guessed exact values. |
| 3.status.watch “immediately … 2 seconds … changed frames … return” | cli.qnt | A background watch/readiness/time/queue stop; O immediate frame, changed-only frames and stopped+no Build/agent termination. |
| 3.status.exit “overview 0 … Landed 0 … otherwise 1 … unknown 2” | cli.qnt | O statusExit and inspection failure mapping; ordinary successful inspection 0. |
| 3.shape “file or stdin … never … argv … block … questions” | cli.qnt | A exact argv/stdin/file transport and blocking script; O paths/warnings/approval command/result. |
| 3.shape.json “--json … result and usage … rejected [planned]” | cli.qnt | O normative JSON result/usage and CLI option; explicit known-gap witness for present rejection, not an alternative allowed behavior. |
| 3.approve.review “Without a hash … review card … status 5” | cli.qnt | O card/hash/exact approval command and exit 5. |
| 3.approve.prefix “≥6 hex … matching … --by … no queue” | cli.qnt | A optional hash and identity; O invalid/short/mismatch exits, successful caller record and queue unchanged. |
| 3.remove “files and approval … one commit … running … --force” | cli.qnt | A remove/force and invalid running removal; I required force categories; Git expectations. Known-gap separate post-commit approval CAS is a conformance failure. |
| 3.queue.foreground “explicit … serially … empty or stopped” | cli.qnt | A foreground start with Build/check/land effects; O exit/output; does not imply approval. |
| 3.queue.detach “background” | cli.qnt | A `[queue,start,--detach]`; O launcher result, queue PID/liveness via status and no second active Build. |
| 3.queue.stop “after its current Build” | cli.qnt | A stop; O acknowledgement/state and current Build allowed to finish. |
| 3.provider.list “saved … signed in … default” | cli.qnt | S machine-local accounts; O list fields/default. |
| 3.provider.login “chatgpt … --as … default” | cli.qnt | A login via fake OpenID; O success/error, label default and named-account isolation. |
| 3.provider.logout “only … selected … default” | cli.qnt | A logout; O selected credential removal, other accounts retained. |
| 3.provider.use “default … project … accounts.yaml … never repo” | cli.qnt | A use/--as/--project; O choice and machine-file effects; account-selection helper. |
| 3.version “commit … date” | cli.qnt | O version shape and typed capture/reuse of binary metadata. |
| 3.help “help [command [subcommand]] … commands … options” | cli.qnt | O complete top/nested help and subcommand/option listing; known-gap nested rejection remains visible. |
| 3.forms “fixed … no model/effort flags … Build” | cli.qnt | S argv grammar; O vocabulary; I reject undeclared options/content forms. |
| 3.exits “0,1,2,3,4,5,70,143 … extra 130” | cli.qnt | O every class and code, with no/mismatch/red, environment/provider/bug/decision and SIGTERM witnesses. SIGINT=130 is separately recorded divergence, not added to allowed set. |

## §4 Lifecycle

| ID / short quote | Owner | Required element |
|---|---|---|
| 4.1.schema “strict-subset YAML … preflight” | config.qnt | S finite syntax witnesses; O validation result; I reject duplicate/unknown keys at all levels. |
| 4.1.required “name … string … checks … list … empty” | config.qnt | S schema; O type/missing-field validation. |
| 4.1.check-schema “unique … non-empty argv … positive … timeout_ms” | config.qnt | I per-check validation, string vector rather than shell string. |
| 4.1.optional “accepted only when core code reads them” | config.qnt | S frozen supported optional-key registry from read-only core; O reject all others, including credential/account config. |
| 4.1.bare “name: project … checks: [] … valid no-op … invalid error” | init.qnt | A initialize/reinitialize; I no writes/commit for existing valid config and no successful init for invalid config. |
| 4.1.ignore “preserves … final effective rules … never ignores .kogen/” | init.qnt | A append effective local-only ignore, preserve existing bytes/rules; O file/ignored-path observations. |
| 4.1.home “Credentials and workspaces … home” | build.qnt | S workspace root and no repo credential storage; I separation. |
| 4.1.stage “stages exactly … both … one commit … no discovery” | init.qnt | I exactly two allowed tracked changes and one commit; A user Git hook path through git owner. |
| 4.1.warning “AGENTS.md … CLAUDE.md … not banned” | init.qnt | O warning and retained agent files; no instructions from these files. Missing warning is a named known-gap witness. |
| 4.1.subject “Initial commit … Initialize Kogen project” | init.qnt | O initSubject(hasHistory), including unborn baseline. |
| 4.2.role “own Shaper … ChatGPT … file/stdin” | shape.qnt | S role/input; A provider request with preserved request bytes, no argv content. |
| 4.2.branches “resolves UX/DX … technical choices … result or questions” | shape.qnt | S branch classification/result/question variants; I remaining branches technical only; finite fixtures, qualitative adequacy R2. |
| 4.2.experiments “shaping … core … audits … effort … later … no success guarantee” | shape.qnt | I no optional experiment in required shape outcome; declare non-guarantee. |
| 4.2.criteria “sufficient … check … never approves … not instructions” | shape.qnt | I nonempty acceptance/verify, no approval actor and agent-file instruction source absent; semantic sufficiency R2. |
| 4.2.detect “Cargo.toml … mix.exs … criteria-only” | shape.qnt | O adapter detection with root marker precedence. |
| 4.2.override “explicit exunit … only … mix.exs … other explicit” | shape.qnt | O explicit override/detection and absent-Elixir tool invocation guards. |
| 4.2.cargo-source “one Rust integration test … local/acceptance/slug.rs … acceptance_a<n>” | shape.qnt | A source generation; S acceptance-id→named test relation; O exact named paths/source hash. |
| 4.2.cargo-base “temporarily … tests/slug.rs … cargo test --offline … json … --locked” | shape.qnt | A temporary stage/base validation and cleanup; O exact command fixture observations, locked iff existing lockfile. |
| 4.2.public-api “ordinary … public API … no runtime probes/rlibs/build tricks” | shape.qnt | I source/command fixture restrictions and role request; qualitative arbitrary-source proof R2. |
| 4.2.base-red “every primary … E0425/E0432/E0433 … staged test … other errors” | shape.qnt | O narrow expected-base-red classification through check's evidence parser; environmental/incomplete cannot reclassify red. |
| 4.2.private-target “run/reports/cargo-target … same … sandbox … outside tree” | process.qnt | S private writable target/env; I Cargo artifact separation on both hosts, for acceptance/configured checks. |
| 4.2.cargo-cleanup “generated lockfile … removed … Cargo.toml never edited” | shape.qnt | A cleanup; I preserve original manifest/lockfile identity. |
| 4.2.package “approval copies … immutable … matching ledger … warnings local” | approve.qnt | A local→tracked approved acceptance/ledger package; I immutable byte binding, no warning-file promotion. |
| 4.2.install “Build installs only … candidate copy” | build.qnt | A protected acceptance installation in private candidate, not origin. |
| 4.2.scratch “local/intents/slug … ledgers/warnings … ignored” | shape.qnt | S named scratch paths; O exact local files and exclusion from tracked paths. |
| 4.2.criteria-only “Acceptance/Verify … no source … reports once” | shape.qnt | A criteria-only shape; O once-only no-runner warning; I no generated/executed source. |
| 4.2.criteria-checks “Approval and gate … at least one … check” | approve.qnt | I approval guard requires configured check; check owns distinct gate verification guard in 4.5.criteria. |
| 4.3.separate “separate caller … before queue … identity … Shaper cannot” | approve.qnt | S authorizing identity; A explicit caller authorization, queue remains stopped. |
| 4.3.bytes “exact Intent … acceptance … criteria-only … change … again” | approve.qnt | I raw-byte/presence exactApproval; A invalidation and reapproval, no acceptance path for criteria-only. |
| 4.4.workspace “queue start … isolated … home … checkout … any project” | build.qnt | A workspace start; I origin/workspace disjoint and no project-type requirement. |
| 4.4.transport “Content … not … command-line” | process.qnt | I content via stdin/file channels, argv metadata only; observed executable fixtures. |
| 4.4.controls “one Builder … no parallel/ladder/escalation/plan/auditor … cache” | build.qnt | S single role; I absent core-control dimensions and no additional automatic repair attempts. |
| 4.4.overload “same … model … bounded request budget” | build.qnt | S attempts/request budget; A scripted overload retries; I model stays fixed and stop at bound. |
| 4.4.fix “fix its own … within … single bounded Build” | build.qnt | A in-Build check feedback/edit with same Build id/deadline. |
| 4.4.conflict “resolve its own rebase conflict … bounded parts” | landing.qnt | A same-Builder integration repair within original budget and turn count. |
| 4.4.protected “candidate … not approved Intent or acceptance” | build.qnt | I protected raw-byte identities through every provider/tool edit. |
| 4.4.deadline “one monotonic … 60 … budget_ms/wall_minutes … through landing” | process.qnt | S absolute Build start/deadline; I one allowance, expiry blocks every later stage/publication; precedence/default resolution from config. |
| 4.4.caps “Builder 30 … generic 120 … acceptance 600 … checks explicit” | process.qnt | S stage/child caps; O effective clipped timeouts, exact default units. |
| 4.4.clip “requests/retry waits/children … remaining … no fresh allowance” | process.qnt | O min of absolute remaining Build/stage/config timeout; I no time resurrection on rebase/landing. |
| 4.4.kill “TERM … group … KILL … bounded grace … only ESRCH” | process.qnt | A cleanup TERM/grace/KILL/probe; S present/absent/unknown; I uncertainty blocks landing. |
| 4.4.reap “bounded reaping/readers … open pipe/leader … log so far” | process.qnt | A bounded return even escaped pipe holder; I unconfirmed status and persisted partial logs. |
| 4.4.parent “durable … custody … registration … retained” | process.qnt | A parent death and watcher result; I ownership retained on unconfirmed cleanup. |
| 4.4.groups “boundary … escaped … unsupported/denied … blocked” | process.qnt | S Unix capabilities and escape/probe outcomes; I actual boundary, no false claim escaped descendants signalled. |
| 4.4.logs “16 KiB tail … 10 MiB … log_limit_bytes … rolling … drain order” | process.qnt | S bounded tail/full log and ordered chunks; A incremental append/overflow; O truncated marker without killing child. |
| 4.4.memory “Linux … non-raisable … existing … close-on-exec … other … unenforced” | process.qnt | S optional memory_limit_bytes, host soft/hard minima and setup result; I non-raisable limits; O host report, none by default. |
| 4.5.exact “configured checks and acceptance … exact candidate … retain” | check.qnt | A controller checks; S immutable configuration/evidence/tree receipt; I Builder cannot alter checks. |
| 4.5.unavailable “missing/malformed/incomplete/zero … distinct … not failure” | check.qnt | S pass/red/could-not-check evidence; I unavailable blocks, cannot reclassify as code/test finding. |
| 4.5.exit101 “without … primary-span … or … summary … both base/candidate” | check.qnt | O command-specific parser cases, all base/candidate fixtures. |
| 4.5.red “known failing test … valid primary span” | check.qnt | O individually identified red evidence and raw compiler span validity. |
| 4.5.criteria “configured … non-blocking … no acceptance source … nothing unverified” | check.qnt | I criteria-only checks exist/complete/pass; A no executable acceptance; I receipt required. |
| 4.5.no-discovery “does not discover or adopt … init” | init.qnt | I no discovery/adoption action. |
| 4.5.dispatch “test/clippy/build/check/rustc … command-specific” | check.qnt | S supported parser dispatch; O generic classification otherwise. |
| 4.5.argv “one Cargo parser … globals/+toolchain … formats … -- … malformed blocks” | check.qnt | O parser and normalizer shared definition; exact configured/effective argv retained; never repair malformed args. |
| 4.5.json “json before -- … preserving … build-finished … no text-only” | check.qnt | O JSON option normalization/completion validation, literal after-separator bytes. |
| 4.5.tests “every summary/target … one collected … ignored/measured … exclude filtered” | check.qnt | S targets/counts/completion; I zero collection/unparsed/incomplete blocks. |
| 4.5.map “acceptance_a<n> … Acceptance ids” | check.qnt | O Cargo acceptance mapping through same Rust parser. |
| 4.5.identity “target and libtest … absent/ambiguous … log … completely” | check.qnt | S identity and log-completeness; I unavailable association/log blocks baseline excusing and green. |
| 4.5.clippy “Warnings … not … red” | check.qnt | O complete warning-only Clippy pass versus individually identified compiler findings. |
| 4.5.baseline “unidentified … red … cannot … excused … unavailable never” | check.qnt | S identified baseline findings; I no unidentified/unavailable excuse. |
| 4.5.pass “exit 0 and complete evidence” | check.qnt | I pass conjunction rather than exit-only for Rust commands. |
| 4.5.rustc “no completion … JSON … text compatibility … source … compilation” | check.qnt | O rustc diagnostics and actual successful compiling-process requirement; help/version/noncompile unavailable. |
| 4.5.finding “file/code/normalized message … source … omits line/column” | check.qnt | O conservative finding identity; I changed relocated-message findings not excused. |
| 4.5.generic “Other commands … generic exit-based” | check.qnt | O generic success/red/unavailable (e.g. timeout), no fabricated Rust parser application. |
| 4.5.project-suite “timing thresholds/static suites … may … configured” | check.qnt | S user configured checks; I no compulsory timing/static suite injected. |
| 4.6.integrate “moved base … before … lost CAS … rebase … rerun … exact tree” | landing.qnt | S expected/current base/tree; A integrate/repair/gate; I invalidate old receipt on tree change. |
| 4.6.turns “one repair … gate … four … all movements … park … stop” | landing.qnt | S shared integration-turn count; A park at exhausted cap, regardless of how base moved. |
| 4.6.stale “lost CAS removes … incoming … only after rebasing … same deadline” | landing.qnt | A stale-ref cleanup → fetch/rebase/gate; I no stale reuse/fresh allowance, calls git CAS primitives. |
| 4.6.recheck “immediately … tree … ordinary commit … identity/config” | git.qnt | A exact tree recheck then normal hooked commit with trusted settings; O commit tree/parents/identity. |
| 4.6.checkout “merge --ff-only … branch/index/worktree … edits/untracked” | git.qnt | A checked-out publication; I HEAD/index/worktree consistency, preserve nonconflicting user bytes. |
| 4.6.drafts “untracked Intent … legacy acceptance … identical bytes only” | git.qnt | A narrowly conditioned draft deletion; I mismatching local bytes preserved. |
| 4.6.detach “local changes … detach previous … CAS … tested recovery command” | git.qnt | A detach-before-CAS; I previous HEAD/index; O warning/stash tracked+untracked/switch command, replay that command. |
| 4.6.no-checkout “not checked out … CAS expected base” | git.qnt | A publication compare-and-swap success/loss with unrelated refs untouched. |
| 4.6.hooks “core.hooksPath/.git/hooks … fails … output … unchanged ref” | git.qnt | A user hooks selected by trusted origin config; I failure prevents publication; O captured feedback. |
| 4.6.safety “failed/missing/changed/lost … must not … landing” | landing.qnt | I no publication without current exact green receipt, deadline/custody and successful CAS. |
| 4.6.nonpromise “no parallel or crash-resume promise” | landing.qnt | I no parallel integration/resume transition; terminal failures do not manufacture continuation. |

## §§5–9 State, provider, commits, exclusions and open decisions

| ID / short quote | Owner | Required element |
|---|---|---|
| 5.layout “.kogen … config/Intent … local scratch … tree OPEN” | init.qnt | S required tracked/local path classes and ignore rules; O named paths only, remainder explicitly unspecified. |
| 5.init-files “init commits … credentials never … config” | config.qnt | I project credential/account fields forbidden; O tracked bare schema; init effects consumed from init owner. |
| 5.intent “with project … verbatim … serialization OPEN” | intent.qnt | S raw request identity and project ownership; unknown serialization unconstrained. |
| 5.status “enough … Intent/approval/Build/check/landing … status” | status.qnt | S durable outcomes/event projection; O board/detail facts, active-stage/recovery/agent projection consumed by cli. |
| 5.dead “dead Build … crashed/interrupted … unless … reachable” | recovery.qnt | A reconciliation; S recorded target/candidate/reachability; I preserve Landed when candidate reachable. |
| 5.preserve “changed unverified … hook-free … refs/kogen/candidates … archive fallback” | recovery.qnt | A compare unchanged/changed workspace, internal trusted-identity preservation, fallback on ref failure; O paths/hashes, no unnecessary unchanged preservation. |
| 5.retention “retention_days … default 14 … read first … persist expiry” | recovery.qnt | S creation/config snapshot/expiry; I later config changes cannot rewrite persisted expiry. |
| 5.expire “reconciliation/status … removes … journal … locations/expiry” | recovery.qnt | A clock advance/reconcile/delete ref/archive; O required lifecycle records; failed deletion retained for retry. |
| 5.unverified “cannot … approved/queued/landed/resumed … fresh … checks” | recovery.qnt | I preserved recovery never grants authorization/receipt; fresh Build path only. |
| 5.events “beyond required … OPEN” | status.qnt | S required event projection and unconstrained remainder; no invented exact journal schema. |
| 5.accounts “accounts.yaml … project precedence … never repo” | cli.qnt | S machine defaults/project mapping, selection precedence; I no secret/account choices in repo. |
| 5.workspaces “home/workspaces” | build.qnt | S absolute private root; I origin not a workspace. |
| 5.process “no resident daemon/VM … content … without argv” | process.qnt | S supervised process lifetime; I no permanent service/VM and content channel restriction (detached finite queue remains allowed). |
| 5.git-config “user's git configuration” | git.qnt | S trusted origin/global config; I all appropriate commit paths inherit settings. |
| 6.provider “ChatGPT only … own role … no fallback” | kogen.qnt | S role/provider wiring; I provider/role domains and no external shaper. |
| 6.route “backend Responses … account ID … ID token … injected same” | kogen.qnt | S endpoint/auth-mode/account identity; O fake request predicate for canonical route/default and override through IO. |
| 6.search “opt-in Shaper prototype … default off … first roadmap … Initial commit” | shape.qnt | S opt-in flag; I never eligibility input; O no hosted search by default and roadmap-first ordering, no current mandatory research guarantee. |
| 6.models “Builder luna maximum … Shaper sol high … one … no plan/ladder” | build.qnt | S role→model/effort table shared by shape; O provider request assertions and I no escalation/extra Builder. |
| 6.overload “retry … bounded … without changing model” | build.qnt | A overload replay; I same configured model and request budget exhaustion terminal. |
| 6.seam.execution “ordinary executable … temporary HOME … no bypass” | kogen_io.qnt | S Cmd/Setup/Expect/Seam; I interface transport; QUINT-SUITE imposes runner obligations. |
| 6.seam.endpoint “KOGEN_PROVIDER_URL … complete … HTTP(S)” | kogen_io.qnt | S abstract endpoint default/scripted/invalid; O env compilation contract. |
| 6.seam.auth “AUTH_PATH … JSON … exp … reread … no login … no 401 refresh” | kogen_io.qnt | S injected/invalid/no-auth fixtures and expiry; O documented fixture compilation. |
| 6.seam.store “CREDENTIAL_STORE=file … choices … home” | kogen_io.qnt | S credentialStore and named HOME fixture paths. |
| 6.seam.oidc “AUTH_URL … discovery … issuer … PATH shim … validation” | kogen_io.qnt | S script references/local endpoint; O OpenID fixture protocol without bypassing login. |
| 6.seam.scale “TIME_SCALE … positive finite … specific windows … not clock” | kogen_io.qnt | S positive permille subset, real WaitRealMs distinct from logical clock; I validSeam and no implicit scale of all timers. |
| 6.seam.clock “TEST_CLOCK_PATH … now_ms … reread … monotonic unchanged” | kogen_io.qnt | S optional wall clock; A AdvanceClock; O fixture file protocol, required gap G1. |
| 6.seam.barriers “TEST_BARRIER_DIR … three points … bound … no receipt/CAS forcing” | kogen_io.qnt | S optional barriers; A arm/await/release operations, typed ticket binding; required gaps G2/G3. |
| 7.trusted “origin … workspace cannot override … own identity/config” | git.qnt | S trusted settings separate from workspace overrides; I ordinary/internal commits use proper trusted identity/config. |
| 7.init “separate ordinary commit … subject … history” | git.qnt | A ordinary init hook path; O identity/hooks/subject using initSubject. |
| 7.signing “not required … configured signer only when … enables” | git.qnt | S signing-request policy input and trusted config resolution; I no forced signing. Observe stub signer invocation/config behavior through files, never commit signature presence (R3). |
| 7.hooks “user-visible … MUST … failure … nothing bypasses” | git.qnt | I every branch-history commit uses hooks, hook failure output available for Build repair; no bypass repair action. |
| 7.internal “refs/kogen … MAY skip … never pushed … temporary … disable” | git.qnt | S commit kind/hook phase; I internal-only skipped hooks, trusted identity/config, temporary hook phases off. |
| 7.message “one commit … normal subject … only Kogen-Intent … no AI” | git.qnt | O one parent/commit delta, nonempty subject and exact sole trailer; no added attribution. |
| 7.init-trailer “whether … init … OPEN” | git.qnt | S explicit unspecified policy; no mandatory yes/no oracle until owner resolves. |
| 8.controls “not first-core … alternatives/discovery/update/parallel/domains/resume/cache/harness/parity” | kogen.qnt | I no transitions/control inputs for excluded features; supported host obligations limited to stated target. |
| 8.prototypes “ladders/auditor/repair/cache/context/edge tests/audits/escalation/plan/retries/ranking … not … eligibility” | kogen.qnt | I only approval/exact checks/current base/deadline/custody/hooks eligibility; opt-in prototypes cannot alter it. Bounded in-Build self-fix and overload retries remain as §4/6 specify. |
| 8.reserved “only update … detach implemented” | cli.qnt | O reserved/implemented table, no contradictory detach reservation. |
| 8.later “discovery/release/distribution/crash-resume … no promises” | kogen.qnt | S explicit scope/non-guarantees, no success guarantee for absent mechanisms. |
| 9.scope “OPEN … do not widen cut” | kogen.qnt | I unknown decisions cannot authorize excluded behavior. |
| 9.process “OPEN — Process wrapper … guarantees/bounds” | process.qnt | S open refinements constrained by all existing §4.4 concrete bounds; never erase stated guarantees. |
| 9.crash “OPEN — Build crash … beyond preservation … no resume” | recovery.qnt | S open extra behavior; I preservation/expiry still required and no resumed Build transition. |
| 9.mapping “OPEN — Provider mapping … beyond specified … route” | kogen.qnt | S open mapping details constrained by canonical ChatGPT route, account identity and fixed roles/models. |

## What requires abstraction or external evidence

There are no unmodelable safety/lifecycle/CLI clauses. Finite scenarios can express byte identity, tree identity,
parser classes, JSON schema, Git races, process custody/deadlines, retention, hook effects and output/exit behavior.
Quint does not execute Git, HTTP, OS signals or Rust; the replay contract supplies these effects and compares its
observations, so external effects are **not** marked unexpressible.

| Review ID | Clauses | Genuine limit and treatment |
|---|---|---|
| R1 | 1.platform, 1.recipe | A transition language cannot establish implementation language, binary packaging or reuse ancestry by examining abstract state. Retain artifact/source-review obligations with executable/host capability metadata; verify behavioral consequences with traces. |
| R2 | 1.goal, 4.2.branches, 4.2.criteria, 4.2.public-api | Human quality, UX/DX adequacy and acceptance sufficiency for arbitrary natural-language tasks/source programs have no decidable oracle here. Model explicit requirement/branch ids and finite valid/invalid source fixtures; preserve the stated non-guarantees and require semantic review. Do not label an unconstrained bool as proof of quality. |
| R3 | 7.signing | The owner explicitly excludes signed-or-not from observations. Model trusted signing policy and test configured signer invocation/errors with a file-producing signer fixture; actual cryptographic signature verification is outside this observation interface, not a Quint safety limitation. |

OPEN paths, serialization/event formats, outside-Git exact diagnostics, init's optional trailer and unspecified
provider mapping remain explicit abstract/unspecified values. OPEN means no exact oracle is chosen; it does not
exempt their specified effects. The five recorded implementation annotations (shape JSON, nested help, init warning,
remove's split approval CAS, SIGINT 130) are named conformance gaps, never nondeterministic alternatives to the
normative contract. COVERAGE.md also mentions probe details not stated by CORE; do not promote them to new requirements.

## Relationship to existing COVERAGE IDs

COVERAGE is a grouped inventory, with composite rows and repeated clauses. The exclusive IDs above are the
module-writer ownership keys; this crosswalk ensures its existing rows are retained. An entry listing several IDs
splits that grouped row into those exclusive source clauses; it does not assign one clause multiple owners.

| Existing IDs | Ownership IDs above |
|---|---|
| 01–06 | 1.pipeline, 1.chatgpt, 1.command-status, 1.recipe, 1.goal |
| 07–14 | 2.intent, 2.shaper, 2.approval, 2.build, 2.candidate, 2.gate, 2.landing |
| 15–25 | 3.tree, 3.init, 3.shape, 3.shape.json, 3.approve.review/prefix, 3.queue.foreground/detach, all 3.status.*, 3.forms, 3.exits |
| 26–28 | all 4.1.* |
| 29–33 | all 4.2.* |
| 34–35 | all 4.3.* |
| 36–41 | all 4.4.* |
| 42–43 | all 4.5.*, 4.5.no-discovery |
| 44–47 | all 4.6.* |
| 48–54 | 5.layout/init-files/intent/status/dead/preserve/retention/expire/unverified/events/accounts/workspaces/process, 6.provider |
| 55–56 | 6.search/models/route/overload, 9.mapping |
| 57–60 | 7.trusted/init/signing/message/init-trailer |
| 61–65 | all 8.*, 5.init-files, 4.1.schema/required/check-schema/optional, 5.retention |
| 66, 68, 69 | 9.process/crash/mapping, 1.platform (COVERAGE has no row 67) |
| 70–79 | 7.hooks/internal, 3.update/remove/queue.stop/provider.list/provider.login/provider.logout/provider.use/version/help, 5.dead/preserve/expire/unverified |

## Delivery order and composition

1. IO is available now. Writers implement config's schema/domain fixtures; git's ref/tree/commit/checkout primitives;
   process's custody/deadline/log/memory model; and CLI's grammar/renderers/exit table against this common interface.
2. Extend intent/init/shape/approve/build/check/landing/queue/status/recovery with the state/actions/invariants/output
   assigned above, preserving existing abstract tests. Add reachable concrete fixture choices, initial setup,
   `ioSeam` and `lastStep` on every action. Check owns one Rust/Cargo evidence parser model consumed by shape.
   Approve owns approval binding consumed by queue/build; git owns CAS consumed by landing/recovery.
3. kogen imports these owner definitions and composes one state space and one step list. It owns cross-module
   invariants and role/provider wiring; it does not recopy each module's local transition relation. Include full
   end-to-end seeded witnesses, not just independently satisfiable unit abstractions. `status` inspection may first
   run recovery reconciliation, then project durable facts, then use cli's renderer/exit functions.
4. Implement the language-neutral runner and the two missing core seam controls independently. Generate/replay the
   QUINT-SUITE fast/full seed profiles, with one clause/witness manifest; report blocked seams and known divergences
   explicitly. The shared library alone is not conformance evidence.

Writers typecheck each modified file/import closure with the pinned CLI before handing off. Stage 0 adds no Rust
edits, commits, downloaded tools, live provider calls, or bench-host operations.
