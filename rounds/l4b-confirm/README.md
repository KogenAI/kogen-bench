# L4b independent context-packet replication

Round date: HISTORICAL (before 2026-10-09)
Publication badge: VALID; KEPT FOR AUDIT
Recomputation status: FULLY RECOMPUTABLE


## Status

**VALID**

### Limits
- Restored to VALID 2026-10-08: the round executed its registered rule as registered and its numbers recompute; the points below are limits on public evidence, not contradictions in the round's own files.
- **RELEASE_EVIDENCE_MISSING:** Standard run records and strict-validation receipts are unavailable, so execution checklist compliance cannot be established.


STATUS: **VALID** — US part complete

Pre-registered: yes; design frozen 7 October 2026 before any scored cell. The published design is a sanitized copy; original-source SHA-256: `94d0158342fd83188e5a49d3aed538bda401cd96f5335b2992a24e5342634ebc`; published-byte SHA-256: `7b6bd259e4dcf0229f1d4840daaed75fbee27722f916cec3fcc5ac9743f8dc7f`.
Label: DESCRIPTIVE — the 18 US outcomes are reported from official grades; Standard run records and smoke/strict-validation receipts are unavailable in the public snapshot, so strict release compliance is not established.
Question: On three L1-admitted variants unused by L4, does a frozen public-only context packet improve official full-suite results versus a contemporaneous no-packet control?
n: 18 scored US cells (3 variants × 2 arms × 3 paired seeds); all 18 officially graded.
Headline: NOT CONFIRMED: packet 6/9 vs control 6/9; Σ(P−C)=0 (pre-registered threshold: +2); 2 paired rescues and 2 paired losses.
Configuration: direct Codex, `gpt-6-luna` at `max`; worker Codex CLI `0.160.0`; packet-author Codex CLI `0.161.0`; Python `3.14.7`; 3,600-second timeout; zero retries; sequential on `kogen-bench-us`; official route `r70-macbook-window-v1`. Launcher code SHA-256: `d4d181af6ddb8cfa2bb6efe6f73b2ed8de533d1a21340270c864ae7483af25cb`. Token total is uncached input + cached input + output.
Limit: n=3 per arm per variant, one model and one host. A dated pre-outcome preparation receipt recorded ceiling risk from high Luna-max baselines; contemporaneous controls passed 6/9. L4's KEEP came from low-baseline variants. This result is no-confirmation, not evidence against the packet; it does not establish an effect outside these variants and seeds.

## Release evidence disclosure

The public snapshot has no Standard 1.2 run record for any of the 18 cell IDs, no strict-validation output for the seven-cell smoke prefix before the remaining eleven were released, and no strict-validation output for all 18 cells before analysis. The published outcome table and operator-reported grade chronology do not replace these records. The round is published descriptively; strict checklist completion is not established. See [MEASURED.md](MEASURED.md) for the exact evidence gap and [READY.md](READY.md) for the execution record.

### US cohort accounting

| Population | Count |
| --- | ---: |
| Planned scored cells | 18 |
| Started scored cells | 18 |
| Finished cells | 18 |
| Officially graded cells | 18 |
| ITT denominator | 18 |

Sources: [frozen design](DESIGN.md), [pre-registered decision rule](DECISION-RULE.md), [US results](RESULTS.md), [release and execution record](READY.md), [sanitized cell data](data/cells.csv), [frozen order](reproduce/ORDER.json), and [reproducer](reproduce/reproduce_us.py).

## Reproduce

### Source and packet commits

| Source task | Source base commit | Packet task | Packet child commit |
| --- | --- | --- | --- |
| `r70-4-go-fe2` | [21d21a2f420a387c921f998e5b4d16efc8f80904](https://github.com/KogenAI/kogen-ex/commit/21d21a2f420a387c921f998e5b4d16efc8f80904) | `r70-4-go-fe2-l4pk` | [7401a896ef458cd71830dc4d2677ad69e7f4561b](https://github.com/KogenAI/kogen-ex/commit/7401a896ef458cd71830dc4d2677ad69e7f4561b) |
| `r70-4-ts-bun-fe2` | [cc3a831a167020538c4ca2ad90185606a2e4ad6a](https://github.com/KogenAI/kogen-ex/commit/cc3a831a167020538c4ca2ad90185606a2e4ad6a) | `r70-4-ts-bun-fe2-l4pk` | [30c1860e763742c85a20af189bf397a1b726f8b6](https://github.com/KogenAI/kogen-ex/commit/30c1860e763742c85a20af189bf397a1b726f8b6) |
| `r70-5-go` | [e0b4a2478a17a924fcecb965b2941ca3396f49d6](https://github.com/KogenAI/kogen-ex/commit/e0b4a2478a17a924fcecb965b2941ca3396f49d6) | `r70-5-go-l4pk` | [a763145f30890271c8cba0bd5bc048b330cb280b](https://github.com/KogenAI/kogen-ex/commit/a763145f30890271c8cba0bd5bc048b330cb280b) |

The operator created the three signed empty child commits; each packet task used the matching source tree and appended its frozen packet. Packet SHA-256 values and public-source hashes are in [PACKETS.json](reproduce/PACKETS.json).

### Harness, tasks, commands, and data

Tasks: `r70-4-go-fe2`, `r70-4-go-fe2-l4pk`, `r70-4-ts-bun-fe2`, `r70-4-ts-bun-fe2-l4pk`, `r70-5-go`, and `r70-5-go-l4pk`. Seeds 1–3 map to reps 61–63. The exact randomized order and cell IDs are preserved in `reproduce/ORDER.json` and reproduced with the outcomes in [RESULTS.md](RESULTS.md).

The worker used Codex CLI `0.160.0`; packet authorship used Codex CLI `0.161.0`; Python was `3.14.7`. The lane dispatcher code is identified by the SHA-256 above. Official grades came through `r70-macbook-window-v1`. The public cell table contains only cell IDs, outcomes, test counts, arm metadata, and token counters.

Kogen commit: the source and packet child commits are linked above; `21d21a2f420a387c921f998e5b4d16efc8f80904` and `7401a896ef458cd71830dc4d2677ad69e7f4561b` are one linked pair.
Harness commit: not recorded; the lane dispatcher code SHA-256 is recorded above.
Model and effort: `gpt-6-luna` at `max`.
Task IDs: `r70-4-go-fe2`, `r70-4-go-fe2-l4pk`, `r70-4-ts-bun-fe2`, `r70-4-ts-bun-fe2-l4pk`, `r70-5-go`, `r70-5-go-l4pk`.
Historical execution command: the operator ran the two exact batch commands below on `kogen-bench-us`.
Raw records: sanitized official cell data in `data/cells.csv`; frozen IDs and execution order in `reproduce/ORDER.json`.

Operator batch entrypoints on `kogen-bench-us`, run in the frozen order:

```sh
python3 levers/lanes-2026-10-07/l4b/dispatch.py run --batch first
python3 levers/lanes-2026-10-07/l4b/dispatch.py run --batch rest
```

Recompute the public results and validate the SOT repository from its root:

```sh
python3 rounds/l4b-confirm/reproduce/reproduce_us.py
python3 reproduce/validate_repo.py
```

Inputs: `rounds/l4b-confirm/data/cells.csv`, `rounds/l4b-confirm/reproduce/ORDER.json`, `rounds/l4b-confirm/DESIGN.md`, and `rounds/l4b-confirm/DECISION-RULE.md`. The reproducer uses only the Python standard library, checks the frozen inputs and every cell's accounting, then verifies the generated tables and headline.

### Process notes and interpretation

- The task metadata repository path was corrected before deployment.
- The seven-cell smoke prefix stalled for about 25 minutes at the US disk floor. This delayed the run; the prefix was officially graded before the remaining eleven cells were released. Public Standard run records and strict-validation receipts are unavailable, so checklist completion is not verifiable from this snapshot.
- L4's KEEP came from low-baseline variants. Here the controls passed 6/9, consistent with the ceiling-risk concern recorded before scored cells in the [dated preparation receipt](reproduce/CEILING-RISK-RECEIPT.md). The 0 net pass difference does not confirm a packet advantage and is not evidence against the packet.
- Per-variant mean `tests_passed` was equal between arms. The small cohort cannot support a general claim beyond these three variants, one model, one host, and three paired seeds per variant.
- The EU extension, `l4b-confirm-eu`, is **NOT-RUN**. Only task 7 was admitted, its baseline was 5/6, and no cells were spent. The completed 18-cell US cohort is separate; there is no EU scored result.
