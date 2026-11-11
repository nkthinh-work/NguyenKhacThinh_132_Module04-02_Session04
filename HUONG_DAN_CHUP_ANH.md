# Hướng dẫn chụp ảnh bằng chứng để nộp bài

Trong repo chưa có **ảnh chụp chạy thật** vì môi trường tạo bài không cài Docker. Chỉ chụp sau khi chạy trên máy cá nhân có Docker Desktop/Engine, không dựng ảnh giả bằng công cụ vẽ hay chỉnh sửa nội dung terminal.

## Bài 1 — `Bai_01_DNS_StoreX/`

Chạy `docker compose up -d --build`, `docker compose ps`, `docker compose logs --tail=50 backend` và `curl -fsS http://localhost:8080/api/db-check`. Chụp console cho thấy backend trả được kết nối DB; lưu thành `Bai_01_DNS_StoreX/connection_success.png`. Đề gợi ý nộp ảnh log qua Releases/Issues GitHub.

## Bài 2 — `Bai_02_Volume_Healthcheck/`

Chạy `docker compose up -d --build`, `docker compose ps` để hiện `healthy` của Postgres/Redis và `bash test_persistence.sh` để kiểm tra bản ghi tồn tại sau down/up. Có thể lưu ảnh kiểm thử `persistence_success.png`. Cần nộp kèm `GIAI_THICH_HEALTHCHECK.md`.

## Bài 3 — `Bai_03_Env_CustomNetwork/`

Chụp `docker compose ps` và kết quả `curl .../api/db-check`; không chụp lộ mật khẩu trong `.env` hoặc in toàn bộ `docker compose config` lên GitHub.

## Bài 4 — `Bai_04_Nginx_ReverseProxy/`

Chụp `curl -i http://localhost/users/` và `curl -i http://localhost/products/` trả HTTP 200, upstream nhận đúng đường dẫn. Có thể lưu `reverse_proxy_success.png`.

## Bài 5 — `Bai_05_Multi_Environment/`

Sau `./deploy.sh staging`, chụp `./deploy.sh status-staging` để thấy 1 replica. Dừng staging, chạy `./deploy.sh production`, chụp `./deploy.sh status-production` để thấy 3 replica. Lưu `staging.png` và `production.png`. Không công bố `.env`.

## Bài 6 & thực hành Session 04 — `quickbite-project/`

Đề **bắt buộc** các ảnh dưới đây:

1. `screenshots/01_compose_ps.png`: chạy `docker compose ps`, thể hiện cả `db` và `backend` đều Up.
2. `screenshots/02_backend_logs.png`: chạy `docker compose logs --tail=100 backend`; có thông báo Spring Boot đã start, và kết quả `curl .../api/db-check` để chứng minh SQL kết nối thành công.
3. `screenshots/03_compose_down.png`: chạy `docker compose down`, có output xóa container/network.
4. `screenshots/control_success.png`: chạy `./compose-control.sh start`, dòng chữ thành công màu xanh.

Dán link tới những ảnh đã chụp vào `quickbite-project/report_session04.md` và đổi dòng `CHƯA CHẠY` thành kết quả đúng khi đã xác minh.

## Commit ảnh

```bash
git add .
git commit -m "Add verified Docker Compose screenshots"
git push
```
