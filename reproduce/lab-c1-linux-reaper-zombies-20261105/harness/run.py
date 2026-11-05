#!/usr/bin/env python3
"""Lab C1: run one unit under one arm, record pass/fail, wall seconds and orphans left.

usage: run.py <config.json> <arm A|B|C> <unit> <rep> <outdir>
units: shaping, verification, loop (each repo's go-test check), sweep (kogen-verification's
orphan-sweep tests on the helper's own source), fixture (R-20261103-X-V1 residual fixture).
"""
import json, os, re, signal, subprocess, sys, time

FLAG = "--kogen-verification-acceptance-reaper"
CHECKS = {
    "shaping": ("kogen-shaping", "GOFLAGS=-trimpath go test ./..."),
    "verification": ("kogen-verification", "GOFLAGS=-trimpath go test ./..."),
    "loop": ("kogen-loop", "go test ./..."),
}
SWEEP_RUN = "go test -count=1 -v -run 'Sweep|Orphan|Detached|Acceptance|Reap|ClimbLauncher' ./verify/"
GUARD_S = 1500  # harness safety stop only; go test's own 10 m timeout is unchanged


def shq(s):
    return "'" + s.replace("'", "'\\''") + "'"


def procs(uid):
    out = []
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            if os.stat("/proc/" + d).st_uid != uid:
                continue
            stat = open("/proc/%s/stat" % d, "rb").read()
            i = stat.rindex(b")")
            f = stat[i + 2:].split()
            comm = stat[stat.index(b"(") + 1:i].decode(errors="replace")
            try:
                env = open("/proc/%s/environ" % d, "rb").read().split(b"\0")
            except OSError:
                env = []
            try:
                cmd = open("/proc/%s/cmdline" % d, "rb").read().replace(b"\0", b" ").decode(errors="replace")[:160]
            except OSError:
                cmd = ""
            out.append(dict(pid=int(d), state=f[0].decode(), ppid=int(f[1]), pgid=int(f[2]), comm=comm, env=env, cmd=cmd))
        except (OSError, ValueError):
            continue
    return out


def main():
    cfg = json.load(open(sys.argv[1]))
    arm, unit, rep, outdir = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    os.makedirs(outdir, exist_ok=True)
    runid = "c1r2-%s-%s-%s-%s-%d" % (cfg["host"], unit, arm, rep, int(time.time()))
    src, W = cfg["src"], cfg["work"]
    env = dict(os.environ)
    for k in ("GOFLAGS", "GOROOT", "GOPATH"):
        env.pop(k, None)
    env.update(PATH=cfg["gobin"] + ":" + cfg["nodebin"] + ":/usr/local/bin:/usr/bin:/bin", GOTOOLCHAIN="local",
               GOCACHE=cfg["gocache"], TMPDIR=cfg["tmp"], C1RUN=runid, GOL=os.path.join(W, "xv1", "gol", "launch"))
    pidfile = os.path.join(outdir, "fixture-pids.txt")
    if unit in CHECKS:
        repo, cmd = CHECKS[unit]
        cwd = os.path.join(src, repo)
        subprocess.run(["go", "clean", "-testcache"], cwd=cwd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif unit == "sweep":
        cwd = os.path.join(src, "kv-b" if arm == "B" else "kv-a")
        cmd = SWEEP_RUN
    elif unit == "fixture":
        cwd = os.path.join(W, "fixture")
        cmd = "sh ./fixture.sh " + shq(pidfile)
    else:
        sys.exit("unknown unit " + unit)
    helper = {"A": cfg["helper_a"], "B": cfg["helper_b"], "C": None}[arm]
    script = cmd if helper is None else "exec %s %s %s" % (shq(helper), FLAG, shq(cmd))
    load1 = open("/proc/loadavg").read().split()[0]
    log = open(os.path.join(outdir, "output.log"), "wb")
    t0 = time.time()
    p = subprocess.Popen(["/bin/sh", "-c", script], cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                         start_new_session=True)
    guard = False
    try:
        rc = p.wait(timeout=GUARD_S)
    except subprocess.TimeoutExpired:
        guard = True
        os.killpg(p.pid, signal.SIGKILL)
        rc = p.wait()
    wall = time.time() - t0
    log.close()
    time.sleep(1.5)
    uid = os.getuid()
    fpids = {}
    if os.path.exists(pidfile):
        for line in open(pidfile):
            a = line.split()
            if len(a) == 2 and a[0].isdigit():
                fpids[int(a[0])] = a[1]
    marker = ("C1RUN=" + runid).encode()
    left = []
    for q in procs(uid):
        if q["pid"] == os.getpid():
            continue
        tag = None
        if marker in q["env"]:
            tag = "marker"
        elif q["pid"] in fpids and "sleep" in q["cmd"]:
            tag = "fixture-" + fpids[q["pid"]]
        if tag:
            left.append(dict(pid=q["pid"], ppid=q["ppid"], pgid=q["pgid"], state=q["state"], tag=tag, cmd=q["cmd"]))
    # Clean up only this run's own leftovers: their process groups when every member is ours, else the pid.
    mine = {x["pid"] for x in left}
    allp = procs(uid)
    for g in sorted({x["pgid"] for x in left if x["state"] not in ("Z", "X")}):
        members = {q["pid"] for q in allp if q["pgid"] == g}
        try:
            if members <= mine:
                os.killpg(g, signal.SIGKILL)
            else:
                for x in left:
                    if x["pgid"] == g:
                        os.kill(x["pid"], signal.SIGKILL)
        except ProcessLookupError:
            pass
    text = open(os.path.join(outdir, "output.log"), "rb").read().decode(errors="replace")
    fails = re.findall(r"^\s*--- FAIL: (\S+)", text, re.M)
    pkgfail = re.findall(r"^FAIL\s+(\S+)", text, re.M)
    timeout_panic = bool(re.search(r"panic: test timed out after", text))
    zprobe = (re.search(r"^ZPROBE (PASS|FAIL).*$", text, re.M) or [None])[0]
    exprow = re.findall(r"^EXPROW (\S+) (\S+)", text, re.M)
    res = dict(runid=runid, host=cfg["host"], arm=arm, unit=unit, rep=rep, rc=rc, passed=(rc == 0 and not guard), wall_s=round(wall, 2),
               start=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)), end=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0 + wall)),
               load1_before=float(load1), guard_stop=guard, fail_tests=fails[:20], fail_pkgs=pkgfail[:20], timeout_panic=timeout_panic,
               zprobe=zprobe, xv1=exprow, fixture_servers=len(fpids),
               orphans_alive=sum(1 for x in left if x["state"] not in ("Z", "X")), orphans_zombie=sum(1 for x in left if x["state"] in ("Z", "X")),
               orphans=left[:30], cwd=cwd, command=cmd, helper=helper)
    json.dump(res, open(os.path.join(outdir, "result.json"), "w"), indent=1)
    print("%s %s %s rep%s rc=%s wall=%.1fs orphans=%d/%dz fails=%s %s %s" % (cfg["host"], unit, arm, rep, rc, wall, res["orphans_alive"], res["orphans_zombie"],
          ",".join(fails[:4]), zprobe or "", " ".join("%s:%s" % e for e in exprow)))


if __name__ == "__main__":
    main()
