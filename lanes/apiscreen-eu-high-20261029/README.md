# EU API patch screen driver (`api-patch-screen` rows of the morning report)

The driver and frozen protocol of the first same-key patch screen on 29 October 2026, which is the `api-patch-screen` experiment in [`reproduce/morning-report-20261030/`](../../reproduce/morning-report-20261030/): the unpatched loop `b8a4046`, `speed2` and five variants (`api-replay`, `api-batch`, `api-answer-end`, `wall-http2`, `wall-h1reuse`), four tasks, one run per arm per task (28 counted cells and 5 dry cells), `gpt-6.1-terra` at high effort, one OpenAI API key, a $5 cap. It is the copy that ran, with host paths turned into the variables of [`../confirm-eu/README.md`](../confirm-eu/README.md); gateway and containment are those of [`../confirm-eu/`](../confirm-eu/).

| file | what it is |
|---|---|
| `run_confirmation.py` | `freeze` (write `protocol.json`), `dry` (the five dry cells), `counted` (the 28 cells, in order, graded) |
| `confirmation_ext.py` | the extension the round used |
| `protocol.json` | the frozen protocol: seed `2026102997`, task and arm order, cells, hashes of the original builds and kits |
| `analyze.py`, `finalize_screen.py` | the round analysis (per-arm tables, paired deltas) and the credential cleanup step |

Builds: put them in `$LANES_CONFIRM_DIR/bin/` as `loop-b8a4046` and `scr-<arm>-kogen-loop` for the other six arms. `speed2` is [`../../reproduce/api-patch-screen-2nd-host/patches/speed2.diff`](../../reproduce/api-patch-screen-2nd-host/patches/speed2.diff) on `b8a4046`; each patch arm is its own diff on top of it: [`api-replay`](../patches/loop/api-replay.diff), `api-batch` and `api-answer-end` (in `reproduce/api-patch-screen-2nd-host/patches/`), and [`wall-http2`](../patches/loop/wall-http2.diff) and [`wall-h1reuse`](../patches/loop/wall-h1reuse.diff). The round directory layout is the one in `../confirm-eu/README.md`.

`protocol.json` holds the SHA-256 of the original builds, kits and cache, and each cell refuses to run if they differ, so with your own builds move it aside and let `freeze` write yours (the seed fixes the order).

```sh
export LANES_CONFIRM_DIR=~/lanes-work/apiscreen-eu-high-20261029
python3 -I lanes/apiscreen-eu-high-20261029/run_confirmation.py freeze
python3 -I lanes/apiscreen-eu-high-20261029/run_confirmation.py dry
python3 -I lanes/apiscreen-eu-high-20261029/run_confirmation.py counted
```

Checked 31 October 2026, no model call: the four files compile and `run_confirmation.py --help` prints `freeze`, `dry` and `counted`, from a stand-in round directory. `freeze`, the dry cells and the counted cells were not run; they need the task kits, the seven builds, Linux with Bubblewrap, the host lease file and an API key.
