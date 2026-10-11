#!/bin/bash
set -e
if [ "$(uname -s)" = Darwin ]; then exec /usr/bin/time -l "$@"; fi
exec /usr/bin/time -f '%e real %U user %S sys\n%M maximum resident set size (KiB)' "$@"
