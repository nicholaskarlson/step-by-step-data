#!/usr/bin/env bash
# check.sh: the quick checks, which apply-overlay.sh runs before it commits an overlay:
# SHA256SUMS, the fixed samples, and both routes (base R when Rscript is found).
# Arguments pass through to run_all.py, for example:  bash scripts/check.sh --require-r
set -euo pipefail
cd "$(dirname "$0")/.."
py=python3
command -v python3 >/dev/null 2>&1 || py=python
exec "$py" run_all.py "$@"
