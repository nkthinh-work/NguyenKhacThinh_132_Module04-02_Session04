#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v docker >/dev/null || { echo 'Can Docker Compose.' >&2; exit 1; }
q() { docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U admin -d storex_db -t -A -c "$1"; }

echo 'Dang khoi dong he thong...'
docker compose up -d --build
# Cho service_healthy va ket noi PostgreSQL thuc te
ready=0
for i in {1..30}; do
    if docker compose exec -T postgres pg_isready -U admin -d storex_db >/dev/null 2>&1; then ready=1; break; fi
    sleep 2
done
((ready == 1)) || { echo 'PostgreSQL chua san sang.' >&2; exit 1; }
q 'CREATE TABLE IF NOT EXISTS persistence_probe (id TEXT PRIMARY KEY, created_at TIMESTAMPTZ DEFAULT NOW());' >/dev/null
marker="persist_$(date +%s)_$$"
q "INSERT INTO persistence_probe (id) VALUES ('$marker');" >/dev/null
before="$(q "SELECT count(*) FROM persistence_probe WHERE id = '$marker';" | tr -d '[:space:]')"
[[ "$before" == 1 ]] || { echo "Insert that bai: $before" >&2; exit 1; }
echo "Da luu ban ghi: $marker"

echo 'docker compose down (KHONG xoa volume)...'
docker compose down
echo 'Khoi dong lai...'
docker compose up -d
ready=0
for i in {1..30}; do
    if docker compose exec -T postgres pg_isready -U admin -d storex_db >/dev/null 2>&1; then ready=1; break; fi
    sleep 2
done
((ready == 1)) || { echo 'PostgreSQL sau khoi dong chua san sang.' >&2; exit 1; }
after="$(q "SELECT count(*) FROM persistence_probe WHERE id = '$marker';" | tr -d '[:space:]')"
if [[ "$after" == 1 ]]; then
    echo "PASS: Ban ghi $marker van ton tai sau docker compose down/up"
else
    echo "FAIL: Ban ghi bien mat (ket qua = $after)" >&2
    exit 1
fi
