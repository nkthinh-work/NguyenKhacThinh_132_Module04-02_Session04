# Bài 1 — Sửa lỗi kết nối `Connection refused`

**Nguyên nhân:** `localhost` trong container backend trỏ đến **chính container backend**, không trỏ đến PostgreSQL chạy ở container khác. Docker Compose gắn các container thuộc project vào một mạng mặc định và đăng ký **tên service** lên DNS nội bộ.

Dòng bị lỗi: `jdbc:postgresql://localhost:5432/storex`.

**Dòng đã sửa:**

```yaml
SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/storex
```

Trong đó `postgres` là tên service trong `docker-compose.yml`, cổng `5432` là cổng **nội bộ** PostgreSQL. Không cần công bố (`ports`) cổng PostgreSQL ra host để backend kết nối được.

Đã bổ sung `healthcheck` và `depends_on: condition: service_healthy` để backend chờ PostgreSQL chấp nhận kết nối, tránh lỗi khởi động do DB chưa sẵn sàng.

## Lệnh kiểm chứng

```bash
docker compose up -d --build
docker compose ps
docker compose logs --tail=60 backend
curl -i http://localhost:8080/api/db-check
```

Với backend **demo đi kèm**, endpoint `/api/db-check` dùng JDBC thực hiện `SELECT 1`, trả kết quả thành công khi Postgres hoạt động. **Ảnh log thực tế phải tự chụp từ máy có Docker.**

Dừng: `docker compose down`.
