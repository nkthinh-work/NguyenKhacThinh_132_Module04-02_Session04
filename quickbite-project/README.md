# QuickBite — Bài 6 + Bài thực hành tổng hợp Session 04

Đây là **backend Spring Boot demo tối thiểu** tự viết thêm vì đề PDF chỉ cung cấp yêu cầu và lệnh `./gradlew clean bootJar`, **không cung cấp source QuickBite gốc**. Source demo có Actuator health và endpoint JDBC `SELECT 1` để kiểm chứng Docker Compose/PostgreSQL.

## Nhiệm vụ 1 — Dockerfile

- `FROM eclipse-temurin:17-jre-alpine`
- `WORKDIR /app`
- `COPY build/libs/app.jar app.jar`
- `ENTRYPOINT ["java", "-jar", "app.jar"]`

`bootJar` được cấu hình sinh đúng `build/libs/app.jar`.

## Nhiệm vụ 2 — Docker Compose

- `db`: `postgres:15-alpine`, user `postgres`, password `secret`, DB `quickbite_db` (mẫu trong `.env.example`), `quickbite_db_data:/var/lib/postgresql/data` và **không ánh xạ cổng 5432**.
- `backend`: build từ `.`, cổng `8080:8080`, JDBC `jdbc:postgresql://db:5432/quickbite_db`, phụ thuộc `db` healthy.
- Cả hai cùng mạng `quickbite_network`.

`POSTGRES_PASSWORD` và `DB_PASSWORD` được **tách thành hai biến** để kiểm thử sai mật khẩu backend mà không đổi password DB được khởi tạo trước đó.

## Chạy bài tổng hợp lần đầu

```bash
cd quickbite-project
cp .env.example .env
./gradlew clean bootJar
docker compose up -d --build
docker compose ps
docker compose logs --tail=100 backend
curl -fsS http://localhost:8080/actuator/health
curl -fsS http://localhost:8080/api/db-check
docker compose down    # KHONG xoa volume
```

> `./gradlew` là **script hỗ trợ** Gradle/Docker, không phải Gradle Wrapper chuẩn. Máy chỉ cần Docker đang chạy hoặc cài Gradle tương thích. Lần đầu sẽ tải dependencies từ Maven Central nên cần Internet. Khi có backend QuickBite thật, phải thay source demo bằng mã nguồn gốc.

## Bài 6 — script điều khiển

```bash
chmod +x compose-control.sh
./compose-control.sh start
./compose-control.sh stop
./compose-control.sh clean  # XOA TOAN BO VOLUME
```

`start` chạy `docker compose up -d --build`, kiểm tra `pg_isready` mỗi 2 giây (DB timeout 10 giây), sau đó đợi Actuator trả `{"status":"UP"}` (tối đa ~30 giây vì JVM khởi động chậm). Thất bại sẽ in thông báo đỏ, 20 dòng log backend cuối và chạy `docker compose down`, **không xóa volume**. `stop` dùng `docker compose stop`; `clean` dùng `docker compose down -v`.

### Test bẫy lỗi sai mật khẩu

1. Chạy `./compose-control.sh stop` nếu hệ thống đang chạy.
2. Giữ `POSTGRES_PASSWORD=secret` trong `.env`, đổi **`DB_PASSWORD=wrong_password`**.
3. Chạy `./compose-control.sh start`; dự kiến script báo lỗi đỏ, in log backend, dọn container.
4. Trả lại `DB_PASSWORD=secret` rồi chạy `./compose-control.sh start`.

**Lưu ý:** thay `POSTGRES_PASSWORD` trong `.env` không thay đổi mật khẩu của DB đã khởi tạo trong named volume cũ. Không xóa volume nếu cần giữ dữ liệu.

## Nhiệm vụ 3 và 4

Chụp ảnh thật `docker compose ps`, `docker compose logs backend`, `docker compose down` khi chạy trên máy bạn. Thêm vào `screenshots/`; dùng `report_session04.md` để hoàn thiện phần kết quả thực tế.
