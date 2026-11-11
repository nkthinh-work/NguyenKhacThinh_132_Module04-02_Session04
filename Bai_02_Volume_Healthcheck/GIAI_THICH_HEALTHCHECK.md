# Bài 2 — Healthcheck, dependency và volume

## 1. Vì sao `depends_on: [postgres, redis]` chưa đủ?

Cú pháp ngắn chỉ quy định container phụ thuộc được **khởi động trước**, không đảm bảo dịch vụ trong container đã sẵn sàng phục vụ yêu cầu. Ví dụ, PostgreSQL còn đang khởi tạo dữ liệu hoặc Redis chưa sẵn sàng thì backend vẫn có thể kết nối thất bại.

## 2. Cấu hình đã triển khai

- PostgreSQL dùng `pg_isready -U $POSTGRES_USER -d $POSTGRES_DB`. Trạng thái `healthy` báo tiến trình DB đang chấp nhận kết nối (không thay thế hoàn toàn việc xác thực bằng tài khoản ứng dụng).
- Redis dùng `redis-cli ping`, thành công khi trả `PONG`.
- Backend khai báo `depends_on.postgres.condition: service_healthy` và tương tự cho Redis.
- Volume có tên `storex_pgdata` được mount đến **`/var/lib/postgresql/data`**. Dữ liệu không nằm trong lớp ghi tạm của container, nên việc xóa container hoặc `docker compose down` **không xóa** dữ liệu.

> **Chú ý:** `docker compose down -v` hoặc xóa volume thủ công **sẽ xóa dữ liệu**. `depends_on` không tự động đảm bảo backend được khởi động lại khi DB mất kết nối giữa chừng.

## 3. Kiểm chứng

```bash
docker compose up -d --build
docker compose ps
docker compose logs --tail=50 backend
curl -fsS http://localhost:8080/api/db-check
curl -fsS http://localhost:8080/api/cache-check
bash test_persistence.sh
```

`test_persistence.sh` tạo một hàng kiểm chứng trong PostgreSQL, chạy `down` (không `-v`), khởi động lại và xác nhận hàng còn tồn tại. Cần Docker đang hoạt động. Dữ liệu test nằm trong DB demo.

**Kết quả:** Chưa chạy container tại môi trường biên soạn; không có ảnh kiểm chứng giả.
