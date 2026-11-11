# Bài 6 — Kịch bản Shell vận hành và Smoke Test

**Mã nguồn chính:** [`../quickbite-project/compose-control.sh`](../quickbite-project/compose-control.sh). Script nằm đúng thư mục **`quickbite-project/`** theo đề và điều khiển stack `quickbite-project/docker-compose.yml`.

```bash
cd ../quickbite-project
cp .env.example .env
./gradlew clean bootJar
./compose-control.sh start
./compose-control.sh stop
./compose-control.sh clean
```

- **start:** `docker compose up -d --build`, pg_isready 2 giây/lần (tối đa 10 giây cho DB), xác thực `/actuator/health`, thông báo xanh **`HỆ THỐNG QUICKBITE HOẠT ĐỘNG ỔN ĐỊNH!`**.
- **lỗi:** in đỏ, 20 dòng log backend cuối, `docker compose down`, exit 1.
- **stop:** `docker compose stop`.
- **clean:** `docker compose down -v` (CẢNH BÁO xóa vĩnh viễn DB volume).

Chưa có ảnh `control_success.png` vì môi trường biên soạn không có Docker. Hãy chụp kết quả chạy thật, lưu vào `quickbite-project/screenshots/control_success.png`.
