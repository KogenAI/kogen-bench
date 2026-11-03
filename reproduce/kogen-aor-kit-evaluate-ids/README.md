# kogen-aor-kit-evaluate-ids

Our Agents-on-Rails task converter built the expected hidden-check ids wrongly for one new task. **A correct solution to that task would have scored as missing all nine of its hidden checks. The converter is fixed and self-tested; no published score used the affected task, so no Agents-on-Rails number, ceiling or baseline changes. This is a model-free check; no run was made and none is needed to support the verdict.**

## What went wrong

The converter turns each upstream task into a task folder for our harness, including the list of hidden checks a solution is graded against. Each check id is the test class name plus the test name. The converter took the class name from the last `class X <` line it had seen so far. When a verifier declares a small helper class before its tests, every id received the helper's name instead of the test class's name. The graded checks then never matched the ids requested, so a correct solution was capped below its real grade.

## Evidence (no model calls, cost 0)

- **Where it showed:** one new task (webhook delivery). All 9 of its ids carried the helper class name; with the fix they carry the test class name. The difference is that single name on each id.
- **Other tasks:** the 13 upstream tasks in the kit give identical ids under the old and the fixed converter, so none was affected.
- **Copies scanned:** 338 task copies on three machines were compared with the fixed converter's output. 336 matched; the 2 that did not are the two qualification copies of the one new task.
- **Published numbers:** no stored run holds a graded cell for the affected task. Its only grades are the reference solution and the final code, both fully passing on the fixed ids. No pooled score, ceiling or baseline changes, so there is nothing to regrade.
- **Upstream:** the upstream repository has no such grading config, and its verifier is unchanged at the version we pinned. The defect was ours alone.

## Fix

Kit version 2 tracks the enclosing test class by indentation, so a nested helper never becomes the prefix. A built-in self-test checks that every task's ids sit under exactly one test class with no duplicates; it passes on all 14 tasks. The old converter is kept next to it for comparison. See `data/selftest.tsv` and `data/copy_scan.tsv`.

## Limits

- One machine that holds copies derived from the 13 unaffected tasks could not be scanned; its copies are built from the same sources, which the self-test covers.
- The affected task's hidden test names are withheld.

## Rerun

In the kit directory, run the self-test of kit version 2. It needs the private task sources:

```sh
python3 mk_tasks.py --selftest
```

It prints one `ok` line per task and exits 0 when each task's ids sit under exactly one test class. To recompute the verdict from the recorded tables:

```sh
python3 -I reproduce/kogen-aor-kit-evaluate-ids/report.py reproduce/kogen-aor-kit-evaluate-ids/data/selftest.tsv reproduce/kogen-aor-kit-evaluate-ids/data/copy_scan.tsv | diff - reproduce/kogen-aor-kit-evaluate-ids/expected-output.txt
```

`report.py` uses only the standard library.
