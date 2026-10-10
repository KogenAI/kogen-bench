#!/bin/sh
set -eu
rm -rf build/dev build/prod build/lsp build/erlang-shipment _build target
if [ -L priv ]; then
    rm -f priv
fi
