#!/usr/bin/env bash
# Regenerates every table/figure in out/ and then checks the headline numbers.
# Usage:  ./run_all.sh            (uses python3 on PATH; set PYTHON=.venv/bin/python to use a venv)
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
mkdir -p out
for s in clock_noise scenarios poc_phases redteam_checks floor_envelope floor_sa65_premise navigator; do
  echo "=== $s.py"; "$PY" "$s.py" > "out/_log_$s.txt"; tail -n 3 "out/_log_$s.txt"
done
echo "=== hybrid_gnss.py"; "$PY" hybrid_gnss.py | tee out/I_hybrid_gnss_ka.txt
rm -f out/_log_*.txt
echo "=== check_results.py"; "$PY" check_results.py
