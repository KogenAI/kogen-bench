# kogen-setup-initial-e580996

Kogen's project setup step (`kogen init`) was moved into its own component, `kogen-setup`, whose first commit is `e580996`. Does the moved step behave differently from the one in the adopted release? **No. The setup logic is byte-identical to the adopted version once the package name line is rewritten, and no model-visible text moved with it. Same behaviour, so nothing changes. This is a model-free check; no run was made and none is needed to support the verdict.**

## What changed

The setup step runs one model conversation to detect a project's commands, verifies them on a copy, and writes the project configuration. Until now its code lived inside the shaping component. The change copies it into a component of its own. The init prompt and the tool definitions do not move: they stay in the executor component, which this commit does not touch.

## Evidence (byte comparisons, no model calls, cost 0)

- **Setup logic:** after rewriting the single package-clause line, the init source (1545 lines) has the same SHA-256 as the shaping component's version at the adopted pin (`94eabe5`) and at its current head (`d69a0a3`).
- **No embedded text:** the new component has no embedded files, so no prompt or template text travels with it. The init prompt is still read from the executor component, unchanged.
- **Conversation helpers:** the three helper functions copied alongside (request building, tool output, cache id) have identical bodies.
- **Test fixtures:** the generation and mix script fixtures are identical. The golden JSON fixture differs from the adopted pin by one serialisation line and is identical to the head. It is test-only and is never sent to a model.
- **The mover's own checks:** the mover reported its move-verification tool OK and the 41 init tests at 47 passed, 0 failed, 0 skipped, before and after the move. Those were not repeated here.

See `data/file_compare.tsv` and `data/init_source_hashes.tsv`.

## Why no run

The model-facing code is the same bytes, so there is nothing for a run to measure. A paired run would only show ordinary rerun variation (18 to 27 % of pairs flip between identical runs).

## Limits

- Only this first commit is covered. Later commits to the new component that change model-visible text or the init behaviour need their own screen within 6 hours of landing; test-only and configuration commits are the same model-free check.
- The test results are the mover's, not ours.
- How the new component is wired into the main product is out of scope here; this checks only that the moved code and text are unchanged.

## Rerun

Byte-compare the init source of the new component against the shaping component at each version, with the package line rewritten:

```sh
git -C <shaping clone> show 94eabe5:<init source> | sed 's/^package shape/package setup/' | cmp - <setup clone>/<init source>
git -C <shaping clone> show d69a0a3:<init source> | sed 's/^package shape/package setup/' | cmp - <setup clone>/<init source>
grep -c 'go:embed' <each source file of the setup package>
```

The two `cmp` commands print nothing when the files are identical, and `grep` counts 0 embedded-file lines in every file. Repeat the `cmp` without the `sed` for each test fixture. These need the private component repositories; the numbers are recorded in `data/`. To recompute the verdict from the recorded tables:

```sh
python3 -I reproduce/kogen-setup-initial-e580996/report.py reproduce/kogen-setup-initial-e580996/data/init_source_hashes.tsv reproduce/kogen-setup-initial-e580996/data/file_compare.tsv | diff - reproduce/kogen-setup-initial-e580996/expected-output.txt
```

`report.py` uses only the standard library.
