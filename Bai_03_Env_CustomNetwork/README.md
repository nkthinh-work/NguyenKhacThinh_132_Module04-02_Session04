# Bài 3 — Tách biến nhạy cảm & mạng nội bộ

## Cấu hình

1. Đã chuyển tài khoản/mật khẩu DB ra `.env` (template an toàn là `.env.example`).
2. Compose sử dụng `${DB_USER}` và `${DB_PASS}` **thay vì viết cứng**.
3. Đã **xóa `ports: 5432:5432`** của PostgreSQL, nên host không kết nối trực tiếp qua cổng 5432 mặc định.
4. Hai service cùng tham gia custom bridge network **`storex-net`**, có DNS theo tên service `postgres`.

## Cách chạy

```bash
cp .env.example .env
# Sua DB_PASS trong .env neu can
docker compose config   # Kiem tra interpolation; KHONG chia se output neu co secrets
docker compose up -d --build
curl -fsS http://localhost:8080/api/db-check
docker compose ps
docker compose down
```

**Bảo mật:** Không commit `.env` thật; `.gitignore` ở root đã chặn. Đổi mật khẩu mẫu khi dùng ngoài môi trường học tập. `networks` của Compose chỉ kiểm soát các container tham gia mạng này; các container được nối vào cùng mạng vẫn có thể kết nối nhau. Không nên tuyên bố đây là cách ly an ninh tuyệt đối.
