#!/bin/bash
# mutate.sh <label> : the mutation control. A copy of tree <label> (scratch only) gets M01: a budget-off Build now carries a budget
# (limit 1000) in its checkpoint state; the budget-off tests must fail on it. Builds <label>-M01.test next to the others.
. "$(dirname "$0")/env.sh"; L=$1; M=$L-M01; [ -d $W/trees/$M ] || cp -R $W/trees/$L $W/trees/$M
cd $W/trees/$M/build || exit 1
grep -q 'if ext == nil && in.BuildRequestBudget > 0 {' build.go || { echo "mutation anchor not found"; exit 2; }
sed -i 's/if ext == nil \&\& in.BuildRequestBudget > 0 {/if ext == nil {/; s/Limit: in.BuildRequestBudget}/Limit: in.BuildRequestBudget + 1000}/' build.go
grep -c 'in.BuildRequestBudget + 1000' build.go
go test -c -o $W/bin/$M.test . && echo built $M
