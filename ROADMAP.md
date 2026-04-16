# BRASLINA — Production Roadmap

> **Source of truth** for all development phases.  
> Updated: 2026-04-16 | Status: Phase 1 in progress  
> Repo: https://github.com/CarmiBanxe/braslina

---

## Definition of Done (Project-wide)

- [ ] Merchant can be onboarded fully in-system (no spreadsheet/manual side-process)
- [ ] Checklist, screenshots, website change detection, reminders, test purchases work end-to-end
- [ ] All tests (unit + integration + E2E) passing in CI
- [ ] Deployment docs, runbooks and backup procedures complete
- [ ] API secured with auth, roles, validation, idempotency

---

## Current Infrastructure

| Service | Port | Notes |
|---|---|---|
| braslina-api (FastAPI) | 8000 | lifespan auto-create tables |
| braslina-db (PostgreSQL) | 5432 | user: braslina / pass: braslina_dev / db: braslina |
| braslina-redis | 6379 | |
| braslina-minio | 9002/9003 | Non-standard — port 9000 conflict |
| n8n | 5680 | Non-standard — port 5678 conflict |

Server: `banxe@banxe-NucBox-EVO-X2` · Tailscale `100.68.102.48` · SSH port `2222`

---

## Phase Status Overview

| Phase | Name | Status | Commit |
|---|---|---|---|
| 1 | Freeze architecture and config contract | 🔄 in progress | — |
| 2 | DB models, Alembic, repositories, seeds | ⬜ todo | — |
| 3 | Merchant checklist module | ⬜ todo | — |
| 4 | Website monitor agent | ⬜ todo | — |
| 5 | Onboarding register | ⬜ todo | — |
| 6 | Test purchases log | ⬜ todo | — |
| 7 | Internal CRM / workflow / reminders | ⬜ todo | — |
| 8 | n8n end-to-end integration | ⬜ todo | — |
| 9 | API hardening: auth, roles, validation, idempotency | ⬜ todo | — |
| 10 | Admin UI screens | ⬜ todo | — |
| 11 | Logs, metrics, health checks, retry/monitoring | ⬜ todo | — |
| 12 | Unit / integration / E2E / CI coverage | ⬜ todo | — |
| 13 | Prod deployment, backups, runbooks | ⬜ todo | — |
| 14 | Final acceptance scenario and release | ⬜ todo | — |

---

## Phase 1 — Freeze Architecture and Config Contract

**Goal:** Lock down all architectural decisions, config schema, environment variables, module boundaries, and coding conventions before any new code is written. This phase produces only documents and config files — no business logic.

### Deliverables

- [ ] `docs/spec/architecture.md` — updated with current module map and data flow
- [ ] `docs/spec/config-contract.md` — all env vars documented with types, defaults, required/optional
- [ ] `docs/spec/module-boundaries.md` — what each module owns, what it must NOT do
- [ ] `docs/spec/coding-conventions.md` — naming, file structure, async patterns, error handling rules
- [ ] `.env.example` — complete, validated against `config-contract.md`
- [ ] `src/common/config.py` — Pydantic Settings class with all env vars
- [ ] `requirements.txt` — pinned versions, no `>=` ranges in production deps
- [ ] `requirements-dev.txt` — separated dev dependencies (pytest, httpx, etc.)
- [ ] `pyproject.toml` — ruff + mypy config

### Definition of Done (Phase 1)

- [ ] All env vars in `config.py` match `.env.example` exactly
- [ ] `python -c "from src.common.config import settings; print(settings)"` succeeds
- [ ] `ruff check src/` returns 0 errors
- [ ] Existing 6/6 tests still pass after config changes

---

## Phase 2 — DB Models, Alembic, Repositories, Seeds

**Goal:** Replace `create_all` in lifespan with proper Alembic migrations. Add repository pattern (no raw SQLAlchemy in routers). Add seed data for dev/test.

### Deliverables

- [ ] Alembic initialized: `alembic/` directory with `env.py` wired to async engine
- [ ] Initial migration covering all existing models (merchants, checklists, check_items, snapshots, test_purchases)
- [ ] `src/*/repository.py` — one per module, encapsulates all DB queries
- [ ] `src/common/seed.py` — seeds 3 test merchants + checklists for local dev
- [ ] `src/main.py` — lifespan no longer calls `create_all`; Alembic handles DDL
- [ ] `docs/spec/domain-model.md` — updated ERD text diagram

### Definition of Done (Phase 2)

- [ ] `alembic upgrade head` runs clean on empty DB
- [ ] `alembic downgrade base` runs clean
- [ ] 6/6 existing tests pass
- [ ] New tests: `tests/test_repositories.py` with CRUD round-trips per module

---

## Phase 3 — Merchant Checklist Module

**Goal:** Fully implement the checklist engine: template loading, item evaluation, status transitions, and result persistence.

### Deliverables

- [ ] Checklist templates stored in `src/checklist/templates/` as YAML
- [ ] `src/checklist/engine.py` — evaluate checklist against merchant data, return `ChecklistResult`
- [ ] `src/checklist/service.py` — orchestrates engine + repository
- [ ] `src/checklist/router.py` — CRUD + trigger evaluation endpoint
- [ ] Checklist statuses: `pending` → `in_progress` → `passed` / `failed` / `needs_review`
- [ ] Tests: `tests/checklist/test_service.py`, `tests/checklist/test_engine.py`

### Definition of Done (Phase 3)

- [ ] `POST /api/v1/checklist/evaluate/{merchant_id}` runs engine and persists result
- [ ] All checklist item statuses correctly transition
- [ ] Tests cover happy path + missing fields + all status transitions

---

## Phase 4 — Website Monitor Agent

**Goal:** Playwright-based screenshot capture, pixelmatch diffing, change detection, alert generation.

### Deliverables

- [ ] `src/agent/monitor.py` — screenshot + diff logic using Playwright + pixelmatch
- [ ] `src/agent/service.py` — orchestrates monitor, stores snapshot, triggers alert if diff > threshold
- [ ] `src/agent/router.py` — `POST /monitor`, `GET /snapshots/{merchant_id}`
- [ ] MinIO integration: screenshots stored as objects (bucket: `braslina-screenshots`)
- [ ] Alert model: diff percentage, changed regions, snapshot URLs
- [ ] Playwright installed in Docker (`apt-get + playwright install chromium`)
- [ ] Tests: mock Playwright, test diff logic, test alert generation

### Definition of Done (Phase 4)

- [ ] `POST /api/v1/monitor/monitor` returns snapshot + diff result
- [ ] Screenshots saved to MinIO (verified via MinIO console at :9003)
- [ ] Alert generated when diff > configurable threshold (default 5%)

---

## Phase 5 — Onboarding Register

**Goal:** Full merchant lifecycle: create → under_review → approved / rejected, with audit trail.

### Deliverables

- [ ] `MerchantStatus` enum: `new` → `under_review` → `approved` / `rejected` / `suspended`
- [ ] `src/register/service.py` — status transitions with validation rules
- [ ] Status change history table: `merchant_status_log`
- [ ] `PATCH /api/v1/onboarding/{merchant_id}/status` endpoint
- [ ] Tests: status transition matrix (valid + invalid transitions)

### Definition of Done (Phase 5)

- [ ] Invalid status transitions return 422 with clear error
- [ ] Status history persisted and queryable
- [ ] Full onboarding lifecycle test passes

---

## Phase 6 — Test Purchases Log

**Goal:** Full CRUD for test purchase records with result tracking and summary statistics.

### Deliverables

- [ ] `src/purchases/service.py` — business logic layer
- [ ] `GET /api/v1/test-purchase/summary/{merchant_id}` — pass/fail counts, last purchase date
- [ ] Validation: `result` must be `passed` | `failed` | `partial`
- [ ] Tests: test_purchase CRUD + summary endpoint

### Definition of Done (Phase 6)

- [ ] Summary endpoint returns correct aggregations
- [ ] All 3 result values accepted; others rejected with 422

---

## Phase 7 — Internal CRM / Workflow / Reminders

**Goal:** Implement `src/crm/` module — workflow stages, notes, reminders, assignee tracking.

### Deliverables

- [ ] `CRMWorkflowDB` — stage, assignee_id, notes (JSONB), due_date
- [ ] `ReminderDB` — merchant_id, message, scheduled_at, sent_at, channel
- [ ] `src/crm/service.py` — create/advance workflow, schedule reminder
- [ ] `src/crm/router.py` — CRUD + `POST /crm/{merchant_id}/remind`
- [ ] Celery task: `src/crm/tasks.py` — `send_reminder` triggered by Celery Beat

### Definition of Done (Phase 7)

- [ ] Workflow advances through stages correctly
- [ ] Reminder Celery task executes (logged, not necessarily emailed in MVP)
- [ ] Tests for workflow transitions + reminder scheduling

---

## Phase 8 — n8n End-to-End Integration

**Goal:** Import and activate both n8n workflows, verify they call braslina-api correctly.

### Deliverables

- [ ] `merchant_onboarding.json` imported into n8n at :5680
- [ ] `website_monitor_cron.json` imported and scheduled
- [ ] n8n credentials configured for braslina-api base URL
- [ ] Webhook endpoints in braslina-api for n8n callbacks (if needed)
- [ ] `docs/n8n-integration.md` — setup instructions

### Definition of Done (Phase 8)

- [ ] Manual trigger of `merchant_onboarding` workflow completes all 6 nodes
- [ ] `website_monitor_cron` runs on schedule and stores snapshot

---

## Phase 9 — API Hardening

**Goal:** Auth (API key or JWT), RBAC roles, input validation, idempotency keys, rate limiting.

### Deliverables

- [ ] `src/common/auth.py` — API key validation middleware (phase 1 of auth)
- [ ] `X-Idempotency-Key` header support on POST endpoints
- [ ] `src/common/rate_limit.py` — Redis-backed rate limiter
- [ ] All input models: field validators, max lengths, enum constraints
- [ ] `docs/spec/api-security.md`

### Definition of Done (Phase 9)

- [ ] Unauthenticated requests to protected endpoints return 401
- [ ] Duplicate POST with same idempotency key returns same response, no duplicate DB row
- [ ] Rate limit test: 101st request returns 429

---

## Phase 10 — Admin UI

**Goal:** Minimal internal web UI for ops team to view merchants, checklists, monitor results.

### Deliverables

- [ ] `ui/` directory with static Next.js or plain HTML admin dashboard
- [ ] Views: merchant list, merchant detail (status + checklist + snapshots + purchases)
- [ ] Served via nginx or FastAPI static files
- [ ] Auth: same API key as backend

### Definition of Done (Phase 10)

- [ ] Ops user can view a merchant and their full onboarding status without API calls

---

## Phase 11 — Observability

**Goal:** Structured logging, Prometheus metrics, health checks, retry logic.

### Deliverables

- [ ] `structlog` or `loguru` — JSON structured logs
- [ ] `/metrics` endpoint (Prometheus format via `prometheus-fastapi-instrumentator`)
- [ ] `/health` returns DB + Redis + MinIO connectivity status
- [ ] Celery task retry logic with exponential backoff
- [ ] `docs/spec/observability.md`

### Definition of Done (Phase 11)

- [ ] `GET /health` returns `{"db": "ok", "redis": "ok", "minio": "ok"}`
- [ ] Logs are JSON in production, human-readable in dev
- [ ] At least 5 business metrics exported (merchant_created, checklist_evaluated, snapshot_captured, etc.)

---

## Phase 12 — Test Coverage

**Goal:** 80%+ coverage, CI pipeline passing on every push.

### Deliverables

- [ ] `tests/` fully restructured: unit / integration / e2e subdirectories
- [ ] `pytest-cov` configured: minimum 80% threshold
- [ ] `.github/workflows/ci.yml` — lint + type check + tests on push to main
- [ ] E2E test: full onboarding scenario from `POST /onboarding` to `approved`

### Definition of Done (Phase 12)

- [ ] `pytest --cov=src --cov-fail-under=80` passes
- [ ] GitHub Actions CI green on main

---

## Phase 13 — Production Deployment

**Goal:** Docker production config, secrets management, backup, runbooks.

### Deliverables

- [ ] `docker-compose.prod.yml` — no dev mounts, resource limits, restart policies
- [ ] `.env.prod.example` — production secrets template
- [ ] `scripts/backup_db.sh` — daily pg_dump to MinIO
- [ ] `scripts/restore_db.sh`
- [ ] `docs/runbooks/deploy.md`
- [ ] `docs/runbooks/rollback.md`
- [ ] `docs/runbooks/backup-restore.md`

### Definition of Done (Phase 13)

- [ ] `docker compose -f docker-compose.prod.yml up -d` brings up all services cleanly
- [ ] Backup script runs and produces valid dump in MinIO

---

## Phase 14 — Final Acceptance

**Goal:** Run full end-to-end acceptance scenario with no manual intervention.

### Acceptance Scenario

1. Create merchant via API
2. Trigger checklist evaluation — all items checked
3. Capture website screenshot — stored in MinIO
4. Log test purchase — `passed`
5. Advance merchant to `approved`
6. Trigger n8n onboarding workflow — all nodes green
7. Query merchant — status `approved`, checklist `passed`, last snapshot present, purchase logged

### Definition of Done (Phase 14)

- [ ] Acceptance scenario passes as automated test in `tests/e2e/test_acceptance.py`
- [ ] Release tag `v1.0.0` created on main
- [ ] `CHANGELOG.md` written

---

## Conventions

### Branch naming
`phase/{N}-short-description`  
Example: `phase/1-config-contract`

### Commit message format
```
type(scope): description

type: feat | fix | docs | test | refactor | chore
scope: phase1 | phase2 | ... | checklist | monitor | register | crm | ...
```

### File structure per module
```
src/{module}/
├── __init__.py
├── db_models.py     # SQLAlchemy ORM models
├── repository.py    # DB queries (no business logic)
├── service.py       # Business logic (no HTTP)
├── router.py        # FastAPI router (no business logic)
└── schemas.py       # Pydantic request/response models
```

### Error handling
- Use `HTTPException` only in routers
- Services raise domain exceptions (defined in `src/common/exceptions.py`)
- Routers catch domain exceptions and translate to HTTP status codes

---

*Last updated by: Moriel Carmi · 2026-04-16*
