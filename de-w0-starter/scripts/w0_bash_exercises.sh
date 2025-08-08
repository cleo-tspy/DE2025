#!/usr/bin/env bash
# W0 Bash exercises — run: bash scripts/w0_bash_exercises.sh

set -euo pipefail

echo "[1/5] Generate sample files in ./data"
mkdir -p data
cat > data/access.log <<'LOG'
127.0.0.1 - - [08/Aug/2025:10:00:00 +0800] "GET / HTTP/1.1" 200 512
10.0.0.2 - - [08/Aug/2025:10:00:01 +0800] "GET /api HTTP/1.1" 500 128
127.0.0.1 - - [08/Aug/2025:10:00:02 +0800] "POST /login HTTP/1.1" 200 64
192.168.0.3 - - [08/Aug/2025:10:00:03 +0800] "GET /api HTTP/1.1" 502 64
10.0.0.2 - - [08/Aug/2025:10:00:04 +0800] "GET / HTTP/1.1" 404 32
LOG

cat > data/sales.csv <<'CSV'
date,city,amount
2025-08-01,Taipei,100.0
2025-08-01,Taichung,80.0
2025-08-02,Taipei,120.0
2025-08-02,Tainan,50.5
CSV

echo "[2/5] Pipeline: top status codes -> ./artifacts/status_top.txt"
mkdir -p artifacts
cut -d' ' -f9 data/access.log | sort | uniq -c | sort -nr > artifacts/status_top.txt
echo "Done. See artifacts/status_top.txt"

echo "[3/5] Redirection: extract errors -> ./artifacts/errors.log"
grep ' 5[0-9][0-9] ' data/access.log > artifacts/errors.log
echo "Done. See artifacts/errors.log"

echo "[4/5] grep/awk/sed mini tasks"
echo "- grep count 404 and 500-series"
grep -c ' 404 ' data/access.log | sed 's/^/404_count=/' > artifacts/grep_counts.txt
grep -c ' 5[0-9][0-9] ' data/access.log | sed 's/^/5xx_count=/' >> artifacts/grep_counts.txt

echo "- awk sum bytes column (field 10)"
awk '{sum+=$10} END{print sum}' data/access.log > artifacts/bytes_sum.txt

echo "- sed replace HTTP version with HTTP" 
sed -E 's#HTTP/[0-9.]+#HTTP#g' data/access.log > artifacts/access_clean.log

echo "[5/5] Show preview"
head -n 3 artifacts/status_top.txt || true
head -n 3 artifacts/errors.log || true

echo "All Bash tasks completed."
