#!/bin/sh
# Archive equivalence A vs B (outside timed runs). Same gate as abrun2.sh. Writes $1/eq.json.
OUT=$1; W=$HOME/work.noindex/scratch/research/work/e6d
mkdir -p "$OUT"
n=0; until [ "$(sysctl -n vm.loadavg | tr -d '{}' | awk '{print ($2 <= 24) ? 1 : 0}')" = 1 ] && [ -z "$(pgrep -f 'verify\.test|kogen-verify|verify-land|landtree-' | head -1)" ]; do n=$((n+1)); [ $n -gt 120 ] && exit 3; sleep 10; done
. $HOME/work.noindex/hostbin/kenv.sh >/dev/null 2>&1
TD=$HOME/work.noindex/scratch/research/tmp-20261105/deq; mkdir -p "$TD/go"
export PATH="$PATH:/usr/sbin:/sbin" TMPDIR="$TD/" GOTMPDIR="$TD/go"
for a in A D; do
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
a, b = rows('A'), rows('D')
diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
res = dict(entries_A=len(a), entries_D=len(b), identical_AD=not diff, n_differing_AD=len(diff), differing_AD=diff[:20])
open(out + '/eq.json', 'w').write(json.dumps(res)); print(json.dumps(res))
PY
find "$TD" -mindepth 1 -delete 2>/dev/null; rmdir "$TD" 2>/dev/null
