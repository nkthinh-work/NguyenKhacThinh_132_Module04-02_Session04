# BÁO CÁO THỰC HÀNH TỔNG HỢP — SESSION 04

**Chủ đề:** Container hóa backend Java Spring Boot cùng PostgreSQL bằng Docker Compose  
**Hệ thống:** QuickBite (mã Spring Boot demo minh họa, không phải code gốc)  
**Sinh viên:** *[Điền họ tên và mã sinh viên]*  
**Ngày thực hiện:** *[Điền ngày chạy thực tế]*

## I. Mục tiêu

Sử dụng Dockerfile để đóng gói Java Spring Boot thành Docker image; chạy đồng thời backend và PostgreSQL trên Docker Compose; cấu hình biến môi trường, named volume, network và theo dõi log; chứng minh dữ liệu không mất sau khi khởi tạo lại container.

## II. Nhiệm vụ 1 — Đóng gói backend

1. Có `build.gradle` (Spring Boot Web, JDBC, Actuator, PostgreSQL driver và Java 17).
2. Chạy `./gradlew clean bootJar` để tạo file `build/libs/app.jar`.
3. Dockerfile: `FROM eclipse-temurin:17-jre-alpine`, `WORKDIR /app`, `COPY build/libs/app.jar app.jar`, `ENTRYPOINT ["java", "-jar", "app.jar"]`.

**Giải thích:** Docker runtime chỉ cần JRE để chạy JAR đã build; không phải cài Gradle/JDK trong image runtime.

**Kết quả thực nghiệm:** **CHƯA CHẠY** — điền thông tin sau khi thực hiện trên Docker thật.

## III. Nhiệm vụ 2 — Hệ thống đa dịch vụ

| Service | Image/build | Kết nối, lưu trữ |
|---|---|---|
| db | `postgres:15-alpine` | Database `quickbite_db`; user `postgres`; volume `quickbite_db_data:/var/lib/postgresql/data`; không publish cổng |
| backend | `build: .` | Host 8080 → container 8080; JDBC `jdbc:postgresql://db:5432/quickbite_db` |

Hai service tham gia mạng `quickbite_network`. Backend phụ thuộc `db` healthy thông qua `pg_isready`. `.env` không được commit.

**Vì sao phải dùng `db`, không phải `localhost`?** Trong container backend, `localhost` trỏ về chính container backend. Docker Compose phân giải tên service `db` trên mạng riêng.

**Vì sao dùng named volume?** Volume lưu dữ liệu ngoài lớp ghi container; `docker compose down` không xóa volume. `docker compose down -v` xóa volume được khai báo.

## IV. Nhiệm vụ 3 — Khởi chạy và theo dõi

Chạy:

```bash
./gradlew clean bootJar
docker compose up -d --build
docker compose ps
docker compose logs --tail=100 backend
curl -fsS http://localhost:8080/actuator/health
curl -fsS http://localhost:8080/api/db-check
```

**Kết quả mong đợi:** `db` và `backend` đều Up; Spring Boot startup thành công; `/actuator/health` trả `status=UP`; `/api/db-check` chạy SQL `SELECT 1` và trả `select_1=1`.

**Kết quả thực tế:** **CHƯA CHẠY** — bổ sung kết quả terminal/log thật.

**Ảnh 1:** `screenshots/01_compose_ps.png` — *chưa có ảnh*.  
**Ảnh 2:** `screenshots/02_backend_logs.png` — *chưa có ảnh*.

## V. Nhiệm vụ 4 — Dọn dẹp

```bash
docker compose down
```

Quan sát container/network bị xóa. `quickbite_db_data` vẫn tồn tại nếu không dùng `-v`.

**Ảnh 3:** `screenshots/03_compose_down.png` — *chưa có ảnh*.

**Kiểm thử persistence bổ sung:** Tạo bảng và một dòng dữ liệu trong Postgres, chạy `down`, chạy `up -d`, kiểm tra lại dòng dữ liệu. **Chỉ ghi PASS sau khi thực hiện thực tế**.

## VI. Bài 6 — Kịch bản vận hành và smoke test

`compose-control.sh start` thực hiện Compose up/build; kiểm tra `pg_isready` cách 2 giây, tối đa 10 giây cho DB; tiếp tục kiểm tra API `/actuator/health`. Thành công in thông điệp xanh. Lỗi in đỏ, 20 dòng log backend cuối, cleanup `docker compose down`. `stop` dùng `docker compose stop`; `clean` dùng `docker compose down -v`.

**Test bẫy lỗi:** sửa `DB_PASSWORD=wrong_password` trong `.env`, vẫn giữ `POSTGRES_PASSWORD=secret`, chạy start để quan sát lỗi đăng nhập DB (và health không UP). Sau đó sửa lại `.env`.

**Kết quả thực tế:** **CHƯA CHẠY**, cần bổ sung ảnh `screenshots/control_success.png` và ảnh bẫy lỗi nếu giảng viên yêu cầu.

## VII. Kết luận

Đã hoàn thành **mã nguồn/cấu hình**; chưa xác minh Docker chạy thành công trong môi trường tạo bài, không có log hay ảnh thực thi giả.
