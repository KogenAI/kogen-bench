#!/usr/bin/env python3
"""night_grade.py JOBS.json OUT.json -- independent Studio grading for benchmark night 2026-10-01 (driver-owned, v1).
JOBS: [{"id": str, "task": tid, "patch": "/abs/patch.diff" | "", "control": "candidate|noop|reference|negative:<path>"}]
Builds a fresh cell-identical workspace (git archive/base copy + setup + commit), applies the patch (none for noop; sealed
reference resolved inside the grade window), and grades with the runner's mac-private-v2 concurrent private grader.
Results are appended incrementally to OUT (one JSON object per line)."""
import json, os, sys, tempfile, shutil, subprocess, time, contextlib, hashlib
from pathlib import Path
sys.path.insert(0, os.path.expanduser("~/bench/night-2026-10-01/runner"))
import bench as B
import concurrent_grade as CG

STAGE = Path(os.path.expanduser(os.environ.get("NIGHT_STAGE", "~/bench/.concurrent-grader/night-stage")))

def staged_restore(B, rels, target):
    """night v2: sealed material is pushed by the MacBook into STAGE (0700, below the sandbox-denied private grader root)
    instead of being pulled over Studio->MacBook ssh (no unattended key on Studio)."""
    for rel in rels:
        p = Path(rel)
        if p.is_absolute() or '..' in p.parts or rel.startswith('_bench/'):
            raise RuntimeError('invalid private sealed path')
        src = STAGE / p; dest = target / p
        if not src.exists():
            raise RuntimeError('staged sealed path missing: ' + rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(['rsync', '-a', '--exclude', '_build', '--exclude', 'deps', '--exclude', 'node_modules', str(src), str(dest.parent) + '/'], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError('staged restore failed for %s (rc=%d)' % (rel, r.returncode))
        paths = [dest] + list(dest.rglob('*')) if dest.is_dir() else [dest]
        if any(x.is_symlink() for x in paths):
            raise RuntimeError('symlink in restored sealed tree')
        subprocess.run(['chmod', '-R', 'go-rwx', str(dest)], check=True, capture_output=True)

CG.restore = staged_restore

# HC01 count-only instrumentation (AMENDMENT-4). The verdict classifier receives the full
# runner output before the unchanged grader truncates it for the result tail.
# Count source: exactly one official grader summary line "Result: P/T passed".
# Diagnostics (integers only): number of such lines and of ExUnit "N tests, M failures" summaries.
# The full runner output is written once, mode 0600, to $HC01_RAW_STAGE/<id>.out for transfer to
# the private store; only its byte count and sha256 enter the row.
import re as _count_re
_COUNT_ANSI = _count_re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_COUNT_RESULT = _count_re.compile(r"^Result: (?P<passed>\d+)/(?P<total>\d+) passed$")
_COUNT_EXUNIT = _count_re.compile(r"^(?:\d+ doctests?, )?(?:\d+ propert(?:y|ies), )?\d+ tests?, \d+ failures?\b")


def _count_summary(output):
    counts = {"tests_total": None, "failures": None, "tests_passed": None,
              "n_result_lines": None, "n_exunit_summaries": None,
              "status": "count unavailable"}
    if not isinstance(output, str):
        return counts
    try:
        lines = [_COUNT_ANSI.sub("", raw).strip() for raw in output.splitlines()]
        results = [m for m in (_COUNT_RESULT.match(x) for x in lines) if m]
        counts["n_result_lines"] = len(results)
        counts["n_exunit_summaries"] = sum(1 for x in lines if _COUNT_EXUNIT.match(x))
        if len(results) != 1:
            return counts
        passed, total = int(results[0].group("passed")), int(results[0].group("total"))
        if passed > total:
            return counts
        counts.update(tests_total=total, tests_passed=passed, failures=total - passed, status="ok")
        return counts
    except Exception:
        return counts


def _retain_raw(cell_id, output):
    stage = os.environ.get("HC01_RAW_STAGE")
    if not stage or not isinstance(output, str):
        return {"raw_retained": False, "raw_output_bytes": None, "raw_output_sha256": None}
    data = output.encode("utf-8", "surrogateescape")
    fd = os.open(os.path.join(stage, cell_id + ".out"), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)
    return {"raw_retained": True, "raw_output_bytes": len(data), "raw_output_sha256": hashlib.sha256(data).hexdigest()}


def _count_record(cell_id, output):
    rec = _count_summary(output)
    rec.update(_retain_raw(cell_id, output))
    return rec

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest() if p and Path(p).exists() else None

def main(jobs_path, out_path):
    jobs = json.loads(Path(jobs_path).read_text())
    runner_capture = {"output": None}
    original_classify_grade = B.classify_grade

    def capture_classify_grade(*args, **kwargs):
        runner_capture["output"] = args[1] if len(args) > 1 else kwargs.get("out")
        return original_classify_grade(*args, **kwargs)

    B.classify_grade = capture_classify_grade
    wroot = Path(os.path.expanduser("~/bench/night-2026-10-01/grading/work")); wroot.mkdir(parents=True, exist_ok=True)
    with B.run_lock(False, private_grade=True):
        for j in jobs:
            t0 = time.time(); rec = dict(j, grader="night_grade v2 / " + CG.VERSION, host="studio", started=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            try:
                task = B.load_task(j["task"])
                ws = Path(tempfile.mkdtemp(prefix="ng-", dir=str(wroot))); os.chmod(ws, 0o755); work = ws / "work"
                info = B.prepare_workdir(task, work)
                env, _ = B.child_env(task.get("env"))
                if task.get("setup"):
                    p = subprocess.run(task["setup"], shell=True, cwd=work, env=env, capture_output=True, text=True)
                    if p.returncode: raise RuntimeError("setup failed: " + p.stderr[-300:])
                B.sh(["git", "add", "-A"], cwd=work); B.sh(["git"] + B.GIT_ENV_ARGS + ["commit", "-q", "--allow-empty", "-m", "setup"], cwd=work)
                rec["base"] = info
                rels = B.sealed_rels_for_task(task) if B.sealed_on() else []
                with contextlib.ExitStack() as st:
                    st.enter_context(CG.capacity(B, j["task"]))
                    ptask = st.enter_context(CG.task_tree(B, task, rels))
                    ctl = j.get("control", "candidate"); patch = j.get("patch") or ""
                    if ctl == "reference":
                        td = Path(ptask["dir"]); root = Path(ptask["_private_grade"]["root"])
                        c = sorted(root.rglob("tasks/%s/sealed/reference.patch" % j["task"])) + sorted(root.rglob("%s/sealed/solution.patch" % j["task"]))
                        patch = str(c[0]) if c else ""
                        rec["patch_kind"] = "sealed reference (not exported)"
                        if not patch: raise RuntimeError("reference patch not found in private tree")
                    elif ctl.startswith("refdrop:"):
                        root = Path(ptask["_private_grade"]["root"]); n = int(ctl.split(":", 1)[1])
                        c = sorted(root.rglob("tasks/%s/sealed/reference.patch" % j["task"])) + sorted(root.rglob("%s/sealed/solution.patch" % j["task"]))
                        if not c: raise RuntimeError("reference patch not found for refdrop")
                        txt = c[0].read_text(); parts = ["diff --git" + x for x in txt.split("diff --git")[1:]]
                        app = [i for i, x in enumerate(parts) if "/test/" not in x.split("\n", 1)[0] and "_test." not in x.split("\n", 1)[0]]
                        if not app: raise RuntimeError("no non-test file to drop")
                        drop = app[n % len(app)]; rec["patch_kind"] = "derived plausible-wrong: reference minus %s" % parts[drop].split("\n", 1)[0][11:120]
                        kept = [x for i, x in enumerate(parts) if i != drop]
                        dp = Path(ptask["_private_grade"]["root"]) / "refdrop.patch"; dp.write_text("".join(kept)); patch = str(dp)
                    elif ctl.startswith("negative:"):
                        root = Path(ptask["_private_grade"]["root"]); name = ctl.split(":", 1)[1]
                        c = sorted(root.rglob(name))
                        if not c: raise RuntimeError("negative patch %s not found" % name)
                        patch = str(c[0]); rec["patch_kind"] = "sealed negative " + name
                    if patch:
                        if ctl == "candidate": rec["patch_sha256"] = sha(patch)
                        a = subprocess.run(["git", "apply", "--whitespace=nowarn", patch], cwd=work, capture_output=True, text=True)
                        if a.returncode:
                            rec.update(outcome="fail", kind="model", cause="patch_apply_failed: " + a.stderr[:300], pass_=False)
                            raise StopIteration
                    g = CG.grade(B, ptask, work, None)
                    rec.update(pass_=g["pass"], outcome=g["outcome"], kind=g["kind"], cause=g.get("cause"), rc=g["rc"], grade_wall_s=g["wall_s"], tests_ran=g.get("tests_ran"), tail=g["output_tail"][-800:])
                    rec["counts"] = _count_record(rec["id"], runner_capture["output"])
            except StopIteration:
                pass
            except Exception as ex:  # noqa
                rec.update(pass_=False, outcome="grader_error", kind="infra", cause=repr(ex)[:400])
            finally:
                if "counts" not in rec:
                    rec["counts"] = _count_record(rec["id"], runner_capture["output"])
                runner_capture["output"] = None
                try: shutil.rmtree(ws, ignore_errors=True)
                except Exception: pass
            rec["total_s"] = round(time.time() - t0, 1)
            with open(out_path, "a") as f: f.write(json.dumps(rec) + "\n")
            print(j["id"], j["task"], j.get("control"), rec.get("outcome"), rec.get("total_s"), flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "--rels":
        out = {}
        for t in sys.argv[2:]:
            out[t] = B.sealed_rels_for_task(B.load_task(t))
        print(json.dumps(out))
    else:
        main(sys.argv[1], sys.argv[2])
