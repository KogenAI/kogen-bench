#!/bin/sh
# Model-free. usage: run-mode.sh <a|b|a-noci|b-ci> <rails app tree> <scratch dir> <ruby bin dir> <vips preload .rb>
# Runs the declared probe command in a fresh copy of the tree (no .git, no .kogen/local) under one environment, built with `env -i`.
#   a      the shaper session's environment (caller variables set by the benchmark harness)
#   b      the readiness probe environment (the allowlist of verify/probe.go probeEnv, private empty HOME)
#   a-noci a without CI_PROGRESS_BAR      b-ci  b plus CI_PROGRESS_BAR=0
M=$1; SRC=$2; S=$3; RB=$4; VIPS=-r$5
W=$S/run-$M; [ -e "$W" ] && { echo "refuse: $W exists"; exit 2; }
mkdir -p "$W/tree" "$W/home" "$W/tmp" || exit 2
for e in $(ls -A "$SRC"); do [ "$e" = .git ] || cp -R "$SRC/$e" "$W/tree/$e"; done
rm -rf "$W/tree/.kogen/local" 2>/dev/null
CMD="env -u RUBYOPT PARALLEL_WORKERS=1 bin/rails test test/models/zip_file_test.rb 2>&1 | grep -E \"runs,|rror|Could not|aborted\" | cut -c1-200 | head -n 5; true"
cd "$W/tree" || exit 2
case $M in
 a)      ENVV="PATH=$RB:$PATH RUBYOPT=$VIPS CI_PROGRESS_BAR=0 DATABASE_ADAPTER=sqlite SE_AVOID_STATS=true PARALLEL_WORKERS=2 HOME=$HOME" ;;
 a-noci) ENVV="PATH=$RB:$PATH RUBYOPT=$VIPS DATABASE_ADAPTER=sqlite SE_AVOID_STATS=true PARALLEL_WORKERS=2 HOME=$HOME" ;;
 b)      ENVV="PATH=$RB:$PATH LANG=en_US.UTF-8 MISE_DATA_DIR=$HOME/.local/share/mise TMPDIR=$W/tmp MISE_TRUSTED_CONFIG_PATHS=$W/tree:$W/tmp HOME=$W/home" ;;
 b-ci)   ENVV="PATH=$RB:$PATH LANG=en_US.UTF-8 MISE_DATA_DIR=$HOME/.local/share/mise TMPDIR=$W/tmp MISE_TRUSTED_CONFIG_PATHS=$W/tree:$W/tmp HOME=$W/home CI_PROGRESS_BAR=0" ;;
esac
echo "mode=$M"
echo "env names:"; env -i $ENVV sh -c "env | cut -d= -f1 | sort | tr \"\n\" \" \""; echo
echo "which ruby: $(env -i $ENVV sh -c "which ruby")"
echo "ruby: $(env -i $ENVV sh -c "ruby -v")"
echo "bundle list (minitest, rails, ffi):"; env -i $ENVV sh -c "env -u RUBYOPT bundle list 2>&1 | grep -E \"minitest|  \* rails |  \* ffi \""
echo "probe command output:"
env -i $ENVV sh -c "$CMD"
