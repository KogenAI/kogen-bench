# Measurement harness

This no-model comparison used the same 11 small fixtures for three repetitions. The fixture set covers outside-file read and write attempts, secret-file access, environment-secret exposure, loopback networking, three survivor behaviors, memory and process caps, and an allowed-work positive control.

No sandbox was the negative control. Bubblewrap setup combined the configured bubblewrap policy with a systemd scope. Kogen helper (under qualification) used the pinned helper build and static fixture launcher. Kogen helper running bash used the unchanged bash workload only for launch availability.

The helper's containment results and its bash launch result are kept separate. The helper's static fixture was blocked on all eight escape and survivor checks in repetitions 0 and 1, with three enforced resource observations. Repetition 2 had an invalid positive control, which invalidated its dependent cells. A separate helper memory observation was invalid because the required final sample was missing. The unchanged bash workload failed to launch in all three attempts on the tested merged-/usr layout. LAUNCH-FAILED requires affirmative helper evidence of start-failed; an observer miss without that evidence remains INVALID.

The harness scored cells from observer evidence. Fixture output was diagnostic; invalid cells do not count as passes or failures. Resource cells require cap-level pressure, the corresponding rejection event, effective limits, and a complete final sample. A missing final sample remains INVALID even when earlier counters show pressure or kills.

The helper resource watcher and the Bubblewrap observation path have unequal opportunities. The helper watcher can establish fixture observation through its targeted process scan and must capture the final counters before the helper removes the cgroup. Bubblewrap setup uses the ordinary loop and holds the scope through a protected final read. These details limit direct comparisons and make invalid rates non-comparable. The helper uses a static fixture without dynamic loading, bash-added environment variables, or an external sleep child, so process and timing behavior also differ from the unchanged bash workload.

The public harness copy includes cmp.py, fx.c, fxa.c, test_cmp.py, and SHA256SUMS. Its privacy-edited files and the corresponding source files must each have their own published SHA-256 values:

| File | Source SHA-256 | Privacy-edited public SHA-256 |
|---|---|---|
| cmp.py | `2c7880783df03aadc89c4a2c7aea263f9b40e3895e631809e86b332316c89c37` | `4a5e278b86d9344b0315fdce6f18530df8b4f9632219a84f33d0dca3ef2288df` |
| fx.c | `50c80a5772b92440618a7979bc7b8816a8b946c42f9cf33122592f317838c29b` | `50c80a5772b92440618a7979bc7b8816a8b946c42f9cf33122592f317838c29b` |
| fxa.c | `5dbf539f2c847ea5a99e4f2074e25f10f9ecf10fc5458a1ec1ac0808c33a531a` | `5dbf539f2c847ea5a99e4f2074e25f10f9ecf10fc5458a1ec1ac0808c33a531a` |
| test_cmp.py | `6a0d04c7c295843c99bf9a89cdeb1ed750691bb00f66f3b3d1d4a7971ed98a48` | `2b169a8085516b704b4f6bf366fe66594d79bd0a8826d7e0b84d8a2b77cb7d84` |
| SHA256SUMS | Source digest unavailable through the safe reader | `0d8be957a9894e535a1315e2991ecba0f614dc720c38bb352f770af013cba2a8` |

`SOURCE-HASHES.tsv` records the same values. The source checksum manifest was processed only with the required safe reader, which reported eight line lengths and did not expose a whole-file digest. The public manifest was regenerated from the four public source files.

The privacy edits generalize the deployment root and per-run values; the scoring and observation logic is retained. The final harness review was GO. Earlier resume-status mapping and fail-closed observer issues were corrected in the reviewed source. The result review separately found the measurement publishable with the caveats stated in the round. The fake-backed harness tests model paths; live delegation, setup, preflight and fixture behavior were exercised only through Linux qualification or measurement, which does not qualify future hosts.

The environment-variable names belong to the helper's qualification interface.

The public copy is provided for inspection. It contains no measurement transcript, event stream or fixture output.
