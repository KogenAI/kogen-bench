#!/usr/bin/env python3
"""Lab prelanding: build the n=48 sample (8 breakers + 40 seeded known-good landings).
Read-only on the delivery mirrors and land logs. Run: python3 -I build_sample.py  (writes sample.json, sample.tsv)."""
import json, os, random, re, subprocess, datetime as dt, glob

MD = os.environ.get("MIRRORS_DIR", "mirrors")
LAND = os.environ.get("LAND_LOGS", "land-logs")
OUT = os.path.dirname(os.path.abspath(__file__))
SEED = 20261105
BREAKERS = ["8852812", "10f190b", "91d0a32", "f04edce", "aeeb5be", "f4b7f54", "1e795ed", "bc5b726"]
REL = [("9bf6073f", "2026-11-03T00:12:04Z"), ("6e69ffb3", "2026-11-03T12:23:36Z"),
       ("41d70052", "2026-11-03T20:20:18Z"), ("d98cfe01", "2026-11-04T20:31:32Z")]
GOODREL = {"41d70052", "d98cfe01"}
COMPS = ["kogen-loop", "kogen-coordinator", "kogen-verification", "kogen-shaping", "kogen-build",
         "kogen-executor", "kogen-setup", "kogen-review"]
P = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def g(repo, *a):
    return subprocess.run(["git", "--git-dir", f"{MD}/{repo}.git", *a], capture_output=True, text=True).stdout


def anc(repo, a, b):
    return subprocess.run(["git", "--git-dir", f"{MD}/{repo}.git", "merge-base", "--is-ancestor", a, b],
                          capture_output=True).returncode == 0


# release pins (same method as the report's cycle.py)
pins = {}
for r, _ in REL:
    gm = g("kogen", "show", f"{r}:cli/go.mod"); lp = g("kogen", "show", f"{r}:cli/loop-pin.json")
    p = {}
    for c in COMPS:
        if c == "kogen-loop":
            m = re.search(r'"source_head":\s*"([0-9a-f]+)"', lp); p[c] = m.group(1) if m else None
        else:
            m = re.search(r'github.com/KogenAI/' + c + r'\s+v\S*-([0-9a-f]{12})', gm); p[c] = m.group(1) if m else None
    pins[r] = p

# land logs -> landings
landings = []
for f in sorted(glob.glob(LAND + "/*.log")):
    t = open(f, errors="replace").read()
    m = re.search(r"^== (\S+) onto (kogen-[a-z]+|kogen) main (\w+) on (\S+) (\d\d:\d\dZ)", t, re.M)
    d = re.search(r"^(\S+Z) \S+: done \(landed:([0-9a-f]+)\)", t, re.M)
    if not (m and d):
        continue
    repo = m.group(2)
    if repo not in COMPS:
        continue
    cc = re.search(r"^consumer check.*$", t, re.M)
    kg = re.search(r"^consumer kogen(?:@(\w+) mode=(\w+) rc=(\d+)|: (skipped.*))$", t, re.M)
    cons = re.findall(r"^consumer ([\w-]+)(?:@\w+ mode=\w+ rc=\d+|: skipped.*)$", t, re.M)
    landings.append(dict(log=os.path.basename(f), repo=repo, slug=m.group(1), sha7=d.group(2), done=d.group(1),
                         consumer_check=cc.group(0) if cc else "(no consumer-check line)",
                         kogen_consumer=(kg.group(0) if kg else "(kogen not listed as a consumer)"),
                         green="GREEN: landing" in t))

# resolve full sha, first release
rows = []
for L in landings:
    full = g(L["repo"], "rev-parse", "--verify", "-q", L["sha7"] + "^{commit}").strip()
    if not full:
        L["full"] = None; L["first_release"] = "unresolved"; rows.append(L); continue
    L["full"] = full
    L["subject"] = g(L["repo"], "log", "-1", "--format=%s", full).strip()
    L["first_release"] = None
    for r, t in REL:
        pin = pins[r][L["repo"]]
        if not pin:
            continue
        pf = g(L["repo"], "rev-parse", "--verify", "-q", pin + "^{commit}").strip()
        if pf and anc(L["repo"], full, pf):
            L["first_release"] = r; break
    rows.append(L)

# landing-time kogen main (first-parent, last commit with committer time <= landing done time)
kog = [l.split() for l in g("kogen", "log", "--first-parent", "main", "--format=%H %cI").splitlines()]
kog = [(h, P(c).astimezone(dt.timezone.utc)) for h, c in kog]  # newest first


def kogen_at(done):
    t = P(done)
    for h, c in kog:
        if c <= t:
            return h
    return None


for L in rows:
    L["kogen_main"] = kogen_at(L["done"])

by7 = {}
for L in rows:
    by7.setdefault(L["sha7"], L)
miss = [b for b in BREAKERS if b not in by7]
assert not miss, miss
breakers = [by7[b] for b in BREAKERS]
for b in breakers:
    b["role"] = "breaker"

bset = {b["full"] for b in breakers}
elig = [L for L in rows if L.get("full") and L["first_release"] in GOODREL and L["full"] not in bset and L["green"]]
elig.sort(key=lambda L: (L["done"], L["repo"], L["full"]))
rng = random.Random(SEED)
good = rng.sample(elig, 40)  # draw order is kept: a prefix of the run is itself a random sample
for L in good:
    L["role"] = "good"

sample = breakers + good
json.dump(dict(seed=SEED, eligible=len(elig), releases=dict(REL), pins=pins, sample=sample),
          open(OUT + "/sample.json", "w"), indent=1)
with open(OUT + "/sample.tsv", "w") as f:
    f.write("n\trole\trepo\tsha7\tfull\tdone\tkogen_main\tfirst_release\tlog\tconsumer_check\n")
    for i, L in enumerate(sample, 1):
        f.write("\t".join([str(i), L["role"], L["repo"], L["sha7"], L["full"], L["done"], L["kogen_main"][:12],
                           str(L["first_release"]), L["log"], L["consumer_check"]]) + "\n")
print("landings", len(rows), "eligible", len(elig), "sample", len(sample))
print("distinct kogen mains", len({L['kogen_main'] for L in sample}))
from collections import Counter
print(Counter(L["repo"] for L in good))
print(Counter(L["consumer_check"][:60] for L in good))
