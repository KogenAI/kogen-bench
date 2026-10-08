#!/usr/bin/env bash
# One explicit Codex task cell. Requires bench's manual device login.
set -euo pipefail
if (( $# != 4 )); then
  echo 'usage: run-lane.sh TASK_ID RUN_ID MODEL EFFORT' >&2; exit 2
fi
task=$1 run_id=$2 model=$3 effort=$4
[[ $task =~ ^[a-zA-Z0-9][a-zA-Z0-9-]*$ && $run_id =~ ^[a-zA-Z0-9][a-zA-Z0-9_.-]*$ ]] || exit 2
[[ $model =~ ^[a-zA-Z0-9][a-zA-Z0-9_.-]*$ && $effort =~ ^(low|medium|high|xhigh|max)$ ]] || exit 2
[[ $EUID == 0 ]] || { echo 'Run with sudo to launch the bench systemd slice' >&2; exit 1; }
ROOT=/srv/bh/bench
exec 9>"$ROOT/launch.lock"
flock -n 9 || { echo 'Another benchmark launch is active' >&2; exit 1; }
if systemctl list-units --type=service --state=running --no-legend 'bench-*.service' | grep -q .; then
  echo 'A benchmark service is already running' >&2; exit 1
fi
KIT=$ROOT/kits/current
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
expected=$(python3 - "$TD/task.json" <<'PY'
import json,sys
print(json.load(open(sys.argv[1]))['base_bundle_sha256'])
PY
)
[[ $(sha256sum "$KIT/tasks/$bundle" | cut -d' ' -f1) == "$expected" ]] || { echo 'Base bundle SHA-256 mismatch' >&2; exit 1; }
mkdir -p "$WORK" "$RESULT"
git clone -q "$KIT/tasks/$bundle" "$WORK/repo"
git -C "$WORK/repo" checkout -q "$base"
install -m 0644 "$TD/prompt.md" "$WORK/prompt.md"
chown -R bench:bench "$WORK" "$RESULT"
BIN=$KIT/reproduce/sandbox-profile.sh
PATH_PINNED=/srv/bh/bench/toolchains/go-1.27.1/bin:/srv/bh/bench/toolchains/rust-1.97.1/bin:/srv/bh/bench/toolchains/bun-1.4.2/bin:/srv/bh/bench/toolchains/gleam-1.18.1/bin:/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/opt/bench/mise/installs/node/24.20.0/bin:/opt/bench/mise/installs/ruby/3.4.8/bin:/srv/bh/bench/toolchains/python-3.14.7/bin:/opt/bench/tools/bin:/usr/bin:/bin
set +e
systemd-run --quiet --collect --wait --pipe --slice=bench.slice --unit="bench-$run_id" \
  --uid=bench --gid=bench -p UMask=0002 -p KillMode=control-group -p TasksMax=4096 \
  /usr/bin/env PATH="$PATH_PINNED" HOME=/home/bench CODEX_HOME=/home/bench/.codex \
  "$BIN" agent "$WORK" -- /opt/bench/tools/bin/codex exec --skip-git-repo-check \
  --json --model "$model" --config "model_reasoning_effort=$effort" \
  --dangerously-bypass-approvals-and-sandbox -C /work/repo \
  "$(cat "$TD/prompt.md")" > "$RESULT/codex.jsonl" 2> "$RESULT/codex.stderr"
rc=$?
set -e
git -C "$WORK/repo" diff --binary "$base" > "$RESULT/patch.diff"
grade_rc=0
/opt/bench/mise/installs/python/3.14.7/bin/python3 "$KIT/reproduce/control-worker.py" \
  "$KIT" grade-candidate "$task" "$WORK/repo" "$RESULT" || grade_rc=$?
python3 - "$RESULT/manifest.json" "$RESULT/grade.json" "$TD/prompt.md" "$BIN" "$KIT" "$task" "$run_id" "$model" "$effort" "$base" "$rc" <<'PY'
import hashlib,json,os,sys
path,grade_path,prompt,sandbox,kit,task,run_id,model,effort,base,rc=sys.argv[1:]
digest=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
try: grade=json.load(open(grade_path))
except FileNotFoundError: grade=None
usage=None
events=os.path.join(os.path.dirname(path),'codex.jsonl')
with open(events,errors='replace') as source:
 for line in source:
  try: event=json.loads(line)
  except json.JSONDecodeError: continue
  if event.get('type')=='turn.completed': usage=event.get('usage')
with open(path,'w') as f:
 json.dump(dict(task=task,run_id=run_id,model=model,effort=effort,base_sha=base,
                kit=os.path.realpath(kit),prompt_sha256=digest(prompt),sandbox_sha256=digest(sandbox),usage=usage,
                codex_version='0.160.0',codex_binary_sha256='12eb3e81114588aca3b7998f4f19e8997b056aca08e57a7ca7c8a3ec8c652aad',
                runner_rc=int(rc),graded=grade is not None,grade=grade),f,sort_keys=True)
 f.write('\n')
PY
printf 'Cell %s: runner rc=%s, grader rc=%s; records in %s\n' "$run_id" "$rc" "$grade_rc" "$RESULT"
if (( rc )); then exit "$rc"; fi
exit "$grade_rc"
