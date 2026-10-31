# API patch screen driver (`api-patch-screen-2nd-host`)

The driver and frozen protocol of the 16-run round in [`reproduce/api-patch-screen-2nd-host/`](../../reproduce/api-patch-screen-2nd-host/): `speed2` against `api-replay`, `api-batch` and `api-answer-end`, four tasks, one run per tool per task, `gpt-6.1-terra` at high effort, one OpenAI API key, a $3 cap. It is the copy that ran on the second Linux host, with host paths turned into variables; the gateway and containment are those of [`../confirm-eu/`](../confirm-eu/) (see its README for the variables).

| file | what it is |
|---|---|
| `run_confirmation.py` | `prepare` (freeze the protocol and print its hash), `counted INDEX` (exactly one frozen cell, graded) |
| `confirmation_ext.py` | the extension the round used |
| `protocol-frozen.json` | the frozen protocol: seed `20261030`, the shuffled task and tool order, the 16 cells and the hashes of the original binaries and kits |

Setup the driver expects in `LANES_CONFIRM_DIR`: the layout of [`../confirm-eu/README.md`](../confirm-eu/README.md) with `bin/scr-speed2-kogen-loop` inside it, and the three patched builds in `LANES_PATCHED_BIN_DIR` as `scr-api-replay-kogen-loop`, `scr-api-batch-kogen-loop` and `scr-api-answer-end-kogen-loop`. Build each from kogen-loop `b8a4046` plus the pack's `patches/speed2.diff` and then its own patch (`speed2` is the baseline and each candidate patch applies on top of it). Spend rows go to the file named by `LANES_SPEND_LEDGER`. One deviation from the original: its extension pointed at the parent directory holding identical copies of the kits and builds; here both files use `LANES_CONFIRM_DIR`.

`prepare` writes `protocol-frozen.json` only if it is missing. The published one holds the hashes of the original builds, so with your own builds move it aside first and let `prepare` write yours; the seed fixes the order.

```sh
export LANES_CONFIRM_DIR=~/lanes-work/apiscreen-patches-high LANES_PATCHED_BIN_DIR=~/lanes-work/apiscreen-bins LANES_SPEND_LEDGER=~/lanes-work/api-spend-ledger.tsv
python3 -I lanes/apiscreen-patches-high-20261030/run_confirmation.py prepare
for i in $(seq 0 15); do python3 -I lanes/apiscreen-patches-high-20261030/run_confirmation.py counted $i || break; done
```

Checked 31 October 2026, no model call: both files compile and `run_confirmation.py --help` prints `prepare`, `dry` and `counted`, from a stand-in round directory. `prepare` and the cells were not run; they need the task kits, the four builds, Linux with Bubblewrap, the host lease file and an API key.
