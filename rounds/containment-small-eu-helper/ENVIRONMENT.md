# Environment and configuration

## Test scope

The measurement used one test server and one kernel, three repetitions, the same set of 11 small fixtures, and no language model. The results are specific to this host layout and these configurations. They do not measure macOS behavior.

The four reader-facing setups are No sandbox, Bubblewrap setup, Kogen helper (under qualification), and Kogen helper running bash. The last setup uses the unchanged bash workload only for the helper's dynamic-tool availability check. The containment comparison for the helper uses the static fixture launcher.

## Helper configuration

The helper used build cgfix4 with SHA-256 `5b61d5a713e981f81da11d076bf99aa1a0e7b3e343c5b38428e960569443569b`. It ran under qualification admission, with no production admission record. The helper reported a seeded workspace-quota capability because each cell seeds the allowed-work input; that capability was not independently qualified. These observations do not represent a production-admitted helper configuration.

The helper's fixture and launcher were granted read-only access to their fixture files and four writable, per-cell directories on a dedicated tmpfs, owned with mode 0700. HOME was inside the helper's writable home directory. Its configured environment did not include the secret value. The deployment tree was also protected by the helper configuration.

The helper's memory and process caps matched the comparison's headline caps: 256 MiB of memory and 64 tasks. Its memory reservation was applied while keeping the effective cap at the scorer's limit. The helper meters the candidate process cgroup; its client and helper run outside it. The helper disables swap and groups out-of-memory kills.

The helper has additional wall, CPU, reaction, grace and cleanup settings with no Bubblewrap counterpart. The relevant configured limits include 60 seconds each for wall and CPU, a 1000 ms reaction period, a 200 ms grace period, a 1600 ms cleanup period, 64 MiB of disk storage, 4096 files, and output limits of 256 KiB, 256 KiB and 1 MiB. The helper's final resource read must complete before the helper removes the candidate cgroup.

## Bubblewrap setup configuration

Bubblewrap setup ran inside a systemd scope; the reported resource enforcement includes those systemd limits. The scope meters its launcher processes as well as the candidate. The setup had read-only system and library roots, proc and device views, a different HOME, and one writable disk directory with mode 0777. It did not configure the helper's swap or OOM-group settings.

## No sandbox control

No sandbox used process custody without filesystem or network sandboxing. Its scope had no memory, task, or CPU cap. Its resource cells are UNSUPPORTED because no resource-control mechanism was configured. The allowed-work positive control succeeded in all three repetitions.

## Why the configurations are not equivalent

The helper and Bubblewrap setup differ in filesystem grants, HOME, writable permissions and storage type, metered processes, swap and OOM settings, helper-only timeouts and storage/output budgets, and resource observation and final-read mechanisms. The helper has four 0700 tmpfs folders, while Bubblewrap setup has one writable disk directory with mode 0777. The helper meters only the candidate; the Bubblewrap systemd scope also meters its launcher.

The resource observation paths also differ. A targeted helper watcher can observe the candidate under a different schedule and must obtain a final sample before cgroup removal. Bubblewrap setup uses the ordinary observation loop and a holder-protected final read. Its resource evidence is not directly interchangeable with the helper's. Equal headline memory and process caps do not make the environments equivalent.

The absence of the environment secret for Bubblewrap setup and the helper reflects their configured allowlists. It does not by itself establish a general secret-filtering property.

## Limits stated with the result

1. **Final-read order.** The helper's final resource sample requires `populated=0`, then counters, then `populated=0` again on the same cgroup directory. If the candidate cgroup disappears before that complete sequence, the result is INVALID.
2. **Unequal observation opportunity.** The helper uses a targeted 2 ms watcher, which can also establish fixture visibility from a verified fixture row. Bubblewrap setup uses the ordinary observation loop and a holder-protected final read. The helper must finish its final read before removing the candidate cgroup; Bubblewrap setup keeps its scope alive. Invalid rates therefore are not comparable.
3. **Unmarked apparatus.** The helper, client, custodian and guardian have no independent marker. Cleanup assurance depends on that apparatus remaining inside the custody scope. Bubblewrap setup's marked launcher provides another attribution path.
4. **Static fixture.** The containment comparison uses the static fixture launcher, not bash. It does not exercise dynamic loading, bash-added environment variables, or the fixture's external sleep child. The unchanged bash workload was checked separately for launch availability. Its three LAUNCH-FAILED outcomes are not containment successes.
5. **Different filesystem grants.** The helper receives read-only fixture files and four writable per-cell tmpfs roots, mode 0700, with HOME inside one root and the deployment tree protected. Bubblewrap setup receives read-only system/library, proc and device views, one writable disk directory with mode 0777, and a different HOME. These are configured policies, not equivalent tool environments.
6. **Different resource budgets despite equal headline caps.** Both configurations use 256 MiB memory and 64 tasks. The helper meters only the candidate cgroup; its helper and client run outside it. Bubblewrap setup's systemd scope also meters its launcher. The helper configures swap off and grouped OOM kills; Bubblewrap setup configures neither, and the harness reads neither setting. A helper reservation adjustment leaves the effective memory and task caps at the headline values.
7. **Helper-only timeouts.** The helper has 60 second wall and CPU limits, a 1000 ms reaction period, 200 ms grace, 1600 ms cleanup, a 2000 ms overrun limit, 64 MiB storage, 4096 files, and output limits of 256 KiB, 256 KiB, and 1 MiB. Bubblewrap setup has no corresponding helper settings. The reaction, grace and cleanup settings govern the helper’s owner-loss teardown. A termination-resistant survivor still present at the 200 ms scoring point scores NOT-BLOCKED even if the helper kills it later. Bubblewrap setup uses a different runner-death teardown mechanism. CPU pressure was not tested, and equal CPU percentages would not establish equal bandwidth periods.
8. **Overhead boundary.** The helper's launch latency measures the complete configured path: delegation, two inspections, identity and configuration generation, harness client startup, protocol session, and helper start. The interval runs from immediately before `Popen` through the waiter-thread `waitpid` completion. It does not isolate helper cost or time until a useful tool is ready; teardown is measured separately.
9. **Qualification and reported capability.** Build cgfix4 with SHA-256 `5b61d5a713e981f81da11d076bf99aa1a0e7b3e343c5b38428e960569443569b` ran in qualification admission mode with no production admission record. The helper reported a seeded workspace-quota capability because each cell seeds the allowed-work input; that capability was not independently qualified. Production admission would refuse this seeded capability. Production readiness is not implied.
10. **Exact measured binary.** The measured helper was cgfix4, pinned above. The earlier helper binary with SHA-256 `3680c06680b29dbfee00e4a348fdd6457265451b66834410dba11b7acdb3a326` cannot start any candidate because its bootstrap root bind returns EINVAL. That earlier binary was not measured and is excluded from these results.
11. **Launch-failure rule.** LAUNCH-FAILED requires affirmative helper evidence of `start-failed`. An observer miss without that evidence remains INVALID.
12. **Coverage limits.** The fake-backed harness tests model observer and cgroup behavior. The live qualification check's escape cells exercise the No sandbox path; helper escape fixtures are observed in this measurement, and earlier rehearsal cells are excluded. Delegation, setup, preflight and the static fixture were exercised live only through Linux qualification or measurement, which does not qualify future hosts. The compact evidence cannot independently prove raw counter or final-read correctness. No transcript or event stream is published.
13. **Incomplete preflight.** Preflight checks pins, tmpfs presence and emptiness, and the AppArmor profile file at check time. It records the user-namespace sysctl but does not enforce it, does not verify loaded policy or tmpfs mount options, and is not rerun at measurement time.
14. **Interruption scope.** The helper's interruption qualification exercised the No sandbox path; helper interruption behavior was not qualified.

## Other assurance boundaries

Survivors were checked 200 ms after SIGKILL of the selected runner. These are runner-death observations, not explicit scope-stop results. Environment-secret absence reflects the configured allowlists. Fixture output is diagnostic; observer evidence determines scores. Invalid cells are not passes or failures.

This comparison used one test server, one kernel, and three repetitions. It does not measure macOS, include the nono setup, or establish general security or production readiness for any mechanism. An earlier rehearsal and dry cells on a second machine are excluded; one dry cell ran while a lock on that machine was breached. That machine's cells are not part of the result.
