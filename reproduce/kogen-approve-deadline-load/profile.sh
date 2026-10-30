#!/bin/sh
# Profile the steps that share Kogen's single 120 s approval deadline for one task kit (here goose-labels-go).
# usage: profile.sh TASK_START_TREE [OUT_CSV]
#   TASK_START_TREE  a COPY of the task's start tree (never the original); it is not modified except for a throwaway node_modules
# Run as the unprivileged benchmark user, one heavy job at a time, with the default timeouts.
# Needs: git, go (the version in the task's go.mod; the tree is vendored), /usr/bin/time -p style timing via python3 below, npm for the last step.
# Written for this pack from the measurement note; the original ad-hoc commands were not kept. Not executed when the pack was built.
set -eu
T=${1:?task start tree copy}; OUT=${2:-profile.csv}
cd "$T"
timeit() { python3 - "$@" <<'PY'
import resource, subprocess, sys, time
step, cond = sys.argv[1], sys.argv[2]
cmd = sys.argv[3:]
r0 = resource.getrusage(resource.RUSAGE_CHILDREN); t0 = time.monotonic()
p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
print('%s,%s,%.2f,%.2f,%d' % (step, cond, time.monotonic() - t0, (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime), p.returncode))
PY
}
echo "step,condition,wall_s,cpu_s,exit" > "$OUT"
# tree size
echo "files,tracked tree (excluding .git),$(find . -path ./.git -prune -o -type f -print | wc -l | tr -d ' '),," >> "$OUT"
# 1. the snapshot step: git add into a fresh index, as Kogen's candidate snapshot does
IDX=$(mktemp -u); GIT_INDEX_FILE=$IDX timeit git_add "no node_modules" git add -A -- . >> "$OUT"
echo "git_add_staged_files,no node_modules,$(GIT_INDEX_FILE=$IDX git ls-files | wc -l | tr -d ' '),," >> "$OUT"; rm -f "$IDX"
# 2. the check step: go build, cold then warm cache (vendored, offline)
export GOFLAGS=-mod=vendor GOPROXY=off
GOCACHE=$(mktemp -d); export GOCACHE
timeit go_build "cold GOCACHE" go build ./... >> "$OUT"
timeit go_build "warm GOCACHE" go build ./... >> "$OUT"
# 3. the setup step: npm ci from a warm npm cache, then git add with node_modules present (it is gitignored)
npm ci --ignore-scripts --no-audit --no-fund >/dev/null 2>&1 || true
rm -rf node_modules; timeit npm_ci "warm npm cache" npm ci --ignore-scripts --no-audit --no-fund >> "$OUT"
IDX=$(mktemp -u); GIT_INDEX_FILE=$IDX timeit git_add "with node_modules" git add -A -- . >> "$OUT"
echo "git_add_staged_files,with node_modules,$(GIT_INDEX_FILE=$IDX git ls-files | wc -l | tr -d ' '),," >> "$OUT"; rm -f "$IDX"
cat "$OUT"
