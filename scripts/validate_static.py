#!/usr/bin/env python3
"""Kiểm tra nội dung bài tập bằng YAML, không cần Docker Engine."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []

def check(expr, reason):
    if not expr:
        errors.append(reason)

def load(relative):
    target = ROOT / relative
    check(target.exists(), f'Missing {relative}')
    if not target.exists():
        return {}
    with target.open(encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

b1 = load('Bai_01_DNS_StoreX/docker-compose.yml')
check(b1.get('services', {}).get('backend', {}).get('environment', {}).get('SPRING_DATASOURCE_URL') == 'jdbc:postgresql://postgres:5432/storex', 'Bai 1 JDBC URL must use postgres service')

b2 = load('Bai_02_Volume_Healthcheck/docker-compose.yml')
s2 = b2.get('services', {})
for dep in ('postgres', 'redis'):
    check(s2.get('backend', {}).get('depends_on', {}).get(dep, {}).get('condition') == 'service_healthy', f'Bai 2 depends_on {dep}')
    check('healthcheck' in s2.get(dep, {}), f'Bai 2 healthcheck {dep}')
check('storex_pgdata:/var/lib/postgresql/data' in s2.get('postgres', {}).get('volumes', []), 'Bai 2 named volume postgres')

b3 = load('Bai_03_Env_CustomNetwork/docker-compose.yml')
s3 = b3.get('services', {})
check('ports' not in s3.get('postgres', {}), 'Bai 3 postgres cannot expose ports')
check('storex-net' in b3.get('networks', {}), 'Bai 3 custom network')
for x in ('backend', 'postgres'):
    check('storex-net' in s3.get(x, {}).get('networks', []), f'Bai 3 {x} must use storex-net')
check((ROOT / 'Bai_03_Env_CustomNetwork/.env.example').is_file(), 'Bai 3 .env.example')
check('${DB_PASS:' in str(b3), 'Bai 3 must interpolate DB_PASS')

b4 = load('Bai_04_Nginx_ReverseProxy/docker-compose.yml')
conf = (ROOT / 'Bai_04_Nginx_ReverseProxy/nginx.conf').read_text(encoding='utf-8')
for service, port in [('user_service', '8081'), ('product_service', '8082')]:
    check(service in b4.get('services', {}), f'Bai 4 missing service {service}')
    check(f'proxy_pass http://{service}:{port}/;' in conf, f'Bai 4 upstream {service}')
check('localhost:8081' not in conf and 'localhost:8082' not in conf, 'Bai 4 nginx should not proxy localhost')

base = load('Bai_05_Multi_Environment/docker-compose.yml')
staging = load('Bai_05_Multi_Environment/docker-compose.override.yml')
prod = load('Bai_05_Multi_Environment/docker-compose.prod.yml')
check('postgres' in base.get('services', {}) and 'backend' in base.get('services', {}), 'Bai 5 base services')
check(staging.get('services', {}).get('backend', {}).get('deploy', {}).get('replicas') == 1, 'Bai 5 staging replica')
back5 = prod.get('services', {}).get('backend', {})
check(back5.get('deploy', {}).get('replicas') == 3, 'Bai 5 production 3 replicas')
check(back5.get('deploy', {}).get('resources', {}).get('limits', {}).get('memory') == '512M', 'Bai 5 production memory')
check(back5.get('restart') == 'always', 'Bai 5 production restart')
check('ports' not in back5, 'Bai 5 production backend must not publish port')

qb = load('quickbite-project/docker-compose.yml')
qs = qb.get('services', {})
check(qs.get('db', {}).get('image') == 'postgres:15-alpine', 'Session04 postgres 15-alpine')
check('quickbite_db_data:/var/lib/postgresql/data' in qs.get('db', {}).get('volumes', []), 'Session04 DB named volume')
check('ports' not in qs.get('db', {}), 'Session04 DB port should not be mapped to host')
check('8080:8080' in qs.get('backend', {}).get('ports', []), 'Session04 backend port 8080')
check('jdbc:postgresql://db:5432/' in qs.get('backend', {}).get('environment', {}).get('SPRING_DATASOURCE_URL', ''), 'Session04 JDBC name db')
for x in ('backend', 'db'):
    check('quickbite_network' in qs.get(x, {}).get('networks', []), f'Session04 network {x}')
check(qs.get('backend', {}).get('depends_on', {}).get('db', {}).get('condition') == 'service_healthy', 'Session04 backend waits DB')

qbdocker = (ROOT / 'quickbite-project/Dockerfile').read_text(encoding='utf-8')
for s in ('FROM eclipse-temurin:17-jre-alpine', 'WORKDIR /app', 'COPY build/libs/app.jar', 'ENTRYPOINT'):
    check(s in qbdocker, f'Session04 Dockerfile contains {s}')
ctl = (ROOT / 'quickbite-project/compose-control.sh').read_text(encoding='utf-8')
for s in ('docker compose up -d --build', 'pg_isready', 'sleep 2', '/actuator/health', '--tail=20 backend', 'docker compose stop', 'docker compose down -v', 'HỆ THỐNG QUICKBITE HOẠT ĐỘNG ỔN ĐỊNH!'):
    check(s in ctl, f'Bai 6 script contains {s}')

if errors:
    print('FAILED:')
    for problem in errors:
        print(' -', problem)
    sys.exit(1)
print('PASS: cau truc cau hinh 6 bai + thuc hanh Session 04')
