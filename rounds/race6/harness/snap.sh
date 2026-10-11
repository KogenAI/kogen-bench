#!/bin/bash
# snap.sh LABEL [ARM] — APFS copy of selected arms, without scoring.
set -e
R=$(cd "$(dirname "$0")" && pwd); L=${1:?label required}; ONLY=${2:-}
case "$L" in *[!A-Za-z0-9+_-]*|'') echo 'invalid snapshot label' >&2; exit 2;; esac
if command -v shasum >/dev/null; then SHA=(shasum -a 256); else SHA=(sha256sum); fi
ARMS=$(cat "$R/ARMS")
if [ -n "$ONLY" ]; then
  case " $ARMS " in *" $ONLY "*) ARMS=$ONLY;; *) echo 'unknown arm' >&2; exit 2;; esac
fi
D=$R/snapshots/$L; mkdir -p "$D" "$R/out"
t0=$(/usr/bin/python3 -c 'import time;print(time.time())')
/usr/bin/python3 - "$D" "$t0" <<'PYCODE'
import datetime, sys
from pathlib import Path
root = Path(sys.argv[1]); instant = float(sys.argv[2])
(root / 'TAKEN_AT').write_text(datetime.datetime.fromtimestamp(instant, datetime.timezone.utc).isoformat().replace('+00:00', 'Z') + '\n')
(root / 'TAKEN_EPOCH').write_text(str(int(instant)) + '\n')
PYCODE
held=''
: > "$D/STOPPED_ARMS"
trap '[ -z "$held" ] || rmdir "$held"' EXIT
for A in $ARMS; do
  # Periodic snapshots cease for a stopped arm; FINAL still captures every arm.
  case "$L" in T+*) if [ -f "$R/STOP-$A" ]; then echo "$A" >> "$D/STOPPED_ARMS"; continue; fi;; esac
  lock_path=$R/out/snap-lock-$A
  until mkdir "$lock_path" 2>/dev/null; do sleep 0.1; done
  held=$lock_path
  case "$L" in T+*) if [ -f "$R/STOP-$A" ]; then echo "$A" >> "$D/STOPPED_ARMS"; rmdir "$held"; held=''; continue; fi;; esac
  mkdir -p "$D/$A"
  date +%s > "$D/$A/.taken_epoch"
  for e in "$R/$A"/* "$R/$A"/.[!.]*; do
    b=$(basename "$e"); case "$b" in .kitcache|.git|spec|conformance) continue;; esac
    [ ! -e "$e" ] || if [ "$(uname -s)" = Darwin ]; then cp -c -p -R "$e" "$D/$A/$b"; else cp -p -R "$e" "$D/$A/$b"; fi
  done
  grep -rIl --exclude-dir=target --exclude-dir=_build --exclude-dir=deps --exclude-dir=node_modules --exclude-dir=.venv --exclude-dir=.git --exclude-dir=conformance --exclude-dir=spec --exclude-dir=build "$R/$A" "$D/$A" 2>/dev/null | while IFS= read -r f; do if [ "$(uname -s)" = Darwin ]; then sed -i '' "s#$R/$A#$D/$A#g" "$f"; else sed -i "s#$R/$A#$D/$A#g" "$f"; fi; done
  for f in spec; do
    (set -o pipefail; cd "$R/$A/$f" && find . -type f -not -path '*/__pycache__/*' -print0 | sort -z | xargs -0 "${SHA[@]}" | "${SHA[@]}" | cut -c1-16) > "$D/$A/.$f.sha"
  done
  "${SHA[@]}" "$R/$A/INTERFACE.md" | cut -d' ' -f1 > "$D/$A/.interface.sha"
  "${SHA[@]}" "$R/$A/TARGET.md" | cut -d' ' -f1 > "$D/$A/.target.sha"
  rmdir "$held"; held=''
done
touch "$D/SNAPSHOT_COMPLETE"
/usr/bin/python3 - "$R" "$D" "$L" <<'PYDISK'
from pathlib import Path
import shutil, sys, time
root, snap = map(Path, sys.argv[1:3]); usage = shutil.disk_usage(root)
(snap/'DISK_FREE_BYTES').write_text(str(usage.free)+'\n')
with (root/'out/disk-usage.tsv').open('a') as stream:
    stream.write(f'{int(time.time())}\t{sys.argv[3]}\t{usage.total}\t{usage.used}\t{usage.free}\n')
PYDISK
dt=$(/usr/bin/python3 -c 'import time,sys;print(round(time.time()-float(sys.argv[1]),1))' "$t0")
echo "$L $(cat "$D/TAKEN_AT") copy_s=$dt" >> "$R/out/snap-times.log"
echo "snapshot $L at $(cat "$D/TAKEN_AT") copy ${dt}s"
