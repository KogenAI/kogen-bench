#!/usr/bin/env bash
# One explicit Codex task cell. Requires bench's manual device login.
set -euo pipefail
plan_file=${BENCH_PLAN:-}
cell_id=${BENCH_CELL:-}
positional=()
while (( $# )); do
  case $1 in
    --plan) (( $# >= 2 )) || { echo '--plan requires a file' >&2; exit 2; }; plan_file=$2; shift 2 ;;
    --cell) (( $# >= 2 )) || { echo '--cell requires an id' >&2; exit 2; }; cell_id=$2; shift 2 ;;
    --*) echo "unknown option: $1" >&2; exit 2 ;;
    *) positional+=("$1"); shift ;;
  esac
done
if (( ${#positional[@]} != 4 )); then
  echo 'usage: run-lane.sh TASK_ID RUN_ID MODEL EFFORT [--plan PLANFILE --cell CELL_ID]' >&2; exit 2
fi
task=${positional[0]} run_id=${positional[1]} model=${positional[2]} effort=${positional[3]}
[[ $task =~ ^[a-zA-Z0-9][a-zA-Z0-9-]*$ && $run_id =~ ^[a-zA-Z0-9][a-zA-Z0-9_.-]*$ ]] || exit 2
[[ $model =~ ^[a-zA-Z0-9][a-zA-Z0-9_.-]*$ && $effort =~ ^(low|medium|high|xhigh|max)$ ]] || exit 2
[[ $EUID == 0 ]] || { echo 'Run with sudo to launch the bench systemd slice' >&2; exit 1; }
ROOT=/srv/bh/bench
KIT=$ROOT/kits/current
capture_failures=()
capture() {
  local label=$1 status
  shift
  if timeout --signal=KILL 15 "$@"; then return 0; else status=$?; fi
  capture_failures+=("$label")
  printf 'Capture failed (%s, status %s); continuing to patch and grade\n' "$label" "$status" >&2
  return 0
}
capture_value() {
  local label=$1 target=$2 value status
  shift 2
  if value=$(timeout --signal=KILL 15 "$@"); then
    printf -v "$target" '%s' "$value"
  else
    status=$?
    printf -v "$target" '%s' ''
    capture_failures+=("$label")
    printf 'Capture failed (%s, status %s); continuing to patch and grade\n' "$label" "$status" >&2
  fi
  return 0
}
plan_json=''
if [[ -n $plan_file || -n $cell_id ]]; then
  [[ -n $plan_file && -n $cell_id && -r $plan_file ]] || { echo 'BENCH_PLAN/--plan and BENCH_CELL/--cell must both be provided' >&2; exit 2; }
  plan_json=$(python3 "$KIT/reproduce/lane-plan.py" --plan "$plan_file" --cell "$cell_id" --task "$task" --model "$model" --effort "$effort") || exit 2
fi
exec 9>"$ROOT/launch.lock"
flock -n 9 || { echo 'Another benchmark launch is active' >&2; exit 1; }
if systemctl list-units --type=service --state=running --no-legend 'bench-*.service' | grep -q .; then
  echo 'A benchmark service is already running' >&2; exit 1
fi
TD=$KIT/tasks/$task
[[ -f $KIT/.complete && -f $TD/task.json && -f $TD/prompt.md ]] || { echo 'Task kit or public prompt unavailable' >&2; exit 1; }
[[ -d /home/bench/.codex ]] || { echo 'Run codex login --device-auth as the bench user first' >&2; exit 1; }
/usr/local/bin/bench-disk-floor "$ROOT"
WORK=$ROOT/work/$run_id
RESULT=$ROOT/results/$run_id
[[ ! -e $WORK && ! -e $RESULT ]] || { echo 'Run ID already exists' >&2; exit 1; }
bundle=$(python3 - "$TD/task.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); print(d.get('base_bundle') or '')
PY
)
base=$(python3 - "$TD/task.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); print(d.get('base_sha') or '')
PY
)
[[ $bundle == _bases/* && -f $KIT/tasks/$bundle && $base =~ ^[0-9a-f]{40}$ ]] || { echo 'Bundled base unavailable' >&2; exit 1; }
if [[ -n $plan_json ]]; then
  python3 - "$plan_json" "$TD/task.json" "$base" <<'PY'
import json,sys
plan=json.loads(sys.argv[1]); task=json.load(open(sys.argv[2])); base=sys.argv[3]
expected=plan.get('base_revision',{})
if isinstance(expected,dict): expected=expected.get('hash')
expected=expected or plan.get('base_sha')
if expected and expected != base: raise SystemExit('base revision does not match plan cell')
expected_repo=plan.get('base_repo')
actual_repo=task.get('base_repo')
if isinstance(expected_repo,str) and expected_repo and actual_repo and expected_repo != actual_repo: raise SystemExit('base repository does not match plan cell')
PY
fi
expected=$(python3 - "$TD/task.json" <<'PY'
import json,sys
print(json.load(open(sys.argv[1]))['base_bundle_sha256'])
PY
)
[[ $(sha256sum "$KIT/tasks/$bundle" | cut -d' ' -f1) == "$expected" ]] || { echo 'Base bundle SHA-256 mismatch' >&2; exit 1; }
mkdir -p "$WORK" "$RESULT"
capture_value cell-start-utc cell_start_utc date -u +%Y-%m-%dT%H:%M:%S.%NZ
capture timing-cell-start python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" cell start
capture timing-setup-start python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" setup start
capture timing-plan-start python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" plan start
if [[ -n $plan_json ]]; then
  if ! printf '%s\n' "$plan_json" > "$RESULT/plan.json"; then capture_failures+=(plan-file); fi
else
  if ! printf '{}\n' > "$RESULT/plan.json"; then capture_failures+=(plan-file); fi
fi
capture timing-plan-end python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" plan end
capture boundary-start python3 "$KIT/reproduce/lane-sample.py" "$RESULT/boundary-samples.json" start "${BENCH_CELL_SECONDS:-3600}" "$RESULT/plan.json"
capture timing-shape-start python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" shape start
git clone -q "$KIT/tasks/$bundle" "$WORK/repo"
git -C "$WORK/repo" checkout -q "$base"
install -m 0644 "$TD/prompt.md" "$WORK/prompt.md"
capture timing-shape-end python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" shape end
chown -R bench:bench "$WORK" "$RESULT"
capture timing-setup-end python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" setup end
source "$KIT/reproduce/host-pins.lock"
BIN=$KIT/reproduce/sandbox-profile.sh
PATH_PINNED=/srv/bh/bench/toolchains/go-1.27.1/bin:/srv/bh/bench/toolchains/rust-1.97.1/bin:/srv/bh/bench/toolchains/bun-1.4.2/bin:/srv/bh/bench/toolchains/gleam-1.18.1/bin:/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/opt/bench/mise/installs/node/24.20.0/bin:/opt/bench/mise/installs/ruby/3.4.8/bin:/srv/bh/bench/toolchains/python-3.14.7/bin:/opt/bench/tools/bin:/usr/bin:/bin
capture launch-snapshot env PATH="$PATH_PINNED" python3 "$KIT/reproduce/lane-snapshot.py" "$RESULT/launch-snapshot.json" "$KIT" "${BENCH_EGRESS_ALLOW:-}" "${BENCH_VENUE:-}" "${BENCH_ACCOUNT_CLASS:-}"
EGRESS_SOCKET=$WORK/.egress.sock
proxy_args=(--socket "$EGRESS_SOCKET" --log "$RESULT/egress.jsonl"
  --socket-uid "$(id -u bench)" --socket-gid "$(id -g bench)")
if [[ -n ${BENCH_EGRESS_ALLOW:-} ]]; then
  [[ -f $BENCH_EGRESS_ALLOW && -r $BENCH_EGRESS_ALLOW ]] || {
    echo 'BENCH_EGRESS_ALLOW must name a readable host allowlist file' >&2; exit 1;
  }
  proxy_args+=(--allow-file "$BENCH_EGRESS_ALLOW")
fi
/usr/bin/python3 "$KIT/reproduce/egress-proxy.py" "${proxy_args[@]}" \
  >"$RESULT/egress-proxy.stderr" 2>&1 &
proxy_pid=$!
cleanup_proxy() {
  kill "$proxy_pid" 2>/dev/null || true
  for _ in {1..50}; do
    jobs -pr | grep -Fxq "$proxy_pid" || break
    sleep 0.1
  done
  if jobs -pr | grep -Fxq "$proxy_pid"; then kill -KILL "$proxy_pid" 2>/dev/null || true; fi
  wait "$proxy_pid" 2>/dev/null || true
}
trap cleanup_proxy EXIT
for _ in {1..50}; do
  [[ -S $EGRESS_SOCKET ]] && break
  kill -0 "$proxy_pid" 2>/dev/null || { cat "$RESULT/egress-proxy.stderr" >&2; exit 1; }
  sleep 0.1
done
[[ -S $EGRESS_SOCKET ]] || { echo 'Egress proxy did not create its socket' >&2; exit 1; }
stall=false
stall_seconds=${BENCH_STALL_SECONDS:-600}
[[ $stall_seconds =~ ^[1-9][0-9]*$ ]] || { echo 'BENCH_STALL_SECONDS must be a positive integer' >&2; exit 2; }
cell_seconds=${BENCH_CELL_SECONDS:-3600}
[[ $cell_seconds =~ ^[1-9][0-9]*$ ]] || { echo 'BENCH_CELL_SECONDS must be a positive integer' >&2; exit 2; }
set +e
capture timing-develop-start python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" develop start
systemd-run --quiet --collect --wait --pipe --slice=bench.slice --unit="bench-$run_id" \
  --uid=bench --gid=bench -p UMask=0002 -p KillMode=control-group -p TasksMax=4096 \
  /usr/bin/env PATH="$PATH_PINNED" HOME=/home/bench CODEX_HOME=/home/bench/.codex \
  PYTHONPATH=/srv/bh/bench/toolchains/python-3.14.7/lib/python3.14/site-packages \
  GOPROXY=off GOTOOLCHAIN=local CARGO_NET_OFFLINE=true RUSTUP_HOME=/opt/bench/rustup \
  "$BIN" agent "$WORK" "$EGRESS_SOCKET" -- /opt/bench/tools/bin/codex exec --skip-git-repo-check \
  --json --model "$model" --config "model_reasoning_effort=$effort" \
  --dangerously-bypass-approvals-and-sandbox -C /work/repo \
  "$(cat "$TD/prompt.md")" > "$RESULT/codex.jsonl" 2> "$RESULT/codex.stderr" &
runner_pid=$!
watchdog_rc=0
python3 "$KIT/reproduce/lane_watchdog.py" "$RESULT/codex.jsonl" "$RESULT/stall.json" \
  "$stall_seconds" "$runner_pid" "bench-$run_id" "$cell_seconds" "$RESULT/timeout.json" || watchdog_rc=$?
if (( watchdog_rc == 10 )); then stall=true; fi
timed_out=false
if (( watchdog_rc == 11 )); then timed_out=true; fi
wait "$runner_pid"
rc=$?
set -e
capture timing-develop-end python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" develop end
capture timing-gate-start python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" gate start
cleanup_proxy
trap - EXIT
patch_error=""
if ! timeout --signal=KILL 315 "$KIT/reproduce/lane-patch.sh" "$base" "$KIT/tasks/$bundle" "$WORK/repo" "$RESULT/patch.diff"; then
  patch_error='patch extraction failed; see runner stderr'
  : > "$RESULT/patch.diff"
fi
capture timing-gate-end python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" gate end
capture timing-grade-start python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" grade start
grade_rc=0
timeout --signal=KILL 900 /opt/bench/mise/installs/python/3.14.7/bin/python3 "$KIT/reproduce/control-worker.py" \
  "$KIT" grade-candidate "$task" "$WORK/repo" "$RESULT" || grade_rc=$?
capture timing-grade-end python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" grade end
capture timing-review-start python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" review start
audit_flagged=false
printf '{}\n' > "$RESULT/audit.json"
if timeout --signal=KILL 30 /usr/bin/python3 "$KIT/reproduce/audit_cell.py" "$ROOT/results" "$run_id" > "$RESULT/audit.raw.json" 2>/dev/null; then
  if timeout --signal=KILL 15 python3 - "$RESULT/audit.raw.json" "$RESULT/audit.json" <<'PY'
import json,sys
rows=[json.loads(line) for line in open(sys.argv[1], encoding='utf-8')]
counts={k:v for k,v in rows[0].items() if k not in ('run_id','missing')} if rows else {}
with open(sys.argv[2],'w',encoding='utf-8') as out:
 json.dump(counts,out,sort_keys=True); out.write('\n')
PY
  then
    if ! audit_flagged=$(timeout --signal=KILL 10 python3 - "$RESULT/audit.json" <<'PY'
import json,sys
print('true' if json.load(open(sys.argv[1])).get('flagged',0)>0 else 'false')
PY
); then audit_flagged=false; capture_failures+=(audit-summary); fi
  fi
fi
rm -f "$RESULT/audit.raw.json"
capture timing-review-end python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" review end
capture_value codex-info codex_info python3 "$KIT/reproduce/lane-codex-info.py" /opt/bench/tools/bin/codex "$CODEX_VERSION"
if [[ -z $codex_info ]]; then codex_info=$'unknown\tunknown\t\tfalse'; fi
if ! timeout --signal=KILL 30 python3 - "$RESULT/manifest.json" "$RESULT/grade.json" "$TD/prompt.md" "$BIN" "$KIT" "$task" "$run_id" "$model" "$effort" "$base" "$rc" "$codex_info" "$audit_flagged" "$stall" "$timed_out" "$patch_error" "${capture_failures[@]}" <<'PY'
import hashlib,json,os,stat,subprocess,sys
path,grade_path,prompt,sandbox,kit,task,run_id,model,effort,base,rc,codex_info,audit_flagged,stall,timed_out,patch_error,*capture_failures=sys.argv[1:]
codex_version,codex_binary_version,codex_binary_sha256,codex_version_mismatch=codex_info.split('\t')
def digest(path):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  info=os.fstat(fd)
  if not stat.S_ISREG(info.st_mode) or info.st_size>16*1024*1024: raise ValueError('not a bounded regular file')
  h=hashlib.sha256()
  while True:
   block=os.read(fd,1024*1024)
   if not block: break
   h.update(block)
  return h.hexdigest()
 finally: os.close(fd)
safe_rows=os.path.expanduser('~/Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py')
try: grade=json.loads(subprocess.check_output([sys.executable,safe_rows,grade_path,'--keys','pass_,tests_ran'],text=True,timeout=8))
except Exception: grade=None
usage=None
events=os.path.join(os.path.dirname(path),'codex.jsonl')
try:
 fd=os.open(events,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 if not stat.S_ISREG(os.fstat(fd).st_mode): raise ValueError('event log is not a regular file')
 with os.fdopen(fd,encoding='utf-8',errors='replace') as source:
  fd=None
  for line in source:
   try: event=json.loads(line)
   except json.JSONDecodeError: continue
   if event.get('type')=='turn.completed': usage=event.get('usage')
except Exception:
 pass
finally:
 if 'fd' in locals() and fd is not None: os.close(fd)
with open(path,'w') as f:
 json.dump(dict(task=task,run_id=run_id,model=model,effort=effort,base_sha=base,
                kit=os.path.realpath(kit),prompt_sha256=digest(prompt),sandbox_sha256=digest(sandbox),usage=usage,
                effective_effort=effort,
                codex_version=codex_version,codex_binary_version=codex_binary_version,
                codex_binary_sha256=codex_binary_sha256,
                codex_version_mismatch=codex_version_mismatch=='true',
                audit_flagged=audit_flagged=='true',stall=stall=='true',
                timeout=timed_out=='true',patch_error=patch_error or None,
                capture_failures=capture_failures,
                runner_rc=int(rc),graded=grade is not None,grade=grade),f,sort_keys=True)
 f.write('\n')
PY
then
  capture_failures+=(manifest-write)
  printf 'Manifest capture failed; retaining cell patch and grade results\n' >&2
  timeout --signal=KILL 15 python3 - "$RESULT/manifest.json" "$task" "$run_id" "$model" "$effort" "$base" <<'PY'
import json,sys
path,task,run_id,model,effort,base=sys.argv[1:]
with open(path,'w') as out: json.dump({'task':task,'run_id':run_id,'model':model,'effort':effort,'effective_effort':effort,'base_sha':base,'runner_rc':1,'capture_failures':['manifest-write']},out); out.write('\n')
PY
fi
capture_value cell-end-utc cell_end_utc date -u +%Y-%m-%dT%H:%M:%S.%NZ
capture timing-cell-end python3 "$KIT/reproduce/lane-receipt.py" "$RESULT/lane-timing.json" cell end
capture boundary-end python3 "$KIT/reproduce/lane-sample.py" "$RESULT/boundary-samples.json" end "${BENCH_CELL_SECONDS:-3600}" "$RESULT/plan.json"
if ! timeout --signal=KILL 10 python3 - "$RESULT/capture-status.json" "${capture_failures[@]}" <<'PY'
import json,sys
with open(sys.argv[1],'w') as out: json.dump({'failed':sys.argv[2:]},out); out.write('\n')
PY
then capture_failures+=(capture-status-write); fi
if ! timeout --signal=KILL 25 python3 - "$RESULT/manifest.json" "$RESULT/manifest-sha256.txt" "$RESULT/lane-timing.json" "$RESULT/boundary-samples.json" "$cell_start_utc" "$cell_end_utc" "$plan_json" "$KIT" "$TD/task.json" "$cell_seconds" "$WORK/repo" "${capture_failures[@]}" <<'PY'
import hashlib,json,os,re,stat,subprocess,sys
manifest_path,hash_path,timing_path,samples_path,start,end,plan_raw,kit,task_meta,timeout_cap,worktree,*capture_failures=sys.argv[1:]
safe=os.path.expanduser('~/Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py')
keys='task,run_id,model,effort,effective_effort,base_sha,kit,prompt_sha256,sandbox_sha256,usage,codex_version,codex_binary_version,codex_binary_sha256,codex_version_mismatch,audit_flagged,stall,timeout,patch_error,capture_failures,runner_rc,graded,grade,cell_start_utc,cell_end_utc,release_eligible,plan,lane_timing,boundary_samples,candidate_revision,kit_revision,grader_sha256,timeout_cap_s,base_repo,base_revision'
def read_regular_json(path):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  info=os.fstat(fd)
  if not stat.S_ISREG(info.st_mode) or info.st_size>16*1024*1024: raise ValueError('not a bounded regular file')
  raw=bytearray()
  while True:
   block=os.read(fd,1024*1024)
   if not block: break
   raw.extend(block)
   if len(raw)>16*1024*1024: raise ValueError('file exceeded limit')
  return json.loads(raw)
 finally: os.close(fd)
def regular_file(path):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try: return stat.S_ISREG(os.fstat(fd).st_mode)
 finally: os.close(fd)
if not regular_file(manifest_path): raise ValueError('manifest receipt is not a regular file')
base_manifest=json.loads(subprocess.check_output([sys.executable,safe,manifest_path,'--keys',keys],text=True,timeout=8))
try: timing=read_regular_json(timing_path)
except Exception: timing={}
try: samples=read_regular_json(samples_path)
except Exception: samples={}
plan=json.loads(plan_raw) if plan_raw else {}
task=read_regular_json(task_meta)
candidate=None
candidate_env={'PATH':'/usr/bin:/bin','HOME':'/nonexistent'}
try:
 candidate=subprocess.check_output(['/usr/bin/timeout','--signal=KILL','8',sys.executable,
   kit+'/reproduce/candidate_revision.py',worktree],text=True,stderr=subprocess.DEVNULL,
   env=candidate_env,timeout=10).strip() or None
except Exception: pass
safe_env={'PATH':'/usr/bin:/bin','HOME':'/nonexistent','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_ATTR_NOSYSTEM':'1'}
git=['/usr/bin/git','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','safe.directory='+kit,'-C',kit,'rev-parse','HEAD']
try: kit_revision=subprocess.check_output(['/usr/bin/timeout','--signal=KILL','8',*git],text=True,stderr=subprocess.DEVNULL,env=safe_env).strip()
except Exception: kit_revision=None
def hash_regular(path):
 try:
  fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
  try:
   st=os.fstat(fd)
   if not __import__('stat').S_ISREG(st.st_mode) or st.st_size>16*1024*1024: return None
   digest=hashlib.sha256()
   while True:
    block=os.read(fd,1024*1024)
    if not block: break
    digest.update(block)
   return digest.hexdigest()
  finally: os.close(fd)
 except Exception: return None
grader_sha=hash_regular(kit+'/reproduce/control-worker.py')
base_repo=plan.get('base_repo')
if isinstance(base_repo,dict): base_repo=task.get('base_repo')
if isinstance(base_repo,str) and (base_repo.startswith(('/','~')) or '@' in base_repo or re.match(r'^[a-z]:[/\\]',base_repo,re.I)):
 base_repo={'missing':'m39'}
base_manifest.update(cell_start_utc=start or None,cell_end_utc=end or None,
 release_eligible=bool(plan),plan=plan,lane_timing=timing,boundary_samples=samples,
 candidate_revision=candidate,kit_revision=kit_revision,grader_sha256=grader_sha,
 timeout_cap_s=int(timeout_cap),base_repo=base_repo or task.get('base_repo'),
 capture_failures=sorted(set(base_manifest.get('capture_failures',[])+capture_failures)))
if plan.get('base_revision'): base_manifest['base_revision']=plan['base_revision']
elif base_manifest.get('base_sha'): base_manifest['base_revision']={'kind':'git-commit','hash':base_manifest['base_sha']}
payload=(json.dumps(base_manifest,sort_keys=True)+'\n').encode()
with open(manifest_path,'wb') as out: out.write(payload)
with open(hash_path,'w') as out: out.write(hashlib.sha256(payload).hexdigest()+'\n')
PY
then
  capture_failures+=(manifest-enrichment)
  printf 'Manifest enrichment failed; capture failures recorded separately\n' >&2
  timeout --signal=KILL 10 python3 - "$RESULT/capture-status.json" "${capture_failures[@]}" <<'PY' || true
import json,sys
with open(sys.argv[1],'w') as out: json.dump({'failed':sys.argv[2:]},out); out.write('\n')
PY
fi
before_standard=${#capture_failures[@]}
capture standard-record python3 "$KIT/reproduce/standard_record.py" "$RESULT"
if (( ${#capture_failures[@]} > before_standard )); then
  timeout --signal=KILL 10 python3 - "$RESULT/capture-status.json" "${capture_failures[@]}" <<'PY' || true
import json,sys
with open(sys.argv[1],'w') as out: json.dump({'failed':sys.argv[2:]},out); out.write('\n')
PY
fi
printf 'Cell %s: runner rc=%s, grader rc=%s; records in %s\n' "$run_id" "$rc" "$grade_rc" "$RESULT"
if (( rc )); then exit "$rc"; fi
exit "$grade_rc"
