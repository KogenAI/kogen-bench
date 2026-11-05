# env.sh (sourced by runsuite.sh; paths relative to the user's home, no secrets)
M=$HOME/.local/share/mise/installs
export PATH=$M/go/1.27.2/bin:$M/node/24.21.0/bin:$M/python/3.13.16/bin:/usr/local/bin:/usr/bin:/bin
umask 022
export LABW=${LABW:?set LABW to the scratch work dir}
export TMPDIR=$LABW/tmp GOTMPDIR=$LABW/tmp/go GOCACHE=$LABW/gocache GOMAXPROCS=2 GOFLAGS="-mod=mod -p=2"
mkdir -p $TMPDIR $GOTMPDIR $GOCACHE
