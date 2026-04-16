# Changelog

## [1.0.0] - 2026-04-17

### Added
- **Phase 1**: Architecture docs, config contract, coding conventions, Pydantic settings
- **Phase 2**: Alembic migrations, repository pattern, seed data, domain model ERD
- **Phase 3**: Checklist engine with YAML templates, evaluation endpoint, status transitions
- **Phase 4**: Playwright-based website monitor, MinIO screenshot storage, diff detection
- **Phase 5**: Merchant onboarding lifecycle (new > under_review > approved/rejected), audit trail
- **Phase 6**: Test purchases CRUD, summary statistics, result validation
- **Phase 7**: CRM module with workflows, reminders, Celery tasks, assignee tracking
- **Phase 8**: n8n workflow integration (onboarding + website monitor cron), integration docs
- **Phase 9**: API key auth, Redis rate limiting, idempotency keys, input validation
- **Phase 10**: Admin UI dashboard (merchant list, detail view with tabs for checklist/snapshots/purchases/CRM)
- **Phase 11**: Structured JSON logging, Prometheus metrics (5+ business counters), health check (DB/Redis/MinIO)
- **Phase 12**: GitHub Actions CI (lint + type check + tests), shared conftest, E2E acceptance test
- **Phase 13**: Production docker-compose, env template, backup/restore scripts, deploy/rollback/backup runbooks
- **Phase 14**: Full acceptance scenario, CHANGELOG, release v1.0.0

### Infrastructure
- FastAPI + PostgreSQL + Redis + MinIO + n8n
- Docker Compose (dev + prod)
- Alembic migrations
- Celery Beat for scheduled tasks
