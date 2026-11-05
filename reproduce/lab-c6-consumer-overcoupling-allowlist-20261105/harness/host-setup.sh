#!/bin/bash
# host-setup.sh <trees.tsv> <arm test file> [label ...]   (Lab C6, runs on the Linux host as lanes)
# Per tree: scratch clone of kogen-build at the consumer commit, the producer module replaced (go mod edit -replace, as
# consumer-check.sh does) by a checkout of the producer commit, the arm-A test file added, and ONE test binary built.
# Nothing is committed or pushed. Compile failures are recorded, not hidden.
. "$(dirname "$0")/env.sh"; T=$1; A=$2; shift 2; MIR=$HOME/work.noindex/mirrors; LOG=$W/out/setup.tsv
[ -s $LOG ] || printf 'label\tclass\tconsumer\trepo\tproducer\ttest_blob\tbuild_seconds\tstatus\n' > $LOG
want=" $* "
tail -n +2 "$T" | while IFS=$'\t' read -r label cls cons repo prod cand tv; do
  [ -n "$*" ] && case "$want" in *" $label "*) ;; *) continue;; esac
  [ -x $W/bin/$label.test ] && continue
  p=${cand/#-/$prod}; s=$(date +%s)
  d=$W/trees/$label; pd=$W/prod/$repo-${p:0:12}
  [ -d $pd ] || { git clone -q $MIR/$repo.git $pd && git -C $pd checkout -q --detach $p; } 2>/dev/null || { printf '%s\t%s\t%s\t%s\t%s\t-\t0\tPRODUCER_MISSING\n' $label $cls ${cons:0:7} $repo ${p:0:7} >> $LOG; continue; }
  if [ ! -d $d ]; then git clone -q $MIR/kogen-build.git $d && git -C $d checkout -q --detach $cons || { printf '%s\t%s\t%s\t%s\t%s\t-\t0\tCONSUMER_MISSING\n' $label $cls ${cons:0:7} $repo ${p:0:7} >> $LOG; continue; }; fi
  blob=$(git -C $d rev-parse --short HEAD:build/build_request_budget_test.go 2>/dev/null || echo none)
  (cd $d && go mod edit -replace=github.com/KogenAI/$repo=$pd && cp "$A" build/budget_allow_test.go && go test -c -o $W/bin/$label.test ./build) > $W/out/build-$label.log 2>&1; rc=$?
  st=OK; if [ $rc -ne 0 ]; then   # retry without the arm-A file: the current-arm binary may still build
    (cd $d && rm -f build/budget_allow_test.go && go test -c -o $W/bin/$label.test ./build) >> $W/out/build-$label.log 2>&1 && st=NO_ARM_A || st=COMPILE_FAIL; fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%d\t%s\n' $label $cls ${cons:0:7} $repo ${p:0:7} $blob $(( $(date +%s)-s )) $st >> $LOG
done
