# Observability Specification

## Structured Logging

### Module: `src/common/logging.py`
- JSON format in production (`BRASLINA_ENV=production`)
- Human-readable format in dev (default)
- Logger factory: `get_logger(name)` returns `braslina.<name>`

## Prometheus Metrics

### Module: `src/common/metrics.py`
- `braslina_merchant_created_total` — merchant creation counter
- `braslina_checklist_evaluated_total` — checklist eval counter (by result)
- `braslina_snapshot_captured_total` — screenshot capture counter
- `braslina_test_purchase_logged_total` — purchase log counter (by result)
- `braslina_workflow_advanced_total` — CRM workflow advance counter
- `braslina_request_duration_seconds` — request latency histogram

### Endpoint
- `GET /metrics` — Prometheus scrape endpoint via `prometheus-fastapi-instrumentator`

## Health Check

### Module: `src/common/health.py`
- `GET /health` returns:
```json
{"status": "ok", "db": "ok", "redis": "ok", "minio": "ok"}
```
- Status is `degraded` if any component is down

## Celery Retry Logic
- Tasks use `autoretry_for=(Exception,)`
- `retry_backoff=True` (exponential)
- `max_retries=5`

## Environment Variables

| Variable | Description |
|---|---|
| `BRASLINA_ENV` | `dev` or `production` — controls log format |
