# API Security Specification

## Authentication

### API Key (`src/security/auth.py`)
- Header: `X-API-Key`
- Env: `BRASLINA_API_KEY`
- If key is empty (dev mode), auth is bypassed
- Returns `401 Unauthorized` on mismatch

## Rate Limiting

### Configuration (`src/security/rate_limit.py`)
- Sliding window counter per client IP
- Default: 60 requests / 60 seconds
- Env: `BRASLINA_RATE_LIMIT`, `BRASLINA_RATE_WINDOW`
- Returns `429 Too Many Requests` when exceeded

## Idempotency

### Implementation (`src/security/idempotency.py`)
- Header: `Idempotency-Key` on POST requests
- Configurable via `BRASLINA_IDEMPOTENCY_TTL` (default 86400s)
- Cache: returns cached response, no duplicate processing
- Requests without the header pass through normally

## Input Validation

- Pydantic v2 with strict types
- Status fields: `Literal["passed", "failed", "pending"]`
- Validated against allowed transition maps
- Returns `422 Unprocessable Entity` on validation failure

## Environment Variables

| Variable | Description |
|---|---|
| `BRASLINA_API_KEY` | API key; empty = dev mode |
| `BRASLINA_RATE_LIMIT` | Max requests per window |
| `BRASLINA_RATE_WINDOW` | Window in seconds |
| `BRASLINA_IDEMPOTENCY_TTL` | Idempotency cache TTL |
| `REDIS_URL` | Redis connection string |
