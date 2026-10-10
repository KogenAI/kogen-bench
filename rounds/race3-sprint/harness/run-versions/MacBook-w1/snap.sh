#!/bin/bash
# snap.sh LABEL — instant APFS snapshot of every arm (no scoring); rewrite live paths inside the snapshot
R=$(cd "$(dirname "$0")" && pwd); L=$1; D=$R/snapshots/$L; mkdir -p $D; t0=$(/usr/bin/python3 -c "import time;print(time.time())")
for A in $(cat $R/ARMS); do mkdir -p $D/$A; for e in $R/$A/* $R/$A/.[!.]*; do b=$(basename "$e"); case "$b" in .kitcache|.git|spec|conformance) continue;; esac; [ -e "$e" ] && cp -c -p -R "$e" "$D/$A/$b" 2>/dev/null; done; grep -rIl --exclude-dir=target --exclude-dir=_build --exclude-dir=deps --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=conformance --exclude-dir=spec --exclude-dir=build "$R/$A" $D/$A 2>/dev/null | while read f; do sed -i '' "s#$R/$A#$D/$A#g" "$f"; done; done
for A in $(cat $R/ARMS); do
  for f in spec conformance; do (set -o pipefail; cd "$R/$A/$f" && find . -type f -not -path "*/__pycache__/*" -print0 | sort -z | xargs -0 shasum -a 256 | shasum -a 256 | cut -c1-16) > "$D/$A/.$f.sha" 2>/dev/null & done
  shasum -a 256 "$R/$A/TARGET.md" | cut -d' ' -f1 > "$D/$A/.target.sha"
done
wait; date -u +%T > $D/TAKEN_AT; date +%s > "$D/TAKEN_EPOCH"; dt=$(/usr/bin/python3 -c "import time,sys;print(round(time.time()-float(sys.argv[1]),1))" $t0); echo "$L $(cat $D/TAKEN_AT) copy_s=$dt" >> $R/out/snap-times.log; echo "snapshot $L at $(cat $D/TAKEN_AT) copy ${dt}s"
