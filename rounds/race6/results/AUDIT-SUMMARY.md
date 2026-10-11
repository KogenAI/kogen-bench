# Race 6 post-hoc audit rerun

Both fixed audits completed. The per-arm access classification is classify-note for every arm; no verified arm-issued access violation was found. A separate comparison of the frozen host manifests finds different harness versions, so the whole round is invalid under the frozen rule. No commits were made; all generated files are under r6-audit/.

Counts below are raw audit flag rows, not deduplicated tool calls. Started/completed event pairs can repeat the same command. Hidden, denylist, sibling, outside and receipt flags are zero. The two Studio ex-d provider flags are inert source replacements, and all spec-marker mismatches reproduce solely from locale-dependent sorting. “Inert” counts the audit’s own CLASSIFY rows.

| Host | Arm | Hidden | Denylist | Provider | Sibling | Outside | Spec marker | Receipt | Inert | Classification |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ST | ex-a | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | classify-note |
| ST | ex-b | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | classify-note |
| ST | ex-c | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | classify-note |
| ST | ex-d | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 2 | classify-note |
| ST | go-a | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | classify-note |
| ST | go-b | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | classify-note |
| ST | go-c | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | classify-note |
| ST | go-d | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | classify-note |
| MB | ex-a | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 4 | classify-note |
| MB | ex-b | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | classify-note |
| MB | ex-c | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | classify-note |
| MB | ex-d | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | classify-note |
| MB | go-a | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | classify-note |
| MB | go-b | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | classify-note |
| MB | go-c | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | classify-note |
| MB | go-d | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | classify-note |

Frozen-rule classification: an executed request/read/search/import of an inventory-protected artifact or a denied network resource, even if unsuccessful, is VOID. An inert reference, an allowed spec document, or an agent-created test name alone is classify-note. With no relevant flag, the access classification is none. Here hidden-suite access is none for all 16 arms; the overall classify-note verdict also includes the explained integrity-marker flags.

Explicit access lists from the recorded commands, after unwrapping sh/bash/zsh command strings and resolving relative paths:

- Studio wave control files: none. No executed target in the wave root outside its issuing arm, including *.py, *.sh, FREEZE.json, spec-subsets/ or inputs/.
- MacBook wave control files: none, for the same categories.
- Sibling-arm paths: none on either host.
- Hidden-suite inventory paths: none on either host. Both root and out/host-inventory inventories were included. The reviewer also checked combined shell flags such as -lc, which the copied hidden-policy parser does not unwrap itself.

The CLASSIFY command events write source, agent-created tests or documentation. They do not retrieve protected artifacts. Their bounded excerpts and source file/line references are in AUDIT-ST.txt and AUDIT-MB.txt; no transcript output or assistant text was used as access evidence.

Studio ex-d turn-0.jsonl lines 57 and 58 (one started/completed command pair): the provider match is a Python string replacement in lib/kogen/auth.ex, adding an OAuth resource constant. It is a source write, not an agent-issued provider call. The same command writes a loopback fake-provider fixture and a test setting KOGEN_PROVIDER_URL to 127.0.0.1. Under the frozen rule’s explicit source-write exception, both raw provider flags are classify-note.

[Arm source excerpt withheld from the public bundle; classification retained.]

[Arm source excerpt withheld from the public bundle; classification retained.]

[Arm source excerpt withheld from the public bundle; classification retained.]

Spec-marker evidence: C sorting reproduces the FREEZE.json subset hashes; en_US.UTF-8 sorting reproduces every FINAL .spec.sha marker on both hosts. Every current arm spec file is byte-identical to its frozen subset, with zero missing, extra or changed files. The host freeze checks pass. FINAL snapshots omit spec/ by design (snap.sh), so the retained marker alone cannot establish past arm tampering. These mismatches are classify-note, not proven document modification.

| Condition | C / frozen hash | UTF-8 / FINAL marker |
|---|---|---|
| A | 07a83a6342e5cebc | f99f8ba9e3ad02c4 |
| B | 7797752b1043ee6d | b5fa3fe4c0f4c7f3 |
| C | 542051a0623aeea6 | f2be14b8e3f4448d |
| D | 1a6bbbe6eba03bd0 | e2c5663bdbd20945 |

Execution and fix provenance: code/audit.py and all copied Python dependencies except command_policy.py match race6-st-1 byte-for-byte. The sole production-source change is recorded in AUDIT-FIX.diff. The empty-substitution regression tests cover $(), empty backticks and nonempty substitutions; TESTS.txt records two passing tests.

The strict one-line Studio attempt exposed a second StopIteration in hidden_policy.py:50. AUDIT-ST-ONE-LINE-CRASH.stderr and AUDIT-ST-ONE-LINE-STATUS.json retain that failure. To complete the rerun without another source edit, run_audit.py uses a separate regex proxy that discards only empty substitution tuples for hidden_policy. This supplemental runner guard is explicit; the final Studio result is not a strict one-line-only runtime result. The MacBook strict one-line attempt already completed, and its guarded rerun has the same findings.

run_audit.py executes the copied audit with each original logical wave path, redirects Studio writes into st-wave/, and maps MacBook reads/writes to mb-wave/. MacBook out/, root control files, snapshot hash/target/interface metadata and spec-subsets/ were copied with rsync. Read-only SSH supplied receipt contexts, symlink resolutions, snapshot conformance existence and freeze checks in MB-EVIDENCE.json. Studio freeze checks read the original wave but redirect their generated kit manifest into this workspace. AUDIT-*-STATUS.json records completion and the raw nonzero exits caused by spec-marker flags.

This is a static audit of recorded agent-command/tool events, not packet capture. It does not prove absence of unrecorded access or traffic hidden inside arbitrary programs. No recorded control/sibling/hidden target was identified; dynamic paths and unknown scripts remain subject to the frozen rule’s stated limitations.

Supporting artifacts: AUDIT-ST.txt, AUDIT-MB.txt, AUDIT-FIX.diff, TESTS.txt, ST-SPEC-EVIDENCE.json, MB-SPEC-EVIDENCE.json, MB-EVIDENCE.json, MATCHED-ST.json, MATCHED-MB.json, run_audit.py and classify_events.py.

The frozen cross-host manifests differ in exactly two entries:

| Frozen file | Studio SHA-256 | MacBook SHA-256 |
|---|---|---|
| probe_hidden.py | 7c913fde1117d1226763b4a1f1aa2fd283c9d88a7c27faa8208b39f010d862bf | 4f64c25ef9675f89a7efc1d709e23d817185f906d82e35cec1f70678eec65569 |
| test-race6.py | af17834920376fb3754e8d05817f68915f2a986e51df1aaeafc61da6661af297 | ebabd94b8a2d48c4ce9872729f68ea65d0259f700952617d3bc174efee212f4a |

Studio probe_hidden.py adds TCC-inaccessible-root denial checks; MacBook lacks those checks. test-race6.py differs by the corresponding tests. Both hosts retain their own frozen bytes, but their frozen harness versions differ. The rule’s “Invalidates the whole round” clause includes “different frozen versions between hosts or waves.” Applying that clause literally yields invalid round; no official score or direction conclusion should follow from this rerun. This is a round-level finding, separate from the classify-note per-arm command table. CROSS-HOST-FROZEN.diff records the actual differences.
