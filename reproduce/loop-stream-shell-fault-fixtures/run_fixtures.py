#!/usr/bin/python3 -I
"""Run kogen-loop against the fakeprov scenarios, one at a time. usage: run_fixtures.py WORK LOOPBIN FAKEBIN SCEN.json name[:deadline] ...
No model calls: provider chatgpt with KOGEN_PROVIDER_URL pointing at the local fake. Fake credentials only."""
import json, os, subprocess, sys, time, signal, tempfile
work, loopbin, fakebin, scenp = sys.argv[1:5]
names = sys.argv[5:]
os.makedirs(work, exist_ok=True)
import socket
LOCAL = socket.gethostbyname("localhost")  # this machine's loopback address
port_f = os.path.join(work, "port"); log_f = os.path.join(work, "fake.jsonl")
fake = None
if not os.path.exists(port_f):
    fake = subprocess.Popen([fakebin, "-log", log_f, "-port", port_f, "-scenarios", scenp], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    for _ in range(100):
        if os.path.exists(port_f): break
        time.sleep(0.1)
port = open(port_f).read().strip()
open(os.path.join(work, "fake.pid"), "w").write(str(fake.pid if fake else ""))
def one(spec):
    name, _, dl = spec.partition(":")
    deadline = int(dl) if dl else 900
    d = os.path.join(work, name); os.makedirs(d + "/hm/.kogen/credentials", exist_ok=True); os.makedirs(d + "/root", exist_ok=True)
    json.dump({"client_id": "oaiapp_fixture", "access_token": "fixture-token", "refresh_token": "fixture-refresh", "expires_at": int(time.time()) + 86400*30},
              open(d + "/hm/.kogen/credentials/chatgpt.json", "w"))
    os.chmod(d + "/hm/.kogen/credentials/chatgpt.json", 0o600)
    task = {"protocol": "kogen-loop/v1", "root": d + "/root", "role": {"provider": "chatgpt", "model": "fake-model", "effort": "medium"},
            "instructions": "", "prompt": "fixture " + name, "tools": ["shell"], "protected": [], "excluded": [], "terminal": [],
            "deadline_seconds": deadline, "session": {"dir": "", "resume": False}, "requires": []}
    json.dump(task, open(d + "/task.json", "w"))
    env = {"PATH": "/usr/bin:/bin", "HOME": d + "/hm", "KOGEN_PROVIDER_URL": f"http://{LOCAL}:{port}"}
    import urllib.request
    urllib.request.urlopen(f"http://{LOCAL}:{port}/_set/{name}").read()
    t0 = time.time()
    p = subprocess.Popen([loopbin, "run", "--task", d + "/task.json"], stdout=subprocess.PIPE, stderr=open(d + "/stderr.txt", "w"),
                         env=env, start_new_session=True, stdin=subprocess.DEVNULL)
    open(d + "/loop.pgid", "w").write(str(p.pid))
    ev = open(d + "/events.jsonl", "w")
    for line in p.stdout:
        ev.write(json.dumps({"t": round(time.time() - t0, 3), "e": json.loads(line)}) + "\n"); ev.flush()
    rc = p.wait(); wall = time.time() - t0
    # leftover processes in the loop's session/group
    left = subprocess.run(["pgrep", "-g", str(p.pid), "-c"], capture_output=True, text=True).stdout.strip()
    sess_left = subprocess.run(["pgrep", "-s", str(p.pid), "-c"], capture_output=True, text=True).stdout.strip()
    summ = {"scenario": name, "exit": rc, "wall_s": round(wall, 2), "left_in_group": left, "left_in_session": sess_left}
    last_err = None; attempts = []; tools = []
    for l in open(d + "/events.jsonl"):
        r = json.loads(l); e = r["e"]
        if e["type"] == "error": last_err = {"t": r["t"], "class": e.get("class"), "reason": e.get("reason"), "detail": str(e.get("detail"))[:200]}
        if e["type"] == "request.attempt":
            rec = e.get("record", {})
            attempts.append({"t": r["t"], "n": e.get("n"), "outcome": rec.get("outcome"), "status": rec.get("http_status", rec.get("status")), "keys": sorted(rec.keys())[:0]})
        if e["type"] in ("tool.call", "tool.result"): tools.append({"t": r["t"], "type": e["type"], "len": len(json.dumps(e))})
        if e["type"] == "round.ended": summ["round_ended"] = {"t": r["t"], "ending": e.get("ending")}
        if e["type"] == "session.ended": summ["session_ended"] = {"t": r["t"], "status": e.get("status"), "exit": e.get("exit")}
    summ.update(error=last_err, attempts=attempts, tool_events=tools, stderr_tail=open(d + "/stderr.txt").read()[-300:])
    open(os.path.join(work, "summary.jsonl"), "a").write(json.dumps(summ) + "\n")
    # kill anything the fixture left in its session (own group only, recorded pgid)
    if sess_left not in ("", "0"):
        subprocess.run(["pkill", "-KILL", "-s", str(p.pid)])
    print(json.dumps({k: summ[k] for k in ("scenario", "exit", "wall_s")}), flush=True)
for spec in names: one(spec)
