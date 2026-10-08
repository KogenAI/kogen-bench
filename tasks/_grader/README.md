# Vendored shared grader helpers

These files publish only the helpers imported by the shared R70 grader. Host-specific paths are configurable with `BENCH_HOST`, `BENCH_SYSROOT`, `BENCH_BWRAP`, and `BENCH_PROC_ROOT`.

| Helper | As-run/recovered source | As-run/recovered SHA-256 | Published file | Published SHA-256 |
|---|---|---|---|---|
| `sandbox_linux.base_args` | `levers/llm-latency/source/sandbox_linux.py` (exact as-run file not found; this is the recovered comparison copy) | `89f025d1dc47bfafb7058a1b45d818bb38cf6d957eb8e17a6c16165ef683afe6` | `tasks/_grader/sandbox_linux.py` | `10e9f8816964910fdb0be15de3ff2d6f7f8a50658c0cd3cc991614ac67921969` |
| `dispatch.active` | `levers/r70/dispatch.py` | `5487610c0bd3e2806d683d7739ed6ceeaabc5476b557f8b75f33c27f07f5ce6a` | `tasks/_grader/dispatch.py` | `690b928ae5f9d265a35cded531af8762f87a48daa6406b59ce031b37d426deab` |

The recovered tree has no `.git` directory, so source commit history could not be read. `dispatch.active` delegates to `levers/lib/count_cells.py`'s process matching behavior; the published helper contains only the process enumeration and match logic needed for the grader. The historical sandbox helper's exact as-run hash remains unavailable because its imported runner path was absent; the listed hash identifies the closest recovered operator copy and is not represented as the historical-host hash.
