# Bài 4 — Reverse proxy Nginx và Docker DNS

## Nguyên nhân 502 Bad Gateway

Trong container Nginx, `localhost:8081` là chính container Nginx, không phải service `user_service`. Để Nginx kết nối upstream qua mạng Docker, phải gọi **tên service**, tức `user_service:8081` và `product_service:8082`. Khi Nginx không kết nối được upstream, nó có thể trả HTTP 502.

## Sửa `proxy_pass` và rewrite path

```nginx
location /users/    { proxy_pass http://user_service:8081/; }
location /products/ { proxy_pass http://product_service:8082/; }
```

Chú ý dấu `/` sau hostname: với prefix `location /users/`, Nginx chuyển `/users/profile` sang upstream `/profile`. Chỉ chọn cách này khi backend định tuyến từ `/`, như hai **mock-service** trong repo. Nếu backend thật đã khai báo `/users/**`, nên dùng `proxy_pass http://user_service:8081;` (không có URI `/`) để giữ nguyên đường dẫn.

## Kiểm chứng

```bash
docker compose up -d --build
docker compose ps
curl -i http://localhost/users/
curl -i http://localhost/users/profile
curl -i http://localhost/products/
docker compose logs --tail=50 nginx_proxy
docker compose down
```

**Giới hạn:** Đề không cung cấp source `storex-user`/`storex-product`, nên repo đi kèm mock HTTP để kiểm thử DNS/path (không giả làm microservice nghiệp vụ thật).
