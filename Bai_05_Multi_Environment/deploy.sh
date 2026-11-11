#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v docker >/dev/null || { echo "Can cai Docker" >&2; exit 1; }
[[ -f .env ]] || { echo "Chua co .env. Chay: cp .env.example .env" >&2; exit 1; }
base=(docker compose -p storex-staging -f docker-compose.yml -f docker-compose.override.yml)
prod=(docker compose -p storex-production -f docker-compose.yml -f docker-compose.prod.yml)
case "${1:-}" in
  staging)         "${base[@]}" up -d --build ;;
  status-staging)  "${base[@]}" ps ;;
  down-staging)    "${base[@]}" down ;;
  production)      "${prod[@]}" up -d --build --scale backend=3 ;;
  status-production) "${prod[@]}" ps ;;
  down-production) "${prod[@]}" down ;;
  *) echo 'Cach dung: ./deploy.sh {staging|status-staging|down-staging|production|status-production|down-production}' >&2; exit 2 ;;
esac
