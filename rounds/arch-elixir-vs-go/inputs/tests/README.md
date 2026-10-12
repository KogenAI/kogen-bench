# ARCH hidden black-box runner

Run with Python 3.9 or newer, Git, and an executable implementation or wrapper:

```sh
python3 run_hidden.py --kogen /absolute/path/to/kogen --groups B,F,M --out results.json --reps 2
```

Relative output names resolve under this `tests/` directory, regardless of the
calling working directory. Absolute outputs must also be under `tests/`. Fixtures
live under `tests/.tmp/` and are removed after each repetition unless
`--keep-fixtures` is supplied. Every case gets a new directory and localhost port.
The runner never writes to the real repositories or forbidden external services.
Fixtures ignore host global/system Git configuration and disable seed-repository
hooks, so unrelated user hooks and signing preferences cannot affect scoring.

`--list` prints the case catalog. `--cases B01,F05` selects cases for investigation.
`--case-timeout 90` sets the hard wall-clock cap for each case repetition, including
startup; bounded emergency cleanup follows a deadline. A subprocess isolates each
repetition so a hung CLI cannot hang the suite.
Individual commands also have deadlines. The runner cleans up marked descendants
after successful cases, failures, and timeouts, including processes that detached
with `setsid`. A cleanup survivor fails the repetition.

The JSON report has `schema_version`, `reps`, contract hashes, a `cases` array,
group counters, and `k_ids` passing/total counts overall and for each repetition.
K-07, K-19, and K-39 are also grouped under `priority_k_ids`. Each case records
its K-ID tags, numbered contract clauses, and full repetition records. A case's
`passed` is true **only if every repetition passed**. Partial results are replaced
atomically after each completed case. Exit code 0 means all selected cases passed;
1 means at least one failed; 2 means invalid invocation. A contract change during
a run is flagged in `spec_changed_during_run` and invalidates freeze evidence.

The suite observes only public CLI/protocol outputs, fixture filesystem markers,
Git history/content, and process command lines. It uses gates to hold a build or
landing at a known point before fault injection. It does not infer an internal
implementation architecture. Priority cases belong to the maintenance phase.

Run the runner's independent self-check with:

```sh
python3 selftest.py
```

The fake records calls and replays fixed transcripts; it does not implement the
external contract. Self-tests use simulated `ps` rows because the authoring
sandbox blocks `ps`, and skip localhost-dependent checks when bind is denied;
the production runner requires real `ps` before launching anything.
The separate passability gate document is not included in this public runner export.
