# Rikkei Education — Bài Docker Compose 1–6 & thực hành Session 04

Đây là **bài làm mã nguồn** dựa trên 7 đề PDF gửi kèm (b1–b6 và bài thực hành tổng hợp Session 04). Repo có cấu hình Docker Compose, Nginx, shell script điều khiển, báo cáo và **backend Spring Boot mẫu tự tạo** nhằm cho phép kiểm thử khi chưa có mã nguồn/image thực tế của StoreX hoặc QuickBite.

> **Quan trọng:** Backend trong `storex-demo/` và `quickbite-project/` là **demo**, không phải mã nguồn chính thức Rikkei/StoreX/QuickBite. Chưa có Docker engine trong môi trường tạo bài nên **chưa xác nhận chạy container thực tế**, chưa có ảnh bằng chứng. Chỉ chụp ảnh sau khi bạn tự chạy thành công; không dùng ảnh mô phỏng nộp bài.

## Mục lục

| Đề | Đường dẫn | Yêu cầu đã triển khai |
|---|---|---|
| Bài 1 | `Bai_01_DNS_StoreX/` | Sửa JDBC URL `localhost` ➜ tên service `postgres` |
| Bài 2 | `Bai_02_Volume_Healthcheck/` | Healthcheck PostgreSQL, Redis; `service_healthy`; named volume |
| Bài 3 | `Bai_03_Env_CustomNetwork/` | `.env.example`, `${DB_PASS}`, mạng `storex-net`, không publish 5432 |
| Bài 4 | `Bai_04_Nginx_ReverseProxy/` | DNS service `user_service`/`product_service`, sửa đường dẫn proxy |
| Bài 5 | `Bai_05_Multi_Environment/` | Compose base + override staging + production (3 replica, 512 MB, restart) |
| Bài 6 | `quickbite-project/compose-control.sh` | `start`, `stop`, `clean`, pg_isready, Actuator health, logs lỗi |
| Tổng hợp | `quickbite-project/` | Dockerfile Java 17, Gradle, Compose `db`/`backend`, báo cáo Markdown |

## Chuẩn bị

- Docker Desktop (Windows, macOS) hoặc Docker Engine + Docker Compose v2 (Linux). Trên Windows, dùng Git Bash hoặc WSL để chạy các file `.sh`; có thể dùng `gradlew.bat` trong CMD/PowerShell. Kiểm tra: `docker --version` và `docker compose version`.
- Kết nối Internet lần đầu để pull image Gradle, Java, PostgreSQL, Redis, Python và Nginx, đồng thời tải dependency Java.
- RAM trống phù hợp để build Java và chạy nhiều container.
- Không chạy tất cả bài cùng lúc vì nhiều bài cùng chiếm cổng 8080 / 80.

## Cách chạy nhanh

### Bài 1
```bash
cd Bai_01_DNS_StoreX
docker compose up -d --build
docker compose ps
docker compose logs --tail=50 backend
curl -fsS http://localhost:8080/api/db-check
docker compose down
```

### Bài 2
```bash
cd Bai_02_Volume_Healthcheck
docker compose up -d --build
docker compose ps
bash test_persistence.sh
```

### Bài 3
```bash
cd Bai_03_Env_CustomNetwork
cp .env.example .env        # doi mat khau demo truoc khi su dung thuc te
docker compose up -d --build
curl -fsS http://localhost:8080/api/db-check
docker compose down
```

### Bài 4
```bash
cd Bai_04_Nginx_ReverseProxy
docker compose up -d --build
curl -i http://localhost/users/
curl -i http://localhost/products/
docker compose down
```

### Bài 5
```bash
cd Bai_05_Multi_Environment
cp .env.example .env
bash deploy.sh staging
bash deploy.sh down-staging
bash deploy.sh production
bash deploy.sh status-production
bash deploy.sh down-production
```

### Bài 6 + thực hành Session 04
```bash
cd quickbite-project
cp .env.example .env
./gradlew clean bootJar
./compose-control.sh start
./compose-control.sh stop
./compose-control.sh clean  # CANH BAO: xoa ca named volume du lieu
```

`./gradlew` trong repo là **script trợ giúp tương thích cách gọi Gradle**, chạy Gradle có sẵn trên máy hoặc sử dụng image `gradle:8.10.2-jdk17` qua Docker, **không phải wrapper chính thức `gradle-wrapper.jar`**. Nhờ vậy có thể build JAR trên máy chỉ cài Docker.

## Tài liệu báo cáo và ảnh

- Xem `Bai_01.../GIAI_THICH.md`, `Bai_02.../GIAI_THICH_HEALTHCHECK.md` và README từng bài.
- Xem `quickbite-project/report_session04.md` là mẫu báo cáo **đã viết phần lý thuyết/cấu hình**; phần log và screenshot đánh dấu **CHƯA THỰC THI**.
- Xem `HUONG_DAN_CHUP_ANH.md` để biết các ảnh thật phải chụp và đưa vào repo.
- Có `scripts/validate_static.py` và `scripts/test_control_mock.py` để kiểm tra cấu hình/lệnh điều khiển (mô phỏng) không cần Docker.

## Commit và push lên GitHub

```bash
git init
git add .
git commit -m "Complete Docker Compose exercises 1-6 and Session 04"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

**Đừng commit `.env` thật**, dữ liệu database hay thông tin cá nhân. `docker compose down` giữ lại volume; riêng `docker compose down -v`/`clean` **xóa vĩnh viễn volume**.
