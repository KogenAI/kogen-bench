#!/bin/bash
# mk-crane-case.sh <name> <fix sha> <test file> : base = fix^ tree (git archive), test.patch = the fix's new test file,
# fix.patch = the fix's non-test, non-doc source changes. Public repo github.com/zig-whatwg/crane.
set -eu
W=${WORK:?set WORK to a directory that holds crane.git, a clone of github.com/zig-whatwg/crane}; G="/usr/bin/git -C $W/crane.git"
N=$1; FIX=$2; TF=$3; C=$W/kit/cases/$N
P=$($G rev-parse "$FIX^"); FIXF=$($G rev-parse "$FIX")
mkdir -p $C/base; $G archive $P | tar x -C $C/base
$G diff --no-ext-diff $P $FIXF -- "$TF" > $C/test.patch
$G diff --no-ext-diff $P $FIXF -- . ":(exclude)$TF" ":(exclude)docs" ":(exclude)*.md" > $C/fix.patch
printf 'repo https://github.com/zig-whatwg/crane\nfix %s\nbase %s\ntest_file %s\n' $FIXF $P "$TF" > $C/origin
echo "$N base=$P fix=$FIXF test=$(wc -l < $C/test.patch) ref=$(wc -l < $C/fix.patch) files=$(grep -c '^diff --git' $C/fix.patch)"
