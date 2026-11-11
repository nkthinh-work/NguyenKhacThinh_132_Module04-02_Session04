#!/usr/bin/env bash
# Bai 6: quan ly vong doi QuickBite (chi tac dong Compose project trong folder nay)
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
err() { printf '%b%s%b\n' "$RED" "$*" "$NC" >&2; }
ok() { printf '%b%s%b\n' "$GREEN" "$*" "$NC"; }
usage() { echo 'Cach dung: ./compose-control.sh {start|stop|clean}' >&2; exit 2; }

failure() {
    err 'HE THONG QUICKBITE KHOI DONG THAT BAI.'
    err '20 dong log backend cuoi cung:'
    docker compose logs --no-color --tail=20 backend >&2 || true
    err 'Dang don dep container va network (KHONG xoa volume du lieu)...'
    docker compose down || true
    exit 1
}

case "${1:-}" in
    start)
        command -v docker >/dev/null 2>&1 || { err 'Chua cai Docker'; exit 1; }
        command -v curl >/dev/null 2>&1 || { err 'Chua cai curl (can de kiem tra Actuator)'; exit 1; }
        [[ -f .env ]] || { err 'Chua co .env. Chay: cp .env.example .env'; exit 1; }
        # De bai yeu cau co san app.jar tu lenh ./gradlew clean bootJar
        [[ -f build/libs/app.jar ]] || {
            err 'Chua co build/libs/app.jar. Chay truoc: ./gradlew clean bootJar'
            exit 1
        }
        echo 'Dang chay: docker compose up -d --build'
        docker compose up -d --build || failure

        # Kiem tra pg_isready moi 2 giay; tong thoi gian cho DB <= 10 giay.
        db_ready=0
        for attempt in {1..5}; do
            if docker compose exec -T db sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"' >/dev/null 2>&1; then
                db_ready=1
                break
            fi
            sleep 2
        done
        (( db_ready == 1 )) || { err 'PostgreSQL chua ready sau 10 giay'; failure; }

        # Actuator co the can them thoi gian de JVM/Spring Boot khoi dong.
        api_ready=0
        for attempt in {1..15}; do
            if curl -fsS --max-time 2 http://localhost:8080/actuator/health \
                | grep -Eq '"status"[[:space:]]*:[[:space:]]*"UP"'; then
                api_ready=1
                break
            fi
            sleep 2
        done
        (( api_ready == 1 )) || { err 'API /actuator/health khong tra ve UP'; failure; }
        ok 'HỆ THỐNG QUICKBITE HOẠT ĐỘNG ỔN ĐỊNH!'
        ;;
    stop)
        command -v docker >/dev/null 2>&1 || { err 'Chua cai Docker'; exit 1; }
        docker compose stop
        ;;
    clean)
        command -v docker >/dev/null 2>&1 || { err 'Chua cai Docker'; exit 1; }
        echo 'CANH BAO: docker compose down -v SE XOA CA NAMED VOLUME VA DU LIEU POSTGRESQL.' >&2
        docker compose down -v
        ;;
    *) usage ;;
esac
