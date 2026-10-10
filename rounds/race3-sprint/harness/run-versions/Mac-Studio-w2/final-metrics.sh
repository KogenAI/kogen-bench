#!/bin/bash
# final-metrics.sh — after the race, on an idle machine, ONE arm at a time, same caps for every arm: measurements on a CLEAN copy of each FINAL snapshot.
# Writes out/final-metrics.tsv: arm, metric, value, method. A metric that cannot be captured is written as n/a with the reason (never dropped).
R=$(cd "$(dirname "$0")" && pwd); O=$R/out/final-metrics.tsv; mkdir -p "$R/out"; : > $O; source $R/env.sh
METRICS="cold_ready_s incremental_ready_s startup_median_s own_tests_s lint_findings artifact_bytes invocation_median_s peak_rss_kb"
now() { /usr/bin/python3 -c 'import time;print(time.time())'; }
put() { local value="$3" method="$4"; [ -n "$value" ] || { value=n/a; method="empty measurement: $method"; }; method=${method//$'\t'/ }; method=${method//$'\n'/ }; printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$value" "$method" >> "$O"; }
timed() { local t0=$(now); ( "$@" ) > $T/last.log 2>&1; local rc=$?; /usr/bin/python3 -c "import time,sys;print(round(time.time()-float(sys.argv[1]),2))" $t0; return $rc; }
for A in $(cat $R/ARMS); do
  F=$R/snapshots/FINAL/$A; [ -x "$F/kogen" ] || { for metric in $METRICS; do put "$A" "$metric" n/a "no executable ./kogen in FINAL"; done; continue; }
  T=$(mktemp -d "$R/.final-metrics.XXXXXX"); C=$T/$A
  /usr/bin/python3 "$R/clean-copy.py" "$F" "$C" || exit 1
  ( source $R/env.sh; [ -f $R/$A/.kit-env.sh ] && source $R/$A/.kit-env.sh; cd $C
    if v=$(timed ./kogen version); then
    put $A cold_ready_s $v "clean copy (no build output), first ./kogen version"
    ext=$(case $A in (rust) echo rs;; (go) echo go;; (ts) echo ts;; (gleam) echo gleam;; (ex) echo ex;; esac)
    big=$(find . -name "*.$ext" -not -path "./spec/*" -not -path "./conformance/*" -not -path "./node_modules/*" -not -path "./deps/*" -not -path "./test*" -print0 2>/dev/null | xargs -0 ls -S 2>/dev/null | head -1)
    if [ -n "$big" ]; then touch "$big"; v=$(timed ./kogen version) && put $A incremental_ready_s $v "touch $big, ./kogen version" || put $A incremental_ready_s n/a "rebuild failed"; else put $A incremental_ready_s n/a "no .$ext source found"; fi
    s=""; failed=0; for i in $(seq 1 20); do v=$(timed ./kogen version) || failed=1; s="$s $v"; done
    if [ "$failed" = 0 ]; then put $A startup_median_s $(echo "$s" | tr ' ' '\n' | sed '/^$/d' | sort -n | awk '{a[NR]=$1} END{print (a[10]+a[11])/2}') "median of 20 ./kogen version"; else put $A startup_median_s n/a "one or more ./kogen version invocations failed"; fi
    tc=$(case $A in (rust) echo "cargo test --offline -q";; (go) echo "go test ./...";; (ts) echo "bun test";; (gleam) echo "gleam test";; (ex) echo "mix test";; esac)
    v=$(timed sh -c "$tc"); rc=$?; put $A own_tests_s "$v" "$tc (rc=$rc)"
    case $A in
      rust) lint="cargo clippy --offline --all-targets --message-format=short"; pattern='(warning|error)';;
      go) lint="golangci-lint run ./..."; pattern='\.go:[0-9]+:[0-9]+: ';;
      ts) lint='./node_modules/.bin/tsc --noEmit -p .; a=$?; ./node_modules/.bin/biome lint .; b=$?; [ "$a" = 0 ] && [ "$b" = 0 ]'; pattern='error TS|lint/|×';;
      gleam) lint="gleam build"; pattern='^warning';;
      ex) lint='mix compile --force; a=$?; mix credo --strict --format oneline; b=$?; [ "$a" = 0 ] && [ "$b" = 0 ]'; pattern='warning|^\[';;
    esac
    /bin/bash -c "$lint" > "$T/lint.log" 2>&1; lrc=$?; n=$(grep -cE "$pattern" "$T/lint.log")
    if [ "$lrc" -eq 0 ] || { [ "$lrc" -eq 1 ] && [ "$n" -gt 0 ]; }; then put "$A" lint_findings "$n" "$lint (rc=$lrc)"; else put "$A" lint_findings n/a "$lint failed (rc=$lrc): $(tail -1 "$T/lint.log" | cut -c1-120)"; fi
    case $A in
      rust) cargo build --release --offline -q > $T/rel.log 2>&1 && b=$(find target/release -maxdepth 1 -type f -perm -111 -not -name '*.d' -exec ls -l {} + | sort -k5 -n | tail -1 | awk '{print $5}') && put $A artifact_bytes $b "cargo build --release (largest binary)" || put $A artifact_bytes n/a "release build failed";;
      go) m=$(go list -f '{{if eq .Name "main"}}{{.Dir}}{{end}}' ./... 2>/dev/null | head -1); [ -n "$m" ] && go build -o $T/kogen-go "$m" 2>$T/rel.log && put $A artifact_bytes $(stat -f %z $T/kogen-go) "go build (main package)" || put $A artifact_bytes n/a "no main package / build failed";;
      ts) e=$(grep -oE '[A-Za-z0-9_./-]+\.ts' kogen | head -1); [ -n "$e" ] && bun build --compile "$e" --outfile $T/kogen-ts > $T/rel.log 2>&1 && put $A artifact_bytes $(stat -f %z $T/kogen-ts) "bun build --compile $e (includes the Bun runtime)" || put $A artifact_bytes n/a "no .ts entry in ./kogen / compile failed";;
      gleam) gleam export erlang-shipment > $T/rel.log 2>&1 && put $A artifact_bytes $(( $(du -sk build/erlang-shipment | cut -f1)*1024 )) "gleam export erlang-shipment (BEAM files; needs an Erlang runtime)" || put $A artifact_bytes n/a "erlang-shipment export failed";;
      ex) if grep -q escript mix.exs; then mix escript.build > $T/rel.log 2>&1 && b=$(ls -l $(grep -oE 'name: *"?[a-z_]+' mix.exs | head -1 | grep -oE '[a-z_]+$') 2>/dev/null | awk '{print $5}') && put $A artifact_bytes ${b:-n/a} "mix escript.build (needs an Erlang runtime)" || put $A artifact_bytes n/a "escript build failed"; else MIX_ENV=prod mix compile > $T/rel.log 2>&1 && put $A artifact_bytes $(( $(du -sk _build/prod | cut -f1)*1024 )) "MIX_ENV=prod compiled _build (no escript configured; needs Erlang+Elixir)" || put $A artifact_bytes n/a "prod compile failed"; fi;;
    esac
    else
      put "$A" cold_ready_s n/a "first ./kogen version failed: $(tail -1 "$T/last.log" | cut -c1-120)"
      for metric in incremental_ready_s startup_median_s own_tests_s lint_findings artifact_bytes; do put "$A" "$metric" n/a "cold build failed"; done
    fi )
  st=$R/out/kgstats/$A.tsv
  if [ -s $st ]; then put $A invocation_median_s $(cut -f1 $st | sort -n | awk '{a[NR]=$1} END{print a[int((NR+1)/2)]}') "median wall time of every kogen invocation during FINAL scoring (per-case timings are not recorded by the runner)"; put $A peak_rss_kb $(cut -f2 $st | sort -n | tail -1) "max RSS of kogen invocations during FINAL scoring"; else put $A invocation_median_s n/a "no FINAL scoring stats"; put $A peak_rss_kb n/a "no FINAL scoring stats"; fi
  case "$T" in "$R"/.final-metrics.?*) rm -rf "$T";; esac
done
cat $O
