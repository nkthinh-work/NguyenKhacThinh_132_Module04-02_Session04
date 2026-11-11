package edu.rikkei.demo.storex;

import java.util.Map;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class StorexDemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(StorexDemoApplication.class, args);
    }
}

@RestController
class StorexDemoController {
    private final JdbcTemplate jdbc;
    private final StringRedisTemplate redis;
    private final boolean redisEnabled;

    StorexDemoController(JdbcTemplate jdbc, StringRedisTemplate redis,
            @Value("${STOREX_ENABLE_REDIS:false}") boolean redisEnabled) {
        this.jdbc = jdbc;
        this.redis = redis;
        this.redisEnabled = redisEnabled;
    }

    @GetMapping("/")
    public Map<String, String> home() {
        return Map.of("service", "storex-demo", "message", "See /api/db-check");
    }

    @GetMapping("/api/db-check")
    public Map<String, Object> dbCheck() {
        Integer value = jdbc.queryForObject("SELECT 1", Integer.class);
        return Map.of("database", "connected", "select_1", value == null ? -1 : value);
    }

    @GetMapping("/api/cache-check")
    public Map<String, Object> cacheCheck() {
        if (!redisEnabled) return Map.of("redis", "not_enabled");
        redis.opsForValue().set("storex:health", "ok");
        return Map.of("redis", redis.opsForValue().get("storex:health"));
    }
}
