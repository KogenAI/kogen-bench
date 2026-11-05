# env.sh: sourced by the C6 scripts on the Linux host (as lanes). No env is printed.
W=${W:-$HOME/work.noindex/scratch/research/work/lab-c6}; export W
export PATH=$HOME/.local/share/mise/installs/go/1.27.2/bin:/usr/local/bin:/usr/bin:/bin
[ -d $HOME/.local/share/mise/installs/node ] && export PATH=$(ls -d $HOME/.local/share/mise/installs/node/*/bin 2>/dev/null | tail -1):$PATH
export GOCACHE=$W/gocache GOMODCACHE=$W/gomod TMPDIR=$W/tmp GOTOOLCHAIN=local GOFLAGS=-mod=mod GONOSUMDB=github.com/KogenAI GOWORK=off
mkdir -p $W/tmp $W/trees $W/prod $W/bin $W/out
