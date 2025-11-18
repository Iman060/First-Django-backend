# EXPLAIN Plans – Sprint 2

## 1. User trade history query

```sql
EXPLAIN ANALYZE
SELECT *
FROM trades_trade t
WHERE t.user_id = :user_id
ORDER BY t.created_at DESC
LIMIT 50;
```

(We will paste PostgreSQL EXPLAIN output later.)

## 2. Materialized view query

```sql
EXPLAIN ANALYZE
SELECT *
FROM market_activity_summary
WHERE market_id = :market_id
ORDER BY day DESC
LIMIT 30;
```

(We will paste PostgreSQL EXPLAIN ANALYZE output here later.)


