# Regrade and rerun tasks

Task directories contain task metadata and, where available, the public prompt. Of 125 catalogued tasks, 90 include a prompt, 78 include a hidden suite, and 50 include a per-task grader. Sixty-five deterministic base bundles and their `MANIFEST.sha256` are included in `tasks/_bases/`; `tasks/index.json` and each task's `task.json` link the exact bundle and SHA-256 when the recorded base commit is present. `base_missing: true` marks records without that exact base. Dependency caches are not bundled. Not every task can be regraded from this snapshot alone. The layout is:

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

`tasks/_grader/linux-r70/grade_worker.py` imports two Python modules that are not published in this repository: `sandbox_linux` (the `base_args` sandbox setup helper) and `dispatch` (the `active` job-state check). The historical host places them in its runner package. `grade_window.py` also imports `dispatch.active` remotely when it checks active work. Neither host module is vendored here, so the shared R70 worker cannot run from this repository alone; provide those modules on the controlled grading host or replace the imports with reviewed published implementations before using that worker.

The one-command, fresh-VM-verified rerun kit is in progress. This repository does not yet claim that a new operator can reproduce a full model run with one command on a clean VM. Follow the per-task instructions and verify the isolation and grader prerequisites locally until that kit is complete; no delivery date is promised.

Historical records remain historical records. Rerunning a task creates a new observation and does not overwrite or retroactively validate a published result.
