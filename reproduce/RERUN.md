# Regrade and rerun tasks

Task directories contain task metadata and, where available, the public prompt. Of 125 catalogued tasks, 90 include a prompt, 103 include a hidden suite, and 100 include a per-task grader. Sixty-nine deterministic base bundles and their `MANIFEST.sha256` are included in `tasks/_bases/`; `tasks/index.json` and each task's `task.json` link available bundles and SHA-256 values; recovered Rails snapshot commits are recorded separately from upstream commit claims. `base_missing: true` marks records without a bundled base. Dependency caches are not bundled. Not every task can be regraded from this snapshot alone. The layout is:

```text
tasks/<id>/
  README.md                 # task notes and public setup
  ...                       # public prompt, base, and task files
  hidden/                   # grading inputs, not exposed to the agent during a run
  grader/                   # official grading logic and dependencies
```

The hidden suite is hidden from the agent while it is solving the task, not from you. After the run, use the task's shipped grader and its documented dependencies to grade the resulting worktree. Keep the grader and `hidden/` outside the agent's visible workspace and do not include their contents in prompts, logs, or run artifacts.

## Requirements and operator steps

- Use Linux. The grading isolation requires `bwrap` (Bubblewrap) and the grader's documented system packages. A host without working user namespaces or the required Bubblewrap features cannot provide the same isolation.
- Bring your own Codex login and access. Authenticate Codex on the machine you control before starting; credentials and authentication files are not part of this repository. Use a fresh run directory per attempt and retain the exact task revision, prompt, model and effort settings, tool versions, grader result, and numeric usage fields needed by the record schema.
- Prepare the task's public base in the run workspace, give the agent only the public task materials, and run the shipped grader against the completed workspace after the agent exits. Preserve the grader output needed for your own audit without publishing raw transcripts or account data.

## Shared Linux grader host imports

`tasks/_grader/linux-r70/grade_worker.py` uses the published minimal implementations of `sandbox_linux.base_args` and `dispatch.active` from `tasks/_grader/`. Their recovered-source and published-file SHA-256 values, plus source caveats, are recorded in [the grader vendor note](../tasks/_grader/README.md). `grade_window.py` checks active work through the same published `dispatch.active` implementation installed under `$BENCH_HOST/recovery-2026-10-02/tasks/_grader/` on the grading host.

Set `BENCH_HOST` to the grading host's bench root (default host-specific bench root) and `BENCH_PYTHON` to its Python executable (default `/opt/bench/mise/installs/python/3.14.7/bin/python3`) before running the window controller. The worker resolves the recovery archive, result store, and toolchains below `BENCH_HOST`; `BENCH_SYSROOT` and `BENCH_BWRAP` configure the sandbox helper; `BENCH_RUSTUP` sets the Rust toolchain home (default `/opt/bench/rustup`). Install this repository's `tasks/_grader/` tree below the configured recovery root on each grading host.

The exact historical `probe-kgn/runner/sandbox_linux.py` file was not present in the recovery archive. The matching recovery search found only `levers/llm-latency/source/sandbox_linux.py`, which supplies the same `base_args` implementation shape; its hash is retained as the recovered comparison source, not asserted as the historical host file's hash. The recovery directory has no Git metadata, so file-specific `git log` history was unavailable there.

## Ubuntu host setup (verified on a fresh host for tasks 1, 5 and 7)

From a clone of this repository on Ubuntu 24.04 x86_64:

```sh
sudo ./reproduce/setup-host.sh --dry-run
sudo ./reproduce/setup-host.sh
sudo /usr/local/bin/bench-doctor
sudo -u bench -H /opt/bench/tools/bin/codex login --device-auth
sudo chmod -R go-rwx ~bench/.codex
sudo /usr/local/bin/bench-run-controls r70-1-go
```

The setup command installs the packages and SHA-256-checked toolchains in [`host-pins.lock`](host-pins.lock), creates `benchadmin` and `bench`, installs Bubblewrap 0.9.0, `bench.slice`, a 10 GiB launch floor, and copies this release's `tasks/` bundles and graders into a root-owned kit under `/srv/bh/bench/kits/`. It installs [`run-lane.sh`](run-lane.sh), [`sandbox-profile.sh`](sandbox-profile.sh), [`run-controls.sh`](run-controls.sh), and a model-free [`doctor.sh`](doctor.sh). Re-running setup preserves run work and results. A Codex login belongs to the local `bench` user and is always a manual device-auth step; setup and doctor make no model call.

To run a task after login, call `sudo bench-run-lane TASK_ID UNIQUE_RUN_ID MODEL EFFORT`. This launches one Codex cell in `bench.slice` with only its public worktree and the bench user's Codex home mounted into Bubblewrap, then runs the shipped per-task hidden grader after the model exits. It writes a patch, private grader log, JSON grade, Codex JSONL, and manifest under `/srv/bh/bench/results/UNIQUE_RUN_ID/`. Keep the result private until its transcript and grader output are reviewed for publication. The launcher refuses to reuse a run ID or start below 10 GiB free.

The host kit now includes `setup-host.sh` for Ubuntu 24.04 x86_64 provisioning, `doctor.sh` for model-free host qualification, and `run-controls.sh` for reference-pass/no-op-fail checks on selected tasks. Fresh-machine setup was verified on 9 October 2026: the controls admitted every stack of tasks 1, 5 and 7; see the scope note in README.md for the tasks that are not yet rerunnable. Some published tasks have no base, prompt, grader, or reference, and `run-controls.sh` reports those as unavailable. Dependency caches, the complete historical lane runner and its restricted network relay, protected Studio grading route, and historical private data are absent from this repository. The kit does not claim bit-for-bit replay of old cells. A successful doctor proves host prerequisites, not task admission or model access. The published fresh-host proof runs the admission controls on the six task-1 kits (r70-1-rust, r70-1-go, r70-1-elixir, r70-1-ts-bun, r70-1-gleam and r70-1-zig); a sweep over all kits is optional for anyone rerunning older rounds.

Historical records remain historical records. Rerunning a task creates a new observation and does not overwrite or retroactively validate a published result.

## Rails snapshot requirements

The Rails base snapshots use Ruby 3.4.8. Their lockfiles record Bundler 2.5.18 for Writebook and Bundler 2.7.2 for Fizzy, Fizzy SaaS, and the hard2 Fizzy snapshot. None of the four snapshots contains `vendor/cache`. A rerun needs `bundle install --local` with a host cache that already contains every locked gem and any Git-sourced dependencies; this repository does not include those dependencies.

On the MacBook checked for this recovery, Ruby 3.4.8 and Bundler 2.7.2 are available. `bundle check` reports dependencies satisfied for Fizzy, Fizzy SaaS, and hard2 Fizzy. Writebook's check cannot satisfy its dependencies and attempts to fetch the Rails Git source, so the current warm cache is not sufficient for an offline Writebook rerun. The Rails task kits and deterministic base snapshot bundles are packaged in this snapshot. `task.json` records each bundle hash and its source proof; six hard2 Fizzy tasks have no independent as-run comparison. The Writebook dependency cache remains insufficient for an offline rerun. See [the Rails kit recovery report](../tasks/RAILS-KIT-GAPS.md).
