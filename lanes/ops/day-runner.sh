#!/bin/sh
# day-runner.sh (user lanes): the v2 day guard (see chatgpt-day.sh) for any provider, one host.
# Usage: DAYCAP=<usd> DAYDIR=<name> day-runner.sh <id>:<tasks dir>:<cell estimate>[:dry] ...  (':dry' = stop the list unless every cell landed/ok)
# v1 overshot ($31.51 on 25 Oct): it counted only finished cells, so a run's live cells were invisible. v2 counts live spend:
# each finished dispatch adds its spend delta (lanes costguard estimate: finished + live + ledger) to dayspend/<UTC date>,
# and the running dispatch adds (estimate now - estimate at its start). No dispatch starts when the remainder is under one
# cell's estimate. At 25 - slots*cell it pauses new cells (SIGSTOP); at 25 - $STOP_MARGIN, or once no cell is live, it
# stops the run (TERM; lanes-run stops its cells and keeps their spend), and the run resumes the next UTC day.
# Idempotent: a finished run leaves runs/<id>/DONE and is skipped; the 00:00Z timer may start it again safely.
[ -n "$LANES_ENV" ] && . "$LANES_ENV"  # host overrides (paths, PATH, caches)
[ -n "$LANES_NPMFIX_HARNESS" ] && export LANES_DIR="$LANES_NPMFIX_HARNESS"
P=${LANES_P:-$HOME/lanes-work}; KH=${LANES_KH:-$HOME/kogen-home}; LANES=${LANES_DIR:-$(cd "$(dirname "$0")/.." && pwd)}; LOG=$P/${DAYDIR:-dayspend}.log
[ -z "$LANES_ENV" ] && eval "$(mise activate bash --shims 2>/dev/null || mise activate sh --shims)"
export KOGEN_LANES_HOME=${KOGEN_LANES_HOME:-$HOME/.cache/kogen-lanes}
# cells run with HOME=$KH: pin mise to the real install dirs so task setup finds erlang/elixir/node (24 Oct)
[ -z "$LANES_ENV" ] && export MISE_DATA_DIR=$HOME/.local/share/mise MISE_CACHE_DIR=$HOME/.cache/mise MISE_CONFIG_DIR=$HOME/.config/mise MISE_TRUSTED_CONFIG_PATHS=/
export GIT_AUTHOR_NAME="Kogen Lanes" GIT_AUTHOR_EMAIL="lanes@kogen.invalid" GIT_COMMITTER_NAME="Kogen Lanes" GIT_COMMITTER_EMAIL="lanes@kogen.invalid"
DAYCAP=${DAYCAP:-20}; SLOTS=${SLOTS:-3}; STOP_MARGIN=1.0; DD=$P/${DAYDIR:-dayspend}
export KOGEN_SSE_DUMP_DIR=${KOGEN_SSE_DUMP_DIR:-$P/sse-dumps}; mkdir -p $KOGEN_SSE_DUMP_DIR; chmod 700 $KOGEN_SSE_DUMP_DIR   # observation-only (KOGEN-059)
export KOGEN_REVIEW_DUMP_DIR=${KOGEN_REVIEW_DUMP_DIR:-$P/review-dumps}; mkdir -p $KOGEN_REVIEW_DUMP_DIR; chmod 700 $KOGEN_REVIEW_DUMP_DIR   # observation-only (rejected verdicts)
mkdir -p $DD
say() { echo "$(date -u +%FT%TZ) $*" >> $LOG; }
today() { date -u +%F; }
acc() { cat $DD/$1 2>/dev/null || echo 0; }
acc_add() { python3 -c "import sys;print(round(float(sys.argv[1])+float(sys.argv[2]),4))" "$(acc $1)" "$2" > $DD/$1.tmp && mv $DD/$1.tmp $DD/$1;
  printf "%s\t%s\t%s\n" "$1" "${KEY_NAME:-unknown}" "$2" >> $DD/by-key.tsv; }  # cap7: key NAME per spend delta (date, key_name, usd); never the key
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
live_cells() { ls $P/runs/$1/cells/*/*/*/live.json 2>/dev/null | wc -l; }
wait_next_day() { d=$(today); while [ "$(today)" = "$d" ]; do sleep 60; done; }
# run one experiment to completion under the daily guard: capped <id> <tasks dir> <default cell estimate>
capped() { e=$1; tasks=$2; est0=$3
  [ -f $P/runs/$e/DONE ] && return 0
  mkdir -p $P/$e/run-logs
  while :; do
    day=$(today); est=$(cell_est $e $est0); rem=$(calc "$DAYCAP-$(acc $day)")
    if ! ge $rem $est; then say "$e waits for the next UTC day (day spend \$$(acc $day), remainder \$$rem < cell estimate \$$est)"; wait_next_day; continue; fi
    base=$(run_total $e); [ "$base" = FAIL ] && { say "STOP $e: cost estimate failed (see $P/$e/run-logs/guard.err)"; return 1; }
    HOME=$KH python3 $LANES/bin/lanes-run $P/runs/$e --tasks $tasks --hosts $P/runs/$e/hosts.json >> $P/$e/run-logs/run.out 2>&1 &
    D=$!; paused=0; stopped=0; say "$e dispatch started (day spend \$$(acc $day), cell estimate \$$est)"
    while kill -0 $D 2>/dev/null; do
      sleep 60
      t=$(run_total $e); [ "$t" = FAIL ] && { kill -TERM $D; kill -CONT $D; stopped=1; say "$e stopped: cost estimate failed"; continue; }
      if [ "$(today)" != "$day" ]; then acc_add $day $(calc "$t-$base"); day=$(today); base=$t
        [ $paused = 1 ] && [ $stopped = 0 ] && { kill -CONT $D; paused=0; say "new day: $e resumed"; }; fi
      live=$(calc "$(acc $day)+$t-$base")
      if [ $stopped = 0 ] && { ge $live $(calc "$DAYCAP-$STOP_MARGIN") || { [ $paused = 1 ] && [ $(live_cells $e) = 0 ]; }; }; then
        kill -TERM $D; kill -CONT $D; stopped=1; say "daily guard: $e stopped (day spend \$$live, live cells $(live_cells $e))"
      elif [ $paused = 0 ] && [ $stopped = 0 ] && ge $live $(calc "$DAYCAP-$SLOTS*$est"); then
        kill -STOP $D; paused=1; say "daily guard: $e paused new cells (day spend \$$live)"
      fi
    done
    wait $D 2>/dev/null; dispatch_rc=$?; t=$(run_total $e); [ "$t" != FAIL ] && acc_add $day $(calc "$t-$base")
    say "$e dispatch ended (day spend \$$(acc $day))"
    [ $stopped = 1 ] && { wait_next_day; continue; }
    if [ "$dispatch_rc" = 5 ] || python3 "$LANES/bin/lanes-carry" pending "$P/runs/$e"; then
      grade "$e" "$tasks"
      python3 "$LANES/bin/lanes-carry" enqueue "$P/approval-carry" "$P/runs/$e" "$tasks" ccr "$SLOTS" "$est0" || return 1
      say "$e carried: approval infrastructure gap; original plan retained, no DONE/GRADED"
      return 5
    fi
    touch $P/runs/$e/DONE; return 0
  done; }
grade() { GL=$P/grade.lock; if command -v flock >/dev/null 2>&1; then LK="flock 9"; else LK="lockf -k $GL true"; fi; # lock on fd 9: only python carries bin/lanes-grade in argv (the host gate counts each match as a live cell; 28 Oct)
  exec 9>>$GL; $LK; nice -n 19 python3 $LANES/bin/lanes-grade $P/runs/$1 --tasks $2 > $P/$1/run-logs/grade.out 2>&1; exec 9>&-; python3 $LANES/bin/lanes-report $P/runs/$1 > $P/$1/run-logs/report.out 2>&1; say "$1 graded: $(tail -1 $P/$1/run-logs/report.out)"; }
say "day-runner start (cap \$$DAYCAP, day spend \$$(acc $(today)))"
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
