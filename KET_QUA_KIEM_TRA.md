# Nhật ký kiểm tra và giới hạn

## Đã có nội dung

- Docker Compose và giải thích cho Bài 1–5.
- Cấu hình Nginx cho Bài 4.
- `quickbite-project/` gồm Dockerfile Java 17, backend Spring Boot demo với JDBC + Actuator, Compose db/backend, Gradle build file, script điều khiển, báo cáo Session 04.
- Tài liệu hướng dẫn chụp ảnh bằng chứng thực tế.

## Kiểm thử tự động có thể chạy không cần Docker

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_static.py
find . -name '*.sh' -exec bash -n '{}' \;
python scripts/test_control_mock.py
```

### Kết quả kiểm tra trong môi trường soạn bài (11/11/2026)

- `python scripts/validate_static.py`: **PASS** — các yêu cầu YAML và file cấu hình chính.
- `bash -n`: **PASS** — 3 script (`test_persistence.sh`, `deploy.sh`, `compose-control.sh`).
- `python -m py_compile`: **PASS** — hai script Python.
- `python scripts/test_control_mock.py`: **6/6 PASS** — luồng start, stop, clean, lỗi DB, lỗi API, lỗi Docker up, sử dụng **Docker và curl mô phỏng** (không phải container thật).

## Chưa thể xác minh trong môi trường tạo bài

- Không có Docker CLI/Daemon: **chưa build/pull image**, chưa chạy containers, chưa thực thi shell smoke test.
- Chưa thể tạo ra log Docker hoặc ảnh screenshot chạy thật.
- Việc build Spring Boot qua Gradle yêu cầu tải Maven dependencies; **chưa biên dịch thực tế** tại đây.

Sau khi chạy các lệnh theo `README.md` trên máy có Docker, cập nhật bảng kết quả và đính kèm ảnh thật trước khi nộp lớp.
