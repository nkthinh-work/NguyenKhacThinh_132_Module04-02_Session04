# Bài 5 — Thiết kế triển khai đa môi trường

## Ba file đúng yêu cầu đề

- **`docker-compose.yml`** (base): cấu hình chung backend và postgres, environment nhận qua `.env`, network nội bộ, volume DB.
- **`docker-compose.override.yml`**: staging/dev, **một** backend, publish `8080:8080` để debug. Compose tự động nạp override khi dùng `docker compose up`, nhưng script chỉ rõ hai file để tránh nhầm.
- **`docker-compose.prod.yml`**: production, `deploy.replicas: 3`, `restart: always`, `deploy.resources.limits.memory: 512M`, không bind cổng backend để tránh xung đột giữa 3 replica.

### Khởi chạy staging

```bash
cp .env.example .env
./deploy.sh staging
./deploy.sh status-staging
curl -fsS http://localhost:8080/api/db-check
./deploy.sh down-staging
```

### Khởi chạy production

```bash
./deploy.sh production
./deploy.sh status-production
# Lenh Compose tuong duong (KHONG su dung override staging):
docker compose -p storex-production -f docker-compose.yml -f docker-compose.prod.yml up -d --build --scale backend=3
./deploy.sh down-production
```

`docker compose ... up` hỗ trợ Compose hiện đại (V2), không bắt buộc Docker Swarm. `deploy.replicas` kèm `--scale backend=3` nhằm chỉ rõ mục tiêu số lượng instance. Nếu muốn public API production, cần thêm reverse proxy/load balancer vào cùng network và publish cổng **proxy**, không publish cổng từng bản sao backend.

**Giới hạn thiết kế của bài thực hành:** Staging và production chạy với 2 project Compose khác nhau nên hai bộ volume DB tách biệt, song **không có cấu hình secret manager, TLS, backup, giám sát hoặc HA DB**. Không dùng bản mẫu làm production Internet thật nếu chưa bổ sung các thành phần này.
