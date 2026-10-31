# Wide same-key round (`confirm5-clean-route-8tasks`)

The driver and frozen protocol of the 32-run round in [`reproduce/confirm5-clean-route-8tasks/`](../../reproduce/confirm5-clean-route-8tasks/): eight Go tasks, loop `b8a4046` and Codex 0.165.0 at medium and high effort, one repetition, one OpenAI API key. It is the copy that ran, with the host paths turned into the variables listed in [`../confirm-eu/README.md`](../confirm-eu/README.md). The gateway, containment and cell mechanics are the same as in [`../confirm-eu/`](../confirm-eu/); this round changed the effort per cell and the budget handling.

| file | what it is |
|---|---|
| `prepare_wide.py` | builds the round directory from the high-effort round directory (`LANES_HIGH_ROUND_DIR`), copies the eight task kits from `LANES_PRIVATE` (the `specs` list names their folders; edit it to point at your own), derives this round's `confirmation_ext.py` from the high round's (effort taken from each cell, cap $7), qualifies every task (reference passes all expected ids, every wrong tree fails a requested test) and writes `eligibility.json` |
| `confirmation_ext.py` | the extension as it ran at the end of the round, with the effort and model-identity gates, no local request-size limit and the per-request spend reservation |
| `run_confirmation.py` | `preflight` (boundary probe for both tools), `counted` (all cells) and `cell --index N` (one cell, graded, after checking the earlier cells exist) |
| `protocol.json` | the frozen protocol: seed `2026102908`, task order, the 32 cells in their Williams order, policies and hashes of the original binaries and kits |
| `budget-censoring-policy.json` | the recorded policy for the Codex runs the spend-reservation guard stopped |
| `amend_positive_probe.py` | the recorded amendment of the positive workspace probe (`sh-globopts-go` has no `Makefile`) |
| `analyze_wide.py`, `finalize_wide.py` | the round analysis (per-arm tables and paired sign tests) and the credential cleanup and attestation step |

The frozen `protocol.json` carries the SHA-256 of the original kits, cache, binaries and sources in its `attestation`, and `cell` refuses to run if the live files differ. A rerun with your own kits and builds therefore starts by moving `protocol.json` aside; `run_confirmation.py` then freezes a new one from `eligibility.json` and the seed. It reads the high round's `protocol.json` for the inherited policies; that file is published as [`../confirm-eu-20261029/protocol.json`](../confirm-eu-20261029/protocol.json), and it expects that directory to be named `confirmation-eu-20261029` and to sit beside the new one (`prepare_wide.py` reads `LANES_HIGH_ROUND_DIR`).

Admission is checked before each cell as spend so far plus `CELL_ESTIMATE` ($2.50) against `CAP` ($7). With these two values a round refuses a cell once about $4.50 is spent, so set `CAP` to $10.50 or more in `confirmation_ext.py` before running all 32 cells. The original round cost $5.74 for the 32 compared runs and $7.89 with the superseded attempts.

```sh
export LANES_CONFIRM_DIR=~/lanes-work/confirmation-eu-wide-20261029 LANES_HIGH_ROUND_DIR=~/lanes-work/confirmation-eu-20261029 LANES_PRIVATE=~/lanes-work
python3 -I lanes/confirm-eu-wide-20261029/prepare_wide.py
cd "$LANES_CONFIRM_DIR" && python3 run_confirmation.py preflight && for i in $(seq 0 31); do python3 run_confirmation.py cell --index $i || break; done
```

Checked 31 October 2026, no model call: all eight Python files compile, and `python3 -I run_confirmation.py --help` prints `preflight`, `counted` and `cell`, from a stand-in round directory holding only links to `lanes/bare` and `lanes/`. The preparation, preflight and cell steps were not run; they need the task kits, the two tool builds, Linux with Bubblewrap, the host lease file named in `../confirm-eu/README.md` and an OpenAI API key.
