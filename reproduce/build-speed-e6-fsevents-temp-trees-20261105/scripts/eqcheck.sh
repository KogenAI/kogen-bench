#!/bin/sh
# Archive equivalence A vs B (outside timed runs). Same gate as abrun2.sh. Writes $1/eq.json.
OUT=$1; W=$HOME/work.noindex/scratch/research/work/e6
mkdir -p "$OUT"
n=0; until [ "$(sysctl -n vm.loadavg | tr -d '{}' | awk '{print ($2 <= 24) ? 1 : 0}')" = 1 ] && [ -z "$(pgrep -f 'verify\.test|kogen-verify|verify-land|landtree-' | head -1)" ]; do n=$((n+1)); [ $n -gt 120 ] && exit 3; sleep 10; done
. $HOME/work.noindex/hostbin/kenv.sh >/dev/null 2>&1
TD=$HOME/work.noindex/scratch/research/tmp-20261105/eq; mkdir -p "$TD/go"
export PATH="$PATH:/usr/sbin:/sbin" TMPDIR="$TD/" GOTMPDIR="$TD/go" KOGEN_PACKAGE_STORE=$W/store
for a in A B C; do
  ( cd $W/k$a && sh packaging/package.sh > "$OUT/eq-$a.path" 2> "$OUT/eq-$a.err" ); echo "$a rc=$?" >> "$OUT/eq.log"
done
python3 -I - "$OUT" <<'PY'
import sys, tarfile, hashlib, json
out = sys.argv[1]
def rows(a):
    path = open('%s/eq-%s.path' % (out, a)).read().strip().splitlines()[-1]
    r = {}
    with tarfile.open(path, 'r:gz') as tf:
        for m in tf:
            key = m.name.split('/', 1)[1] if '/' in m.name else ''
            if key in ('lib/VERSION', 'lib/VERSION.json'): continue
            if m.isfile(): d = hashlib.sha256(tf.extractfile(m).read()).hexdigest()
            elif m.issym(): d = 'link:' + m.linkname
            else: d = ''
            r[key] = (('d' if m.isdir() else 'f' if m.isfile() else 'l'), oct(m.mode & 0o7777), d)
    return r
a, b, c = rows('A'), rows('B'), rows('C')
diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
diffc = sorted(k for k in set(a) | set(c) if a.get(k) != c.get(k))
res = dict(entries_A=len(a), entries_B=len(b), entries_C=len(c), identical_AB=not diff, n_differing_AB=len(diff), differing_AB=diff[:20], identical_AC=not diffc, n_differing_AC=len(diffc))
open(out + '/eq.json', 'w').write(json.dumps(res)); print(json.dumps(res))
PY
find "$TD" -mindepth 1 -delete 2>/dev/null; rmdir "$TD" 2>/dev/null
