#!/usr/bin/env python3
"""Test luong dieu khien compose-control.sh voi docker/curl GIA LAP.

Khong xac nhan daemon Docker/PostgreSQL/Spring Boot chay that.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / 'quickbite-project' / 'compose-control.sh'
PASS_TEXT = 'HỆ THỐNG QUICKBITE HOẠT ĐỘNG ỔN ĐỊNH!'

with TemporaryDirectory(prefix='quickbite-mock-') as temp:
    t = Path(temp)
    (t / 'mockbin').mkdir()
    (t / 'build' / 'libs').mkdir(parents=True)
    shutil.copy2(CONTROL, t / 'compose-control.sh')
    shutil.copy2(ROOT / 'quickbite-project' / '.env.example', t / '.env')
    (t / 'build' / 'libs' / 'app.jar').write_bytes(b'mock-not-real-jar')
    fake_docker = t / 'mockbin' / 'docker'
    fake_docker.write_text('''#!/usr/bin/env bash
printf '%s\\n' "docker $*" >> "$MOCK_TRACE"
if [[ "${MOCK_UP_FAIL:-0}" == 1 && "$*" == *'compose up '* ]]; then exit 1; fi
if [[ "${MOCK_DB_FAIL:-0}" == 1 && "$*" == *'pg_isready'* ]]; then exit 1; fi
exit 0
''',encoding='utf-8')
    fake_curl = t / 'mockbin' / 'curl'
    fake_curl.write_text('''#!/usr/bin/env bash
printf '%s\\n' "curl $*" >> "$MOCK_TRACE"
if [[ "${MOCK_API_FAIL:-0}" == 1 ]]; then echo '{"status":"DOWN"}'; else echo '{"status":"UP"}'; fi
''',encoding='utf-8')
    fake_sleep = t / 'mockbin' / 'sleep'
    fake_sleep.write_text('#!/usr/bin/env bash\nexit 0\n',encoding='utf-8')
    for p in (fake_docker, fake_curl, fake_sleep):
        p.chmod(0o755)
    trace = t / 'calls.log'
    env_base = {**os.environ, 'PATH': f"{t / 'mockbin'}:{os.environ['PATH']}", 'MOCK_TRACE': str(trace)}

    def run(cmd, **switches):
        trace.write_text('', encoding='utf-8')
        env = {**env_base, **switches}
        result = subprocess.run(['bash', str(t / 'compose-control.sh'), cmd],cwd=t,env=env,
                                capture_output=True,text=True,timeout=10)
        return result, trace.read_text(encoding='utf-8')

    passed = 0
    def check(condition, message):
        global passed
        if not condition: raise AssertionError(message)
        print('PASS:',message)
        passed += 1

    a, log = run('start')
    check(a.returncode == 0 and PASS_TEXT in a.stdout and 'pg_isready' in log and 'actuator/health' in log,
          'start thanh cong: DB + API health + mau xanh')
    a, log = run('stop')
    check(a.returncode == 0 and 'docker compose stop' in log, 'stop goi docker compose stop')
    a, log = run('clean')
    check(a.returncode == 0 and 'docker compose down -v' in log, 'clean goi docker compose down -v')
    a, log = run('start',MOCK_DB_FAIL='1')
    check(a.returncode == 1 and log.count('pg_isready') == 5 and 'docker compose logs --no-color --tail=20 backend' in log and 'docker compose down' in log,
          'DB fail: 5 lan polling, log 20 dong va down')
    a, log = run('start',MOCK_API_FAIL='1')
    check(a.returncode == 1 and log.count('actuator/health') == 15 and 'docker compose down' in log,
          'API fail: khong in thanh cong va chay cleanup')
    a, log = run('start',MOCK_UP_FAIL='1')
    check(a.returncode == 1 and 'docker compose down' in log,
          'Compose up fail: chay cleanup')
    print(f'TOTAL: {passed} mock tests PASS (KHONG phai kiem thu Docker that)')
