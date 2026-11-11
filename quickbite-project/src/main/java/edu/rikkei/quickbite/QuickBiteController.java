package edu.rikkei.quickbite;

import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class QuickBiteController {
    private final JdbcTemplate jdbc;

    public QuickBiteController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/")
    public Map<String, String> index() {
        return Map.of("application", "QuickBite demo", "endpoint", "/actuator/health");
    }

    @GetMapping("/api/db-check")
    public Map<String, Object> checkDatabase() {
        Integer n = jdbc.queryForObject("SELECT 1", Integer.class);
        return Map.of("database", "connected", "select_1", n == null ? -1 : n);
    }
}
