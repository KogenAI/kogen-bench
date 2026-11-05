#!/usr/bin/env python3
"""Stage 0 model-free accounting replay for Lab k-review-wide-change-cost-linear.

No model calls. Ports kogen-review review/parts.go (reviewParter: cut, endBefore, maxTo, hasRoom,
reviewPartHeader) and review/material.go (source layout) to Python and replays the K-MODELS-FILE change
(git diff <base> <landed> of the public KogenAI/kogen repo) plus synthetic fixtures through each arm.

usage: replay.py <kogen clone> <out dir>
inputs: KogenAI/kogen 733363bdf04a2db673ffcaba643a0f2e0aa37b3f (base) and 408a1e46 (landed, Build 69f25f32).
"""
import bisect, hashlib, json, math, os, subprocess, sys

CEILING = 524288          # tools.InputBudgetBytes (inclusive)
PART = 6000               # MaterialPartBytes
DIGEST = PART // 2        # R1 bounded digest per part (= repairedSectionBytes)
LOGGED_WHOLE = 3096086    # k-models-file-1835.log:77
LOGGED = dict(input=12802581, cached=11016987, output=24907, usd=16.9858, parts=9)
CHECKS = "c" * 2500       # check results text (size assumed; folded into the calibration)
HEAD = "# Diff of existing/deleted paths against start HEAD 733363bd\n\n"
PARTS_HEADING = "# Full text of every added file"


def sh(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, check=True).stdout


def digest(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- fixtures
def k9(repo, base, landed):
    ns = sh(repo, "diff", "--name-status", "-z", "-M", base, landed).split(b"\0")
    rows, i = [], 0
    while i < len(ns) and ns[i]:
        st = ns[i].decode(); i += 1
        assert st[0] in "MAD", st
        rows.append((st[0], ns[i].decode())); i += 1
    files = []
    for st, p in rows:
        diff = b"" if st == "A" else sh(repo, "diff", base, landed, "--", p)
        content = b"" if st == "D" else sh(repo, "show", f"{landed}:{p}")
        obj = sh(repo, "rev-parse", f"{landed}:{p}").decode().strip() if st != "D" else "0" * 40
        files.append(dict(path=p, status={"M": "changed", "A": "added", "D": "deleted"}[st],
                          diff=diff.decode("utf-8", "replace"), content=content.decode("utf-8", "replace"), obj=obj))
    return files


def cycle(files, n):
    out = []
    for i in range(n):
        f = dict(files[i % len(files)])
        if i >= len(files):
            f["path"] = f"dup{i // len(files)}/" + f["path"]
            f["diff"] = f["diff"].replace("diff --git a/", f"diff --git a/dup{i // len(files)}/")
        out.append(f)
    return out


def tiny(n):
    out = []
    for i in range(n):
        p = f"internal/generated/component{i // 50:03d}/handler_{i:05d}.go"
        added = i % 10 == 9
        d = "" if added else (f"diff --git a/{p} b/{p}\nindex 1111111..2222222 100644\n--- a/{p}\n+++ b/{p}\n@@ -1,3 +1,3 @@\n"
                              " package generated\n-const Version = 1\n+const Version = 2\n")
        c = f"package generated\n\nconst Version = 2\n// handler {i}\n" + "x" * 300 + "\n"
        out.append(dict(path=p, status="added" if added else "changed", diff=d, content=c, obj=digest(p.encode())[:40]))
    return out


# ---------------------------------------------------------------- material (review/material.go)
def entry_json(f, keys=None):
    c = f["content"].encode()
    e = dict(path=f["path"], status=f["status"], origin="", rename=False, mode="100644", git_object=f["obj"],
             bytes=len(c), sha256=digest(c))
    if keys:
        e = {k: e[k] for k in keys}
    return json.dumps(e, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def build_source(files, legacy):
    """The parts source as bytes plus the ranges of every path's material.
    legacy=True is the pre-7a9fac6 layout (full text of every non-deleted file)."""
    out = bytearray(("# Check results of the final pass\n\n" + CHECKS + "\n\n" + HEAD).encode())
    diff_rng = {}
    for f in files:
        if f["status"] == "deleted" or not f["diff"]:
            continue
        d = f["diff"].encode()
        diff_rng[f["path"]] = (len(out), len(out) + len(d)); out += d
    out += ("\n" + (PARTS_HEADING if not legacy else "# Full text of every changed file") + "\n\n" +
            "Added files appear here with their mode; changed files have hunks in the diff.\n\n").encode()
    file_rng, blocks = {}, []
    for f in files:
        p = f["path"]
        if f["status"] == "deleted":
            ent = f"--- {p} (deleted)"
        elif legacy:
            ent = f"--- {p}\n{f['content']}"
        elif f["status"] == "added":
            ent = f"--- {p} (added; mode 100644)\n{f['content']}"
            if f["content"] and not f["content"].endswith("\n"):
                ent += "\n\\ No newline at end of file"
        else:
            ent = f"--- {p} (changed; hunks in diff)"
        e = ent.encode()
        full_text = (legacy and f["status"] != "deleted") or f["status"] == "added"
        file_rng[p] = (len(out), len(out) + len(e) + 1)
        if full_text:
            blocks.append(dict(start=len(out), end=len(out) + len(e)))
        out += e + b"\n"
    for p, (a, b) in diff_rng.items():
        blocks.append(dict(start=a, end=b))
    blocks.sort(key=lambda s: s["start"])
    ranges = []                                 # per catalog path: its diff range and parts-entry range
    for f in files:
        r = []
        if f["path"] in diff_rng:
            r.append(diff_rng[f["path"]])
        r.append(file_rng[f["path"]])
        ranges.append(r)
    return bytes(out), blocks, ranges


# ---------------------------------------------------------------- the parter (review/parts.go)
REPAIRED_HEAD_NOTE = 0


class Parter:
    """mode: R0 | R1 | R3 | R0p (4c421b7, unlanded). All share cut/endBefore/maxTo."""

    def __init__(self, source, blocks, ranges, files, stable, mode):
        self.source, self.blocks, self.ranges, self.files, self.stable, self.mode = source, blocks, ranges, files, stable, mode
        self.sum = digest(source)
        self.entries = [entry_json(f) for f in files]
        self.slim = [entry_json(f, ("path", "status")) for f in files]
        self.catalog = "[" + ",".join(self.entries) + "]"
        # for the slice-local modes: ranges flattened, sorted by start
        flat = sorted((a, b, i) for i, rs in enumerate(ranges) for (a, b) in rs)
        self.fa, self.fb, self.fi = [x[0] for x in flat], [x[1] for x in flat], [x[2] for x in flat]
        self.maxlen = max((b - a for a, b, _ in flat), default=0)

    def carried(self, frm, to):
        lo = bisect.bisect_left(self.fa, frm - self.maxlen - 1)
        hi = bisect.bisect_left(self.fa, to)
        hit = set()
        for j in range(lo, hi):
            if self.fa[j] < to and self.fb[j] > frm:
                hit.add(self.fi[j])
        return sorted(hit)

    def header(self, k, n, frm, to):
        total = len(self.source)
        top = (f"# Review part {k} of {n}\n\nThis part carries bytes [{frm}, {to}) of the {total} bytes of the candidate's complete review "
               f"source (SHA-256 {self.sum}); the other parts carry the rest, in order.\n\n# Check results of the final pass\n\n{CHECKS}\n\n")
        tail = f"# Source part {k} of {n}\n\n"
        dig = ""
        if self.mode == "R1" and k > 1:
            dig = "# Digest of earlier parts\n\n" + "d" * (DIGEST - len("# Digest of earlier parts\n\n") - 2) + "\n\n"
        if self.mode in ("R0", "R1"):
            mid = f"# Every changed path\n\n{self.catalog}\n\n"
        elif self.mode == "R3":
            hit = set(self.carried(frm, to))
            items = [self.entries[i] if i in hit else self.slim[i] for i in range(len(self.files))]
            mid = "# Changed paths (this part's slice in full, others path and status)\n\n[" + ",".join(items) + "]\n\n"
        else:  # R0p: slice entries in full, the rest only counted; the complete catalog is a retained file
            if len(self.catalog.encode()) <= PART:
                mid = f"# Every changed path\n\n{self.catalog}\n\n"
            else:
                hit = self.carried(frm, to)
                mid = ("# Changed paths of this part\n\n[" + ",".join(self.entries[i] for i in hit) + "]\n\n" +
                       f"The other {len(self.files) - len(hit)} of the {len(self.files)} changed paths are not listed here. Their complete catalog, with the same fields, "
                       f"is retained at /run/executor-review/review-1-catalog.json; `git diff --name-status 733363bd 408a1e46` lists every changed path too.\n\n")
        return (top + mid + dig + tail).encode()

    def prompt(self, k, n, frm, to):
        return self.stable + 4 + len(self.header(k, n, frm, to)) + (to - frm)

    def mandatory(self):
        return self.prompt(1, 1, 0, 0)

    def has_room(self):
        return CEILING - self.mandatory() >= PART

    def max_to(self, k, n, frm):
        if self.prompt(k, n, frm, frm) > CEILING:
            return -1
        lo, hi = frm, len(self.source)
        while lo < hi:
            mid = lo + (hi - lo + 1) // 2
            if self.prompt(k, n, frm, mid) <= CEILING:
                lo = mid
            else:
                hi = mid - 1
        return lo

    def end_before(self, k, n, frm, limit):
        for b in self.blocks:
            if b["start"] < limit < b["end"] and b["start"] > frm and b["end"] <= self.max_to(k + 1, n, b["start"]):
                return b["start"]
            if b["end"] == limit and b["start"] >= frm:
                return limit
        i = self.source.rfind(b"\n", frm, limit)
        if i >= 0:
            return i + 1
        to = limit
        while to > frm + 1 and (self.source[to] & 0xC0) == 0x80:
            to -= 1
        return to

    def cut_assuming(self, n):
        cuts, frm = [], 0
        while frm < len(self.source):
            k = len(cuts) + 1
            limit = self.max_to(k, n, frm)
            if limit <= frm:
                raise RuntimeError(f"part {k} has no room for source: its complete prompt without source is {self.prompt(k, n, frm, frm)} bytes")
            to = limit if limit >= len(self.source) else self.end_before(k, n, frm, limit)
            cuts.append((frm, to)); frm = to
        return cuts

    def cut(self):
        digits, n = 1, 9
        while True:
            cuts = self.cut_assuming(n)
            if len(str(len(cuts))) <= digits:
                return cuts
            digits, n = digits + 1, n * 10 + 9


def account(source, blocks, ranges, files, stable, mode):
    c = Parter(source, blocks, ranges, files, stable, mode)
    mand = c.mandatory()
    res = dict(mandatory_first_part=mand, room_for_source_after_mandatory=CEILING - mand, source_bytes=len(source),
               catalog_bytes=len(c.catalog.encode()), paths=len(files))
    if not c.has_room():
        res.update(sends=False, stop="context_budget_exceeded: mandatory prompt leaves %d B (< %d B) for source under the %d-byte ceiling; nothing sent"
                   % (CEILING - mand, PART, CEILING))
        return res
    try:
        cuts = c.cut()
    except RuntimeError as e:
        res.update(sends=False, stop="context_budget_exceeded: " + str(e))
        return res
    n = len(cuts)
    reqs = [c.prompt(k + 1, n, a, b) for k, (a, b) in enumerate(cuts)]
    slices = [b - a for a, b in cuts]
    res.update(sends=True, parts=n, request_bytes=reqs, slice_bytes=slices, total_input=sum(reqs),
               nonsource_per_part=[r - s for r, s in zip(reqs, slices)], room_left=[CEILING - r for r in reqs],
               ratio_total_to_source=round(sum(reqs) / len(source), 3))
    # growth of request k beyond a bounded digest: bytes of request k that depend on earlier requests, less the digest bound.
    # R0/R3/R0p: nothing from earlier requests (the repaired-paths section only appears when a part repaired a file, bounded at PART//2 = digest).
    dep = [0] * n
    if mode == "R1":
        dep = [0] + [DIGEST] * (n - 1)
    res["dependent_bytes"] = dep
    res["growth_beyond_digest"] = [max(0, d - DIGEST) for d in dep]
    return res


def account_r2(source, files, stable, read=PART):
    """R2 on_demand as a lane patch on the external route: one session; first prompt = authority + checks + catalog + manifest;
    every pinned 6,000-byte part covering a changed hunk is read by one ranged read (required_parts); each read is a request that
    re-sends the whole context. Counts every request (the first prompt and each read)."""
    catalog = "[" + ",".join(entry_json(f) for f in files) + "]"
    manifest = []
    for f in files:
        hunks = [l for l in f["diff"].split("\n") if l.startswith("@@")]
        if f["status"] == "added":
            n = f["content"].count("\n") or 1
            hunks = [f"@@ -0,0 +1,{n} @@"]
        manifest.append({"diff_stat": {"added": 0, "deleted": 0},
                         "hunks": [{"old_start": 0, "old_count": 1, "new_start": 1, "new_count": 1, "header": h[:60]} for h in hunks]})
    man = json.dumps(manifest, separators=(",", ":"))
    required = math.ceil(len(source) / read)          # reads covering hunks, upper bound = all of the source
    mand = stable + 4 + len(("# Review part 1 of 1\n\n" + CHECKS + "\n\n# Every changed path\n\n" + catalog + "\n\n# Manifest\n\n" + man +
                             "\n\n# required_parts\n\n" + json.dumps(list(range(required)))).encode())
    res = dict(mandatory_first_part=mand, room_for_source_after_mandatory=CEILING - mand, source_bytes=len(source),
               catalog_bytes=len(catalog.encode()), manifest_bytes=len(man.encode()), paths=len(files), required_reads=required, read_bytes=read)
    if mand > CEILING - PART:
        res.update(sends=False, stop="context_budget_exceeded: mandatory prompt %d B leaves %d B under the ceiling; nothing sent" % (mand, CEILING - mand))
        return res
    call = 300                                            # per-read tool call/result envelope bytes (assumed)
    ctx = [mand + k * (read + call) for k in range(required + 1)]
    res.update(sends=True, parts=1, requests=len(ctx), request_bytes_first=ctx[:3], request_bytes_last=ctx[-1], total_input=sum(ctx),
               ratio_total_to_source=round(sum(ctx) / len(source), 3), nonsource_per_part=[mand], room_left_first=CEILING - mand,
               room_left_last=CEILING - ctx[-1], dependent_bytes_last=ctx[-1] - mand, growth_beyond_digest_max=max(0, ctx[-1] - mand - DIGEST))
    if ctx[-1] > CEILING:
        res["window_overrun_at_request"] = next(i for i, c in enumerate(ctx) if c > CEILING) + 1
    return res


REGISTERED = ("K9", "C6", "C9", "C12", "T4000")


def gates(arm_by_fix):
    out = {}
    for arm, fx in arm_by_fix.items():
        sending = [r for k, r in fx.items() if k in REGISTERED and r.get("sends")]
        all_send = len(sending) == len(REGISTERED)
        ratios = {k: r["ratio_total_to_source"] for k, r in fx.items() if k in REGISTERED and r.get("sends")}
        g1 = all(v <= 3.0 for v in ratios.values()) and all(fx[k].get("sends") for k in REGISTERED if k != "T4000")
        g2 = all((max(r["growth_beyond_digest"]) if "growth_beyond_digest" in r else r["growth_beyond_digest_max"]) == 0 for r in sending) and bool(sending)
        g3 = bool(fx["T4000"].get("sends"))
        out[arm] = dict(gate1_total_le_3x=g1, gate2_growth_zero=g2, gate3_thousands_send=g3, survives=g1 and g2 and g3,
                        ratios_registered=ratios)
    return out


def tokens(parts_bytes, k9_legacy_bytes, sessions_new, b=3.5):
    """Same-Build token estimate. Calibrate turns per session T and extra uncached E from the logged totals, then scale to an arm."""
    p_log = sum(k9_legacy_bytes) / b
    t_minus_1 = LOGGED["cached"] / p_log
    uncached_log = LOGGED["input"] - LOGGED["cached"]
    extra = uncached_log - p_log
    p_new = sum(parts_bytes) / b
    cached = t_minus_1 * p_new
    uncached = p_new + extra * sessions_new / len(k9_legacy_bytes)
    w_log, w_new = uncached_log + 0.1 * LOGGED["cached"], uncached + 0.1 * cached
    return dict(bytes_per_token=b, turns_per_session=round(t_minus_1 + 1, 2), uncached=round(uncached), cached=round(cached),
                total_input=round(uncached + cached), usd_scaled=round(LOGGED["usd"] * w_new / w_log, 2))


def main(repo, out):
    base = sh(repo, "rev-parse", "733363b").decode().strip()
    landed = sh(repo, "rev-parse", "408a1e46").decode().strip()
    real = k9(repo, base, landed)
    # calibration: stable (authority + task + constraints) so that the one-session legacy prompt is the logged 3,096,086 bytes
    lsrc, _, _ = build_source(real, True)
    stable = LOGGED_WHOLE - 4 - len(lsrc)

    def parts_at(n, legacy):
        fl = cycle(real, n)
        s_, b_, r_ = build_source(fl, legacy)
        a = account(s_, b_, r_, fl, stable, "R0")
        return a.get("parts", 0)

    def paths_for(N, legacy):          # smallest path count (K9's path sizes cycled) whose cut has at least N parts
        lo, hi = 20, 2000
        while lo < hi:
            mid = (lo + hi) // 2
            if parts_at(mid, legacy) >= N:
                hi = mid
            else:
                lo = mid + 1
        # the cut can jump over N (a block no longer fits): the smallest count with at least N parts is kept and its parts recorded
        return lo

    cn = {N: paths_for(N, False) for N in (6, 9, 12)}      # current cut (7a9fac6) yields N parts
    ln = {N: paths_for(N, True) for N in (6, 12)}          # legacy cut (733363b) yields N parts
    fixtures = {"K9": real, "C6": cycle(real, cn[6]), "C9": cycle(real, cn[9]), "C12": cycle(real, cn[12]),
                "T1000": tiny(1000), "T2000": tiny(2000), "T4000": tiny(4000), "T8000": tiny(8000)}
    legfix = {"L6": cycle(real, ln[6]), "K9": real, "L12": cycle(real, ln[12])}
    result = dict(calibration=dict(legacy_source_bytes=len(lsrc), stable_bytes=stable, logged_whole=LOGGED_WHOLE,
                                   paths=len(real), diff_bytes=sum(len(f["diff"].encode()) for f in real),
                                   changed_texts=sum(len(f["content"].encode()) for f in real if f["status"] == "changed"),
                                   added_texts=sum(len(f["content"].encode()) for f in real if f["status"] == "added")))
    result["fixture_paths"] = {"K9": len(real), **{f"C{N}": n for N, n in cn.items()}, **{f"L{N}": n for N, n in ln.items()},
                               "T1000": 1000, "T2000": 2000, "T4000": 4000, "T8000": 8000}
    leg = {}
    for name, fl in legfix.items():
        s, bl, rg = build_source(fl, True)
        leg[name] = account(s, bl, rg, fl, stable, "R0")
    result["legacy_733363b"] = leg
    arms = {}
    for arm in ("R0", "R1", "R3", "R0p"):
        arms[arm] = {}
        for name, fl in fixtures.items():
            s, bl, rg = build_source(fl, False)
            arms[arm][name] = account(s, bl, rg, fl, stable, arm)
    arms["R2"], arms["R2-b64k"] = {}, {}
    for name, fl in fixtures.items():
        s, _, _ = build_source(fl, False)
        arms["R2"][name] = account_r2(s, fl, stable)
        arms["R2-b64k"][name] = account_r2(s, fl, stable, 65536)    # sensitivity: reads batched to 64 KB
    result["arms"] = arms
    result["gates"] = gates({k: v for k, v in arms.items() if k != "R0p"})
    result["gates_R0p_informational"] = gates({"R0p": arms["R0p"]})["R0p"]
    lk = leg["K9"]
    tok = {}
    for b in (3.0, 3.5, 4.0):
        tok[f"legacy_b{b}"] = tokens(lk["request_bytes"], lk["request_bytes"], lk["parts"], b)
        for arm in ("R0", "R1", "R3", "R0p"):
            a = arms[arm]["K9"]
            tok[f"{arm}_b{b}"] = tokens(a["request_bytes"], lk["request_bytes"], a["parts"], b)
    result["token_estimate_K9"] = tok
    result["logged"] = LOGGED
    result["pins"] = dict(kogen_base=base, kogen_landed=landed, kogen_review="b33665f2509d24ec2f6e48b73ce49ca66671add6",
                          kogen_build="81a609a3aa9622a9c766bce222e39357b1ca2031", kogen_review_parked="4c421b724f654c109e94b2124b8cdc18e0c28304")
    os.makedirs(out, exist_ok=True)
    json.dump(result, open(os.path.join(out, "results.json"), "w"), indent=1)
    print(json.dumps(dict(fixture_paths=result["fixture_paths"], legacy_parts=lk.get("parts"), legacy_total=lk.get("total_input"), gates=result["gates"], r0p=result["gates_R0p_informational"]), indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
