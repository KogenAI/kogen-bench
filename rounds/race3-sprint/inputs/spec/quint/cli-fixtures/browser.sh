#!/bin/sh
python3 '${fixtures}/cli-fixtures/server.py' browser "$1" >'${control}/cli-browser.log' 2>&1 &
exit 0
