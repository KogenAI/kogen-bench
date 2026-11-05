"""kontext-matched-2 API pre-screen (cheap pre-screen only; does not drop cases). Adapted from stfill C_run.py (unchanged prompt, flags, scoring); only paths, case list and cap differ.
Original doc: Experiment C (stfill) on st: packet-only localization over the Anthropic API (no tools, no repo access).
Per case x arm (A: issue + bounded failure; B: A + frozen evidence packet) x 2 reps, one claude-sonnet-5-5 call (effort medium) asking for up to 6 ranked
repo-relative file paths to edit. Scored model-free against the files in the case's reference.patch: recall, precision, first-hit.
Key read by this program from ~/kogen-home-optimum/.kogen/credentials/anthropic.json, never printed. Cap USD 2.
Usage: python3 -I C_run.py KITDIR OUT.jsonl"""
import json, os, re, subprocess, sys, time, hashlib, urllib.request, urllib.error
K, OUT = sys.argv[1], sys.argv[2]
CAP, spent = 2.0, 0.0
key = json.load(open(os.path.expanduser("~/kogen-home-optimum/.kogen/credentials/anthropic.json")))["api_key"]
BIN = os.path.join(K, "bin", "kogen-context-build-evidence")
assert hashlib.sha256(open(BIN, "rb").read()).hexdigest().startswith("59ee239c2abf"), "binary pin"
P = (2.0, 2.5, 0.20, 10.0)
PROMPT = """You cannot read files or run commands. Using only the issue and failing output{ev} below, reply with ONLY a JSON object:
{{"files": ["relative/path", ...]}}
listing at most 6 repository-relative file paths, ranked most-likely first, that the fix must edit (source files, not tests). No prose, no code fences.

ISSUE:
{issue}

--- failure ---
{failure}
--- end failure ---
{packet}"""
def bound(t, n=4000):
    d = t.encode()
    if len(d) <= n: return t
    m = f"\n[... truncated {len(d)-n} bytes ...]\n".encode(); h = max((n - len(m)) // 2, 0)
    return (d[:h].decode("utf-8", "ignore").encode() + m + d[len(d)-h:].decode("utf-8", "ignore").encode())[:n].decode("utf-8", "ignore")
def call(prompt):
    body = {"model": "claude-sonnet-5-5", "max_tokens": 1500, "output_config": {"effort": "medium"}, "messages": [{"role": "user", "content": prompt}]}
    r = urllib.request.Request("https://api.anthropic.com/v1/messages", json.dumps(body).encode(),
        {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try: return json.load(urllib.request.urlopen(r, timeout=180))
    except urllib.error.HTTPError as e: raise RuntimeError(f"HTTP {e.code}: {e.read()[:200].decode(errors='replace')}")
for case in ["axios","gin405","kogen","faker","axios4731","bat2201","bat2650","tokio6752","jekyll9141","gin3741","gin3820"]:
    cd = os.path.join(K, "kit", "cases", case)
    issue = open(cd + "/brief.txt", errors="replace").read()
    diag = open(os.path.join(K, "q", case + "-base", "diagnostic.txt"), errors="replace").read()
    failure = bound(diag.split("\n---\n", 1)[-1])
    ref = sorted({re.sub(r"^b/", "", m.group(1)) for m in re.finditer(r"^\+\+\+ (\S+)", open(cd + "/reference.patch", errors="replace").read(), re.M)})
    t0 = time.time()
    pk = subprocess.run([BIN, "evidence", "--repo", cd + "/base", "--brief", cd + "/brief.txt", "--failure", os.path.join(K, "q", case + "-base", "diagnostic.txt"),
                         "--deadline", "1s", "--bytes", "6500", "--ranges", "6"], capture_output=True, text=True, timeout=15)
    packet = pk.stdout; pwall = round(time.time() - t0, 2)
    for rep in (1, 2):
        for arm in (("A", "B") if rep == 1 else ("B", "A")):
            if spent >= CAP * 0.9: print("STOP near cap"); sys.exit(2)
            ev = arm == "B"
            prompt = PROMPT.format(ev=" and evidence packet" if ev else "", issue=issue, failure=failure,
                                   packet=("\nSource evidence packet from the local retrieval tool follows as complete JSON.\n\n" + packet) if ev else "")
            row = dict(case=case, arm=arm, rep=rep, reference=ref, packet_bytes=len(packet.encode()) if ev else 0, packet_wall_s=pwall if ev else None, packet_rc=pk.returncode if ev else None)
            try:
                r = call(prompt); u = r["usage"]
                usage = dict(input=u.get("input_tokens", 0), write=u.get("cache_creation_input_tokens") or 0, read=u.get("cache_read_input_tokens") or 0, out=u.get("output_tokens", 0))
                c = (usage["input"]*P[0] + usage["write"]*P[1] + usage["read"]*P[2] + usage["out"]*P[3]) / 1e6; spent += c
                text = "".join(b.get("text", "") for b in r["content"] if b.get("type") == "text")
                m = re.search(r"\{.*\}", text, re.S)
                files = [f.lstrip("./") for f in json.loads(m.group(0)).get("files", [])][:6] if m else []
                hit = [f for f in files if f in ref]
                row.update(files=files, usage=usage, cost=round(c, 6), recall=len(set(hit)) / len(ref), precision=(len(hit) / len(files)) if files else 0.0,
                           first_hit=(files[0] in ref) if files else False, hit_rank=next((i + 1 for i, f in enumerate(files) if f in ref), None))
            except Exception as e:
                row["error"] = f"{type(e).__name__}: {str(e)[:200]}"
            print(json.dumps(row), flush=True); open(OUT, "a").write(json.dumps(row) + "\n"); time.sleep(1)
print("TOTAL_SPENT", round(spent, 4))
