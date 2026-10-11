RACE6_ENV_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
if [ "$(uname -s)" = Darwin ]; then source "$RACE6_ENV_ROOT/env-studio.sh"; else source "$RACE6_ENV_ROOT/env-linux.sh"; fi
source "$RACE6_ENV_ROOT/mode-env.sh" "$RACE6_ENV_ROOT" || return $?
unset RACE6_ENV_ROOT
