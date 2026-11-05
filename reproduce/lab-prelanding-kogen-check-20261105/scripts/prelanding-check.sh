#!/bin/bash
# prelanding-check.sh <component-repo> <component-sha> <kogen-base-sha> <outdir> [pin|base]
# The unconditional kogen consumer check (Lab lab-prelanding-kogen-check-20261105). Model-free.
#   pin  (default): scratch copy of kogen at <kogen-base-sha>, pin <component-sha> exactly as delivery's adopt-pins-lib.sh does
#                   (sync-kogen-loop + module rename for kogen-loop, go get for the rest, go mod tidy), then
#                   gofmt -l, go build, go vet, go test (cli/, the adoption's own "go" step).
#   base: the same without the pin, to tell new failures from old ones (STOP_AFTER=vet ends it after go vet).
#   basetests <idsfile>: on the unpinned kogen base run only the tests named in idsfile (lines pkg.Test, or pkg.<package> for a whole
#                   package), `go test -run`: "the same test also passes without the pin" at a fraction of the full suite's time.
# Writes <outdir>/result.json. Needs: MIRRORS (dir holding kogen.git and <component>.git), HB (hostbin with kenv.sh, heavy.sh),
# LAB_TMP (scratch root for GOMODCACHE/TMPDIR). Never writes to the mirrors; never commits.
# Steps copied from ~/Areas/Kogen/delivery/bin/adopt-pins-lib.sh (sync_loop, pin_protocol, pins) and adopt-steps.tsv ("go" row).
set -u
repo=$1; sha=$2; base=$3; out=$4; mode=${5:-pin}; idsfile=${6:-}
LABD=$(cd "$(dirname "$0")" && pwd)
MIRRORS=${MIRRORS:-$HOME/work.noindex/mirrors}; HB=${HB:-$HOME/work.noindex/hostbin}
LAB_TMP=${LAB_TMP:-$HOME/work.noindex/scratch/research/work/prelanding}
mkdir -p "$out" "$LAB_TMP/tmp"
wipe() { [ -d "$1" ] && { find "$1" -mindepth 1 -delete; rmdir "$1"; }; true; }  # scratch dirs only, never rm -r on a variable
wipe "$out/tree"; wipe "$out/loop-src"
. "$HB/kenv.sh"
export TMPDIR=$LAB_TMP/tmp/ GOTMPDIR=$LAB_TMP/tmp/go GOMODCACHE=$LAB_TMP/gomodcache GOFLAGS="-mod=mod -p=2" GIT_TERMINAL_PROMPT=0
mkdir -p "$GOTMPDIR" "$GOMODCACHE"
GO=go; tree=$out/tree
t0=$(date +%s); T=$t0
st() { echo "$1" >> "$out/steps.txt"; }
: > "$out/steps.txt"
tick() { local n=$(date +%s); echo "$1 $((n-T))" >> "$out/times.txt"; T=$n; }
: > "$out/times.txt"
fin() { # fin <status> <detail>
  python3 - "$out" "$1" "$2" "$repo" "$sha" "$base" "$mode" "$(( $(date +%s) - t0 ))" "$idsfile" <<'EOP'
import json, os, re, sys
out, status, detail, repo, sha, base, mode, wall, idsfile = sys.argv[1:]
rd = lambda f: open(os.path.join(out, f), errors="replace").read() if os.path.exists(os.path.join(out, f)) else ""
times = {l.split()[0]: int(l.split()[1]) for l in rd("times.txt").splitlines() if l.strip()}
tests = rd("go-test.out"); fails = sorted(set(re.findall(r"^--- FAIL: (\S+)", tests, re.M)))
pk = sorted(set(re.findall(r"^FAIL[ \t]+(\S+)", tests, re.M)))
pk_ok = re.findall(r"^ok\s+(\S+)", tests, re.M)
# a failing test is identified as <package>.<test>: go test prints "FAIL <pkg>" after the "--- FAIL" lines of that package
ids = []; cur = []
for l in tests.splitlines():
    m = re.match(r"--- FAIL: (\S+)", l)
    if m: cur.append(m.group(1)); continue
    m = re.match(r"FAIL\s+(\S+)", l)
    if m:
        pkg = m.group(1); ids += [pkg + "." + t for t in cur] if cur else [pkg + ".<package>"]; cur = []
        continue
    if re.match(r"(ok|\?)\s+\S+", l): cur = []
tested = {}
if mode == "basetests" and os.path.exists(idsfile):
    for i in open(idsfile).read().split():
        tested[i] = "fail" if i in ids else "pass"
res = dict(repo=repo, sha=sha, kogen_base=base, mode=mode, status=status, detail=detail, wall_s=int(wall), times_s=times,
           failed_ids=sorted(set(ids)), tested=tested, packages_ok=len(pk_ok), packages_failed=len(pk),
           steps=rd("steps.txt").split())
json.dump(res, open(os.path.join(out, "result.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ("status", "detail", "wall_s")}), flush=True)
EOP
}
# 1. scratch copy of kogen main as of <base>
git clone -q --no-checkout "$MIRRORS/kogen.git" "$tree" >"$out/clone.out" 2>&1 && git -C "$tree" checkout -q --detach "$base" >>"$out/clone.out" 2>&1 \
  || { fin red "clone/checkout of kogen $base failed: $(tail -1 "$out/clone.out")"; exit 0; }
tick clone
if [ "$mode" = pin ]; then
# ---- pin step (adopt-pins-lib.sh) ----
pin_protocol() { local f=$1/cli/loop-pin.json
  grep -q '^  "protocol": ".*" *+ *"' "$f" 2>/dev/null || return 0
  perl -i -pe 'if (/^  "protocol": /) { 1 while s/" *\+ *"//; }' "$f" && echo "sync: loop-pin.json protocol joined: $(grep '"protocol"' "$f" | tr -d ' ')"
  python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$f"; }
sync_loop() { local d=$1 ls=$2 lm sy=$1/packaging/sync-kogen-loop.sh t rc
  lm=$(awk '$1=="module"{print $2; exit}' "$ls/go.mod" 2>/dev/null)
  if [ -n "$lm" ] && [ "$lm" != kogen-loop ] && grep -qF "'^module kogen-loop\$'" "$sy"; then
    t=$d/packaging/.sync-kogen-loop.renamed.sh
    LM=$lm perl -pe 's/\^module kogen-loop\$/^module $ENV{LM}\$/; s/"module": "kogen-loop"/"module": "$ENV{LM}"/' "$sy" > "$t"
    (cd "$d" && sh "$t" "$ls"); rc=$?; rm -f "$t"; [ $rc = 0 ] && echo "sync: accepted renamed loop module $lm"; [ $rc = 0 ] && pin_protocol "$d"; return $rc
  fi
  (cd "$d" && sh "$sy" "$ls") && pin_protocol "$d"; }
pin_loop() { # pin_loop <loop sha>: vendored loop copy (sync-kogen-loop) + module rename, as the adoption does for kogen-loop
  local ls=$out/loop-src; wipe "$ls"
  git clone -q "$MIRRORS/kogen-loop.git" "$ls" && git -C "$ls" checkout -q --detach "$1" && sync_loop "$tree" "$ls" >"$out/sync.out" 2>&1 \
    || { fin red "PIN sync-kogen-loop failed: $(tail -2 "$out/sync.out" 2>/dev/null | tr '\n' ' ')"; return 1; }
  RENAMED=$(bash "$LABD/loop-module-rename.sh" "$tree/cli" 2>"$out/rename.err") || { fin red "PIN loop module rename failed: $(tail -1 "$out/rename.err")"; return 1; }
  echo "$RENAMED" >> "$out/renamed.txt"; }
if [ -n "${TUPLE:-}" ]; then
  # DIAGNOSTIC arm B-tuple (not the registered arm B): pin every component of the tuple file ("repo sha" lines, loop first), as one
  # adoption window does, instead of the landed commit alone
  while read -r r s; do
    [ -z "$r" ] && continue
    if [ "$r" = kogen-loop ]; then pin_loop "$s" || exit 0
    else (cd "$tree/cli" && $GO get "github.com/KogenAI/$r@$s") >>"$out/goget.out" 2>&1 || { fin red "PIN go get $r failed: $(tail -3 "$out/goget.out" | tr '\n' ' ')"; exit 0; }; fi
  done < "$TUPLE"
elif [ "$repo" = kogen-loop ]; then
  pin_loop "$sha" || exit 0
else
  # DIAGNOSTIC (LOOPALIGN=1, not part of the registered arm B): first move the vendored loop to the version the pinned component
  # requires, as the adoption tuple does, so a post-rename component is not tested against a pre-rename kogen main
  if [ "${LOOPALIGN:-}" = 1 ]; then
    req=$(git --git-dir="$MIRRORS/$repo.git" show "$sha:go.mod" 2>/dev/null | awk '$1=="github.com/KogenAI/kogen-loop"{print $2; exit}')
    lfull=$(git --git-dir="$MIRRORS/kogen-loop.git" rev-parse -q --verify "${req##*-}^{commit}" 2>/dev/null)
    echo "loopalign: component requires loop ${req:-none} -> ${lfull:-none}" >> "$out/steps.txt"
    [ -n "$lfull" ] && { pin_loop "$lfull" || exit 0; }
  fi
  (cd "$tree/cli" && $GO get "github.com/KogenAI/$repo@$sha") >"$out/goget.out" 2>&1 || { fin red "PIN go get failed: $(tail -3 "$out/goget.out" | tr '\n' ' ')"; exit 0; }
fi
(cd "$tree/cli" && $GO mod tidy) >"$out/tidy.out" 2>&1 || { fin red "PIN go mod tidy failed: $(tail -3 "$out/tidy.out" | tr '\n' ' ')"; exit 0; }
git -C "$tree" add -A >/dev/null 2>&1
tick pin
fi
# ---- the adoption's "go" step: gofmt -l, build, vet, test ----
cd "$tree/cli" || exit 1
if [ "$mode" = basetests ]; then
  python3 - "$idsfile" "$out" "$tree" <<'EOP'
import sys, collections
ids, out, tree = sys.argv[1:]; by = collections.OrderedDict()
for i in open(ids).read().split():
    pkg, _, t = i.rpartition("."); by.setdefault(pkg, []).append(t)
lines = ["cd %s/cli && date +%%s > %s/test-start" % (tree, out), ": > %s/go-test.out" % out, "rc=0"]
for pkg, ts in by.items():
    run = "" if "<package>" in ts else " -run '^(%s)$'" % "|".join(sorted(set(ts)))
    lines.append("GOFLAGS=-trimpath go test %s%s >> %s/go-test.out 2>&1 || rc=1" % (pkg, run, out))
lines.append("echo $rc > %s/go-test.rc" % out)
open(out + "/go-test.sh", "w").write("\n".join(lines) + "\n")
EOP
  tw=$(date +%s); sh "$HB/heavy.sh" "$out/go-test.sh" >/dev/null 2>&1; ts=$(cat "$out/test-start" 2>/dev/null || echo "$tw"); te=$(date +%s)
  echo "lockwait $((ts-tw))" >> "$out/times.txt"; echo "test $((te-ts))" >> "$out/times.txt"
  fin basetests "ran the named tests on the unpinned base"; exit 0
fi
f=$(gofmt -l . 2>&1); echo "$f" > "$out/gofmt.out"; tick gofmt
if [ -n "$f" ]; then fin red "gofmt -l lists: $(echo "$f" | head -3 | tr '\n' ' ')"; exit 0; fi
[ "${PIN_ONLY:-}" = 1 ] && { fin pin-only "pinned, gofmt clean"; exit 0; }   # preparation: no suite
$GO build ./... >"$out/build.out" 2>&1 || { tick build; fin red "go build failed: $(grep -v '^#' "$out/build.out" | head -2 | tr '\n' ' ')"; exit 0; }
tick build
$GO vet ./... >"$out/vet.out" 2>&1 || { tick vet; fin red "go vet failed: $(grep -v '^#' "$out/vet.out" | head -2 | tr '\n' ' ')"; exit 0; }
tick vet
[ "${STOP_AFTER:-}" = vet ] && { fin green "build and vet passed (stopped before tests)"; exit 0; }
# go test through heavy.sh (shared exclusive Go lock: delivery's suites go first); wall of the wait is recorded apart from the run
cat > "$out/go-test.sh" <<EOC
cd $tree/cli && date +%s > $out/test-start && GOFLAGS=-trimpath go test ./... > $out/go-test.out 2>&1; echo \$? > $out/go-test.rc
EOC
tw=$(date +%s)
sh "$HB/heavy.sh" "$out/go-test.sh" >/dev/null 2>&1
ts=$(cat "$out/test-start" 2>/dev/null || echo "$tw"); te=$(date +%s)
echo "lockwait $((ts-tw))" >> "$out/times.txt"; echo "test $((te-ts))" >> "$out/times.txt"
rc=$(cat "$out/go-test.rc" 2>/dev/null || echo 99)
if [ "$rc" = 0 ]; then fin green "build, vet, test passed"; else fin red "go test rc=$rc"; fi
