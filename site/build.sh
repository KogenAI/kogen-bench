#!/usr/bin/env bash
set -euo pipefail

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SITE_DIR"

npm ci --no-audit --no-fund
KOGEN_BENCH_RELEASE=true npm run release
