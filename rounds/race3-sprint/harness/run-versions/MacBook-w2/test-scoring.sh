#!/bin/bash
R=$(cd "$(dirname "$0")" && pwd)
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 "$R/selftest.py" scoring
