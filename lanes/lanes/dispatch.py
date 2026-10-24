"""Plan the cells of an experiment and run them across hosts (local or over ssh)."""

import argparse
import hashlib
import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

from . import common, costguard, experiment, noise, plan_hashes

CAP_GRACE_S = 3  # after the hard cap: time for each local cell to stop itself and record `cost_cap`
MARGIN_S = 300  # slack on top of the cell deadline for syncing and for stale claims
LANES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # the `lanes/` folder


class DispatchError(RuntimeError):
    pass


# ---- plan -----------------------------------------------------------------------------------

def make_plan(exp):
    """Cells in run order. Lane order rotates per (task, rep), from a start derived from the id."""
    lanes = [lane["name"] for lane in exp["lanes"]]
    start = int(hashlib.sha256(exp["id"].encode()).hexdigest()[:8], 16)
    cells, k = [], 0
    for task in exp["tasks"]:
        for rep in range(1, exp["reps"] + 1):
            shift = (start + k) % len(lanes)
            for order, lane in enumerate(lanes[shift:] + lanes[:shift]):
                cells.append({"cell": f"{task}/r{rep}/{lane}", "task": task, "rep": rep,
                              "lane": lane, "order": order})
            k += 1
    return cells


def plan_main(argv=None):
    p = argparse.ArgumentParser(description="Plan the cells of an experiment.")
    p.add_argument("experiment")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--tasks", default=os.environ.get("KOGEN_LANES_TASKS"), help="private tasks folder")
    a = p.parse_args(argv)
    if not a.tasks:
        p.error("--tasks or KOGEN_LANES_TASKS is required")
    exp = experiment.load_or_exit(a.experiment)
    try:
        if exp.get("kind") == "climb":
            noise.check_gate(exp, a.experiment)  # no climb without a measured run-to-run noise below min_effect
        lock = os.path.join(a.run_dir, "lanes.lock.json")
        if not os.path.isfile(lock):  # check first: write nothing into a run dir that cannot be planned
            raise DispatchError("lanes.lock.json is missing in the run dir: run lanes-build first")
        os.makedirs(a.run_dir, exist_ok=True)
        shutil.copyfile(a.experiment, os.path.join(a.run_dir, "experiment.json"))
        for lane in exp["lanes"]:  # patches travel with the experiment so the hashes can be re-checked
            src = experiment.patch_path(a.experiment, lane)
            if src:
                dst = os.path.join(a.run_dir, lane["patch"])
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
        common.write_json(os.path.join(a.run_dir, "PLAN.json"), plan_hashes.build_plan(a.experiment, a.tasks, lock))
        with open(os.path.join(a.run_dir, "plan.jsonl"), "w", encoding="utf-8") as f:
            for cell in make_plan(exp):
                f.write(json.dumps(cell, sort_keys=True) + "\n")
    except (DispatchError, noise.NoiseError, plan_hashes.PlanError, OSError, ValueError) as e:
        print(f"plan: {e}", file=sys.stderr)
        return 2
    return 0


# ---- verification ---------------------------------------------------------------------------

def verify_inputs(run_dir, exp, tasks_dir):
    """Refuse to start when task inputs, lane inputs or the lock differ from the PLAN.json hashes."""
    path = os.path.join(run_dir, "PLAN.json")
    if not os.path.isfile(path):
        raise DispatchError("PLAN.json is missing: run lanes-plan first")
    plan = common.read_json(path)
    exp_path = os.path.join(run_dir, "experiment.json")
    form = exp.get("intent_form")
    want = plan["hashes"]
    if {k: v for k, v in exp.items() if k != "hosts"} != plan["experiment"]:
        raise DispatchError("experiment.json no longer matches PLAN.json")
    for t in exp["tasks"]:
        got = plan_hashes.task_hashes(os.path.join(tasks_dir, t), exp["phase"], form)
        if got != want["tasks"].get(t):
            raise DispatchError(f"task {t} no longer matches PLAN.json")
    if want["lanes"] != plan_hashes.lane_hashes(exp, exp_path):
        raise DispatchError("lane patches or settings no longer match PLAN.json")
    lock = os.path.join(run_dir, "lanes.lock.json")
    if not os.path.isfile(lock):
        raise DispatchError("lanes.lock.json is missing: run lanes-build first")
    if not plan["lock"].get("sha256"):
        raise DispatchError("PLAN.json has no lock hash: run lanes-build, then lanes-plan again")
    if plan["lock"]["sha256"] != common.sha256_file(lock):
        raise DispatchError("lanes.lock.json no longer matches PLAN.json")


# ---- hosts ----------------------------------------------------------------------------------

def load_hosts(path, names):
    """`{name: {target, slots, root}}` for the experiment's hosts (all of the file when it names none)."""
    raw = common.read_json(path)
    names = names or sorted(raw)
    out = {}
    for n in names:
        h = raw.get(n)
        if not isinstance(h, dict) or not isinstance(h.get("target"), str):
            raise DispatchError(f"hosts file: no usable entry for {n} (needs target)")
        slots = h.get("slots", 1)
        if isinstance(slots, bool) or not isinstance(slots, int) or slots < 1:
            raise DispatchError(f"hosts file: {n}.slots must be an integer >= 1")
        if h["target"] != "local" and not h.get("root"):
            raise DispatchError(f"hosts file: {n}.root (a work folder on the host) is required")
        out[n] = {"target": h["target"], "slots": slots, "root": h.get("root")}
    return out


# ---- claims ---------------------------------------------------------------------------------

def _alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return True


class Claims:
    """Claim files `<run>/claims/<cell>.json`, created atomically (O_EXCL)."""

    def __init__(self, run_dir, stale_s):
        self.dir = os.path.join(run_dir, "claims")
        self.stale_s = stale_s
        os.makedirs(self.dir, exist_ok=True)

    def path(self, cell):
        return os.path.join(self.dir, cell.replace("/", "__") + ".json")

    def _stale(self, path):
        try:
            info = common.read_json(path)
            pid, at = info["pid"], info["time"]
        except (OSError, ValueError, KeyError):
            pid, at = None, os.path.getmtime(path)  # half-written: judge by age only
        return (pid is not None and not _alive(pid)) or time.time() - at > self.stale_s

    def take(self, cell, host):
        path = self.path(cell)
        for _ in range(2):
            try:
                fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                try:
                    if not self._stale(path):
                        return False
                    grave = f"{path}.stale.{os.getpid()}"
                    os.rename(path, grave)
                    if not self._stale(grave):  # a rival replaced the claim after our check: put it back
                        try:
                            os.link(grave, path)
                        except FileExistsError:
                            pass
                        os.unlink(grave)
                        return False
                    os.unlink(grave)
                except FileNotFoundError:
                    pass
                continue
            with os.fdopen(fd, "w") as f:
                json.dump({"host": host, "pid": os.getpid(), "time": time.time()}, f)
            return True
        return False

    def release(self, cell):
        try:
            os.unlink(self.path(cell))
        except FileNotFoundError:
            pass


# ---- running processes ----------------------------------------------------------------------

class Runner:
    """Starts commands each in its own process group; `stop()` kills every group still running."""

    def __init__(self):
        self.stopped = threading.Event()
        self.halted = set()  # tags (providers) whose commands stop while the others go on
        self._procs = set()
        self._lock = threading.Lock()

    def run(self, cmd, deadline_s=None, env=None, cwd=None, capture=False, force=False, tag=None):
        """Return `(exit_code, output)`; exit 124 on the deadline, 130 when stopped (`force`: ignore stop)."""
        if self.stopped.is_set() and not force:
            return 130, ""
        out = subprocess.PIPE if capture else subprocess.DEVNULL
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=out,
                                stderr=subprocess.STDOUT, start_new_session=True)
        with self._lock:
            self._procs.add(proc)
        reader = []
        if capture:
            t = threading.Thread(target=lambda: reader.append(proc.stdout.read()), daemon=True)
            t.start()
        end = time.monotonic() + deadline_s if deadline_s else None
        code = None
        while code is None:
            try:
                code = proc.wait(timeout=0.1)
            except subprocess.TimeoutExpired:
                if (self.stopped.is_set() or tag in self.halted) and not force:
                    code = 130
                elif end and time.monotonic() > end:
                    code = 124
                if code is not None:
                    common._kill_group(proc)
        common._killpg(proc.pid, signal.SIGKILL)  # stragglers of an exited leader
        with self._lock:
            self._procs.discard(proc)
        if capture:
            t.join(5)
            if not t.is_alive():  # a surviving remote process may still hold the pipe open
                proc.stdout.close()
        text = reader[0].decode(errors="replace") if reader else ""
        return (code if code >= 0 else 128 - code), text

    def halt(self, tag):
        self.halted.add(tag)

    def stop(self):
        self.stopped.set()  # waiting loops notice within 0.1 s and kill their own group


def shell_run(runner, template, **values):
    """Run an operator command template (`{host}`, `{name}`) through `sh -c`."""
    cmd = template.format(**{k: shlex.quote(v) for k, v in values.items()})
    return runner.run(["sh", "-c", cmd], deadline_s=120, capture=True, force=True)


# ---- hosts: preparing and running a cell ----------------------------------------------------

class Host:
    def __init__(self, name, cfg, ctx):
        self.name, self.target, self.slots, self.root = name, cfg["target"], cfg["slots"], cfg["root"]
        self.ctx = ctx
        self.remote = self.target != "local"
        self._lock = threading.Lock()
        self._done = set()
        self.running = set()  # cells running here now (remote hosts: the controller polls their spend)
        self.ssh = shlex.split(os.environ.get("LANES_SSH", "ssh -o BatchMode=yes -o ConnectTimeout=20"))

    def sh(self, command, force=False):
        return self.ctx.runner.run(self.ssh + [self.target, command], deadline_s=MARGIN_S, capture=True, force=force)

    def rsync(self, src, dst, *opts, force=False):
        cmd = ["rsync", "-a", "-e", shlex.join(self.ssh), *opts, src, dst]
        return self.ctx.runner.run(cmd, deadline_s=MARGIN_S, capture=True, force=force)

    def _once(self, key, steps):
        with self._lock:
            if key in self._done:
                return
            for cmd in steps:
                code, out = cmd()
                if code:
                    raise DispatchError(f"{self.name}: sync failed ({code}): {out.strip()[-200:]}")
            self._done.add(key)

    def _dst(self, *parts):
        return f"{self.target}:{os.path.join(self.root, *parts)}"

    def prepare(self, task, lane_artifact):
        """Copy lanes/, the task (no evaluator/) and the artifact once per host."""
        c = self.ctx
        dirs = [os.path.join(self.root, d) for d in ("tasks", "artifacts", "reproduce", os.path.join("runs", c.exp_id))]
        self._once("dirs", [lambda: self.sh("mkdir -p " + " ".join(map(shlex.quote, dirs)))])
        self._once("lanes", [lambda: self.rsync(c.lanes_dir + "/", self._dst("lanes") + "/",
                                                "--delete", "--exclude", "__pycache__", "--exclude", "tests")])
        reproduce = os.path.join(c.lanes_dir, "..", "reproduce")  # the cost guard prices usage with these
        self._once("reproduce", [lambda f=f: self.rsync(os.path.join(reproduce, f), self._dst("reproduce") + "/")
                                 for f in ("cost_calc.py", "price-table-v1.json")
                                 if os.path.isfile(os.path.join(reproduce, f))])
        self._once(("task", task), [lambda: self.rsync(os.path.join(c.tasks, task) + "/",
                                                       self._dst("tasks", task) + "/",
                                                       "--delete", "--exclude", "/evaluator/")])
        self._once(("artifact", lane_artifact), [lambda: self.rsync(
            os.path.join(common.lanes_home(), "artifacts", lane_artifact) + "/",
            self._dst("artifacts", lane_artifact) + "/")])
        self._once("run", [lambda: self.rsync(os.path.join(c.run_dir, "experiment.json"), self._dst("runs", c.exp_id) + "/"),
                           lambda: self.rsync(os.path.join(c.run_dir, "lanes.lock.json"), self._dst("runs", c.exp_id) + "/")])

    def poll(self):
        """`{cell: usd}` of the cells in this host's run dir; raises when it cannot be read."""
        c, q = self.ctx, shlex.quote
        command = (f"cd {q(os.path.join(self.root, 'lanes'))} && KOGEN_LANES_HOME={q(self.root)} "
                   f"python3 -m lanes.costguard cells {q(os.path.join(self.root, 'runs', c.exp_id))}")
        code, out = c.runner.run(self.ssh + [self.target, command], deadline_s=30, capture=True, force=True)
        try:
            if code:
                raise ValueError(f"exit {code}: {out.strip()[-120:]}")
            return {k: float(v) for k, v in json.loads(out.strip().splitlines()[-1]).items()}
        except (ValueError, IndexError, TypeError, AttributeError) as e:
            raise DispatchError(f"{self.name}: cannot read the spend of its cells ({e})") from None

    def run_cell(self, cell, lane_artifact):
        """Run one cell; True when its `result.json` is in the controller's run dir afterwards."""
        self.running.add(cell)
        try:
            return self._run_cell(cell, lane_artifact)
        finally:
            self.settle(cell)

    def settle(self, cell, usd=None):
        """The attempt is over: its spend now lives in its local cell dir, or (`usd`) in the ledger.
        One step under the controller's spend lock, so `spend()` counts the attempt exactly once."""
        c = self.ctx
        with c.spend_lock:
            if usd:
                costguard.ledger_add(c.run_dir, cell, usd)
            self.running.discard(cell)
            c.remote_live.get(self.name, {}).pop(cell, None)

    def store_poll(self, live):
        with self.ctx.spend_lock:  # only cells still running here: a settled attempt is counted elsewhere
            self.ctx.remote_live[self.name] = {k: v for k, v in live.items() if k in self.running}

    def _lost_spend(self, cell, rcell, local_cell):
        """A remote attempt that left no result: keep what it spent (its `spent.json`, or the last polled value)."""
        c = self.ctx
        with tempfile.TemporaryDirectory() as tmp:
            self.rsync(f"{self.target}:{rcell}/", tmp + "/", "--include", "/spent.json", "--exclude", "*", force=True)
            path = os.path.join(tmp, "spent.json")
            usd = float(common.read_json(path)["usd"]) if os.path.isfile(path) else 0.0
        with c.spend_lock:
            usd = max(usd, c.remote_live.get(self.name, {}).get(cell, 0.0))
        self.settle(cell, usd)

    def _run_cell(self, cell, lane_artifact):
        c = self.ctx
        deadline = c.exp["deadline_s"] + MARGIN_S
        local_cell = common.cell_dir(c.run_dir, cell)
        if not self.remote:
            args = [sys.executable, os.path.join(c.lanes_dir, "bin", "lanes-cell"), c.run_dir, cell,
                    "--tasks", c.tasks, "--host", self.name]
            self.ctx.runner.run(args, deadline_s=deadline, tag=self.ctx.provider(cell))
            return os.path.isfile(os.path.join(local_cell, "result.json"))
        self.prepare(cell.split("/")[0], lane_artifact)
        costguard.retire(c.run_dir, cell, local_cell)  # an earlier attempt's partial dir: keep its spend
        rcell = os.path.join(self.root, "runs", c.exp_id, "cells", *cell.split("/"))
        pgfile = os.path.join(self.root, "runs", c.exp_id, "pgid-" + cell.replace("/", "__"))
        q = shlex.quote
        # the launcher starts a new session and records its pgid, so a stop can kill the whole group
        launch = ("import os,sys;os.setsid();open(sys.argv[1],'w').write(str(os.getpid()));"
                  "os.execvp('python3',['python3']+sys.argv[2:])")
        command = (f"rm -rf {q(rcell)} {q(pgfile)} && cd {q(self.root)} && "
                   f"KOGEN_LANES_HOME={q(self.root)} python3 -c {q(launch)} {q(pgfile)} "
                   f"lanes/bin/lanes-cell {q(os.path.join(self.root, 'runs', c.exp_id))} "
                   f"{q(cell)} --tasks {q(os.path.join(self.root, 'tasks'))} --host {q(self.name)}")
        code, _ = self.ctx.runner.run(self.ssh + [self.target, command], deadline_s=deadline, tag=self.ctx.provider(cell))
        if code in (124, 130, 255):  # deadline, stop or lost connection: the ssh client died, the remote group may not have
            kill = f"p=$(cat {q(pgfile)} 2>/dev/null) && {{ kill -TERM -- -$p; sleep 2; kill -KILL -- -$p; true; }}"
            killed = self.sh(kill, force=True)[0] == 0
            self._lost_spend(cell, rcell, local_cell)  # before the dir goes
            if killed:  # no pgid: leave the dir, never rm under a live process
                self.sh(f"rm -rf {q(rcell)} {q(pgfile)}", force=True)
            return False
        os.makedirs(local_cell, exist_ok=True)
        src = f"{self.target}:{rcell}/"
        # result.json last, and only after the rest arrived, so a cell with one is complete
        ok = self.rsync(src, local_cell + "/", "--exclude", "/result.json")[0] == 0
        if ok:
            ok = self.rsync(src, local_cell + "/", "--include", "/result.json", "--exclude", "*")[0] == 0
        self.sh(f"rm -rf {q(rcell)} {q(pgfile)}")
        return ok and os.path.isfile(os.path.join(local_cell, "result.json"))


class Context:
    def __init__(self, run_dir, tasks, lanes_dir, runner, exp):
        self.run_dir, self.tasks, self.lanes_dir, self.runner, self.exp = run_dir, tasks, lanes_dir, runner, exp
        self.remote_live = {}  # host name -> {cell: usd} polled from its running cells
        self.spend_lock = threading.Lock()  # remote_live and the ledger change together under it
        self.exp_id = exp["id"]
        self.providers = costguard.lane_providers(exp)

    def provider(self, cell):
        return self.providers.get(cell.split("/")[-1], experiment.CHATGPT)


# ---- the run loop ---------------------------------------------------------------------------

def run_all(run_dir, tasks, hosts_file, lock_cmd=None, unlock_cmd=None, lanes_dir=LANES_DIR, log=print,
            skip_preflight=False):
    """Run every unfinished cell. Returns the exit code: 0 all done, 1 some cell failed, 3 a cost or cell cap
    stopped the run, 4 a provider's rate limit left cells unstarted, 130 interrupted."""
    run_dir = os.path.abspath(run_dir)
    exp = experiment.load(os.path.join(run_dir, "experiment.json"))
    try:
        costguard.caps(exp)
        costguard.require_provider_caps(exp)
    except costguard.CostCapError as e:
        raise DispatchError(str(e)) from None
    verify_inputs(run_dir, exp, tasks)
    if not skip_preflight:
        from . import preflight  # imported here: it needs Python 3.12 (cell.py), plan and dispatch do not
        if preflight.preflight(run_dir, tasks, out=log):
            raise DispatchError("pre-flight refused a supplied Intent; no cell started")
    cells = common.read_jsonl(os.path.join(run_dir, "plan.jsonl"))
    artifacts = {e["name"]: e["artifact_sha256"] for e in common.read_json(os.path.join(run_dir, "lanes.lock.json"))}
    runner = Runner()
    started = []
    ctx = Context(run_dir, tasks, lanes_dir, runner, exp)
    hosts = [Host(n, c, ctx) for n, c in load_hosts(hosts_file, exp["hosts"]).items()]
    lanes = {l["name"]: l for l in exp["lanes"]}
    claims = Claims(run_dir, exp["deadline_s"] + MARGIN_S)
    pick, failed, mine = threading.Lock(), set(), set()
    active = {h.name: h.slots for h in hosts}
    locked = []
    capped = []  # [message] once a cap stopped the run
    limited = []  # [provider] whose rate limit left a cell unstarted
    noted = set()
    hard_hit = threading.Event()  # the hard cap, or an unreadable spend: stop every cell

    def spend():  # {provider: usd}
        with ctx.spend_lock:
            extra = {}
            for live in ctx.remote_live.values():
                for cell, usd in live.items():
                    extra[cell] = max(extra.get(cell, 0.0), usd)
            return costguard.provider_spend(run_dir, exp, extra=extra)

    def trip(message, hard=True):
        if hard_hit.is_set() or (capped and not hard):
            return
        capped[:] = [message]
        log(message)
        if hard:
            hard_hit.set()

    def refuse(c):
        """Why cell `c` may not start now (its provider's soft cap, cell cap or rate limit), else None."""
        try:
            started = costguard.started_cells(run_dir, exp)
            for m in mine:
                started.setdefault(experiment.lane_provider(lanes[m.split("/")[-1]]), set()).add(m)
            spends = spend()
            why = costguard.blocked(exp, c["lane"], spends, started, costguard.rate_limited(run_dir))
        except Exception as e:  # fail closed
            trip(f"cannot read the run's spend ({e}); stopping")
            return "unreadable spend"
        if why is None:
            return None
        provider = experiment.lane_provider(lanes[c["lane"]])
        if "rate limited" in why:
            if provider not in limited:
                limited.append(provider)
        else:
            if why.startswith("cost cap"):
                costguard.record_stop(run_dir, "soft", spends.get(provider, 0.0), provider)
            if why not in capped:
                capped.append(why)
        if why not in noted:
            noted.add(why)
            log(why)
        return why

    def poll(host):  # remote hosts: their cells' live spend, read over ssh
        fails = 0
        while not runner.stopped.is_set() and not hard_hit.is_set():
            time.sleep(1)
            if not host.running:
                continue
            try:
                host.store_poll(host.poll())
                fails = 0
            except DispatchError as e:
                fails += 1
                if fails >= 3:  # fail closed
                    trip(f"{e}; stopping every cell")

    def finished(cell):
        return os.path.isfile(os.path.join(common.cell_dir(run_dir, cell), "result.json"))

    def next_cell(host):
        with pick:
            for c in cells:
                if c["cell"] in failed or c["cell"] in mine or finished(c["cell"]):
                    continue  # `mine`: a sibling slot is running it, whatever its claim's age
                if hard_hit.is_set():
                    return None
                if refuse(c):
                    continue  # another provider's cells may still start
                if claims.take(c["cell"], host.name):
                    mine.add(c["cell"])
                    return c
        return None

    def unlock(host):
        if unlock_cmd and host in locked:
            shell_run(runner, unlock_cmd, host=host.name, name=exp["id"])

    def loop(host):
        try:
            cell_loop(host)
        finally:
            with pick:
                active[host.name] -= 1
                last = active[host.name] == 0
            if last:  # the host's last slot is done: release the host now, not when all hosts end
                unlock(host)

    def cell_loop(host):
        while not runner.stopped.is_set():
            c = next_cell(host)
            if c is None:
                return
            ok = False
            try:
                ok = host.run_cell(c["cell"], artifacts[c["lane"]])
            except DispatchError as e:
                log(f"{host.name}: {c['cell']}: {e}")
            finally:
                try:  # before the cell is released, so no sibling slot starts another of this provider first
                    reason = costguard.note_rate_limit(run_dir, exp, c["cell"])
                except Exception as e:
                    reason = None
                    log(f"{c['cell']}: cannot read its logs for a rate limit ({e})")
                if reason:
                    log(f"rate limited: {c['lane']} cell {c['cell']} ended with {reason}; no new cell of its provider starts. "
                        f"After the limit resets, delete {costguard.RATE} in the run dir and run lanes-run again")
                claims.release(c["cell"])
                with pick:
                    mine.discard(c["cell"])
            if not ok and not runner.stopped.is_set():
                failed.add(c["cell"])
                log(f"{host.name}: {c['cell']}: no result.json")

    costguard.clear_stop(run_dir)
    old = {s: signal.signal(s, lambda *_: runner.stop()) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        for h in hosts:
            if lock_cmd:
                code, out = shell_run(runner, lock_cmd, host=h.name, name=exp["id"])
                if code:
                    raise DispatchError(f"lock command failed for {h.name} ({code}): {out.strip()[-200:]}")
            locked.append(h)
        started = hosts
        threads = [threading.Thread(target=loop, args=(h,)) for h in hosts for _ in range(h.slots)]
        for t in threads:
            t.start()
        for h in hosts:
            if h.remote:
                threading.Thread(target=poll, args=(h,), daemon=True).start()
        grace_end, checked, hard_at = None, 0.0, {}  # hard_at: provider -> when its hard cap was seen
        while any(t.is_alive() for t in threads):
            time.sleep(0.1)
            if grace_end is None and time.monotonic() - checked >= 1.0:
                checked = time.monotonic()
                try:
                    for p, spent, limit in costguard.over_hard(exp, spend()):
                        if p not in hard_at:
                            costguard.record_stop(run_dir, "hard", spent, p)
                            hard_at[p] = time.monotonic()
                            msg = f"hard cost cap reached ({p}, ${limit:g}): stopping every {p} cell"
                            log(msg)
                            capped.append(msg)
                except Exception as e:  # fail closed
                    trip(f"cannot read the run's spend ({e}); stopping every cell")
            for p, t in hard_at.items():  # local cells stop themselves in the grace time; then the rest of that provider's
                if time.monotonic() >= t + CAP_GRACE_S:
                    runner.halt(p)
            if grace_end is None and hard_hit.is_set():
                grace_end = time.monotonic() + CAP_GRACE_S
            if grace_end is not None and time.monotonic() >= grace_end:
                runner.stop()
        interrupted = runner.stopped.is_set()
    finally:
        runner.stop()
        for h in locked:
            if h not in started:  # never ran a slot (lock of a later host failed): release it here
                unlock(h)
        for s, h in old.items():
            signal.signal(s, h)
    if capped:
        return 3
    if limited:
        return 4
    if interrupted:
        return 130
    return 1 if failed else 0


def run_main(argv=None):
    p = argparse.ArgumentParser(description="Run the planned cells of a run dir across hosts.")
    p.add_argument("run_dir")
    p.add_argument("--tasks", default=os.environ.get("KOGEN_LANES_TASKS"), help="private tasks folder")
    p.add_argument("--hosts", required=True, help="hosts file (JSON, operator's, private)")
    p.add_argument("--lock-cmd", help="command template run before the first cell on each host ({host}, {name})")
    p.add_argument("--unlock-cmd", help="command template run after the last cell on each host")
    p.add_argument("--lanes-dir", default=LANES_DIR, help=argparse.SUPPRESS)
    p.add_argument("--skip-preflight", action="store_true",
                   help="do not lint-approve the supplied Intents first; for tests only, never in a real run")
    a = p.parse_args(argv)
    if not a.tasks:
        p.error("--tasks or KOGEN_LANES_TASKS is required")
    try:
        return run_all(a.run_dir, a.tasks, a.hosts, a.lock_cmd, a.unlock_cmd, a.lanes_dir,
                       skip_preflight=a.skip_preflight, log=lambda m: print(m, file=sys.stderr))
    except (experiment.ExperimentError, DispatchError, plan_hashes.PlanError, OSError, ValueError) as e:
        print(f"run: {e}", file=sys.stderr)
        return 2
