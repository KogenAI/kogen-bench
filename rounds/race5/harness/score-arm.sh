#!/bin/bash
# score-arm.sh LABEL ARM — score one arm snapshot (race 4 scorer config: kg-wrap, per-case sweep, jobs 2, 60 s); keep per-case results
set -e
R=$(cd "$(dirname "$0")" && pwd); L=$1; A=$2; D=$R/snapshots/$L; F=${SCORE_SOURCE:-$D/$A}; N=$(sed -n 's/^N_total=//p' "$R/COUNTS.txt"); NS=$(sed -n 's/^N_scored=//p' "$R/COUNTS.txt"); source $R/env.sh; [ -f $R/$A/.kit-env.sh ] && source $R/$A/.kit-env.sh
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
# Offline warm-up and scoring. macOS has no unprivileged hard network block;
# these proxies/flags enforce the policy while allowing the suite's local fake.
export http_proxy=http://localhost:9 https_proxy=http://localhost:9 HTTP_PROXY=http://localhost:9 HTTPS_PROXY=http://localhost:9 ALL_PROXY=http://localhost:9 all_proxy=http://localhost:9
export NO_PROXY=localhost,localhost no_proxy=localhost,localhost
export UV_OFFLINE=1
export CARGO_NET_OFFLINE=true GOPROXY=off HEX_OFFLINE=1 npm_config_offline=true NPM_CONFIG_OFFLINE=true
unset GOFLAGS
unset CARGO_HOME GOPATH GOMODCACHE GOCACHE MIX_HOME HEX_HOME BUN_INSTALL_CACHE_DIR BUN_RUNTIME_TRANSPILER_CACHE_PATH XDG_CACHE_HOME npm_config_cache RACE4_ARM_ROOT RACE3_KIT RUSTUP_HOME GOTOOLCHAIN
[ -n "$L" ] && [ -n "$A" ] || exit 2
[ ! -f "$F/PRUNED_BUILD_OUTPUT" ] || { echo "source-only snapshot $L/$A; executable scoring unavailable" >&2; exit 2; }
[ -d "$F" ] || { echo "missing snapshot $L/$A" >&2; exit 1; }
export PYTHONDONTWRITEBYTECODE=1
CASE_ARGS=()
if [ "$L" != FINAL ]; then
  SCORE_CASES=${SCORE_CASES:-$(/usr/bin/python3 "$R/scoring_config.py" --cases)}
  export SCORE_CASES
  CASE_ARGS=(--case "$SCORE_CASES")
else
  # FINAL is always the single /N_total run, even if the caller exports SCORE_CASES.
  unset SCORE_CASES
fi
W=$R/score-wd/$L-$A${SCORE_TAG:+-$SCORE_TAG}; case "$W" in "$R/score-wd/"?*) rm -rf "$W";; esac; mkdir -p $W; C=$R/score-cases/$L-$A${SCORE_TAG:+-$SCORE_TAG}; case "$C" in "$R/score-cases/"?*) rm -rf "$C";; esac; mkdir -p $C
mkdir -p "$R/out/results"
# Run on success or early exit, before removing either scoring directory.
sweep_arm() {
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - "$F" "$W" "$C" >> "$R/out/sweep.log" 2>&1 <<'PY'
import os, re, signal, subprocess, sys

roots = {os.path.abspath(p).rstrip('/') for p in sys.argv[1:]}
roots.update(os.path.realpath(p).rstrip('/') for p in sys.argv[1:])
pattern = re.compile(r'''(?:^|[\s='"])(?:''' + '|'.join(re.escape(p) for p in roots) + r''')(?=$|[/\s'"])''')
rows = subprocess.check_output(['ps', '-axo', 'pid=,ppid=,command='], text=True)
processes = {}
for row in rows.splitlines():
    fields = row.strip().split(None, 2)
    if len(fields) == 3:
        processes[int(fields[0])] = (int(fields[1]), fields[2])
# The scorer and its callers may mention these paths in their arguments.
protected = {os.getpid()}
pid = os.getppid()
while pid > 0 and pid not in protected:
    protected.add(pid)
    pid = processes.get(pid, (0, ''))[0]
cwd_rows = subprocess.run(['/usr/sbin/lsof', '-a', '-d', 'cwd', '-Fn'], text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
cwd_by_pid = {}
pid = None
for row in cwd_rows.splitlines():
    if row.startswith('p'):
        pid = int(row[1:])
    elif row.startswith('n') and pid is not None:
        cwd_by_pid[pid] = os.path.realpath(row[1:])
for pid, (_, command) in processes.items():
    cwd = cwd_by_pid.get(pid, '')
    if pid in protected or not (pattern.search(command) or any(cwd == p or cwd.startswith(p + '/') for p in roots)):
        continue
    try:
        os.kill(pid, signal.SIGKILL)
        print(f'swept {pid} cwd={cwd} command={command}')
    except ProcessLookupError:
        pass
    except PermissionError as error:
        print(f'could not sweep {pid}: {error}', file=sys.stderr)
PY
}
trap sweep_arm EXIT
if [ -x "$F/kogen" ]; then
  # warm-up (race 3 scoring config): one build-triggering ./kogen version per arm per snapshot, outside the 60 s case limit; capped at 900 s; time recorded
  w0=$(date +%s)
  set +e
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - "$F" > "$W/warmup.log" 2>&1 <<'PY'
import os, signal, subprocess, sys

warmup_env = dict(os.environ, LANG='en_US.UTF-8', LC_ALL='en_US.UTF-8')
p = subprocess.Popen(['./kogen', 'version'], cwd=sys.argv[1], env=warmup_env, start_new_session=True)
try:
    rc = p.wait(timeout=900)
except subprocess.TimeoutExpired:
    print('warm-up timed out after 900 s', file=sys.stderr)
    rc = 124
finally:
    # Also remove background children left behind after a successful warm-up.
    try:
        os.killpg(p.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    p.wait()
sys.exit(rc if rc >= 0 else 128 - rc)
PY
  wrc=$?; set -e; printf '%s\t%s\t%ss\trc=%s\t%s\n' "$L" "$A" "$(( $(date +%s)-w0 ))" "$wrc" "${SCORE_TAG:-official}" >> $R/out/warmup.tsv
  WR=$W/wrap
  printf '#!/bin/sh\nexport KG_REAL=%q\nexec /usr/bin/python3 %q "$@"\n' "$F/kogen" "$R/kg-wrap.py" > $WR; chmod +x $WR
  (cd "$F" && PYTHONDONTWRITEBYTECODE=1 $R/inputs/conformance/bin/kogen-conformance run --kogen $WR --jobs ${SCORE_JOBS:-2} "${CASE_ARGS[@]}" --timeout 60 --workdir $C --out $W/results.jsonl > $W/run.log 2>&1) || true; $R/sweep.sh $C >> $R/out/sweep.log 2>&1
  p=$(/usr/bin/python3 -c "import json,sys;r=[json.loads(l) for l in open(sys.argv[1]) if l.strip()];print(sum(1 for x in r if x.get('id') and x.get('status')=='pass'))" $W/results.jsonl 2>/dev/null || echo 0)
  if [ ! -s "$W/results.jsonl" ]; then echo "FLAG $A $L scorer produced no results ($W/run.log)" >> "$R/out/scoring-errors.txt"; exit 1; fi
  cp $W/results.jsonl $R/out/results/$L-$A${SCORE_TAG:+-$SCORE_TAG}.jsonl
else
  # Missing arm executable is an implementation failure, with one fail per case.
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - "$R" "$W/results.jsonl" <<'PY'
import json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / 'inputs/conformance'))
from kogen_conformance.runner import load_cases
# The runner owns the frozen case inventory; do not invent IDs from scores.
rows = load_cases(os.environ['SCORE_CASES'].split(',') if os.environ.get('SCORE_CASES') else None)
with open(sys.argv[2], 'w') as f:
    for row in rows:
        f.write(json.dumps({'id': row['id'], 'status': 'fail', 'reason': 'no executable ./kogen'}) + '\n')
PY
  [ $? -eq 0 ] || exit 1
  cp "$W/results.jsonl" "$R/out/results/$L-$A${SCORE_TAG:+-$SCORE_TAG}.jsonl"; p=0
fi
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 "$R/validate-results.py" "$W/results.jsonl" || { echo "FLAG $A $L incomplete or invalid scorer results" >> "$R/out/scoring-errors.txt"; exit 1; }
pe=$(/usr/bin/python3 -c "
import json,sys
ex={line.split()[0] for line in open(sys.argv[2]) if line.strip() and not line.lstrip().startswith('#')}
try: r=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
except Exception: r=[]
print(sum(1 for x in r if x.get('id') and x.get('status')=='pass' and x['id'] not in ex))" $W/results.jsonl $R/SPEC-BUG-CASES.txt 2>/dev/null || echo 0)
[ "$L" = FINAL ] || p=n/a
printf '%s\t%s\t%s/%s\texcl %s/%s\tsnapshot@%s\t%s\n' "$L" "$A" "$p" "$N" "$pe" "$NS" "$(cat $D/TAKEN_AT)" "${SCORE_TAG:-official}" >> $R/out/scores${SCORE_TAG:+-$SCORE_TAG}.tsv
sweep_arm; trap - EXIT
case "$W" in "$R/score-wd/"?*) rm -rf "$W";; esac; case "$C" in "$R/score-cases/"?*) rm -rf "$C";; esac
