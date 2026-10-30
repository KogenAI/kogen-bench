#!/bin/sh
# day-runner-v3.sh (user lanes): the v3 guard (weekly usage file + $ backstop) for any run list on one host.
# Usage: DAYCAP=<usd> DAYDIR=<name> [WEEKLY_OFF=1] day-runner-v3.sh <id>:<tasks dir>:<cell estimate>[:dry] ...
# ChatGPT day orchestrator v2 (user lanes), 25 Oct. One guard per UTC day ($200 from 25 Oct 16:45Z; was $25) across all these ChatGPT runs.
# v1 overshot ($31.51 on 25 Oct): it counted only finished cells, so a run's live cells were invisible. v2 counts live spend:
# each finished dispatch adds its spend delta (lanes costguard estimate: finished + live + ledger) to dayspend/<UTC date>,
# and the running dispatch adds (estimate now - estimate at its start). No dispatch starts when the remainder is under one
# cell's estimate. At 25 - slots*cell it pauses new cells (SIGSTOP); at 25 - $STOP_MARGIN, or once no cell is live, it
# stops the run (TERM; lanes-run stops its cells and keeps their spend), and the run resumes the next UTC day.
# Idempotent: a finished run leaves runs/<id>/DONE and is skipped; the 00:00Z timer may start it again safely.
export LANES_SHARED_GOCACHE=${LANES_SHARED_GOCACHE:-$HOME/.cache/go-build}   # 26 Oct: grading shares the Go build cache
export PATH=$HOME/.lanes-shim:$PATH LANES_NM_CACHE=${LANES_NM_CACHE:-$HOME/.cache/lanes-nm}   # 26 Oct: npm ci reuses one node_modules per lockfile (hardlink copy)
[ -n "$LANES_ENV" ] && . "$LANES_ENV"  # host overrides (paths, PATH, caches)
[ -n "$LANES_NPMFIX_HARNESS" ] && export LANES_DIR="$LANES_NPMFIX_HARNESS"
P=${LANES_P:-$HOME/lanes-work}; KH=${CHATGPT_KH:-${LANES_KH:-$HOME/kogen-home}}; LANES=${LANES_DIR:-$(cd "$(dirname "$0")/.." && pwd)}; LOG=$P/${DAYDIR:-dayspend}.log
[ -z "$LANES_ENV" ] && eval "$(mise activate bash --shims 2>/dev/null || mise activate sh --shims)"
export KOGEN_LANES_HOME=${KOGEN_LANES_HOME:-$HOME/.cache/kogen-lanes}
# cells run with HOME=$KH: pin mise to the real install dirs so task setup finds erlang/elixir/node (24 Oct)
[ -z "$LANES_ENV" ] && export MISE_DATA_DIR=$HOME/.local/share/mise MISE_CACHE_DIR=$HOME/.cache/mise MISE_CONFIG_DIR=$HOME/.config/mise MISE_TRUSTED_CONFIG_PATHS=/
export GIT_AUTHOR_NAME="Kogen Lanes" GIT_AUTHOR_EMAIL="lanes@kogen.invalid" GIT_COMMITTER_NAME="Kogen Lanes" GIT_COMMITTER_EMAIL="lanes@kogen.invalid"
DAYCAP=${DAYCAP:-1000}; SLOTS=${SLOTS:-3}; STOP_MARGIN=1.0   # v3 (25 Oct ~17:05Z): $ is only a runaway backstop; the budget is the plan's weekly usage
WEEKLY=$P/weekly-usage.json; W_PAUSE=100; W_STOP=100; W_STALE=1800   # fed every 10 min by the coordinating host (weekly-feed.sh); stale -> local estimate (OPS-AUTONOMY, see wstate)
DD=$P/${DAYDIR:-dayspend}; mkdir -p $DD
say() { echo "$(date -u +%FT%TZ) $*" >> $LOG; }
today() { date -u +%F; }
acc() { cat $DD/$1 2>/dev/null || echo 0; }
acc_add() { python3 -c "import sys;print(round(float(sys.argv[1])+float(sys.argv[2]),4))" "$(acc $1)" "$2" > $DD/$1.tmp && mv $DD/$1.tmp $DD/$1; }
run_total() { (cd $LANES && python3 -c "import sys;from lanes import costguard;print(costguard.estimate(sys.argv[1]))" $P/runs/$1) 2>>$P/$1/run-logs/guard.err || echo FAIL; }
calc() { python3 -c "import sys;print(round(eval(sys.argv[1]),4))" "$1"; }
ge() { python3 -c "import sys;sys.exit(0 if float(sys.argv[1])>=float(sys.argv[2]) else 1)" "$1" "$2"; }
cell_est() { python3 - $P/runs/$1 $2 <<'PY'
import glob, json, sys
c = [json.load(open(f))["totals"].get("cost_usd") for f in glob.glob(sys.argv[1] + "/cells/*/*/*/result.json")]
c = [x for x in c if x]
print(round(max(sum(c) / len(c), 0.1), 2) if c else sys.argv[2])
PY
}
# weekly guard: ok | stop (>= W_STOP) | stale. OPS-AUTONOMY (28 Oct): the reading comes from the coordinator's feed; while it is fresh
# (age <= W_STALE) the runner records this host's cumulative ChatGPT list spend as the anchor. When the feed is stale (coordinator or
# its network down) the runner keeps going on an estimate: last % + W_K points per $ of this host's spend since the anchor (W_K is
# conservative: about 4x the observed 0.17 points/$ of all hosts, for the other hosts' unseen spend). It fails closed ("stale")
# only after W_STALE_MAX s without a reading, and stops at once on this host's own refusal: a cell in the last 30 min that
# reports the ChatGPT usage limit.
wstate() { [ -n "$WEEKLY_OFF" ] && { echo ok; return; }; python3 - $WEEKLY $W_PAUSE $W_STOP $W_STALE ${W_PACE_RESERVE:-0} $P/${DAYDIR:-dayspend} $P/runs ${W_STALE_MAX:-43200} ${W_K:-0.75} <<'PY'
import glob, json, os, sys, time, datetime as dt
wf, _, wstop, stale, reserve, daydir, runs, stale_max, k = sys.argv[1:10]
anchor_f = wf + ".anchor-" + os.path.basename(daydir)
def cum():
    t = 0.0
    for f in glob.glob(daydir + "/2*"):
        try: t += float(open(f).read().strip() or 0)
        except Exception: pass
    return t
def refused():
    cut = time.time() - 1800
    for f in glob.glob(runs + "/*/cells/*/*/*/stdout.txt"):
        try:
            if os.path.getmtime(f) >= cut and "ChatGPT usage limit reached" in open(f, errors="replace").read(): return True
        except Exception: pass
    return False
if refused(): print("stop"); sys.exit()
try:
    d = json.load(open(wf)); pct = float(d["used_pct"])
    age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.strptime(d["read_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)).total_seconds()
except Exception:
    print("stale"); sys.exit()
limit = float(wstop) - float(reserve)
if age <= float(stale):
    try:
        a = json.load(open(anchor_f)) if os.path.exists(anchor_f) else {}
        if a.get("read_at") != d["read_at"]:
            json.dump({"read_at": d["read_at"], "pct": pct, "local_usd": cum()}, open(anchor_f + ".tmp", "w")); os.replace(anchor_f + ".tmp", anchor_f)
    except Exception: pass
    print("stop" if pct >= limit else "ok"); sys.exit()
if age > float(stale_max): print("stale"); sys.exit()
try:
    a = json.load(open(anchor_f)); base = float(a["local_usd"]) if a.get("read_at") == d["read_at"] else cum()
except Exception:
    base = cum()
est = pct + float(k) * max(cum() - base, 0.0)
print("stop" if est >= limit else "ok")
PY
}
wpct() { python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('used_pct'))" $WEEKLY 2>/dev/null || echo "?"; }
wait_weekly() { while :; do w=$(wstate); [ "$w" = ok ] && return 0; say "weekly guard: $w (used $(wpct)%), waiting"; sleep 300; done; }
live_cells() { ls $P/runs/$1/cells/*/*/*/live.json 2>/dev/null | wc -l; }
wait_next_day() { d=$(today); while [ "$(today)" = "$d" ]; do sleep 60; done; }
# run one experiment to completion under the daily guard: capped <id> <tasks dir> <default cell estimate>
capped() { e=$1; tasks=$2; est0=$3
  [ -f $P/runs/$e/DONE ] && return 0
  mkdir -p $P/$e/run-logs
  while :; do
    day=$(today); est=$(cell_est $e $est0); rem=$(calc "$DAYCAP-$(acc $day)")
    if [ "$(wstate)" != ok ]; then wait_weekly; continue; fi
    if ! ge $rem $est; then say "$e waits for the next UTC day (day spend \$$(acc $day), remainder \$$rem < cell estimate \$$est)"; wait_next_day; continue; fi
    base=$(run_total $e); [ "$base" = FAIL ] && { say "STOP $e: cost estimate failed (see $P/$e/run-logs/guard.err)"; return 1; }
    HOME=$KH python3 $LANES/bin/lanes-run $P/runs/$e --tasks $tasks --hosts $P/runs/$e/hosts.json >> $P/$e/run-logs/run.out 2>&1 &
    D=$!; paused=0; stopped=0; why=day; say "$e dispatch started (day spend \$$(acc $day), cell estimate \$$est)"
    while kill -0 $D 2>/dev/null; do
      sleep 60
      t=$(run_total $e); [ "$t" = FAIL ] && { kill -TERM $D; kill -CONT $D; stopped=1; say "$e stopped: cost estimate failed"; continue; }
      if [ "$(today)" != "$day" ]; then acc_add $day $(calc "$t-$base"); day=$(today); base=$t
        [ $paused = 1 ] && [ $stopped = 0 ] && { kill -CONT $D; paused=0; say "new day: $e resumed"; }; fi
      live=$(calc "$(acc $day)+$t-$base"); w=$(wstate)
      if [ $stopped = 0 ] && { [ "$w" = stop ] || [ "$w" = stale ]; }; then
        kill -TERM $D; kill -CONT $D; stopped=1; why=weekly; say "weekly guard: $e stopped ($w, used $(wpct)%)"; continue
      fi
      if [ $paused = 0 ] && [ $stopped = 0 ] && { [ "$w" = pause ] || [ "$w" = pace ]; }; then kill -STOP $D; paused=1; why=weekly; say "weekly guard: $e paused new cells (used $(wpct)%)"; continue; fi
      if [ $stopped = 0 ] && { ge $live $(calc "$DAYCAP-$STOP_MARGIN") || { [ $paused = 1 ] && [ $(live_cells $e) = 0 ]; }; }; then
        kill -TERM $D; kill -CONT $D; stopped=1; say "daily guard: $e stopped (day spend \$$live, live cells $(live_cells $e))"
      elif [ $paused = 0 ] && [ $stopped = 0 ] && ge $live $(calc "$DAYCAP-$SLOTS*$est"); then
        kill -STOP $D; paused=1; say "daily guard: $e paused new cells (day spend \$$live)"
      fi
    done
    wait $D 2>/dev/null; dispatch_rc=$?; t=$(run_total $e); [ "$t" != FAIL ] && acc_add $day $(calc "$t-$base")
    say "$e dispatch ended (day spend \$$(acc $day))"
    if [ $stopped = 1 ]; then [ "$why" = weekly ] && wait_weekly || wait_next_day; continue; fi
    if [ "$dispatch_rc" = 5 ] || python3 "$LANES/bin/lanes-carry" pending "$P/runs/$e"; then
      grade "$e" "$tasks"
      python3 "$LANES/bin/lanes-carry" enqueue "$P/approval-carry" "$P/runs/$e" "$tasks" cgr "$SLOTS" "$est0" || return 1
      say "$e carried: approval infrastructure gap; original plan retained, no DONE/GRADED"
      return 5
    fi
    touch $P/runs/$e/DONE; return 0
  done; }
grade() { GL=$P/grade.lock; if command -v flock >/dev/null 2>&1; then LK="flock 9"; else LK="lockf -k $GL true"; fi; # lock on fd 9: only python carries bin/lanes-grade in argv (the host gate counts each match as a live cell; 28 Oct)
  exec 9>>$GL; $LK; nice -n 19 python3 $LANES/bin/lanes-grade $P/runs/$1 --tasks $2 > $P/$1/run-logs/grade.out 2>&1; exec 9>&-; python3 $LANES/bin/lanes-report $P/runs/$1 > $P/$1/run-logs/report.out 2>&1; say "$1 graded: $(tail -1 $P/$1/run-logs/report.out)"; }
say "v3 start (weekly $(wpct)%, $(wstate)) (day spend \$$(acc $(today)))"
run() { e=$1; tasks=$2; est=$3
  [ -f $P/runs/$e/GRADED ] && return 0
  capped $e $tasks $est && { grade $e $tasks; touch $P/runs/$e/GRADED; }; }
say "day-runner-v3 start (cap \$$DAYCAP, weekly $(wpct)% $(wstate), day spend \$$(acc $(today)))"
run() { e=$1; tasks=$2; est=$3
  [ -f $P/runs/$e/GRADED ] && return 0
  capped $e $tasks $est && { grade $e $tasks; touch $P/runs/$e/GRADED; }; }
for spec in "$@"; do
  e=${spec%%:*}; rest=${spec#*:}; tasks=${rest%%:*}; rest=${rest#*:}; est=${rest%%:*}; flag=${rest#*:}; [ "$flag" = "$rest" ] && flag=""
  run $e $tasks $est
  case "$flag" in dry|dry=*)   # dry=<event>: §11.8, every dry cell must also log <event> at least once (the lever fired)
    ev=${flag#dry}; ev=${ev#=}
    bad=$(python3 - $P/runs/$e "$ev" <<'PY'
import glob, json, sys
cells = glob.glob(sys.argv[1] + "/cells/*/*/*/result.json"); ev = sys.argv[2]; bad = 0 if cells else 1
for f in cells:
    if json.load(open(f))["outcome"] not in ("landed", "ok"): bad += 1; continue
    if ev:
        n = sum(1 for l in open(f.replace("result.json", "run-log/log.jsonl")) if '"event": "%s"' % ev in l or '"event":"%s"' % ev in l)
        bad += n == 0
print(bad)
PY
)
    [ "$bad" = 0 ] && say "$e dry ok${ev:+ ($ev fired)}" || { say "STOP after $e: dry cell not landed${ev:+ or $ev did not fire}"; exit 1; } ;;
  esac
done
say done
