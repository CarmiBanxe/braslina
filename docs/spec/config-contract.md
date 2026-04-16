# Config Contract

> All env vars used by braslina. Source of truth: src/common/config.py.

| Variable | Type | Default | Required | Description |
|---|---|---|---|---|
| DATABASE_URL | str | postgresql+asyncpg://braslina:braslina_dev@localhost:5432/braslina | yes | Async PG connection string |
| REDIS_URL | str | redis://localhost:6379/0 | yes | Redis for Celery + rate limiter |
| MINIO_ENDPOINT | str | localhost:9002 | yes | MinIO API endpoint |
| MINIO_ACCESS_KEY | str | braslina | yes | MinIO access key |
| MINIO_SECRET_KEY | str | braslina_dev | yes | MinIO secret key |
| MINIO_BUCKET | str | braslina-screenshots | no | Bucket for screenshots |
| MINIO_SECURE | bool | false | no | Use HTTPS for MinIO |
| N8N_BASE_URL | str | http://localhost:5680 | no | n8n instance URL |
| ALERT_THRESHOLD_PCT | float | 5.0 | no | Visual diff alert threshold pct |
| APP_ENV | str | development | no | development / testing / production |
| LOG_LEVEL | str | INFO | no | Python log level |
| API_KEY | str | (empty) | no | API key; empty = auth disabled |

## Rules

1. Never use os.getenv() in application code. Import settings from src.common.config.
2. Every new variable must be added to config.py, .env.example, and this document.
3. Production deployments must set APP_ENV=production and a non-empty API_KEY.
